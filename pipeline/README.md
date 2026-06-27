# pipeline/ — registry validation & self-update

This directory is the **pipeline** side of code-agent-toolsmith: the tooling that
keeps the knowledge base (`registry/tools/*.yaml`) accurate. Unlike the advisor
(model-agnostic, offline), the pipeline may use a strong model + the web.

## Pieces
- **`validate.py`** — the validation gate: schema (`registry/schema.json`) + the
  cross-field rules JSON Schema can't express (`verified_at` discipline,
  `conflicts_with` symmetry, reference integrity).
  Run: `python3 pipeline/validate.py` (needs `pip install pyyaml jsonschema`).
- **`render_readme.py`** — regenerate the human-facing Tooling Index in
  `README.md` from `registry/tools/*.yaml`, with `--check` for CI.
  Run: `python3 pipeline/render_readme.py` or
  `python3 pipeline/render_readme.py --check`.
- **`snapshot.py`** — regenerate `snapshots/v<skill_version>.yaml` from the registry.
  Run: `python3 pipeline/snapshot.py [--date YYYY-MM-DD]`.
- **`diff_snapshot.py`** — compare a release snapshot with the current registry
  projection (or another explicit snapshot) and print an Added / Changed /
  Deprecated / Removed Markdown changelog draft. It only compares structured
  fields already in snapshots/registry; it does not research or invent versions.
  Run: `python3 pipeline/diff_snapshot.py [--from snapshots/vX.Y.Z.yaml] [--to snapshots/vA.B.C.yaml]`.
- **`summarize_candidates.py`** — advisor-side Markdown helper. It reads
  `registry/tools/*.yaml`, filters/sorts candidates by scenario
  (`1`/`new-project`, `2`/`brownfield-adopt`, `3`/`brownfield-optimize`,
  `4`/`quick-oneoff`), and prints layer-grouped version/profile/conflict/risk
  notes. It does not make the final recommendation.
  Run: `python3 pipeline/summarize_candidates.py --scenario new-project`.
- **`validate_advisor_contract.py`** — advisor contract fixture lint. It checks
  `scenarios/fixtures/advisor-contract.yaml` against routing, quick-oneoff
  restraint, spec drift-control, one-tool-per-layer, plan skeleton, and candidate
  summary non-empty rules.
  Run: `python3 pipeline/validate_advisor_contract.py`.
- **`research-playbook.md`** — the orchestration prompt a strong model follows to
  discover → research → normalize → validate → changelog draft → snapshot → open a PR.
- **`sources.yaml`** — discovery sources + search queries the loop scans.

## Advisor candidate summaries
Use `summarize_candidates.py` when the advisor needs a stable short list before
writing a 方案, especially when many candidates are in play or when comparing
versions, security signals, and conflict edges. The helper is offline and
read-only: it reads the registry, emits Markdown, and leaves the final judgment
to `SKILL.md`, the routed `scenarios/*.md` file, and
`references/decision-framework.md`.

Examples:

```bash
python3 pipeline/summarize_candidates.py --scenario 1
python3 pipeline/summarize_candidates.py --scenario brownfield-adopt
python3 pipeline/summarize_candidates.py --scenario brownfield-optimize
python3 pipeline/summarize_candidates.py --scenario quick-oneoff
```

## Advisor contract fixtures
`scenarios/fixtures/advisor-contract.yaml` is a lightweight forward-test suite
for the advisor contract. It does not call a real LLM or generate complete
方案 text; it records scenario-shaped user requests plus the expected route,
default layers, excluded heavy layers, required controls, and plan skeleton.

Run:

```bash
python3 pipeline/validate_advisor_contract.py
```

The checker guards the current hard rules: every fixture must route to its
scenario, quick one-offs must not default to `spec` / `skill` / `orchestration`,
any active `spec` layer must require drift control, active tools are capped at
one per layer by default, the expected skeleton covers the plan template, and
`summarize_candidates.py` renders non-empty output for each covered scenario.

## Running the self-update loop today (manual / agent-driven)
1. Point a capable agent (with web access) at `research-playbook.md`.
2. It researches candidates from `sources.yaml` and writes/updates `registry/tools/*.yaml`.
3. Gate: `python3 pipeline/validate.py` **must pass** →
   `python3 pipeline/render_readme.py` → `python3 pipeline/render_readme.py --check`.
4. Draft release notes before bumping: `python3 pipeline/diff_snapshot.py` compares
   the latest release snapshot to the current registry projection. Use
   `--from/--to` only when comparing explicit snapshot files.
5. Update `CHANGELOG.md` from the reviewed draft, bump `SKILL.md`
   `metadata.version`, then run `python3 pipeline/snapshot.py` to freeze the new
   release snapshot.
6. Open a **draft PR**.

This is the process used to build and freeze the v0.3.0 and v0.4.0 registries;
it is now codified so it can be repeated for future discovery refreshes and,
eventually, scheduled.

The v0.4.0 candidate expansion is done. Taskmaster, SuperClaude, CodeStable,
Comet, ECC, and OMC are profiled, no longer backlog items, and frozen in
`snapshots/v0.4.0.yaml`. The next maintenance step is either a future discovery
refresh or optional scheduled-runner wiring, not continued profiling of the
current candidate batch.

## CI
`.github/workflows/registry-validate.yml` runs `validate.py` and
`render_readme.py --check` on every push / PR, so both human and automated
changes are gated by schema/integrity checks and README index sync. (Requires
GitHub Actions enabled on the repo.)

## Scheduling full automation (opt-in, environment-dependent)
Unattended refresh needs a runner with **model API access + web** (e.g. a
scheduled Action that invokes an agent against `research-playbook.md`). That
substrate is environment-specific, so it is intentionally **not** committed as a
half-working workflow — wire it up when the runner + secrets exist. Until then the
loop runs manually as above. See `PLAN.md` open item #4.

## Guardrails (always)
- Human-reviewable **draft PR** only — never push to the default branch.
- **No hallucinated tools:** unverifiable identity ⇒ `status: unknown` + `TBD`, not a fabricated entry.
- **Registry is the source of truth:** README's Tooling Index is generated from
  `registry/tools/*.yaml`; never patch table versions directly.
- **Deprecate, don't delete:** gone tools get `status: removed` + `removed_at`; the file is kept.
- Large diffs (>5 tools, or any MAJOR schema change) ⇒ flag for extra human scrutiny.
- Secrets live in the runner, never the repo.
