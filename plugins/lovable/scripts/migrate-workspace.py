#!/usr/bin/env python3
"""Migrate the legacy Claude Preview workspace to the neutral agent contract.

The migration is intentionally conservative: existing canonical files win, non-secret test
artifacts are copied (not deleted), and preview tokens are copied only between ignored token paths.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing files")
    return parser.parse_args()


def log(message: str, dry_run: bool) -> None:
    prefix = "DRY RUN: " if dry_run else ""
    print(f"{prefix}{message}")


def copy_if_missing(source: Path, destination: Path, dry_run: bool) -> bool:
    if not source.exists() or destination.exists():
        return False
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
    log(f"copy {source} -> {destination}", dry_run)
    return True


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def build_config(old_config: dict[str, Any], existing: dict[str, Any]) -> dict[str, Any]:
    old = old_config
    testing = dict(existing.get("testing", {}))
    testing.update(
        {
            "enabled": True,
            "preview_url": old.get("preview_url", testing.get("preview_url", "")),
            "access_method": old.get("access_method", testing.get("access_method", "browser-login")),
            "token_captured": old.get("token_captured", testing.get("token_captured", "")),
            "token_expires": old.get("token_expires", testing.get("token_expires", "")),
            "test_after_implementation": old.get(
                "test_after_implementation", testing.get("test_after_implementation", False)
            ),
            "test_after_deploy": old.get("test_after_deploy", testing.get("test_after_deploy", "off")),
            "last_synced_commit": old.get(
                "last_synced_commit", testing.get("last_synced_commit", "")
            ),
            "last_synced_at": old.get("last_synced_at", testing.get("last_synced_at", "")),
            "plan_counter": old.get("plan_counter", testing.get("plan_counter", 0)),
            "default_profile": old.get("default_profile", testing.get("default_profile", "default")),
            "sync_wait_seconds": old.get("sync_wait_seconds", testing.get("sync_wait_seconds", 120)),
        }
    )
    result = dict(existing)
    result["schema_version"] = 1
    result["testing"] = testing
    result.setdefault("sync", {"branch": "main", "auto_sync": True, "auto_push": False})
    result.setdefault(
        "deploy", {"mode": "auto", "confirm_migrations": False, "test_after_deploy": "off"}
    )
    result.setdefault("inventory", {"edge_functions": [], "migrations": [], "secrets": []})
    return result


def ensure_gitignore(root: Path, dry_run: bool) -> None:
    path = root / ".gitignore"
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    entries = [
        ".lovable-agent/preview-token.local",
        ".claude/lovable-claude/test/preview-token.local",
    ]
    missing = [entry for entry in entries if entry not in current.splitlines()]
    if not missing:
        return
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        separator = "" if not current or current.endswith("\n") else "\n"
        path.write_text(current + separator + "\n# Lovable preview credentials\n" + "\n".join(missing) + "\n", encoding="utf-8")
    log(f"protect token paths in {path}", dry_run)


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).expanduser().resolve()
    old_root = root / ".claude" / "lovable-claude" / "test"
    canonical_root = root / ".lovable-agent"
    tests_root = canonical_root / "tests"
    old_config_path = old_root / "test-config.json"
    canonical_config_path = canonical_root / "config.json"

    if not root.is_dir():
        raise SystemExit(f"Project root does not exist: {root}")

    ensure_gitignore(root, args.dry_run)
    for directory in (canonical_root, tests_root, tests_root / "plans", tests_root / "profiles", tests_root / "results"):
        if not args.dry_run:
            directory.mkdir(parents=True, exist_ok=True)

    old_config = read_json(old_config_path) if old_config_path.exists() else {}
    existing_config = read_json(canonical_config_path) if canonical_config_path.exists() else {}
    if old_config and not canonical_config_path.exists():
        config = build_config(old_config, existing_config)
        if not args.dry_run:
            canonical_config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        log(f"write neutral config {canonical_config_path}", args.dry_run)
    elif old_config and canonical_config_path.exists():
        log(f"preserve existing neutral config {canonical_config_path}", args.dry_run)
    elif not canonical_config_path.exists():
        config = build_config({}, existing_config)
        if not args.dry_run:
            canonical_config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        log(f"write default neutral config {canonical_config_path}", args.dry_run)

    context_path = canonical_root / "context.md"
    if not context_path.exists():
        content = (
            "# Lovable Agent Context\n\n"
            "Canonical provider-neutral project state lives in `.lovable-agent/config.json`. "
            "Read `AGENTS.md` and the relevant Lovable skill before acting.\n"
        )
        if not args.dry_run:
            context_path.write_text(content, encoding="utf-8")
        log(f"write {context_path}", args.dry_run)

    for name in ("README.md",):
        copy_if_missing(old_root / name, tests_root / name, args.dry_run)
    for folder in ("plans", "profiles", "results"):
        source_folder = old_root / folder
        destination_folder = tests_root / folder
        if source_folder.exists():
            for source in source_folder.rglob("*"):
                if source.is_file():
                    copy_if_missing(source, destination_folder / source.relative_to(source_folder), args.dry_run)

    old_token = old_root / "preview-token.local"
    new_token = canonical_root / "preview-token.local"
    copy_if_missing(old_token, new_token, args.dry_run)
    if old_root.exists():
        log(
            "legacy workspace retained as a compatibility alias; remove it only after validating the migration",
            args.dry_run,
        )
    else:
        log("no legacy workspace found; canonical workspace is ready", args.dry_run)
    log(f"migration completed at {datetime.now(timezone.utc).isoformat()}", args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
