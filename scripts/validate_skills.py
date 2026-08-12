#!/usr/bin/env python3
"""Validate Agent Skills metadata without requiring third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")


def read_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("unterminated YAML frontmatter") from exc
    result: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.startswith(" "):
            continue
        key, separator, value = line.partition(":")
        if separator:
            result[key.strip()] = value.strip().strip("'\"")
    return result


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    skill_files = sorted((root / "plugins" / "lovable" / "skills").glob("*/SKILL.md"))
    errors: list[str] = []
    for path in skill_files:
        try:
            metadata = read_frontmatter(path)
        except (OSError, ValueError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if not name or not NAME_RE.fullmatch(name):
            errors.append(f"{path}: name must be lowercase hyphen-case (got {name!r})")
        if not description and "|" not in path.read_text(encoding="utf-8").split("\n", 8)[2:3]:
            errors.append(f"{path}: missing description")
        if len(name) > 64:
            errors.append(f"{path}: name exceeds 64 characters")
    if errors:
        print("Agent Skills validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Agent Skills validation passed ({len(skill_files)} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
