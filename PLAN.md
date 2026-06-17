# PLAN — code-agent-toolsmith

> 第一步：规划（Step 1: Planning）。本文件定义这个项目「是什么、怎么记录、怎么版本化、怎么跟踪变更」。
> 本步骤**不填真实版本号**（需逐个核实，见 Roadmap 第 2 步），只确定结构与规则。

---

## 1. 这是什么（What this is）

`code-agent-toolsmith` 是一个 **AI 编码工具生态的版本化注册表（registry）**，并且它**本身以一个 Agent Skill 的形式发布**（见 `SKILL.md`）。

一句话：**它是一份「会记账」的工具清单 —— 记录有哪些工具、各属什么类型、各是什么版本；并且这份清单本身有版本号，每发一个版本就把当时所有工具的版本冻结成快照。**

核心要回答的五件事（来自需求）：

1. **有哪些工具** —— registry 收录的工具列表。
2. **各是什么类型** —— 每个工具归入一个分层/分类（taxonomy）。
3. **每个工具的版本号** —— version + 核实日期 + 来源。
4. **本 skill 自己的版本号** —— SemVer，独立演进。
5. **变更全程留痕** —— 工具**新增 / 更新 / 弃用 / 消失**都写进 CHANGELOG；**每个 skill 版本都写明它覆盖的工具版本**（快照 / lockfile 思路）。

---

## 2. 不在本步骤做的事（Non-goals for Step 1）

- ❌ 不填真实版本号（避免凭空编造；真实数据要逐个核实，放第 2 步用 WebSearch/WebFetch 对各自 repo 的 releases 核对）。
- ❌ 不做推荐引擎 / 安装器 / 自动编排（后续可选阶段）。
- ❌ 不一次性建全部 17+ 条目（先定 schema + 1 个样例，结构通过后批量建）。

---

## 3. 分层与分类（Taxonomy）

参考已有的生态分析，划分为「基础标准层 + 五大类」。允许一个工具有 1 个 `primary_category` 和多个 `tags`（因为有些工具跨层，例如 Kiro 既是 Spec 又是 IDE，gstack 既是编排又是角色团队）。

| code（primary_category） | 中文        | 说明                                   | 典型工具（待入库）                                   |
|--------------------------|-------------|----------------------------------------|----------------------------------------------------|
| `base-standard`          | 基础标准层  | 给 agent 的长期说明书 / 格式规范        | AGENTS.md, Agent Skills (SKILL.md), Cursor Rules   |
| `spec`                   | 规格/SDD 层 | 写代码前先对齐需求/设计/任务           | OpenSpec, Spec Kit, Kiro, BMAD, Agent OS, Taskmaster, CodeStable, Comet |
| `skill`                  | 技能/方法论 | 给 agent 注入工程方法论与可组合技能    | Superpowers, ECC, SuperClaude                      |
| `orchestration`          | 编排/Harness| 多 agent / 多 CLI / 长任务 编排与记忆  | Trellis, GSD, OMC, CCW, CCG, Ralph, gstack         |
| `ide-platform`           | IDE/平台层  | 绑定到具体 IDE/平台的能力              | Kiro, Cursor                                       |
| `directory`              | 市场/目录层 | 技能集合、目录、安全信号源             | anthropics/skills, awesome-agent-skills, awesome-claude-skills, MCP Market, ClaudePluginHub |

> 分类是「路由」用途，不是评测。跨层用 `tags` 补充。

---

## 4. 数据模型（Data model）

**源数据用结构化 YAML，每个工具一个文件**：`registry/tools/<id>.yaml`。
（README 的表是「给人看的索引」，由 registry 维护/生成，**registry 才是 source of truth**。）

**为什么不是纯 Markdown 表？** 因为需求要做「版本快照 / 变更检测 / 每个 skill 版本冻结工具版本」。结构化数据可以被脚本校验、按版本对比、并生成 README。纯表格做不到机器对比。

**每工具一文件**（而不是单一大文件）的理由：`git diff` 里「新增/删除一个工具」一眼可见，天然贴合「工具消失/出现要留痕」的需求。

每个条目的字段（schema 详见 `registry/schema.yaml`）：

| 字段              | 含义                                                                 |
|-------------------|----------------------------------------------------------------------|
| `id`              | 稳定标识（小写、连字符），= 文件名                                    |
| `name`            | 展示名                                                               |
| `aliases`         | 别名/全称（如 CCW = Claude-Code-Workflow）                           |
| `primary_category`| 主分类，取自 taxonomy 的 code                                        |
| `tags`            | 次分类/关键词（可含其他 category code）                              |
| `summary`         | 一句话定位                                                          |
| `source`          | `{ repo, homepage }`                                                |
| `version`         | `{ kind, ref, released_at }`，见下                                  |
| `verified_at`     | 我们最后一次核实该版本的日期（YYYY-MM-DD）                          |
| `status`          | `active` / `maintained` / `deprecated` / `removed` / `unknown`     |
| `ecosystem`       | 目标 agent/CLI 列表（claude-code, codex, cursor, opencode, gemini…）|
| `first_seen`      | 首次收录时的 skill 版本                                              |
| `last_changed`    | 最后一次条目变更时的 skill 版本                                      |
| `notes`           | 备注（风险/安全信号/适用场景）                                       |

