# Code Agent Toolsmith

**An AI tool-selection advisor for AI-assisted coding** — delivered as an Agent
Skill. Instead of just listing tools, it interviews your situation, recommends a
*right-sized* stack of AI coding tools/skills/methodologies, and writes a concrete
adoption plan (方案) with setup steps and cautions. It is itself an AI coding
tool, but its job is to recommend **other** AI coding tools.

It is **model-agnostic** and runs inside whatever agent you already use (Claude
Code, etc.). The recommendation side needs no network and no extra model; strong
models are used only in the offline self-update pipeline that keeps the tool
knowledge fresh.

> **Status**: v0.3.0 — advisor skeleton (Phase 1) + populated, profiled knowledge
> base (Phase 2). 13 tools carry web-verified versions and decision profiles
> (`profile:`), checked by `pipeline/validate.py` and frozen in
> `snapshots/v0.3.0.yaml`. The fully-automated self-update pipeline lands in
> Phase 3 (see [`PLAN.md`](PLAN.md) and the plan history).

## What it does — 4 scenarios

1. **New project** — requirements set, about to start with a code agent → analyze requirements, recommend a stack, generate a usage plan.
2. **Brownfield, adopt** — existing codebase with no AI tooling, adding/changing features → recommend a lightweight, drift-resistant stack.
3. **Optimize / switch** — already using AI tooling but unhappy → audit, then recommend what to *retire* before adding.
4. **Quick one-off** — a throwaway feature → usually "don't adopt a methodology; here's the minimal approach."

## How it works

- The advisor logic is the **skill**: [`SKILL.md`](SKILL.md) (spine + routing + hard rules) → [`scenarios/`](scenarios/) (per-scenario branches) → [`references/`](references/) (interview, decision framework, stacks, anti-patterns, taxonomy) → [`templates/plan-template.md`](templates/plan-template.md) (the output 方案).
- The **knowledge base** is the registry: [`registry/tools/`](registry/tools/) (one YAML per tool — the source of truth for versions/links/profiles), governed by [`registry/schema.yaml`](registry/schema.yaml) and its machine-checkable mirror [`registry/schema.json`](registry/schema.json). Each release is frozen in [`snapshots/`](snapshots/); [`pipeline/validate.py`](pipeline/validate.py) is the validation gate.
- It reasons in **layers** (see [`references/taxonomy.md`](references/taxonomy.md)): a stack is a choice of which layers to turn on and which one tool fills each.

## Tooling Index (knowledge base, human view)

Categories use the layer taxonomy: `base-standard · spec · skill · orchestration · ide-platform · directory`.
This table mirrors `registry/tools/*.yaml`; versions were web-verified on 2026-06-18 (see each entry's `provenance`).

| Name | Layer | Version | One-liner |
|---|---|---|---|
| **AGENTS.md** | base-standard | rolling | Open instruction-file standard; the near-universal base layer. |
| **OpenSpec** | spec | v1.4.1 | Lightweight in-repo spec layer to align humans & AI before code. |
| **Spec Kit** | spec | 0.11.1 | GitHub's spec→plan→tasks→implement SDD toolkit. |
| **BMAD-METHOD** | spec | v6.8.0 | Agile SDD with PM/Architect/Dev/QA agent roles. |
| **Agent OS** | spec | v3.0.0 | Discovers & injects a codebase's standards into agents. |
| **Kiro** | ide-platform | GA · 2025-11-17 | AWS agentic IDE with a built-in spec-driven flow (proprietary). |
| **Superpowers** | skill | v6.0.2 | Composable TDD/plan/review methodology skills. |
| **GSD** | orchestration | v1.5.0 | Fresh-context subagents (Discuss→Ship) for long tasks. |
| **Trellis** | orchestration | v0.5.15 | Repo-persistent specs/tasks/memory; cross-CLI (AGPL-3.0). |
| **CCW** | orchestration | v7.3.14 | JSON workflow-as-code multi-model orchestration. |
| **gstack** | orchestration | rolling | Role-team (CEO/QA/security/release) review layer. |
| **Ralph** | orchestration | technique | ⚠ Full-auto loop; fresh context each iteration (high-risk). |
| **CCG** | orchestration | _unverified_ | Multi-model review **pattern** — no canonical tool; audit a specific impl. |

> Other tools named in `references/taxonomy.md` (Taskmaster, CodeStable, Comet,
> ECC, OMC, SuperClaude) are **not yet profiled** — the advisor treats them as
> "unverified" until a registry entry exists. Base-standard conventions beyond
> AGENTS.md (CLAUDE.md, Cursor Rules) and directory-layer sources are described
> in the taxonomy.

## How to use this repo

- **As an advisor**: invoke the skill in your agent and describe your situation; it routes to the right scenario, asks a few questions, and produces a 方案.
- **As a maintainer**: add/update tools under `registry/tools/` per `registry/schema.yaml`; run `python3 pipeline/validate.py` (schema + `verified_at` discipline + conflict-graph symmetry + reference integrity) and regenerate the snapshot with `python3 pipeline/snapshot.py`; record changes in [`CHANGELOG.md`](CHANGELOG.md); never fabricate versions (mark "unverified" until checked).

## License

MIT
