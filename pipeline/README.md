# pipeline/ — registry validation & self-update

This directory is the **pipeline** side of code-agent-toolsmith: the tooling that
keeps the knowledge base (`registry/tools/*.yaml`) accurate. Unlike the advisor
(model-agnostic, offline), the pipeline may use a strong model + the web.

## Pieces
- **`validate.py`** — the validation gate: schema (`registry/schema.json`) + the
  cross-field rules JSON Schema can't express (`verified_at` discipline,
  `conflicts_with` symmetry, reference integrity).
  Run: `python3 pipeline/validate.py` (needs `pip install pyyaml jsonschema`).
- **`snapshot.py`** — regenerate `snapshots/v<skill_version>.yaml` from the registry.
  Run: `python3 pipeline/snapshot.py [--date YYYY-MM-DD]`.
- **`research-playbook.md`** — the orchestration prompt a strong model follows to
  discover → research → normalize → validate → snapshot → open a PR.
- **`sources.yaml`** — discovery sources + search queries the loop scans.

## Running the self-update loop today (manual / agent-driven)
1. Point a capable agent (with web access) at `research-playbook.md`.
2. It researches candidates from `sources.yaml` and writes/updates `registry/tools/*.yaml`.
3. Gate: `python3 pipeline/validate.py` **must pass** → `python3 pipeline/snapshot.py`.
4. Update `CHANGELOG.md`/`README.md`, bump `SKILL.md` `metadata.version`, open a **draft PR**.

This is exactly the process used to build the v0.3.0 registry — now codified so it
can be repeated (and eventually scheduled).

## CI
`.github/workflows/registry-validate.yml` runs `validate.py` on every push / PR,
so both human and automated changes are gated by the schema + integrity checks.
(Requires GitHub Actions enabled on the repo.)

## Scheduling full automation (opt-in, environment-dependent)
Unattended refresh needs a runner with **model API access + web** (e.g. a
scheduled Action that invokes an agent against `research-playbook.md`). That
substrate is environment-specific, so it is intentionally **not** committed as a
half-working workflow — wire it up when the runner + secrets exist. Until then the
loop runs manually as above. See `PLAN.md` open item #6.

## Guardrails (always)
- Human-reviewable **draft PR** only — never push to the default branch.
- **No hallucinated tools:** unverifiable identity ⇒ `status: unknown` + `TBD`, not a fabricated entry.
- **Deprecate, don't delete:** gone tools get `status: removed` + `removed_at`; the file is kept.
- Large diffs (>5 tools, or any MAJOR schema change) ⇒ flag for extra human scrutiny.
- Secrets live in the runner, never the repo.
