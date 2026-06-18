# Layer taxonomy 层模型

The advisor reasons in terms of **layers**, not individual tools. A recommended
stack is a choice of *which layers to turn on* and *which one tool fills each*.
Most tools belong to one `primary_category`; cross-layer tools carry `tags`.

> 顾问按「层」推理,而非单个工具。一个推荐栈 = 选「开哪几层」+「每层用哪一个工具」。

| code (`primary_category`) | 中文 | What the layer does | Default posture | Example tools |
|---|---|---|---|---|
| `base-standard` | 基础标准层 | A long-lived instruction file / format the agent always reads | **Almost always ON** — cheap, low-token, reduces drift | AGENTS.md, Agent Skills (SKILL.md), Cursor Rules |
| `spec` | 规格/SDD 层 | Align requirements/design/tasks before coding | ON when maintainability matters **and** work is non-trivial | OpenSpec, Spec Kit, Kiro, BMAD, Agent OS, Taskmaster, CodeStable, Comet |
| `skill` | 技能/方法论层 | Inject reusable engineering methodology / composable skills | Optional; avoid stacking onto an already-crowded setup | Superpowers, ECC, SuperClaude |
| `orchestration` | 编排/Harness 层 | Multi-agent / multi-CLI / long-task orchestration & memory | ON **only** for long/complex tasks, multi-model, or high autonomy appetite | Trellis, GSD, OMC, CCW, CCG, Ralph, gstack |
| `ide-platform` | IDE/平台层 | Capability bound to a specific IDE/platform | ON only if the user is committed to that IDE | Kiro, Cursor |
| `directory` | 市场/目录层 | Skill collections, directories, security-signal sources | **Never recommended** — a discovery source, not a stack member | anthropics/skills, awesome-agent-skills, awesome-claude-skills, MCP Market, ClaudePluginHub |

## Cross-layer notes
- **Kiro** is primarily `ide-platform` but also provides a `spec` workflow — recommend it only when the user accepts the IDE.
- **gstack** sits in `orchestration` but is really a *role-team / review* layer (CEO/QA/security/release) — best as a review committee, not a coding base.
- **directory** entries are inputs to the self-update pipeline, not things a user "adopts".

## Layer-selection quick rules (full rubric in `decision-framework.md`)
- `base-standard`: on unless it's a true throwaway.
- `spec`: greenfield can afford a fuller SDD; brownfield should prefer a *lightweight, drift-resistant* spec layer.
- `orchestration`: the layer most often **wrongly** added — high token cost and conflict risk. Require an explicit trigger (long task / multi-model / autonomy).
- Never turn on two tools in the **same** layer by default.
