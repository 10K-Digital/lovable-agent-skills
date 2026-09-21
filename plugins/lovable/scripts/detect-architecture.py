#!/usr/bin/env python3
"""Detect the supported Lovable frontend architecture without reading secret values."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TANSTACK_PACKAGES = {"@tanstack/react-start", "@tanstack/start"}


def package_indicates_tanstack(root: Path) -> list[str]:
    """Return package evidence for TanStack Start without inspecting application source."""
    path = root / "package.json"
    try:
        package = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(package, dict):
        return []
    evidence: list[str] = []
    for field in ("dependencies", "devDependencies"):
        values = package.get(field, {})
        if isinstance(values, dict) and TANSTACK_PACKAGES & set(values):
            evidence.append(f"package.json:{field}")
    return evidence


def detect_architecture(root: Path) -> dict[str, object]:
    tanstack_evidence = package_indicates_tanstack(root)
    app_config = root / "app.config.ts"
    vite_config = root / "vite.config.ts"
    if tanstack_evidence:
        return {"architecture": "tanstack-start", "markers": tanstack_evidence}
    if app_config.is_file():
        return {"architecture": "tanstack-start", "markers": [app_config.name]}
    if vite_config.is_file():
        return {"architecture": "vite-spa", "markers": [vite_config.name]}
    return {"architecture": "unknown", "markers": []}


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