### `version` 怎么填（关键设计）

很多工具是 GitHub repo，没有正式 SemVer 发布。所以 `version` 用一个三元组兼容各种情况：

- `kind`: `release` | `tag` | `commit` | `date` | `rolling` | `none`
- `ref`: 具体值（如 `v1.4.0`、commit SHA、`2026-06-01`、或 `rolling`）
- `released_at`: 该 ref 的发布/提交日期（已知则填）

→ 有 release 用 release；只有 tag 用 tag；都没有就用最新 commit + 日期（`kind: commit`）；持续滚动无版本概念用 `rolling`。

---

## 5. 本 Skill 的版本化（Skill versioning）

`SKILL.md` 里的 `version` 采用 **SemVer** `MAJOR.MINOR.PATCH`，**独立于任何被收录的工具版本**：

- **MAJOR** — schema 或 taxonomy 的破坏性变更（字段含义改了、分类体系重构）。
- **MINOR** — 新增/移除工具，或某工具版本有显著升级。
- **PATCH** — 描述、链接、元数据等修正。

### 「每个 skill 版本写明工具版本」如何落地（快照 / lockfile）

每次发布一个 skill 版本，就生成一份**快照**，冻结当时**所有工具**的 `version.ref` + `verified_at` + `status`。

- 存放：`snapshots/v<MAJOR.MINOR.PATCH>.yaml`（机器可对比）。
- 同时在 `CHANGELOG.md` 该版本段落里以人类可读形式列出关键变化。

这样任何一个历史 skill 版本，都能回答「那时候各工具是什么版本」。两个快照对比即可自动生成「哪些工具升级/新增/消失」。

---

## 6. 变更跟踪（Change tracking）

`CHANGELOG.md` 遵循 [Keep a Changelog](https://keepachangelog.com/) 规范，每个 skill 版本一段，分类记录：

- **Added** — 新工具入库（新建 `registry/tools/<id>.yaml`）。
- **Changed** — 工具版本变化（`version.ref` 改变，`verified_at` 更新）/ 描述更正。
- **Deprecated** — 工具被标记弃用（`status: deprecated`）。
- **Removed** — 工具消失/停更（`status: removed` + `removed_at`）。**条目保留不物理删除**，便于追溯历史。

> 原则：工具「消失」不等于「删文件」。把 `status` 置为 `removed` 并保留条目，是为了让历史快照仍然自洽、可追溯。

---

## 7. 仓库布局（Repo layout）

```
.
├── SKILL.md                 # skill manifest（带 version，本 skill 的身份与版本）
├── PLAN.md                  # 本规划文件
├── CHANGELOG.md             # skill 各版本 + 工具版本变化记录
├── README.md                # 给人看的索引（指向 registry；后续可由脚本生成）
├── registry/
│   ├── schema.yaml          # 条目字段规范（带注释）
│   └── tools/
│       ├── openspec.yaml    # ✅ Step 1 提供的 1 个样例条目
│       └── <id>.yaml        # 其余工具（Step 2 批量建立）
└── snapshots/               # 每个 skill 版本的工具版本快照（Step 2 起）
    └── v0.1.0.yaml          # （Step 2 生成第一个完整快照）
```

---

## 8. 路线图（Roadmap）

| 步骤 | 内容 | 产出 |
|------|------|------|
| **Step 1（本次）** | 规划 + 结构 + schema + 1 个样例 + CHANGELOG 起点 | 本 PR：`PLAN.md` `SKILL.md` `registry/schema.yaml` `registry/tools/openspec.yaml` `CHANGELOG.md` + README 修正 |
| **Step 2** | 逐个工具建条目；用 WebSearch/WebFetch **核实真实版本**；生成第一份完整快照 | `registry/tools/*.yaml`（全量）、`snapshots/v0.2.0.yaml` |
| **Step 3** | JSON Schema 校验 + README 自动生成脚本 + CI（PR 时校验/重生成） | `scripts/`、CI 配置 |
| **Step 4（可选）** | 安全信号标注、路由/推荐、订阅上游 release 自动提醒 | 增强能力 |

---

## 9. 待确认的设计选择（Open decisions）

以下都已给出推荐默认值，可在 review 本 PR 时推翻：

1. **源数据格式**：YAML（**推荐**，可读、可注释）vs JSON vs 纯 Markdown。
2. **每工具一文件**（**推荐**，diff 清晰）vs 单一 `registry/tools.yaml`。
3. **快照存放**：独立 `snapshots/*.yaml`（**推荐**，可机器对比）vs 仅写进 CHANGELOG。
4. **版本核实策略（Step 2）**：以各 repo 的 **latest release/tag** 为准；无 release 的取最新 commit + 日期。

如果以上默认 OK，Step 2 直接按此批量建条目并核实版本。
