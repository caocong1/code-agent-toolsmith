#!/usr/bin/env python3
"""Render README.md's Tooling Index from registry/tools/*.yaml.

The registry is the source of truth. This script only projects registry fields
into the human-facing README table; it does not research, infer, or update tool
versions.

Usage:
  python3 pipeline/render_readme.py          # update README.md in place
  python3 pipeline/render_readme.py --check  # fail if README.md is stale
"""
from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required:  pip install pyyaml")

REPO = Path(__file__).resolve().parent.parent
README = REPO / "README.md"
TOOLS = REPO / "registry" / "tools"

START = "<!-- tooling-index:start -->"
END = "<!-- tooling-index:end -->"
HEADING = "## Tooling Index (knowledge base, human view)"

CATEGORY_ORDER = {
    "base-standard": 0,
    "spec": 1,
    "skill": 2,
    "orchestration": 3,
    "ide-platform": 4,
    "directory": 5,
}


def load_tools() -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    paths = sorted(TOOLS.glob("*.yaml"))
    if not paths:
        raise RuntimeError(f"No tool files found under {TOOLS.relative_to(REPO)}")

    for path in paths:
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            raise RuntimeError(f"{path.relative_to(REPO)}: YAML parse error: {exc}") from exc
        if not isinstance(data, dict):
            raise RuntimeError(f"{path.relative_to(REPO)}: top level is not a mapping")
        data["_path"] = path
        tools.append(data)

    return sorted(
        tools,
        key=lambda tool: (
            CATEGORY_ORDER.get(str(tool.get("primary_category", "")), 99),
            str(tool.get("name", "")).lower(),
            str(tool.get("id", "")),
        ),
    )


def markdown_cell(value: object) -> str:
    text = " ".join(str(value or "").split())
    return text.replace("|", r"\|")


def display_version(tool: dict[str, Any]) -> str:
    version = tool.get("version") or {}
    ref = str(version.get("ref") or "").strip()
    verified_at = tool.get("verified_at")
    if verified_at in (None, "") or ref == "TBD":
        return "_unverified_"
    return markdown_cell(ref)


def verified_summary(tools: list[dict[str, Any]]) -> str:
    dates = sorted({str(tool.get("verified_at")) for tool in tools if tool.get("verified_at")})
    if not dates:
        return "No registry entries have verified versions yet; unverified entries are marked."
    if len(dates) == 1:
        return f"Verified registry entries were checked on {dates[0]}; unverified entries are marked."
    return (
        "Verified registry entries have per-entry `verified_at` dates in "
        "`registry/tools/*.yaml`; unverified entries are marked."
    )


def render_block(tools: list[dict[str, Any]]) -> str:
    lines = [
        START,
        "",
        "Categories use the layer taxonomy: `base-standard`, `spec`, `skill`, "
        "`orchestration`, `ide-platform`, `directory`.",
        "This table is generated from `registry/tools/*.yaml`; edit registry entries, "
        "then run `python3 pipeline/render_readme.py`.",
        verified_summary(tools),
        "",
        "| Name | Layer | Version | One-liner |",
        "|---|---|---|---|",
    ]

    for tool in tools:
        name = markdown_cell(tool.get("name"))
        layer = markdown_cell(tool.get("primary_category"))
        version = display_version(tool)
        summary = markdown_cell(tool.get("summary"))
        lines.append(f"| **{name}** | {layer} | {version} | {summary} |")

    lines.extend(["", END])
    return "\n".join(lines)


def replace_block(readme_text: str, block: str) -> str:
    if START in readme_text or END in readme_text:
        start = readme_text.find(START)
        end = readme_text.find(END)
        if start == -1 or end == -1 or end < start:
            raise RuntimeError("README.md has mismatched Tooling Index markers")
        return readme_text[:start] + block + readme_text[end + len(END) :]

    heading = readme_text.find(HEADING)
    if heading == -1:
        raise RuntimeError(f"README.md is missing heading: {HEADING}")

    after_heading = readme_text.find("\n", heading)
    if after_heading == -1:
        raise RuntimeError("README.md Tooling Index heading is not followed by a newline")
    after_heading += 1

    next_heading = readme_text.find("\n## ", after_heading)
    if next_heading == -1:
        raise RuntimeError("README.md Tooling Index section has no following level-2 heading")
    next_heading += 1

    return readme_text[:after_heading] + "\n" + block + "\n\n" + readme_text[next_heading:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if README.md is not up to date")
    args = parser.parse_args()

    tools = load_tools()
    current = README.read_text()
    expected = replace_block(current, render_block(tools))

    if args.check:
        if current == expected:
            print(f"README.md Tooling Index is up to date ({len(tools)} tool file(s)).")
            return 0
        diff = difflib.unified_diff(
            current.splitlines(keepends=True),
            expected.splitlines(keepends=True),
            fromfile="README.md",
            tofile="README.md (generated)",
        )
        sys.stderr.writelines(diff)
        print(
            "README.md Tooling Index is stale; run `python3 pipeline/render_readme.py`.",
            file=sys.stderr,
        )
        return 1

    if current == expected:
        print(f"README.md Tooling Index already up to date ({len(tools)} tool file(s)).")
        return 0

    README.write_text(expected)
    print(f"Updated README.md Tooling Index from {len(tools)} registry tool file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
