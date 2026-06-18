# Self-update playbook (Phase 3)

This is the **orchestration prompt** for the automated self-update loop that keeps
`registry/tools/*.yaml` fresh and accurate. A strong model with web access (the
*pipeline* side — distinct from the model-agnostic *advisor* side) follows these
stages. Every run ends at a **human-reviewable PR**, never a direct push to the
default branch.

> This playbook codifies the exact process used to build the v0.3.0 registry by
> hand. Automating it must not relax any of the integrity rules below.

## Loop: Discover → Research → Normalize → Validate → Snapshot/Docs → PR

### 1. Discover
- Scan the sources in [`sources.yaml`](sources.yaml): curated awesome-lists, the
  `directory`-layer entries, and the GitHub search queries.
- Produce a candidate set = (tools already in `registry/tools/`) ∪ (newly seen
  names). For existing tools, the job is re-verification (versions drift);
  for new names, full research.

### 2. Research (strong model + web)
For each candidate, gather from **primary sources** (the repo's releases/tags
page, the official homepage/docs) — not from search-summary snippets:
- canonical repo + homepage (a page you actually loaded),
- latest version (exact tag/release string) + release date,
- license, ecosystem (which agents/CLIs/IDEs), maturity signals (age, stars,
  release cadence),
- the `profile:` fields (problem_solved, strengths, weaknesses,
  `token_cost_profile`, `learning_curve`, `setup_complexity`, `maturity`,
  `team_fit`, `project_fit`, `autonomy_level`, `multi_model`, `security_signals`,
  `plays_well_with`, `conflicts_with`, `best_fit`, `anti_fit`).

**Integrity rules (non-negotiable):**
- **No hallucination.** If a candidate has no single canonical owner / repo, or
  you find only ambiguous, conflicting matches, record it as
  `status: unknown` with `version.ref: "TBD"`, `verified_at: null`, and a note
  explaining what you found. **Do not fabricate a plausible entry.** (This is how
  `ccg` is handled — it is a pattern with several incompatible implementations,
  not a product.)
- **Provenance required.** Every entry carries `profile.provenance` = the URLs you
  actually used.
- **`verified_at` is a check date, never a guess.** Set it only to the date you
  confirmed `version.ref` against the source. If you cannot confirm a version,
  leave `version.ref: "TBD"` and `verified_at: null`.
- **Versions come from real release/tag/commit/date** — never invented. Tools
  with no releases use `kind: rolling`/`none`.

### 3. Normalize
Emit one `registry/tools/<id>.yaml` per tool, matching `registry/schema.yaml`:
- `id` lowercase-hyphenated, equal to the filename stem.
- `primary_category` from the layer taxonomy (`references/taxonomy.md`).
- `conflicts_with` lists same-layer rivals / same-resource claimants and **must be
  symmetric** (if A lists B, B lists A).
- Bump `last_changed` to the skill version being released; set `first_seen` on new
  entries. **Deprecation = set `status: deprecated`/`removed` (+ `removed_at`) and
  KEEP the file** — never delete history.

### 4. Validate (hard gate)
Run `python3 pipeline/validate.py`. It enforces schema conformance, the
`verified_at` discipline, `conflicts_with` symmetry, and reference integrity.
**Exit non-zero ⇒ stop. No PR is opened.**

### 5. Snapshot + docs
- `python3 pipeline/snapshot.py` → refresh `snapshots/v<skill_version>.yaml`.
- Update `CHANGELOG.md` (Keep a Changelog: Added/Changed/Deprecated/Removed) with
  the diff vs the previous snapshot.
- Reflect material changes in `README.md` (the tool table) and bump
  `metadata.version` in `SKILL.md` per SemVer (see `PLAN.md`):
  MINOR = new tools / additive profile changes; MAJOR = advisor-contract breaks
  (schema fields the rubric depends on, plan-template structure).

### 6. Open a PR (the only landing surface)
- Open a **draft PR** against the default branch with the snapshot diff and a
  summary. Never push to the default branch directly.
- **Large-change guardrail:** if a run adds/removes/changes more than a threshold
  (e.g. >5 tools or any `MAJOR` schema change), label it for extra human scrutiny
  and do not auto-merge.

## Boundaries
- The **advisor** side (`SKILL.md`, `scenarios/`, `references/`, `templates/`)
  stays model-agnostic and needs no network. Only this pipeline uses a strong
  model + the web.
- Secrets (model API keys) belong to the runner/Action, never the repo.
