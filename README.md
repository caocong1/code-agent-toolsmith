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

> **Status**: v0.4.0 — advisor skeleton + populated, profiled knowledge base,
> now frozen with the v0.4.0 candidate expansion. 19 tools are pinned in
> [`snapshots/v0.4.0.yaml`](snapshots/v0.4.0.yaml), including Taskmaster,
> SuperClaude, CodeStable, Comet, ECC, and OMC.

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

<!-- tooling-index:start -->

Categories use the layer taxonomy: `base-standard`, `spec`, `skill`, `orchestration`, `ide-platform`, `directory`.
This table is generated from `registry/tools/*.yaml`; edit registry entries, then run `python3 pipeline/render_readme.py`.
Verified registry entries have per-entry `verified_at` dates in `registry/tools/*.yaml`; unverified entries are marked.

| Name | Layer | Version | One-liner |
|---|---|---|---|
| **AGENTS.md** | base-standard | rolling | An open, Markdown instruction-file standard that gives coding agents project-specific context — the near-universal base layer. |
| **Agent OS** | spec | v3.0.0 | Lightweight standards layer that discovers, documents, and injects a codebase's conventions into AI agents so output matches team practice. |
| **BMAD-METHOD** | spec | v6.8.0 | Agile SDD framework that casts AI agents as roles (PM/Architect/Dev/QA) driving a full PRD → architecture → stories → build lifecycle. |
| **CodeStable** | spec | 74f1aa3dee789b3c803f81c8cd34e2a95a40f4c8 | Human-in-the-loop software lifecycle workflow that stores requirements, roadmaps, features, issues, refactors, and retained knowledge under .codestable/. |
| **Comet** | spec | 0.3.9 | Phase-guarded Agent Skill harness that chains OpenSpec and Superpowers into a resumable five-phase idea-to-archive workflow. |
| **OpenSpec** | spec | v1.4.1 | Lightweight spec layer — specs/ as current state, changes/ as proposals — to align humans and AI before coding. |
| **Spec Kit** | spec | 0.11.1 | GitHub's spec-driven toolkit: a structured Spec → Plan → Tasks → Implement workflow that treats specifications as executable artifacts. |
| **Taskmaster** | spec | task-master-ai@0.43.1 | AI task-management layer that turns a PRD into dependency-aware tasks/subtasks and exposes them through CLI/MCP for coding agents. |
| **ECC** | skill | v2.0.0 | Cross-harness agent operating system that packages agents, skills, hooks, rules, MCP conventions, and operator workflows for Claude Code and peer CLIs. |
| **SuperClaude Framework** | skill | v4.3.0 | Claude Code configuration framework that installs /sc commands, specialist agents, behavioral modes, and optional MCP integrations. |
| **Superpowers** | skill | v6.0.2 | Composable Markdown skills that encode engineering discipline (brainstorm → plan → TDD → review) as reusable commands for AI agents. |
| **CCG (multi-model review pattern)** | orchestration | _unverified_ | A cross-model review PATTERN (Claude orchestrates; Gemini/Codex assist + review) — multiple community implementations, no canonical tool. |
| **Claude-Code-Workflow** | orchestration | v7.3.14 | JSON-driven multi-agent orchestration for Claude Code: declarative workflows, CLI routing, a skill registry, and terminal dashboards. |
| **Get Shit Done (GSD)** | orchestration | v1.5.0 | Phase-based orchestration that spawns fresh-context subagents (Discuss → Plan → Execute → Verify → Ship) to fight context rot on long tasks. |
| **gstack** | orchestration | rolling | Installs specialist personas (CEO/QA/Security/Release…) into Claude Code, enforcing review gates so a solo dev gets a virtual engineering team. |
| **oh-my-claudecode (OMC)** | orchestration | v4.15.0 | Claude Code orchestration framework with plugin/CLI install, Team pipelines, autopilot flows, hooks, skills, agents, and tmux workers for peer CLIs. |
| **Ralph (Ralph Wiggum loop)** | orchestration | technique (no formal version) | A full-auto technique: run a coding agent in a loop with fresh context each iteration, using files/git as memory, for hands-off multi-hour runs. |
| **Trellis** | orchestration | v0.5.15 | Persists specs, tasks, and memory into the repo (.trellis/) so any agent resumes cross-session context and work ports across CLIs. |
| **Kiro** | ide-platform | GA | AWS's agentic IDE that mandates a spec-driven workflow (requirements → design → tasks → code) with built-in property-based testing and checkpoints. |

<!-- tooling-index:end -->

> Base-standard conventions beyond AGENTS.md (CLAUDE.md, Cursor Rules) and
> directory-layer sources are described in the taxonomy.

## How to use this repo

- **As an advisor**: invoke the skill in your agent and describe your situation; it routes to the right scenario, asks a few questions, and produces a 方案.
- **As a maintainer**: add/update tools under `registry/tools/` per `registry/schema.yaml`; run `python3 pipeline/validate.py` (schema + `verified_at` discipline + conflict-graph symmetry + reference integrity), `python3 pipeline/render_readme.py`, and `python3 pipeline/render_readme.py --check`; regenerate the snapshot with `python3 pipeline/snapshot.py`; record changes in [`CHANGELOG.md`](CHANGELOG.md); never fabricate versions (mark "unverified" until checked).

## License

MIT
