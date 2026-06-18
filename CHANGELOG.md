# Changelog

All notable changes to **code-agent-toolsmith** (the skill) are recorded here,
following [Keep a Changelog](https://keepachangelog.com/) and SemVer.

Each released version also pins the versions of every tracked tool in
`snapshots/v<version>.yaml` (starting Step 2). See `PLAN.md`.

## [Unreleased]

_Next (Phase 2): extend `registry/schema.yaml` with the `profile:` block
(strengths/weaknesses/token_cost/conflicts_with/…), add `registry/schema.json`,
backfill per-tool profiles, and produce the first complete snapshot
`snapshots/v<version>.yaml`. Then (Phase 3) the fully-automated self-update
pipeline under `pipeline/`._

## [0.2.0] — 2026-06-18

Re-framed the project from a tool **registry** into an AI tool-selection
**advisor**, delivered as a model-agnostic Agent Skill. This release ships the
recommendation **workflow skeleton** (Phase 1); the registry remains the
knowledge-base layer beneath it.

### Added
- `SKILL.md` body re-framed as the advisor: common 5-phase spine, scenario
  routing table, and hard rules (smallest stack, one-tool-per-layer, conflict
  gate, no fabricated versions, output in user's language).
- `scenarios/` — four branch files: `new-project.md`, `brownfield-adopt.md`,
  `brownfield-optimize.md`, `quick-oneoff.md` (deltas over the common spine).
- `references/` — `interview.md` (infer-first question bank), `decision-framework.md`
  (4-step rubric + worked example), `stacks.md` (named default stacks),
  `anti-patterns.md` (over-stacking, spec drift, full-auto-without-tests, …),
  `taxonomy.md` (six-layer model).
- `templates/plan-template.md` — the 方案 output skeleton with a provenance footer.

### Changed
- `SKILL.md` frontmatter: `description` rewritten as a third-person advisor
  trigger; `version` moved into `metadata` (top-level `version` is non-standard);
  added `compatibility` (model-agnostic, no network); bumped to `0.2.0`.
- `README.md` re-framed around the advisor + 4 scenarios; tool table re-categorized
  to the layer taxonomy.

### Notes
- Knowledge base still uses seed data; tool version numbers remain **unverified**
  (filled in Phase 2). The advisor degrades gracefully on empty tool profiles.

## [0.1.0] — 2026-06-17

Initial planning & structure (Step 1). No tool versions are verified yet.

### Added
- `PLAN.md` — project goals, taxonomy, data model, skill-versioning scheme, change-tracking workflow, repo layout, and roadmap.
- `SKILL.md` — skill manifest (version 0.1.0) with maintenance rules.
- `registry/schema.yaml` — field specification for tool entries.
- `registry/tools/openspec.yaml` — one worked example entry (version fields left unverified, pending Step 2).
- `CHANGELOG.md` — this file.

### Changed
- `README.md` — pointed at the registry as source of truth; fixed the `penSpec` typo and a few incorrect tool descriptions in the legacy seed table.

### Notes
- Tool **version numbers are deliberately unverified** at 0.1.0 — Step 1 defines *how* to record versions, not the versions themselves.
