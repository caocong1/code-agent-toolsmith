# Interview & inference 访谈与推断

**Core rule: never ask what you can read.** Infer from the repo first, then ask
only the unfilled axes. Present inferred values back for confirmation rather than
asking from scratch — this saves turns and demonstrates the analysis.

> 核心原则:**能读到的绝不问**。先从仓库推断,只问填不上的偏好轴,并把推断值回显请用户纠正。

## Preference axes → source

| # | Axis 偏好轴 | Prefer to INFER from… | Ask only if unobservable |
|---|---|---|---|
| A0 | Scenario 场景 | repo state + scope cues (see SKILL.md routing) | **Q0** (one line) if ambiguous |
| A1 | greenfield vs brownfield | empty repo vs git history / file count | — (almost always inferable) |
| A2 | existing stack / languages | manifests, lockfiles, framework files | only if exotic/unclear |
| A3 | existing AI tooling | `.cursor/`, `CLAUDE.md`, `AGENTS.md`, `openspec/`, `.kiro/`, `.claude/`, `SKILL.md` | — |
| A4 | test maturity | test dir, CI config, coverage files | **Q5** if absent and a full-auto tool is in play |
| A5 | team vs solo | git author count, `CODEOWNERS` | Q if unclear |
| A6 | primary goal / pain | — | **Q1 (always)** |
| A7 | risk tolerance | — | **Q2** |
| A8 | multi-model availability | — | **Q3** |
| A9 | lifetime / horizon | scenario (one-off ⇒ short) | Q if not implied |

## Question bank (ask the smallest subset; batch them — aim for 3–5 max)

- **Q0 — disambiguate (only if routing unclear):**
  "这是全新项目、给已有代码库加 AI 工具、改进已在用的 AI 配置,还是临时一次性需求?"
- **Q1 — goal (always):**
  "现在最看重什么 —— 速度/效率、省 token、长期可维护,还是先把这个快速做完?"(可多选;这是 rubric 的主导轴)
- **Q2 — risk/autonomy:**
  "工具应该多自治 —— 全自动循环,还是每步人工把关?"
- **Q3 — multi-model:**
  "你有不止一个强模型可用吗(例如 Claude + GPT)?"(决定是否考虑利用多模型的编排工具)
- **Q4 — current pain (scenario 3 only):**
  "现状最不满意哪点 —— 成本/烧 token、冲突/不稳定、spec 与代码脱节,还是工具太多难管理?"
- **Q5 — test trust (only if A4 unknown AND a full-auto tool is a candidate):**
  "你的测试套件有多可信,能拦住一次糟糕的改动吗?"

## Output of this phase
A **situation profile**: the axis table with each cell filled and tagged
*(inferred)* or *(asked)*. This profile feeds Phase 2/3 and becomes section 0 of
the 方案. Always echo inferred values, e.g.:

> "我看到一个用 Jest 测试的 Express 应用,还有 `.cursor/rules` 文件,单人开发 —— 有需要纠正的吗?"
