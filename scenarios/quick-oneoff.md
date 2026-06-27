# Scenario 4 — Quick / one-off 临时一次性

A throwaway or temporary feature. **Inherit the common spine (SKILL.md), but
collapse it.** The right answer is usually *"don't adopt a methodology."*

## Phase 1 — Intake (delta)
- Ask **nothing or near-nothing**. Infer the task from the prompt; only clarify if the task itself is unclear (not the tooling preferences).

## Phase 3 — Recommend (delta)
- Default to **Minimal or none** (`stacks.md`): base-standard only, or just a good prompt.
- Do **not** turn on `spec`, `skill`, or `orchestration` for a throwaway (anti-pattern #4).
- If the user already has an agent, the recommendation is often "use it directly with a clear prompt; here's the prompt shape."

## Phase 4 — Plan (delta)
- Emit a **3-line plan**: what to do, the one tool/prompt to use, and the single caveat.
- **Omit** the maintenance-posture section (5). Keep token/cost note to one line.

## Common traps for this scenario
- Resist the urge to recommend your favorite framework — it's a throwaway.
- If the "one-off" turns out to be load-bearing/long-lived, say so and route to scenario 1 or 2 instead.
