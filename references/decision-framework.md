# Decision framework 推荐决策框架

Philosophy: **start from a named default stack chosen by scenario, then add/remove
layers driven by specific axis values, checking conflicts at each step.** Every
decision cites the registry field or axis that justified it. This is what makes
the recommendation explain **WHY**, not just emit names.

> 从场景选一个命名默认栈 → 据具体偏好轴增删层 → 每步查冲突。每个决定都要引用是哪个轴/registry 字段驱动的。

## Step 1 — Pick the base stack by layer model
Think in layers (see `taxonomy.md`): which layers to turn on.

- **`base-standard`** — almost always ON. Cheap, universal, low token cost, reduces drift. OFF only for true throwaways.
- **`spec`** — ON when *long-term maintainability* (A6) is a goal **and** the work is non-trivial.
  - greenfield (A1) ⇒ can adopt a fuller SDD (Spec Kit / Kiro / BMAD).
  - brownfield (A1) ⇒ prefer *lightweight, drift-resistant* SDD (OpenSpec): heavy mandatory specs create friction on existing code, and static specs drift fast.
- **`skill`** — ON when the user wants reusable engineering discipline and is **not** already drowning in tooling.
- **`orchestration`** — ON **only** for long/complex tasks, multi-model availability (A8), or explicit autonomy appetite (A7). High token cost + conflict risk: the layer most often *wrongly* added.
- **`ide-platform`** — ON only if the user is committed to that IDE.
- **`directory`** — never a recommendation; a discovery source.

## Step 2 — Named default stacks
Starting points, not mandates. Full definitions in `stacks.md`.

| Stack | Layers | Default for | Token/maintenance posture |
|---|---|---|---|
| **Minimal** | base-standard only | one-off (4); cautious adopt (2) | lowest cost, lowest ceremony |
| **Spec-light** | base-standard + lightweight spec (OpenSpec) | adopt (2) with maintainability goal | low cost, drift-aware |
| **Spec-first** | base-standard + fuller SDD (Spec Kit/Kiro/BMAD) | new project (1) with maintainability goal | higher upfront, pays off long-term |
| **Disciplined solo** | base-standard + spec-light + one skill pack | solo dev wanting quality without orchestration | medium |
| **Orchestrated** | base-standard + spec + one orchestration harness | large/long tasks, multi-model, higher risk tolerance | highest cost; needs strong tests |

## Step 3 — Add/remove rules (each tied to an axis + a registry field)
- IF goal includes **token-saving** (A6) → drop `orchestration`; prefer tools whose `profile.token_cost_profile: low`; warn that MCP/skill stacking can inject large token overhead per call.
- IF **brownfield** (A1) AND weak/no tests (A4) → **forbid full-auto loops** (Ralph-style); cite the "full-auto compounds errors without strong tests" anti-pattern.
- IF **multi-model available** (A8) AND **long tasks** → `orchestration` becomes eligible (tools that exploit >1 model); otherwise it is dead weight.
- IF **solo** (A5) → de-prioritize team-first orchestration; prefer single-agent flows.
- IF scenario 3 and pain = "too many tools / conflicts" → **remove before add**: retire overlapping layers (check `profile.conflicts_with`); keep one tool per layer.
- IF unknown `profile.*` for a candidate → assume the conservative value (e.g. token cost = medium) and **say so** in the plan.

## Step 4 — Conflict & anti-pattern gate (always run)
- Never recommend two tools whose `profile.conflicts_with` intersect (e.g. two competing orchestration harnesses, or two spec systems claiming the same `specs/` dir).
- Cap: **at most one tool per layer**; a second requires an explicit reason in the plan.
- Enforce `anti-patterns.md`: over-stacking, spec drift, full-auto-without-tests, methodology-for-throwaway.

## Worked example (include this style of derivation in the plan)
> **Input**: Scenario 2 (existing Express.js API, Jest tests present, a `.cursor/rules` file, solo dev). Q1 goal = "long-term maintainability + don't burn tokens". Q2 = human-in-loop. Q3 = single model.
>
> **Derivation**:
> 1. Scenario 2 + maintainability goal → start at **Spec-light**.
> 2. `base-standard`: **ON** (already has `.cursor/rules`; recommend also consolidating into an `AGENTS.md`). Low token cost; A3 shows partial adoption.
> 3. `spec`: **ON, lightweight (OpenSpec)** not Spec Kit/Kiro — because A1=brownfield (heavy mandatory specs add friction) and A6 includes token-saving (`token_cost_profile: low`). Add a drift-control step (review specs each PR).
> 4. `orchestration`: **OFF** — A6 token-saving + A8 single-model + A5 solo all argue against it; its `token_cost_profile: high` fails the budget goal.
> 5. `skill`: **OFF** for now (avoid over-stacking on a first brownfield adoption); offer as the "heavier" fallback.
> 6. Conflict gate: OpenSpec vs `.cursor/rules` — different layers, no `conflicts_with` overlap. OK.
>
> **Output stack**: AGENTS.md (consolidate rules) + OpenSpec; human-in-loop; adopt on ONE endpoint first.
> **WHY (surfaced in plan)**: maintainability ⇒ a spec layer; brownfield + token budget ⇒ the *lightweight* one; solo + single-model + budget ⇒ no orchestration; deliberately *excluded* skill packs and harnesses to avoid context bloat.

The recommendation must read as a **derivation over axes and registry fields**, and must name what was excluded and why.
