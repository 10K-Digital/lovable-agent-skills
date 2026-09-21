#!/usr/bin/env python3
"""Install Lovable skills as safe standalone symlinks with a source manifest.

The default prints a plan. Pass --install to change a target directory. Existing entries are moved
to a timestamped backup, never deleted. --check performs a read-only verification.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


MANIFEST_NAME = ".lovable-standalone-manifest.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--target", type=Path, default=Path.home() / ".codex" / "skills")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--install", action="store_true", help="Create or update symlinks")
    group.add_argument("--check", action="store_true", help="Verify an existing installation")
    return parser.parse_args()


def load_identity(source: Path) -> dict[str, str]:
    module_path = source / "scripts" / "source-integrity.py"
    spec = importlib.util.spec_from_file_location("lovable_source_integrity", module_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"source identity helper is unavailable: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.identity(source)


def git_commit(source: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True, capture_output=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else "unavailable"


def manifest(source: Path) -> dict[str, Any]:
    source = source.resolve()
    return {
        "format": 1,
        "source": str(source),
        "commit": git_commit(source),
        "identity": load_identity(source),
        "skills": sorted(path.name for path in (source / "skills").iterdir() if path.is_dir()),
    }


def expected_target(source: Path, name: str) -> Path:
    return (source / "skills" / name).resolve()


def verify(source: Path, target: Path, expected: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    manifest_path = target / MANIFEST_NAME
    try:
        recorded = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        errors.append(f"missing or invalid manifest: {manifest_path}")
        recorded = None
    if recorded != expected:
        errors.append("source manifest does not match the selected source")
    if isinstance(recorded, dict) and recorded.get("skills") != expected["skills"]:
        errors.append("installed skill inventory differs from the selected source; rerun --install to back up and update links")
    for name in expected["skills"]:
        link = target / name
        if not link.is_symlink() or link.resolve() != expected_target(source, name):
            errors.append(f"invalid skill link: {link}")
    return errors


def removed_installed_skills(target: Path, expected: dict[str, Any]) -> list[str]:
    """Return previously installed skills absent from the proposed source, without changing state."""
    try:
        recorded = json.loads((target / MANIFEST_NAME).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(recorded, dict) or not isinstance(recorded.get("skills"), list):
        return []
    return sorted(set(recorded["skills"]) - set(expected["skills"]))


def backup_path(target: Path) -> Path:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return target / ".lovable-standalone-backups" / stamp


def install(source: Path, target: Path, expected: dict[str, Any]) -> None:
    target.mkdir(parents=True, exist_ok=True)
    backup = backup_path(target)
    for name in expected["skills"]:
        link = target / name
        desired = expected_target(source, name)
        if link.is_symlink() and link.resolve() == desired:
            continue
        if link.exists() or link.is_symlink():
            backup.mkdir(parents=True, exist_ok=True)
            shutil.move(str(link), str(backup / name))
        os.symlink(desired, link, target_is_directory=True)
    (target / MANIFEST_NAME).write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    source = args.source.expanduser().resolve()
    target = args.target.expanduser().resolve()
    try:
        expected = manifest(source)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.check:
        errors = verify(source, target, expected)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print(json.dumps(expected, sort_keys=True))
        return 0
    if not args.install:
        print(json.dumps({"action": "plan", "target": str(target), **expected}, sort_keys=True))
        return 0
    removed = removed_installed_skills(target, expected)
    if removed:
        print(
            "refusing install: selected source removes installed skills: " + ", ".join(removed),
            file=sys.stderr,
        )
        return 2
    install(source, target, expected)
    errors = verify(source, target, expected)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(json.dumps({"action": "installed", "target": str(target), **expected}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
