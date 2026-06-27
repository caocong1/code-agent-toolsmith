# Changelog

All notable changes to **code-agent-toolsmith** (the skill) are recorded here,
following [Keep a Changelog](https://keepachangelog.com/) and SemVer.

Each released version also pins the versions of every tracked tool in
`snapshots/v<version>.yaml` (starting Step 2). See `PLAN.md`.

## [Unreleased]

_No unreleased changes are staged. Future work is limited to optional scheduled
runner wiring and future discovery refreshes._

## [0.4.0] — 2026-06-26

Freezes the v0.4.0 registry after the candidate expansion batch.
`snapshots/v0.4.0.yaml` pins 19 tools; the snapshot diff from v0.3.0 shows
13 → 19 tools with six additions and no changed, deprecated, or removed tool
records.

### Added
- `snapshots/v0.4.0.yaml`: frozen tool-version snapshot for v0.4.0 (19 tools).
- `agents/openai.yaml` — UI-facing skill metadata for discovery surfaces, with a
  concise default prompt for invoking `$code-agent-toolsmith`.
- `pipeline/research-playbook.md` — the self-update orchestration prompt
  (discover → research → normalize → validate → snapshot → human-review PR),
  codifying the registry process with its no-hallucination / provenance /
  deprecate-don't-delete guardrails.
- `pipeline/sources.yaml` — discovery sources, search queries, and the empty
  backlog tracker after the v0.4.0 candidate expansion batch.
- `pipeline/README.md` — how to run the loop manually today and what unattended
  scheduling requires.
- `.github/workflows/registry-validate.yml` — CI gate running `pipeline/validate.py`
  on every push / PR, so human and automated changes face the same checks.
- `pipeline/render_readme.py` — README Tooling Index renderer/checker. It reads
  `registry/tools/*.yaml`, writes the generated table by default, and supports
  `--check` for CI without inventing or researching versions.
- `pipeline/diff_snapshot.py` — offline changelog draft helper. By default it
  compares the latest release snapshot to the current registry projection; it
  also supports explicit `--from/--to` snapshot comparisons and emits Added /
  Changed / Deprecated / Removed Markdown sections.
- `pipeline/summarize_candidates.py` — offline advisor candidate summary helper.
  It reads `registry/tools/*.yaml`, accepts scenario names or IDs
  (`new-project`/`1`, `brownfield-adopt`/`2`, `brownfield-optimize`/`3`,
  `quick-oneoff`/`4`), and emits Markdown with default starting points,
  candidates by layer, version/verification status, profile fields, security
  signals, relationship/conflict notes, and scenario cautions. It is analysis
  input only; final recommendation logic stays in `SKILL.md` and the scenario
  rubric.
- `scenarios/fixtures/advisor-contract.yaml` — lightweight advisor contract
  fixtures for the four core request shapes: new project, brownfield adoption,
  brownfield optimization, and quick one-off.
- `pipeline/validate_advisor_contract.py` — offline fixture checker for advisor
  routing, quick-oneoff restraint, spec drift-control, one-tool-per-layer,
  plan-template skeleton coverage, and non-empty candidate summaries.
- `registry/tools/taskmaster.yaml` — Taskmaster, verified from primary
  repo/release/docs sources and profiled as a spec/task management layer.
- `registry/tools/superclaude.yaml` — SuperClaude, verified from the canonical
  org repo/release/docs sources and profiled as a Claude Code skill/command
  framework.
- `registry/tools/codestable.yaml` — CodeStable, verified from the canonical
  repo/commit/docs sources and profiled as a human-in-the-loop spec/lifecycle
  workflow.
- `registry/tools/comet.yaml` — Comet, verified from the canonical
  repo/release/docs sources and profiled as a phase-guarded OpenSpec +
  Superpowers workflow harness.
- `registry/tools/ecc.yaml` — ECC / Everything Claude Code, verified from the
  canonical affaan-m/ECC repo/release/docs sources and profiled as a broad
  Claude Code / cross-harness skill surface.
- `registry/tools/omc.yaml` — oh-my-claudecode (OMC), verified from the
  canonical Yeachan-Heo/oh-my-claudecode repo/release/docs sources and profiled
  as a Claude Code orchestration/hook framework.

### Fixed
- `SKILL.md` frontmatter now keeps compatibility notes under `metadata` so the
  skill passes the standard `quick_validate.py` manifest check.

### Changed
- `SKILL.md`: bumped `metadata.version` to 0.4.0.
- `README.md` status and generated Tooling Index now reflect the frozen v0.4.0
  registry: 19 tools in `snapshots/v0.4.0.yaml`, including Taskmaster,
  SuperClaude, CodeStable, Comet, ECC, and OMC.
- `README.md` Tooling Index is generated from the registry and guarded by
  `.github/workflows/registry-validate.yml` via `render_readme.py --check`.
- `pipeline/README.md` now documents README rendering as part of the manual
  self-update gate, places `diff_snapshot.py` before release changelog editing,
  version bumping, and snapshot generation, and treats scheduled runner wiring
  as optional future work.
- `PLAN.md` now records the snapshot diff helper as the changelog-draft step in
  the self-update loop and marks the v0.4.0 candidate expansion as done.
- `SKILL.md`, `pipeline/README.md`, and `PLAN.md` document when to run the
  candidate summary helper before writing a final 方案.
- `pipeline/README.md`, `PLAN.md`, and `scenarios/fixtures/advisor-contract.yaml`
  document the advisor reliability fixture suite and checker.
- `templates/plan-template.md` now explicitly allows a routed scenario, such as
  quick-oneoff, to omit or shrink a section when its scenario file says so.
- `pipeline/sources.yaml` now has an empty candidate backlog after the v0.4.0
  batch and points future maintenance at discovery refreshes.
- `conflicts_with` edges now include Taskmaster, CodeStable, and Comet
  spec-layer conflicts, SuperClaude / Superpowers / ECC as symmetric
  skill-layer alternatives, and OMC as a same-surface alternative to ECC,
  SuperClaude, GSD, Trellis, CCW, gstack, and Ralph.

## [0.3.0] — 2026-06-18

Populated and profiled the knowledge base (Phase 2). The advisor's
recommendations now resolve against real, web-verified tool data instead of
prose names.

### Added
- `registry/schema.yaml`: a `profile:` block — `problem_solved`, `strengths`,
  `weaknesses`, `token_cost_profile`, `learning_curve`, `setup_complexity`,
  `maturity`, `team_fit`, `project_fit`, `autonomy_level`, `multi_model`,
  `security_signals`, `plays_well_with`, `conflicts_with`, `best_fit`,
  `anti_fit`, `provenance`, `profile_verified_at`.
- `registry/schema.json`: machine-enforceable mirror (JSON Schema 2020-12) — the
  validation gate Phase 3 reuses.
- `registry/tools/`: 12 new profiled entries — `spec-kit`, `bmad`, `agent-os`,
  `kiro`, `superpowers`, `ralph`, `gsd`, `trellis`, `ccw`, `gstack`, `ccg`,
  `agents-md` — each with web-verified versions (2026-06-18) and `provenance` URLs.
- `snapshots/v0.3.0.yaml`: first frozen tool-version snapshot (13 tools).
- `pipeline/validate.py` + `pipeline/snapshot.py`: the registry validation gate
  (schema + `verified_at` discipline + `conflicts_with` symmetry + reference
  integrity) and the snapshot generator.

### Changed
- `registry/tools/openspec.yaml`: verified to v1.4.1 (2026-06-03) and given a
  full `profile:`.
- `SKILL.md`: bumped to 0.3.0; added `metadata.schema_json`.
- `README.md`: tool table rebuilt to mirror the registry with verified versions.
- `references/stacks.md`: CCG references softened to reflect it is a pattern.

### Notes
- **CCG is recorded as an UNVERIFIED pattern** (`status: unknown`, `version.ref:
  TBD`), not a canonical tool: research found multiple incompatible community
  implementations and no canonical owner. The registry flags this rather than
  fabricate an entry — matching the project's no-hallucination rule.
- Tools named in the taxonomy but not yet profiled (Taskmaster, CodeStable,
  Comet, ECC, OMC, SuperClaude) remain name-only; the advisor degrades
  gracefully and marks them "unverified".

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
