# Code Agent Toolsmith

An index of AI-assisted development tools, skills, and methodologies for modern code agents.

This repository exists to help both new and existing projects pick the right AI companion — whether it's a planning framework, a spec-first workflow, or an autonomous orchestration layer.

> **Status**: Planning (v0.1.0). This table is the legacy human-readable index.
> The **source of truth is the structured registry** under [`registry/tools/`](registry/tools/),
> governed by [`registry/schema.yaml`](registry/schema.yaml). See [`PLAN.md`](PLAN.md) for the
> data model, taxonomy, skill-versioning scheme, and roadmap, and [`CHANGELOG.md`](CHANGELOG.md)
> for what changed between versions. Verified tool version numbers land in Step 2.

---

## Tooling Index

| Name          | Category         | One-liner                                              |
|---------------|------------------|--------------------------------------------------------|
| **GSD**       | Orchestration    | Git. Ship. Done — fresh-context subagents for long tasks.|
| **BMAD**      | Methodology      | AI-first development method driven by personas.        |
| **Spec Kit**  | Specification    | Spec-driven development toolkit.                       |
| **Kiro**      | IDE / Agent      | AWS-backed AI coding agent with spec-to-code flow.     |
| **OpenSpec**  | Specification    | Lightweight spec layer to align humans & AI before code.|
| **Superpowers** | Capability     | Extended capability pack for coding agents.            |
| **Trellis**   | Management       | AI-guided project planning & tracking framework.       |
| **CCW**       | Orchestration    | Claude-Code-Workflow: skill workflow + multi-CLI orchestration.|
| **Agent OS**  | Orchestration    | Operating-system-style layer for AI agents.            |
| **Taskmaster**| Task Mgmt        | AI-native task management / breakdown.                 |
| **OMC**       | Orchestration    | oh-my-claudecode: teams-first multi-agent orchestration.|
| **CCG**       | Generation       | Code-generation-focused agent skill.                   |
| **ECC**       | Skill            | Everything Claude Code: large agents/skills/hooks pack. |
| **gstack**    | Tooling          | Utility stack for AI-assisted delivery.                |
| **Ralph**     | Loop / Autonomy  | Self-referential execution loop for coding agents.     |
| **CodeStable**| Stability        | Stability-focused agent workflow.                      |
| **Comet**     | Workflow         | Lightweight AI workflow accelerator.                   |

> **Category key**: Workflow · Methodology · Specification · Orchestration · Task Mgmt · IDE/Agent · Skill · Generation · Execution · Tooling · Loop/Autonomy · Stability · Capability.

---

## How to Use This Repo

- **New project**: scan the table, pick a category that fits your team's current pain point, dive into that tool's own docs.
- **Existing project**: look for a tool that plugs into the layer you already have (e.g. if you already use OpenCode, start from the `Skill` / `Orchestration` rows).
- **Comparison**: the table is intentionally shallow — the goal is routing, not evaluation. Deep dives belong in each tool's home repo.

---

## Contributing

This is a living index. PRs welcome to:

- Fix a description
- Add a tool
- Recategorize
- Link to a real homepage

Keep entries **one line, one claim**. Depth belongs elsewhere.

---

## License

MIT
