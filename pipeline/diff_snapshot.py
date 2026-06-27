#!/usr/bin/env python3
"""Draft changelog sections by comparing registry snapshots.

Default behavior compares the latest existing snapshots/v*.yaml release snapshot
with the current registry/tools/*.yaml projection. Pass --from and optionally
--to to compare explicit snapshot files instead.

Usage:
  python3 pipeline/diff_snapshot.py
  python3 pipeline/diff_snapshot.py --from snapshots/v0.3.0.yaml
  python3 pipeline/diff_snapshot.py --from snapshots/v0.3.0.yaml --to snapshots/v0.4.0.yaml
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required:  pip install pyyaml")

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "registry" / "tools"
SNAPSHOTS = REPO / "snapshots"

TRACKED_FIELDS = ("name", "primary_category", "status", "version", "verified_at")
VERSION_FIELDS = ("kind", "ref", "released_at")


def repo_relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def resolve_path(raw: str) -> Path:
    path = Path(raw).expanduser()
    if path.is_absolute():
        return path
    return REPO / path


def normalize_value(value: Any) -> Any:
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): normalize_value(inner) for key, inner in value.items()}
    if isinstance(value, list):
        return [normalize_value(inner) for inner in value]
    return value


def normalize_tool(data: dict[str, Any]) -> dict[str, Any]:
    return {field: normalize_value(data.get(field)) for field in TRACKED_FIELDS}


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text())
    except FileNotFoundError:
        raise SystemExit(f"{repo_relative(path)} does not exist")
    except yaml.YAMLError as exc:
        raise SystemExit(f"{repo_relative(path)}: YAML parse error: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{repo_relative(path)}: top level is not a mapping")
    return data


def load_snapshot(path: Path) -> dict[str, Any]:
    data = load_yaml_mapping(path)
    tools = data.get("tools")
    if not isinstance(tools, dict):
        raise SystemExit(f"{repo_relative(path)}: missing tools mapping")

    normalized: dict[str, dict[str, Any]] = {}
    for tool_id, tool in tools.items():
        if not isinstance(tool, dict):
            raise SystemExit(f"{repo_relative(path)}: tools.{tool_id} is not a mapping")
        normalized[str(tool_id)] = normalize_tool(tool)

    snapshot_label = str(data.get("snapshot") or path.stem)
    return {
        "label": f"{repo_relative(path)} ({snapshot_label})",
        "path": path,
        "tools": normalized,
    }


def current_registry_projection() -> dict[str, Any]:
    paths = sorted(TOOLS.glob("*.yaml"))
    if not paths:
        raise SystemExit(f"No tool files found under {repo_relative(TOOLS)}")

    tools: dict[str, dict[str, Any]] = {}
    for path in paths:
        data = load_yaml_mapping(path)
        tool_id = data.get("id") or path.stem
        tools[str(tool_id)] = normalize_tool(data)

    return {
        "label": "current registry/tools/*.yaml projection",
        "path": None,
        "tools": tools,
    }


def snapshot_sort_key(path: Path) -> tuple[int, int, int, int, str]:
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", path.stem)
    if match:
        major, minor, patch = (int(part) for part in match.groups())
        return (1, major, minor, patch, path.name)
    return (0, 0, 0, int(path.stat().st_mtime), path.name)


def latest_snapshot_path() -> Path:
    paths = sorted(SNAPSHOTS.glob("v*.yaml"))
    if not paths:
        raise SystemExit(f"No snapshots found under {repo_relative(SNAPSHOTS)}")
    return max(paths, key=snapshot_sort_key)


def markdown_code(value: Any) -> str:
    if value in (None, ""):
        return "`null`"
    text = str(value).replace("`", r"\`")
    return f"`{text}`"


def version_ref(tool: dict[str, Any]) -> Any:
    version = tool.get("version")
    if isinstance(version, dict):
        return version.get("ref")
    return version


def tool_title(tool_id: str, tool: dict[str, Any]) -> str:
    name = str(tool.get("name") or tool_id)
    if name == tool_id:
        return f"`{tool_id}`"
    return f"**{name}** (`{tool_id}`)"


def describe_tool(tool_id: str, tool: dict[str, Any]) -> str:
    details: list[str] = []
    if tool.get("primary_category"):
        details.append(f"category {markdown_code(tool.get('primary_category'))}")
    if tool.get("status"):
        details.append(f"status {markdown_code(tool.get('status'))}")
    if version_ref(tool):
        details.append(f"version {markdown_code(version_ref(tool))}")
    if tool.get("verified_at"):
        details.append(f"verified_at {markdown_code(tool.get('verified_at'))}")
    if details:
        return f"{tool_title(tool_id, tool)} - " + "; ".join(details)
    return tool_title(tool_id, tool)


def version_changes(before: Any, after: Any) -> list[str]:
    if isinstance(before, dict) and isinstance(after, dict):
        keys = list(VERSION_FIELDS)
        keys.extend(sorted(key for key in set(before) | set(after) if key not in VERSION_FIELDS))
        return [
            f"version.{key} {markdown_code(before.get(key))} -> {markdown_code(after.get(key))}"
            for key in keys
            if before.get(key) != after.get(key)
        ]
    return [f"version {markdown_code(before)} -> {markdown_code(after)}"]


def field_changes(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    changes: list[str] = []
    for field in TRACKED_FIELDS:
        if before.get(field) == after.get(field):
            continue
        if field == "version":
            changes.extend(version_changes(before.get(field), after.get(field)))
        else:
            changes.append(f"{field} {markdown_code(before.get(field))} -> {markdown_code(after.get(field))}")
    return changes


def bullet(tool_id: str, tool: dict[str, Any], details: list[str]) -> str:
    if details:
        return f"- {tool_title(tool_id, tool)} - " + "; ".join(details)
    return f"- {describe_tool(tool_id, tool)}"


def compare_snapshots(
    before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]]
) -> dict[str, list[str]]:
    sections = {"Added": [], "Changed": [], "Deprecated": [], "Removed": []}

    before_ids = set(before)
    after_ids = set(after)

    for tool_id in sorted(after_ids - before_ids):
        sections["Added"].append(f"- {describe_tool(tool_id, after[tool_id])}")

    for tool_id in sorted(before_ids - after_ids):
        sections["Removed"].append(
            bullet(tool_id, before[tool_id], ["missing from target registry/snapshot"])
        )

    for tool_id in sorted(before_ids & after_ids):
        old_tool = before[tool_id]
        new_tool = after[tool_id]
        changes = field_changes(old_tool, new_tool)
        old_status = old_tool.get("status")
        new_status = new_tool.get("status")

        if new_status == "deprecated" and old_status != "deprecated":
            sections["Deprecated"].append(bullet(tool_id, new_tool, changes))
        elif new_status == "removed" and old_status != "removed":
            sections["Removed"].append(bullet(tool_id, new_tool, changes))
        elif changes:
            sections["Changed"].append(bullet(tool_id, new_tool, changes))

    return sections


def render_markdown(source: dict[str, Any], target: dict[str, Any]) -> str:
    source_tools = source["tools"]
    target_tools = target["tools"]
    sections = compare_snapshots(source_tools, target_tools)

    lines = [
        "# Changelog Draft",
        "",
        f"Compared {markdown_code(source['label'])} -> {markdown_code(target['label'])}.",
        f"Tool count: {len(source_tools)} -> {len(target_tools)}.",
        "",
    ]
    for heading in ("Added", "Changed", "Deprecated", "Removed"):
        lines.append(f"## {heading}")
        if sections[heading]:
            lines.extend(sections[heading])
        else:
            lines.append("_No changes._")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from",
        dest="from_path",
        help="source snapshot path; defaults to the latest snapshots/v*.yaml",
    )
    parser.add_argument(
        "--to",
        dest="to_path",
        help="target snapshot path; defaults to the current registry/tools/*.yaml projection",
    )
    args = parser.parse_args()

    source_path = resolve_path(args.from_path) if args.from_path else latest_snapshot_path()
    source = load_snapshot(source_path)
    target = load_snapshot(resolve_path(args.to_path)) if args.to_path else current_registry_projection()

    print(render_markdown(source, target), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
