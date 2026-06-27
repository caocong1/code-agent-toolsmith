#!/usr/bin/env python3
"""Render a scenario-shaped candidate summary from registry/tools/*.yaml.

This helper is for advisor analysis only. It projects registry facts into a
compact Markdown short list by scenario/layer; it does not make the final
recommendation. The final plan still comes from SKILL.md, the routed scenario
file, and the decision rubric.

Usage:
  python3 pipeline/summarize_candidates.py --scenario new-project
  python3 pipeline/summarize_candidates.py --scenario 2
"""
from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required:  pip install pyyaml")

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "registry" / "tools"

LAYER_ORDER = [
    "base-standard",
    "spec",
    "skill",
    "orchestration",
    "ide-platform",
    "directory",
]

LAYER_LABELS = {
    "base-standard": "Base standard",
    "spec": "Spec / SDD",
    "skill": "Skill / methodology",
    "orchestration": "Orchestration / harness",
    "ide-platform": "IDE / platform",
    "directory": "Directory / discovery",
}

SCENARIO_ALIASES = {
    "1": "new-project",
    "2": "brownfield-adopt",
    "3": "brownfield-optimize",
    "4": "quick-oneoff",
    "new-project": "new-project",
    "brownfield-adopt": "brownfield-adopt",
    "brownfield-optimize": "brownfield-optimize",
    "quick-oneoff": "quick-oneoff",
}

SCENARIOS: dict[str, dict[str, Any]] = {
    "new-project": {
        "id": "1",
        "title": "New project",
        "starting_stack": "Spec-first",
        "starting_point": [
            "Start from `base-standard` + a fuller `spec` layer.",
            "Typical fill: `agents-md` + `spec-kit`; consider `kiro` only when the user accepts the IDE, or `bmad` for a full PRD/agile lifecycle.",
            "Add `skill` or `orchestration` only for a specific trigger: reusable discipline, long task, strong tests, multi-model access, or explicit autonomy appetite.",
        ],
        "default_layers": ["base-standard", "spec"],
        "include_layers": [
            "base-standard",
            "spec",
            "ide-platform",
            "skill",
            "orchestration",
        ],
        "preferred_ids": [
            "agents-md",
            "spec-kit",
            "kiro",
            "bmad",
            "openspec",
            "agent-os",
            "superpowers",
            "trellis",
            "gsd",
            "gstack",
            "ccw",
            "ralph",
            "ccg",
        ],
        "layer_notes": {
            "base-standard": "Default from day one.",
            "spec": "Default comparison set; pick weight by project lifetime, team size, and IDE commitment.",
            "ide-platform": "Conditional: only if the user accepts the IDE/platform lock-in.",
            "skill": "Optional: only when the user wants reusable engineering discipline.",
            "orchestration": "Conditional: large/long work plus tests, multi-model access, or autonomy appetite.",
        },
        "cautions": [
            "Short-lived or tiny projects can drop from Spec-first to Spec-light or Minimal.",
            "Any spec-layer choice needs a drift-control step in the final plan.",
        ],
    },
    "brownfield-adopt": {
        "id": "2",
        "title": "Brownfield adopt",
        "starting_stack": "Spec-light",
        "starting_point": [
            "Start from `base-standard` + lightweight, drift-resistant `spec`.",
            "Typical fill: `agents-md` + `openspec`; `agent-os` is also worth comparing when convention capture is the main pain.",
            "Avoid adding both a skill pack and an orchestration harness during first adoption.",
        ],
        "default_layers": ["base-standard", "spec"],
        "include_layers": [
            "base-standard",
            "spec",
            "ide-platform",
            "skill",
            "orchestration",
        ],
        "preferred_ids": [
            "agents-md",
            "openspec",
            "agent-os",
            "spec-kit",
            "kiro",
            "superpowers",
            "trellis",
            "gsd",
            "gstack",
            "ccw",
            "bmad",
            "ccg",
            "ralph",
        ],
        "layer_notes": {
            "base-standard": "Default: document existing conventions and commands first.",
            "spec": "Default comparison set, but prefer low-friction tools on an existing codebase.",
            "ide-platform": "Conditional: only if the team is already ready to move into that IDE.",
            "skill": "Heavier fallback; avoid global skill-pack adoption on the first slice.",
            "orchestration": "Usually off for first adoption; require a large/long change and strong tests.",
        },
        "cautions": [
            "Full SDD and full-auto loops are brownfield risks unless the slice is large and tests are strong.",
            "Adopt on one feature/slice first; do not turn on many layers at once.",
        ],
    },
    "brownfield-optimize": {
        "id": "3",
        "title": "Brownfield optimize / switch",
        "starting_stack": "Remove-before-add baseline",
        "starting_point": [
            "Do not select from scratch: audit the current stack, retire duplicate/conflicting layers, then compare replacements only for the missing or broken layer.",
            "Keep or create a small `base-standard` layer unless the current setup already has a clean equivalent.",
            "Pain drives sorting: token burn favors low-cost candidates; conflicts favor one authority per layer; spec drift favors lighter spec plus drift control.",
        ],
        "default_layers": ["base-standard"],
        "include_layers": [
            "base-standard",
            "spec",
            "ide-platform",
            "skill",
            "orchestration",
        ],
        "preferred_ids": [
            "agents-md",
            "openspec",
            "agent-os",
            "spec-kit",
            "kiro",
            "superpowers",
            "trellis",
            "gsd",
            "gstack",
            "ccw",
            "bmad",
            "ccg",
            "ralph",
        ],
        "layer_notes": {
            "base-standard": "Keep/consolidate if it reduces repeated prompting.",
            "spec": "Compare for drift and ceremony; lighter is often the replacement.",
            "ide-platform": "Keep only if platform commitment is part of the user's desired setup.",
            "skill": "Audit whether skills are scoped per task or globally bloating every task.",
            "orchestration": "Most likely retirement target when the pain is cost, instability, or too many tools.",
        },
        "cautions": [
            "This helper cannot know the installed stack; use it as a conflict/risk map after inventory.",
            "The final plan must say what to retire before saying what to add.",
        ],
    },
    "quick-oneoff": {
        "id": "4",
        "title": "Quick one-off",
        "starting_stack": "Minimal or none",
        "starting_point": [
            "Default to a direct prompt, or at most an existing/base `base-standard` file.",
            "Do not recommend `spec`, `skill`, or `orchestration` for a throwaway task.",
            "If the task is actually load-bearing or long-lived, re-route to scenario 1 or 2 instead.",
        ],
        "default_layers": [],
        "include_layers": ["base-standard"],
        "excluded_layers": ["spec", "skill", "orchestration", "ide-platform", "directory"],
        "preferred_ids": ["agents-md"],
        "layer_notes": {
            "base-standard": "Only if already present or cheap enough to write in a few lines.",
        },
        "cautions": [
            "Spec, skill, and orchestration layers are deliberately excluded by default for one-off work.",
            "Keep the final plan to the smallest useful prompt/tool note.",
        ],
    },
}

