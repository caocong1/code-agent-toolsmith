# Changelog

All notable changes to **code-agent-toolsmith** (the skill) are recorded here,
following [Keep a Changelog](https://keepachangelog.com/) and SemVer.

Each released version also pins the versions of every tracked tool in
`snapshots/v<version>.yaml` (starting Step 2). See `PLAN.md`.

## [Unreleased]

_Planned for 0.2.0 (Step 2): create the full set of `registry/tools/*.yaml`
entries, verify each tool's real version against its source, and produce the
first complete snapshot `snapshots/v0.2.0.yaml`._

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
