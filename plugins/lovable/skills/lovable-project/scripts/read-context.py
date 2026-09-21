#!/usr/bin/env python3
"""Standalone skill entrypoint for safe Lovable project context reads.

It resolves this file first so it keeps working after `lovable-project` is symlinked into
`~/.codex/skills`. The policy implementation stays at the plugin root.
"""

from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    plugin_root = Path(__file__).resolve().parents[3]
    target = plugin_root / "scripts" / "read-project-policy.py"
    if not target.is_file():
        raise SystemExit(f"Lovable policy reader is missing: {target}")
    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()