COST_ORDER = {"low": 0, "medium": 1, "high": 2}
STATUS_ORDER = {"active": 0, "maintained": 1, "unknown": 2, "deprecated": 3, "removed": 4}


def normalize_scalar(value: Any) -> str:
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    if value in (None, ""):
        return ""
    return str(value)


def markdown_cell(value: Any) -> str:
    text = " ".join(normalize_scalar(value).split())
    return text.replace("|", r"\|") if text else "_unknown_"


def code(value: Any) -> str:
    text = normalize_scalar(value)
    if not text:
        return "`null`"
    return "`" + text.replace("`", r"\`") + "`"


def clean_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [normalize_scalar(item) for item in value if normalize_scalar(item)]


def load_tools() -> list[dict[str, Any]]:
    paths = sorted(TOOLS.glob("*.yaml"))
    if not paths:
        raise SystemExit(f"No tool files found under {TOOLS.relative_to(REPO)}")

    tools: list[dict[str, Any]] = []
    for path in paths:
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            raise SystemExit(f"{path.relative_to(REPO)}: YAML parse error: {exc}") from exc
        if not isinstance(data, dict):
            raise SystemExit(f"{path.relative_to(REPO)}: top level is not a mapping")
        data["_path"] = path
        tools.append(data)
    return tools


def version_display(tool: dict[str, Any]) -> str:
    version = tool.get("version") or {}
    kind = normalize_scalar(version.get("kind"))
    ref = normalize_scalar(version.get("ref"))
    verified_at = normalize_scalar(tool.get("verified_at"))

    if not verified_at or ref == "TBD":
        return f"_unverified_ (kind: {code(kind)}, ref: {code(ref or 'TBD')}, verified_at: `null`)"
    if kind and kind != ref:
        return f"{code(kind)} {code(ref)}; verified_at: {code(verified_at)}"
    return f"{code(ref)}; verified_at: {code(verified_at)}"


def profile_value(profile: dict[str, Any], field: str) -> str:
    value = normalize_scalar(profile.get(field))
    return value if value else "unknown"


def profile_display(profile: dict[str, Any]) -> str:
    return "<br>".join(
        [
            f"token: {code(profile_value(profile, 'token_cost_profile'))}",
            f"setup: {code(profile_value(profile, 'setup_complexity'))}",
            f"learning: {code(profile_value(profile, 'learning_curve'))}",
            f"autonomy: {code(profile_value(profile, 'autonomy_level'))}",
        ]
    )


