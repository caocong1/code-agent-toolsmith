# Scenario 2 — Brownfield, adopt AI tooling 旧项目首次引入

An existing codebase with **no AI tooling yet**; the user wants to add/modify
features. **Inherit the common spine (SKILL.md). Below are only the deltas.**

## Phase 1 — Situation intake (delta)
- Lean **hard on codebase inference** (A1–A5): language/stack from manifests, **test maturity** from test dir/CI, size & **team vs solo** from git history. Echo these for confirmation.
- Confirm there really is no AI tooling (A3 fingerprints absent).
- Ask the **specific pain point** being solved (the feature/change), plus Q1 (goal) and Q2 (risk). Ask Q5 only if tests are weak and a full-auto tool might come up.

## Phase 3 — Recommend (delta)
- Bias toward **lightweight, drift-resistant** layers. Brownfield can't absorb a heavy mandatory spec workflow up front.
  - Default **Spec-light**: `AGENTS.md` + **OpenSpec**, with a drift-control step.
  - Maintainability goal + bigger team ⇒ still prefer lightweight first; grow into fuller SDD later.
- Keep `orchestration` OFF unless the change is large/long with strong tests.
- Avoid over-stacking on a first adoption (no skill pack + harness at once).

## Phase 4 — Plan (delta)
- Section 2 **front-loads**: (1) add an `AGENTS.md` capturing existing conventions/build/test commands; (2) **adopt on ONE feature/slice first** to limit blast radius; then (3) the daily loop.
- Caveats: call out brownfield-specific risks (spec drift against legacy code, partial test coverage).

## Common traps for this scenario
- Don't impose full SDD on a large legacy codebase in one shot.
- Don't recommend a full-auto loop when tests are weak (anti-pattern #3).
