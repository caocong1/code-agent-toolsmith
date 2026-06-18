# Named default stacks 命名默认栈

Each stack is a **starting point** chosen by scenario in Step 2 of the rubric,
then adjusted by the add/remove rules. Tool names are the *typical* fill for each
layer — always confirm version/links from `registry/tools/<id>.yaml` and mark
"unverified" when absent.

> 每个栈是 rubric 第 2 步按场景选的**起点**,再用增删规则调整。工具名是各层的典型填充,版本/链接以 registry 为准。

## Minimal
- **Layers**: `base-standard` only.
- **Default for**: one-off tasks (scenario 4); cautious first brownfield adoption.
- **Typical fill**: an `AGENTS.md` (and/or `CLAUDE.md`, `.cursor/rules`).
- **Posture**: lowest token cost, lowest ceremony. The honest recommendation for throwaways is often *"don't adopt a methodology; here's the minimal prompt approach."*

## Spec-light
- **Layers**: `base-standard` + lightweight `spec`.
- **Default for**: brownfield adoption (scenario 2) with a maintainability goal.
- **Typical fill**: `AGENTS.md` + **OpenSpec**.
- **Posture**: low cost, drift-aware. **Always** pair with a drift-control step (specs reviewed each PR).

## Spec-first
- **Layers**: `base-standard` + fuller SDD `spec`.
- **Default for**: new projects (scenario 1) with a maintainability goal — greenfield can afford to start clean.
- **Typical fill**: `AGENTS.md` + **Spec Kit** (or **Kiro** if IDE-committed, **BMAD** for full agile/PRD lifecycle).
- **Posture**: higher upfront ceremony, pays off over a long-lived codebase.

## Disciplined solo
- **Layers**: `base-standard` + lightweight `spec` + one `skill` pack.
- **Default for**: a solo dev who wants engineering discipline (TDD, planning, review) without multi-agent orchestration.
- **Typical fill**: `AGENTS.md` + OpenSpec + **Superpowers** (enable per medium/large task, not for trivial changes).
- **Posture**: medium. Watch for verbosity/token cost on small tasks — keep the skill scoped.

## Orchestrated
- **Layers**: `base-standard` + `spec` + one `orchestration` harness.
- **Default for**: large/long/multi-day tasks, multi-model availability, higher autonomy tolerance.
- **Typical fill**: AGENTS.md + a spec layer + **one** of GSD (long context-heavy tasks) / Trellis (cross-session memory & standards) / CCG·CCW (multi-model review) / gstack (product/QA/security review committee).
- **Posture**: highest token cost; **requires strong tests**. Pick exactly one primary loop authority — never stack two harnesses.

## Selection cheatsheet
| Situation signal | Lean toward |
|---|---|
| throwaway / spike | Minimal |
| brownfield + maintainability + token budget | Spec-light |
| greenfield + long-lived + team | Spec-first |
| solo + wants quality, no orchestration | Disciplined solo |
| long task + multi-model + strong tests | Orchestrated |
| "context keeps getting lost across sessions" | add Trellis (memory) over raw GSD |
| "want cross-model review" | CCG (ask three models) / CCW (continuous workflow) — only when needed |
