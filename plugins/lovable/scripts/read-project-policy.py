#!/usr/bin/env python3
"""Print the safe policy or inventory slice of a Lovable project configuration.

This reader intentionally never emits project URLs, credentials, arbitrary extension fields, or
the inventory's secret metadata. It is read-only and does not migrate or normalize configuration.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def one_of(*allowed: str):
    allowed_values = frozenset(allowed)
    return lambda value: type(value) is str and value in allowed_values


def control_priority(value: Any) -> bool:
    allowed = {"lovable-mcp", "in-app-browser", "browser", "manual"}
    return isinstance(value, list) and all(type(item) is str and item in allowed for item in value)


POLICY_VALIDATORS = {
    "sync": {
        "branch": lambda value: type(value) is str,
        "auto_sync": lambda value: type(value) is bool,
        "auto_push": lambda value: type(value) is bool,
    },
    "deploy": {
        "mode": one_of("auto", "mcp", "browser", "manual"),
        "yolo_mode": lambda value: type(value) is bool,
        "auto_deploy": lambda value: type(value) is bool,
        "control_priority": control_priority,
        "confirm_migrations": lambda value: type(value) is bool,
        "deployment_testing": lambda value: type(value) is bool,
        "auto_run_tests": lambda value: type(value) is bool,
        "debug": lambda value: type(value) is bool,
        "debug_mode": lambda value: type(value) is bool,
        "persist_across_sessions": lambda value: type(value) is bool,
        "test_after_deploy": one_of("off", "smoke", "all"),
    },
    "testing": {
        "enabled": lambda value: type(value) is bool,
        "access_method": one_of("token", "browser-login"),
        "test_after_implementation": lambda value: type(value) is bool,
        "test_after_deploy": one_of("off", "smoke", "all"),
    },
}
INVENTORY_FIELDS = ("edge_functions", "migrations")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Path to the target project")
    parser.add_argument("--section", required=True, choices=("policies", "inventory"))
    return parser.parse_args()


def read_config(project: Path) -> dict[str, Any]:
    path = project / ".lovable-agent" / "config.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Lovable configuration not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Lovable configuration is invalid JSON: {path}") from exc
    except OSError as exc:
        raise ValueError(f"Could not read Lovable configuration: {path}") from exc
    if not isinstance(value, dict):
        raise ValueError("Lovable configuration must contain a JSON object")
    return value


def selected_fields(source: Any, validators: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(source, dict):
        return {}
    result: dict[str, Any] = {}
    for name, valid in validators.items():
        if name not in source:
            continue
        if not valid(source[name]):
            raise ValueError(f"invalid policy value at {name}")
        result[name] = source[name]
    return result


def policies(config: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    if type(config.get("schema_version")) is int:
        result["schema_version"] = config["schema_version"]
    for section, validators in POLICY_VALIDATORS.items():
        if section not in config:
            continue
        if not isinstance(config[section], dict):
            raise ValueError(f"invalid policy structure at {section}")
        try:
            fields = selected_fields(config.get(section), validators)
        except ValueError as exc:
            raise ValueError(f"invalid policy value at {section}.{str(exc).removeprefix('invalid policy value at ')}") from exc
        if fields:
            result[section] = fields
    return result


def safe_inventory(source: Any) -> dict[str, list[str]]:
    if not isinstance(source, dict):
        return {}
    result: dict[str, list[str]] = {}
    for name in INVENTORY_FIELDS:
        value = source.get(name)
        if isinstance(value, list):
            # Inventory can be hand-edited. Return only simple names, never arbitrary nested objects.
            result[name] = [item for item in value if isinstance(item, str)
                            and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,254}", item)]
    return result


def inventory(config: dict[str, Any]) -> dict[str, Any]:
    # Do not return inventory.secrets: even names/status can reveal sensitive operations.
    return {"inventory": safe_inventory(config.get("inventory"))}


def main() -> int:
    args = parse_args()
    try:
        config = read_config(Path(args.project).expanduser().resolve())
        result = policies(config) if args.section == "policies" else inventory(config)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