def format_refs(ids: list[str], by_id: dict[str, dict[str, Any]]) -> str:
    if not ids:
        return "_none_"
    parts: list[str] = []
    for tool_id in ids:
        tool = by_id.get(tool_id)
        if tool:
            parts.append(f"{code(tool_id)} ({markdown_cell(tool.get('name'))})")
        else:
            parts.append(code(tool_id))
    return "<br>".join(parts)


def security_display(profile: dict[str, Any]) -> str:
    signals = clean_list(profile.get("security_signals"))
    if not signals:
        return "_none noted_"
    return "<br>".join(markdown_cell(signal) for signal in signals)


def fit_display(profile: dict[str, Any]) -> str:
    best = markdown_cell(profile.get("best_fit"))
    anti = markdown_cell(profile.get("anti_fit"))
    return f"best: {best}<br>anti: {anti}"


def tool_row(tool: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> str:
    profile = tool.get("profile") or {}
    relations = "<br>".join(
        [
            f"plays: {format_refs(clean_list(profile.get('plays_well_with')), by_id)}",
            f"conflicts: {format_refs(clean_list(profile.get('conflicts_with')), by_id)}",
        ]
    )
    candidate = "<br>".join(
        [
            f"**{markdown_cell(tool.get('name'))}** ({code(tool.get('id'))})",
            f"status: {code(tool.get('status'))}",
            markdown_cell(tool.get("summary")),
        ]
    )
    return (
        f"| {candidate} | {version_display(tool)} | {profile_display(profile)} | "
        f"{fit_display(profile)} | {security_display(profile)} | {relations} |"
    )


def scenario_sort_key(config: dict[str, Any], tool: dict[str, Any]) -> tuple[int, int, int, int, str]:
    preferred = {tool_id: index for index, tool_id in enumerate(config["preferred_ids"])}
    profile = tool.get("profile") or {}
    token = COST_ORDER.get(profile_value(profile, "token_cost_profile"), 1)
    setup = COST_ORDER.get(profile_value(profile, "setup_complexity"), 1)
    status = STATUS_ORDER.get(normalize_scalar(tool.get("status")), 9)
    return (
        preferred.get(normalize_scalar(tool.get("id")), 99),
        token,
        setup,
        status,
        normalize_scalar(tool.get("name")).lower(),
    )


def tools_by_layer(
    tools: list[dict[str, Any]], config: dict[str, Any]
) -> dict[str, list[dict[str, Any]]]:
    included = set(config["include_layers"])
    grouped: dict[str, list[dict[str, Any]]] = {layer: [] for layer in config["include_layers"]}
    for tool in tools:
        layer = normalize_scalar(tool.get("primary_category"))
        if layer in included:
            grouped.setdefault(layer, []).append(tool)
    for layer, items in grouped.items():
        grouped[layer] = sorted(items, key=lambda item: scenario_sort_key(config, item))
    return grouped


def default_layers_display(config: dict[str, Any]) -> str:
    layers = config.get("default_layers") or []
    if not layers:
        return "`none` (direct prompt) or optional existing `base-standard`"
    return ", ".join(code(layer) for layer in layers)


def render_starting_point(scenario: str, config: dict[str, Any]) -> list[str]:
    lines = [
        f"# Advisor Candidate Summary - Scenario {config['id']}: {scenario}",
        "",
        "> Analysis helper output only. Use this to compare candidates; apply `SKILL.md`, the routed scenario file, and `references/decision-framework.md` for the final 方案.",
        "",
        "## Recommended / Default Stack Starting Point",
        f"- Starting point: **{markdown_cell(config['starting_stack'])}**.",
        f"- Default layers: {default_layers_display(config)}.",
    ]
    lines.extend(f"- {item}" for item in config["starting_point"])
    lines.append("")
    return lines


def conflict_pairs(tools: list[dict[str, Any]]) -> list[tuple[str, str]]:
    ids = {normalize_scalar(tool.get("id")) for tool in tools}
    pairs: set[tuple[str, str]] = set()
    for tool in tools:
        tool_id = normalize_scalar(tool.get("id"))
        profile = tool.get("profile") or {}
        for other in clean_list(profile.get("conflicts_with")):
            if other in ids:
                pairs.add(tuple(sorted((tool_id, other))))
    return sorted(pairs)


def high_cost_tools(tools: list[dict[str, Any]]) -> list[str]:
    flagged: list[str] = []
    for tool in tools:
        profile = tool.get("profile") or {}
        values = {
            "token": profile_value(profile, "token_cost_profile"),
            "setup": profile_value(profile, "setup_complexity"),
            "learning": profile_value(profile, "learning_curve"),
        }
        if "high" in values.values():
            high_fields = ", ".join(name for name, value in values.items() if value == "high")
            flagged.append(f"{code(tool.get('id'))} ({high_fields})")
    return flagged


def unverified_tools(tools: list[dict[str, Any]]) -> list[str]:
    flagged: list[str] = []
    for tool in tools:
        version = tool.get("version") or {}
        ref = normalize_scalar(version.get("ref"))
        if not normalize_scalar(tool.get("verified_at")) or ref == "TBD":
            flagged.append(code(tool.get("id")))
    return flagged


def security_tools(tools: list[dict[str, Any]]) -> list[str]:
    flagged: list[str] = []
    for tool in tools:
        profile = tool.get("profile") or {}
        signals = clean_list(profile.get("security_signals"))
        if signals:
            flagged.append(f"{code(tool.get('id'))}: " + "; ".join(markdown_cell(s) for s in signals))
    return flagged


def excluded_layer_note(
    config: dict[str, Any], tools: list[dict[str, Any]]
) -> list[str]:
    notes: list[str] = []
    excluded = config.get("excluded_layers") or []
    if not excluded:
        return notes

    for layer in excluded:
        names = [
            f"{normalize_scalar(tool.get('name'))} ({normalize_scalar(tool.get('id'))})"
            for tool in tools
            if normalize_scalar(tool.get("primary_category")) == layer
        ]
        if names:
            notes.append(
                f"`{layer}` deliberately excluded by default: "
                + ", ".join(sorted(names))
                + "."
            )
        else:
            notes.append(f"`{layer}` deliberately excluded by default.")
    return notes


def render_cautions(
    config: dict[str, Any],
    included_tools: list[dict[str, Any]],
    all_tools: list[dict[str, Any]],
) -> list[str]:
    lines = ["## Deliberately Excluded / Caution Notes"]
    notes: list[str] = list(config.get("cautions") or [])
    notes.append("`directory` layer entries are discovery sources, not stack members.")
    notes.extend(excluded_layer_note(config, all_tools))

    unverified = unverified_tools(included_tools)
    if unverified:
        notes.append("Unverified/version caution: " + ", ".join(unverified) + ".")

    high_cost = high_cost_tools(included_tools)
    if high_cost:
        notes.append("High-overhead candidates need an explicit trigger: " + ", ".join(high_cost) + ".")

    security = security_tools(included_tools)
    if security:
        notes.append("Security signals to surface in caveats: " + " | ".join(security) + ".")

    pairs = conflict_pairs(included_tools)
    if pairs:
        rendered = ", ".join(f"{code(left)} <-> {code(right)}" for left, right in pairs)
        notes.append("Conflict graph among shown candidates: " + rendered + ".")

    if not notes:
        lines.append("- _None._")
    else:
        lines.extend(f"- {note}" for note in notes)
    lines.append("")
    return lines


def render_candidates(
    scenario: str,
    config: dict[str, Any],
    tools: list[dict[str, Any]],
) -> str:
    by_id = {normalize_scalar(tool.get("id")): tool for tool in tools}
    grouped = tools_by_layer(tools, config)
    included_tools = [tool for items in grouped.values() for tool in items]

    lines = render_starting_point(scenario, config)
    lines.extend(
        [
            "## Candidates by Layer",
            "",
        ]
    )

    for layer in config["include_layers"]:
        label = LAYER_LABELS.get(layer, layer)
        default_marker = " - default layer" if layer in config.get("default_layers", []) else ""
        lines.append(f"### {label} (`{layer}`){default_marker}")
        note = (config.get("layer_notes") or {}).get(layer)
        if note:
            lines.append(f"_Posture: {note}_")
            lines.append("")
        items = grouped.get(layer, [])
        if not items:
            lines.append("_No registry candidates in this layer._")
            lines.append("")
            continue
        lines.extend(
            [
                "| Candidate | Version / verified_at | Profile | Best fit / anti-fit | Security signals | Relationships |",
                "|---|---|---|---|---|---|",
            ]
        )
        for tool in items:
            lines.append(tool_row(tool, by_id))
        lines.append("")

    lines.extend(render_cautions(config, included_tools, tools))
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario",
        required=True,
        help="Scenario id/name: 1/new-project, 2/brownfield-adopt, 3/brownfield-optimize, 4/quick-oneoff",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    scenario = SCENARIO_ALIASES.get(str(args.scenario).strip())
    if not scenario:
        valid = ", ".join(["1", "2", "3", "4", "new-project", "brownfield-adopt", "brownfield-optimize", "quick-oneoff"])
        raise SystemExit(f"Unknown scenario {args.scenario!r}. Expected one of: {valid}")

    tools = load_tools()
    print(render_candidates(scenario, SCENARIOS[scenario], tools), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
