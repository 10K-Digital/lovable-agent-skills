#!/usr/bin/env python3
"""Detect the supported Lovable frontend architecture without reading secret values."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def detect_architecture(root: Path) -> dict[str, object]:
    markers = {
        "tanstack-start": root / "app.config.ts",
        "vite-spa": root / "vite.config.ts",
    }
    matches = [name for name, marker in markers.items() if marker.is_file()]
    if len(matches) == 1:
        return {"architecture": matches[0], "markers": [str(markers[matches[0]].name)]}
    return {
        "architecture": "ambiguous" if matches else "unknown",
        "markers": [str(markers[name].name) for name in matches],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"project root does not exist: {root}")
    print(json.dumps(detect_architecture(root), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
