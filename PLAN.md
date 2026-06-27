# PLAN — code-agent-toolsmith（registry / 知识库层）

> **范围说明（v0.2.0 起）**：本项目的整体定位已明确为一个 **AI 工具选型顾问**
> (advisor)，见 `README.md` 与 `SKILL.md`。**本文件只描述其底层「知识库 / registry」
> 的设计**(数据模型、版本化、变更跟踪)——它是顾问的弹药库,被整合而非取代。
> 顾问的推荐工作流骨架见 `SKILL.md` / `scenarios/` / `references/` / `templates/`。
>
> 以下为知识库层的原始规划(术语「skill 版本」即整个项目的 SemVer)：

> 本文件定义知识库「怎么记录、怎么版本化、怎么跟踪变更」。
> **不凭空填版本号**（需逐个核实），只确定结构与规则。

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

| code（primary_category） | 中文        | 说明                                   | 典型工具                                             |
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
>
> `pipeline/diff_snapshot.py` 可离线比较上一份 release snapshot 与当前
> `registry/tools/*.yaml` 投影（或显式 `--from/--to` 两份 snapshot），生成
> Added / Changed / Deprecated / Removed 草稿；maintainer 审阅后再写入
> `CHANGELOG.md`。
>
> `pipeline/summarize_candidates.py` 可离线读取同一批 registry 条目，按 scenario
> 输出 advisor 使用的候选短表（版本状态、profile 成本、fit、风险、安全信号与冲突图）。
> 它只辅助比较，不替代 `SKILL.md` / `scenarios/` / rubric 的最终推荐判断。
>
> `pipeline/validate_advisor_contract.py` 读取
> `scenarios/fixtures/advisor-contract.yaml`，把 advisor 的四个核心场景、
> quick-oneoff 约束、spec drift-control、每层一个 active tool、方案模板骨架和
> candidate summary 非空要求变成离线回归检查；它不调用真实 LLM。

---

## 7. 仓库布局（Repo layout）

```
.
├── SKILL.md                 # skill manifest（带 version，本 skill 的身份与版本）
├── agents/
│   └── openai.yaml          # UI-facing skill metadata
├── PLAN.md                  # 本规划文件
├── CHANGELOG.md             # skill 各版本 + 工具版本变化记录
├── README.md                # 给人看的索引（Tooling Index 由 registry 自动生成）
├── pipeline/                # registry 校验、README 渲染、快照、候选摘要、self-update playbook
├── scenarios/
│   └── fixtures/
│       └── advisor-contract.yaml  # advisor contract forward-test fixtures
├── registry/
│   ├── schema.yaml          # 条目字段规范（带注释）
│   ├── schema.json          # 机器可校验 mirror
│   └── tools/
│       └── <id>.yaml        # 每个工具一个条目，registry 的 source of truth
└── snapshots/               # 每个 skill 版本的工具版本快照（Step 2 起）
    ├── v0.3.0.yaml          # 旧版发布快照（13 tools）
    └── v0.4.0.yaml          # 当前已发布快照（19 tools）
```

---

## 8. 当前状态与路线图（Roadmap）

| 阶段 | 状态 | 已有产出 | 还缺什么 |
|------|------|----------|----------|
| **v0.1.0 registry skeleton** | ✅ Done | `PLAN.md`、`registry/schema.yaml`、`openspec` 样例、`CHANGELOG.md` | — |
| **v0.2.0 advisor skeleton** | ✅ Done | `SKILL.md` 推荐工作流、`scenarios/`、`references/`、`templates/plan-template.md` | — |
| **v0.3.0 profiled registry** | ✅ Done | 13 个 profiled 工具条目、`schema.json`、`validate.py`、`snapshot.py`、`snapshots/v0.3.0.yaml` | — |
| **Phase 3 foundation** | ✅ Done | `research-playbook.md`、`sources.yaml`、CI validation、`agents/openai.yaml`、`pipeline/render_readme.py`、`pipeline/diff_snapshot.py`、`pipeline/summarize_candidates.py`、`pipeline/validate_advisor_contract.py` | 可选 scheduled runner / future discovery refresh |
| **v0.4.0 candidate expansion** | ✅ Done | Taskmaster、SuperClaude、CodeStable、Comet、ECC、OMC 已入库；`snapshots/v0.4.0.yaml` 冻结 19 个工具 | — |
| **Future advisor reliability** | Planned | v0.4.0 已包含 `pipeline/summarize_candidates.py`、`scenarios/fixtures/advisor-contract.yaml`、`pipeline/validate_advisor_contract.py` | 扩展更多真实输出样例 / UAT，让最终 方案 更稳定、更可测试 |

---

## 9. 还缺什么（Open work）

1. **advisor contract fixtures 已有初版**：`pipeline/summarize_candidates.py`
   已可按 scenario/layer 输出候选短表与冲突图；
   `pipeline/validate_advisor_contract.py` 已把 4 个核心场景的路由与硬规则做成
   离线回归检查。下一步可在真实使用后补充更多 UAT 样例。
2. **v0.4.0 candidate batch 已清空并冻结**：Taskmaster、SuperClaude、
   CodeStable、Comet、ECC、OMC 都已在 v0.4.0 入库；当前 batch 不再保留待处理项。
3. **future discovery refresh**：当前发布快照是 `snapshots/v0.4.0.yaml`
   （19 tools，生成日期 `2026-06-26`）。后续发版前应跑 `research-playbook.md`
   做 freshness check，不能把旧快照说成未来日期的最新状态。
4. **optional unattended scheduled runner 尚未接入**：这依赖带 web + model API secrets 的
   runner。接入前保持 manual / draft PR 流程；接入后也只开 human-reviewable PR，
   不自动合并。

## 10. 已定设计（Accepted decisions）

1. **源数据格式**：YAML 为 source of truth，JSON Schema 为机器校验 mirror。
2. **每工具一文件**：`registry/tools/<id>.yaml`，便于 diff 新增/删除/变更。
3. **快照存放**：`snapshots/v<skill-version>.yaml`，每次 release 冻结全量版本。
4. **版本核实策略**：优先 release/tag；无正式版本时用 rolling/commit/date/none，
   并严格遵守 `verified_at` 不猜测。
5. **README Tooling Index**：由 `pipeline/render_readme.py` 从
   `registry/tools/*.yaml` 生成；CI 用 `--check` 防止 README 与 registry 分叉。
6. **CHANGELOG 草稿**：由 `pipeline/diff_snapshot.py` 离线比较上一份 release
   snapshot 与当前 registry 投影；结果是 maintainer 审阅用草稿，不自动改
   `CHANGELOG.md`。
7. **Advisor 候选摘要**：由 `pipeline/summarize_candidates.py` 离线读取
   `registry/tools/*.yaml` 并按 scenario/layer 投影候选；它是分析输入，不是
   最终推荐引擎。
8. **Advisor contract fixtures**：由 `scenarios/fixtures/advisor-contract.yaml`
   记录四个核心场景的期望路由、默认层、排除项、drift-control 和方案骨架；
   `pipeline/validate_advisor_contract.py` 离线校验这些约束，不调用 LLM。
