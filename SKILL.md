---
name: code-agent-toolsmith
description: A versioned registry of AI coding-agent tools, skills, and methodologies. Use when you need to know which agent tooling exists (OpenSpec, Superpowers, GSD, Trellis, CCW, Spec Kit, BMAD, etc.), what category/layer each belongs to, its current version, and what changed between registry releases.
version: 0.1.0
license: MIT
metadata:
  status: planning
  source_of_truth: registry/tools/
  schema: registry/schema.yaml
  taxonomy: PLAN.md
  changelog: CHANGELOG.md
---

# code-agent-toolsmith

一个 **AI 编码工具生态的版本化注册表**，本身以 Agent Skill 形式发布。

它回答四个问题：**有哪些工具 / 各是什么类型 / 各是什么版本 / 版本之间变了什么。**

## 怎么读这份 registry

- 所有工具条目在 `registry/tools/<id>.yaml`，**每个文件一个工具**，这是 source of truth。
- 字段含义见 `registry/schema.yaml`；分类体系见 `PLAN.md` 的 Taxonomy。
- `README.md` 是给人看的索引（后续可由 registry 自动生成）。

## 怎么维护（贡献规则）

- **新增工具** → 新建 `registry/tools/<id>.yaml`，`first_seen` 填当前 skill 版本，CHANGELOG 记 `Added`。
- **工具更新** → 改 `version.ref` 并更新 `verified_at`，CHANGELOG 记 `Changed`。
- **工具弃用/消失** → 置 `status: deprecated`/`removed`（不要删文件），CHANGELOG 记 `Deprecated`/`Removed`。
- **不要凭空填版本号**：`version.ref` 必须能在工具的 repo releases/tags 处核实，并记 `verified_at`。

## 版本规则

- 本 skill 用 SemVer：MAJOR=schema/taxonomy 破坏性变更；MINOR=工具增减或显著升级；PATCH=描述修正。
- **每发一个 skill 版本，就在 `snapshots/v<version>.yaml` 冻结当时所有工具的版本**，使任一历史版本都能回答「那时各工具是什么版本」。

> 当前状态：`planning`（Step 1）。结构与规则已定，真实版本号将在 Step 2 逐个核实后填入。详见 `PLAN.md`。
