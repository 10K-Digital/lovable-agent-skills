#!/usr/bin/env python3
"""Produce or verify a reproducible Lovable plugin source identity.

Use this before installing the repository source into a local plugin directory. The command only
reads source trees; it never edits an installed plugin.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


EXCLUDED_PARTS = {"__pycache__", ".DS_Store"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=Path(__file__).resolve().parents[1], type=Path)
    parser.add_argument("--check", type=Path, help="Compare another plugin source tree to --source")
    return parser.parse_args()


def identity(root: Path) -> dict[str, str]:
    root = root.resolve()
    manifest_path = root / ".codex-plugin" / "plugin.json"
    try:
        version = json.loads(manifest_path.read_text(encoding="utf-8"))["version"]
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        raise ValueError(f"invalid plugin manifest: {manifest_path}") from exc
    digest = hashlib.sha256()
    files = [path for path in root.rglob("*") if path.is_file() and not (set(path.parts) & EXCLUDED_PARTS)]
    for path in sorted(files, key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        executable = b"1" if path.stat().st_mode & 0o111 else b"0"
        digest.update(relative + b"\0" + executable + b"\0" + path.read_bytes() + b"\0")
    return {"version": str(version), "sha256": digest.hexdigest()}


def main() -> int:
    args = parse_args()
    try:
        source = identity(args.source)
        if args.check:
            candidate = identity(args.check)
            if candidate != source:
                print(json.dumps({"expected": source, "actual": candidate}, sort_keys=True), file=sys.stderr)
                return 1
        print(json.dumps(source, sort_keys=True))
        return 0
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
