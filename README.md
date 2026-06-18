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

> **Status**: v0.2.0 — advisor workflow skeleton (Phase 1). The 4-scenario
> recommendation flow, interview model, decision rubric, and plan template are in
> place. Deep per-tool profiles and the self-update pipeline land in later phases
> (see [`PLAN.md`](PLAN.md) and the plan history).

## What it does — 4 scenarios

1. **New project** — requirements set, about to start with a code agent → analyze requirements, recommend a stack, generate a usage plan.
2. **Brownfield, adopt** — existing codebase with no AI tooling, adding/changing features → recommend a lightweight, drift-resistant stack.
3. **Optimize / switch** — already using AI tooling but unhappy → audit, then recommend what to *retire* before adding.
4. **Quick one-off** — a throwaway feature → usually "don't adopt a methodology; here's the minimal approach."

## How it works

- The advisor logic is the **skill**: [`SKILL.md`](SKILL.md) (spine + routing + hard rules) → [`scenarios/`](scenarios/) (per-scenario branches) → [`references/`](references/) (interview, decision framework, stacks, anti-patterns, taxonomy) → [`templates/plan-template.md`](templates/plan-template.md) (the output 方案).
- The **knowledge base** is the registry: [`registry/tools/`](registry/tools/) (one YAML per tool, the source of truth for versions/links/profiles), governed by [`registry/schema.yaml`](registry/schema.yaml).
- It reasons in **layers** (see [`references/taxonomy.md`](references/taxonomy.md)): a stack is a choice of which layers to turn on and which one tool fills each.

## Tooling Index (knowledge base, human view)

Categories use the layer taxonomy: `base-standard · spec · skill · orchestration · ide-platform · directory`.
Versions/links/deep profiles live in `registry/tools/*.yaml` (being populated).

| Name          | Layer          | One-liner                                              |
|---------------|----------------|--------------------------------------------------------|
| **OpenSpec**  | spec           | Lightweight spec layer to align humans & AI before code.|
| **Spec Kit**  | spec           | Spec-driven development toolkit.                        |
| **BMAD**      | spec           | AI-first agile development driven by personas.          |
| **Agent OS**  | spec           | Injects codebase standards; writes better specs.        |
| **Taskmaster**| spec           | AI-native task breakdown from a PRD.                    |
| **CodeStable**| spec           | Lifecycle capture of requirements/decisions/constraints.|
| **Comet**     | spec           | Lightweight AI workflow accelerator (OpenSpec×Superpowers).|
| **Kiro**      | ide-platform   | AWS-backed AI IDE with a spec-to-code flow.            |
| **Superpowers**| skill         | Engineering-methodology skill pack (TDD/plan/review).  |
| **ECC**       | skill          | Everything Claude Code: large agents/skills/hooks pack. |
| **GSD**       | orchestration  | Git. Ship. Done — fresh-context subagents for long tasks.|
| **Trellis**   | orchestration  | Repo-persistent specs/tasks/memory; agent harness.     |
| **OMC**       | orchestration  | oh-my-claudecode: teams-first multi-agent orchestration.|
| **CCW**       | orchestration  | Claude-Code-Workflow: skill workflow + multi-CLI.      |
| **CCG**       | orchestration  | Claude+Codex+Gemini multi-model workflow engine.       |
| **gstack**    | orchestration  | Role-team (CEO/Eng/QA/security/release) review layer.  |
| **Ralph**     | orchestration  | Autonomous PRD-driven execution loop.                  |

> Base-standard layer (AGENTS.md, Agent Skills/SKILL.md, Cursor Rules) and
> directory layer (awesome-lists, MCP Market, plugin hubs) are tracked in the
> registry but omitted from this table — see `references/taxonomy.md`.

## How to use this repo

- **As an advisor**: invoke the skill in your agent and describe your situation; it routes to the right scenario, asks a few questions, and produces a 方案.
- **As a maintainer**: add/update tools under `registry/tools/` per `registry/schema.yaml`; record changes in [`CHANGELOG.md`](CHANGELOG.md); never fabricate versions (mark "unverified" until checked).

## License

MIT
