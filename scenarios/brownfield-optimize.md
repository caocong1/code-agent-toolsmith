# Scenario 3 — Optimize / switch existing AI tooling 旧项目优化切换

The user **already uses AI tooling** but is unsatisfied and wants to optimize or
switch. **Inherit the common spine (SKILL.md). Below are only the deltas.** This
scenario relies most heavily on `anti-patterns.md`.

## Phase 1 — Current-setup audit (delta)
- Inventory what's installed: read `A3` fingerprints (`.claude/`, `.cursor/`, `CLAUDE.md`, `AGENTS.md`, `openspec/`, `.kiro/`, installed skills/hooks/MCP). Where readable, quantify the burden (how many hooks/skills, global vs scoped); where not, fall back to self-report.
- Ask **Q4 (the pain)**: cost/token burn, conflicts/instability, spec drift, or too-many-tools. The answer drives the whole recommendation.

## Phase 2 — Gap / diff analysis (delta)
- Don't select from scratch — **diff the current stack against an ideal stack** for this situation. Identify: redundant layers, conflicting tools, and missing layers.

## Phase 3 — Recommend: remove before add (delta)
- **Retire/replace before adding.** The rationale must say what to **stop using**.
  - pain = token burn ⇒ drop `orchestration` / global heavy skills; prefer `token_cost_profile: low`.
  - pain = conflicts/instability ⇒ collapse to **one primary loop authority**; remove duplicate-layer tools (check `conflicts_with`).
  - pain = spec drift ⇒ keep spec but add drift-control, or switch to a lighter spec layer.
  - pain = too many tools ⇒ enforce one-tool-per-layer; cut the rest.

## Phase 4 — Plan (delta)
- Section 1 explicitly lists **what to retire** alongside what to keep/add.
- Section 2 includes a **migration + rollback path** (change one thing at a time; how to revert).
- Caveats cite the specific anti-pattern they hit (usually over-stacking).

## Common traps for this scenario
- Don't answer "switch tool X for tool Y" without first checking whether the real fix is **removing** a layer.
- Don't propose a big-bang migration; sequence it.
