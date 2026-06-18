#!/usr/bin/env python3
"""Validate every registry/tools/*.yaml against registry/schema.json plus the
cross-field rules JSON Schema cannot express.

This is the registry's validation gate. Phase 1/2 run it by hand; the Phase 3
self-update pipeline reuses it as a hard gate before opening a PR.

Checks
------
1. Schema:        each tool YAML conforms to registry/schema.json.
2. Filename:      <id>.yaml — the `id` field must equal the filename stem.
3. verified_at:   if verified_at is null, version.ref must be "TBD"; if a real
                  date is set, version.ref must NOT be "TBD" (no guessed versions).
4. References:    every id in profile.conflicts_with / profile.plays_well_with
                  must be a real registry entry.
5. Symmetry:      profile.conflicts_with must be symmetric — if A lists B, B lists A.

Usage:  python3 pipeline/validate.py        # from repo root
Exit code 0 = all good, 1 = at least one error.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required:  pip install pyyaml")
try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("jsonschema is required:  pip install jsonschema")

REPO = Path(__file__).resolve().parent.parent
SCHEMA = REPO / "registry" / "schema.json"
TOOLS = REPO / "registry" / "tools"


def main() -> int:
    schema = json.loads(SCHEMA.read_text())
    validator = Draft202012Validator(schema)

    errors: list[str] = []
    entries: dict[str, dict] = {}

    paths = sorted(TOOLS.glob("*.yaml"))
    if not paths:
        print(f"No tool files found under {TOOLS}")
        return 1

    # Pass 1 — load, schema-validate, per-file lints.
    for path in paths:
        stem = path.stem
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            errors.append(f"{path.name}: YAML parse error: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{path.name}: top level is not a mapping")
            continue

        for err in sorted(validator.iter_errors(data), key=lambda e: e.path):
            loc = "/".join(str(p) for p in err.path) or "(root)"
            errors.append(f"{path.name}: schema: {loc}: {err.message}")

        if data.get("id") != stem:
            errors.append(f"{path.name}: id '{data.get('id')}' != filename stem '{stem}'")

        verified = data.get("verified_at")
        ref = (data.get("version") or {}).get("ref")
        if verified in (None, "") and ref != "TBD":
            errors.append(f"{path.name}: verified_at is null but version.ref is '{ref}' (expected 'TBD')")
        if verified not in (None, "") and ref == "TBD":
            errors.append(f"{path.name}: version.ref is 'TBD' but verified_at is set ('{verified}') — no guessed/placeholder versions with a verify date")

        if isinstance(data.get("id"), str):
            entries[data["id"]] = data

    # Pass 2 — cross-entry reference + symmetry checks.
    ids = set(entries)
    for tid, data in entries.items():
        profile = data.get("profile") or {}
        for field in ("conflicts_with", "plays_well_with"):
            for ref_id in profile.get(field, []) or []:
                if ref_id not in ids:
                    errors.append(f"{tid}.yaml: profile.{field} references unknown id '{ref_id}'")
                if ref_id == tid:
                    errors.append(f"{tid}.yaml: profile.{field} references itself")
        for other in profile.get("conflicts_with", []) or []:
            back = ((entries.get(other) or {}).get("profile") or {}).get("conflicts_with", []) or []
            if other in ids and tid not in back:
                errors.append(f"conflicts_with asymmetry: {tid} lists {other}, but {other} does not list {tid}")

    print(f"Validated {len(paths)} tool file(s) against {SCHEMA.relative_to(REPO)}.")
    if errors:
        print(f"\n{len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("All checks passed: schema OK, verified_at discipline OK, references resolve, conflicts_with symmetric.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
