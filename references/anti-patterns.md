# Anti-patterns 反模式

Hard constraints the rubric enforces in **every** scenario. Each has a
**detect → avoid** line. These exist because community experience repeatedly
shows them backfiring.

> rubric 在所有场景强制的硬约束。每条都有「如何识别 → 如何规避」。

## 1. Over-stacking 过度堆叠
- **What**: running many tools/harnesses/hooks at once → hook conflicts, context bloat, token burn, opaque behavior.
- **Detect**: more than one tool in the same layer; two orchestration harnesses; "install everything" requests; global hooks from several big packs.
- **Avoid**: at most one tool per layer by default; **one primary loop authority** per session; add a layer only with an explicit trigger; prefer enabling heavy skills per-task, not globally.

## 2. Spec drift 规格漂移
- **What**: specs stop matching the code, then actively mislead the AI — worse than no spec.
- **Detect**: any `spec` layer is ON; long-lived branches; specs not part of review.
- **Avoid**: whenever a spec layer is recommended, **include a drift-control step** — specs reviewed/updated every PR; treat `specs/` as source of truth only if maintained. For small changes, don't force a full proposal.

## 3. Full-auto without tests 全自动但无测试
- **What**: autonomous loops (Ralph-style) compound errors across iterations when there's no strong feedback signal.
- **Detect**: weak/absent tests (A4) + a full-auto / autopilot tool as a candidate.
- **Avoid**: do **not** recommend full-auto loops without a trustworthy test/CI gate. Require `lint / typecheck / test / e2e` (at least some) before autonomy. Otherwise downgrade to human-in-loop.

## 4. Methodology for a throwaway 给一次性任务上方法论
- **What**: imposing SDD/TDD/orchestration on a one-off script wastes time and tokens.
- **Detect**: scenario 4, or "quick / throwaway / 临时" cues.
- **Avoid**: recommend **Minimal or nothing**; a 3-line how-to beats a framework here.

## 5. Spec-as-documentation-graveyard 规格变文档坟场
- **What**: piling up specs/PRDs nobody syncs — ceremony without payoff.
- **Detect**: heavy SDD recommended for a small team/solo with no maintenance capacity.
- **Avoid**: match SDD weight to project lifetime and team; prefer lightweight spec for small/solo.

## 6. Blindly installing third-party skills 盲装第三方 skills
- **What**: skills can carry scripts/hooks; malicious or careless ones cause vulnerabilities, data exfiltration, or surprising behavior.
- **Detect**: recommending a large pack (e.g. ECC-class) or any unaudited third-party skill.
- **Avoid**: surface `profile.security_signals` in the plan's Caveats; recommend auditing files/deps/scripts/network before install; prefer selective adoption over whole-pack installs.

---
**Conflict gate** (mechanical): never co-recommend tools whose
`profile.conflicts_with` intersect; if two candidates claim the same resource
(e.g. `specs/` directory, the primary loop), keep one and state why.
