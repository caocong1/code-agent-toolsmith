# Scenario 1 — New project 新项目

Requirements are set; the user is about to start using a code agent on a
greenfield repo. **Inherit the common spine (SKILL.md). Below are only the
deltas.**

## Phase 1 — Situation intake (delta)
- Greenfield: little to infer from code. Emphasize **requirements analysis** instead.
- Ask (batched): domain & expected **lifetime** of the project, **team size**, **multi-model** availability (Q3), and the primary goal (Q1) + risk tolerance (Q2).
- Capture target language/stack if already decided (affects ecosystem fit).

## Phase 3 — Recommend (delta)
- Bias toward **Spec-first** (`stacks.md`) — greenfield can afford to start clean, and SDD up front is cheap when there's no legacy.
  - Long-lived + team ⇒ a fuller SDD (Spec Kit; Kiro if IDE-committed; BMAD for full PRD/agile lifecycle).
  - Short-lived or tiny ⇒ drop back to Spec-light or Minimal.
- `base-standard` ON from day one (`AGENTS.md`).
- Add `orchestration` only if the build is genuinely large/long AND tests will exist AND (multi-model or autonomy appetite).

## Phase 4 — Plan (delta)
- Section 2 includes **"scaffold from day one"** steps: create `AGENTS.md`, initialize the spec workflow, set up the test/CI gate **before** generating feature code.
- Maintenance posture (section 5) is important here — this code will live a long time.

## Common traps for this scenario
- Don't over-scaffold a project whose lifetime/size you haven't confirmed.
- Establish the test/CI gate early so any later autonomy is safe.
