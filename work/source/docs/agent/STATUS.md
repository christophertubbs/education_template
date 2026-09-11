# STATUS

Current objective: provide Sphinx documentation that lets a new maintainer map
everything under ``src/``, understand cross-package effects, and build the guide
reliably.

Requirements: `SPEC.md` sections 3-46, especially generation architecture,
completion state, product/runtime boundaries, assessment constraints, progress,
validation, and completion.

Implemented: shared runtime models/import/views/templates/admin/scoring/progress;
thin environment-configured runner; staged generator with v2 artifacts, source
integrity, durable phase state, regeneration impact, staging and promotion;
independent CFE and SAC-SMA Curriculum Products; structured semantic lessons;
accessible MathJax equations; source-aware code; callouts; definitions;
variable/comparison tables; worked and diagnostic examples; procedures; and
glossary-linked terms.

Curriculum Products now publish an `education_curriculum.products` package entry
point containing their Django application configuration. The standalone runner
discovers, validates, deduplicates, and deterministically orders all advertised
products before Django builds `INSTALLED_APPS`. `EDUCATION_PRODUCTS` is no longer
needed for migration or server startup; it remains an additive legacy-package
compatibility mechanism.

Schema 2.2 requires a stable machine-readable terminology contract for every
declared specialized item. Variable tables map to contracts, equations declare
variables and follow their definitions, lessons declare used and newly
introduced terms, and assessments map vocabulary to review lessons.
`terminology_closure` and `readability_review` are required coverage dimensions,
completion passes, and evidence-bearing audits. Supplemental glossary summaries
follow lesson content rather than front-loading jargon.

SAC-SMA content now includes reviewed PCTIM/ADIMP/ADIMC/PAREA distinctions,
their name decomposition, units and invariants, dry/intermediate/wet behavior,
an area-weighted numerical example, capacities, ET terms, recession parameters,
and principal runoff/baseflow components. CFE partitioning begins with a
plain-language, bounded soil-sponge analogy before technical names and equations.

Expected uncommitted root state on `project-pivot`: the user-modified
`project.json`, user-provided `cfe.project.json` and `prompt.md`, reviewed
`curricula/sac-sma/`, imported LGAR-C draft archive and expanded draft directory,
reviewed `curricula/lgar-c/`, `lgar-c.project.json`, schema 2.2 artifacts and
validation changes, runtime lesson ordering and coverage-preserving assessment
selection, tests, the terminology maintenance tool, and these durable state
updates. Generated output and target checkouts remain outside root tracking.

Generation and validation completed on 2026-09-09:

* Ruff formatting and lint passed for `src`, `tests`, `tools`, and `manage.py`.
* All 17 Django/unit tests passed with `manage.py test`; Django system checks
  passed and `makemigrations --check --dry-run` reported no changes.
* Raw `unittest discover` was attempted and failed because it does not initialize
  Django settings. This was an invocation failure; the project test runner
  loaded and passed the same generator and runtime tests.
* CFE resolved and detached target commit
  `f9182dfb3d81c407c66c5b782114173893c30cf2`. All generation phases, artifact
  checks, terminology checks, and source-reference validation passed. The clean
  generated product is commit
  `c6431330dd5e6330f539f869373ec0606ee4b1a8`.
* SAC-SMA resolved and detached target commit
  `975902e3d44785f3b3503f29adfb5755120f5bf5`. All generation phases, artifact
  checks, terminology checks, and source-reference validation passed. The clean
  generated product is commit
  `25cf18748f3906334f984098b7ee100f7ea481b7`.
* Both products built `py3-none-any` wheels. Wheel installation with `--no-deps`
  and both generated-product provenance tests passed. The first isolated build
  failed because the restricted sandbox could not resolve `setuptools>=77`; an
  approved-network retry passed, as did final no-isolation builds.
* Product and runtime migrations applied to separate clean SQLite databases.
  CFE loaded 1 curriculum, 7 lessons, 7 assessments, and 64 questions. SAC-SMA
  loaded 1 curriculum, 8 lessons, 7 assessments, and 64 questions.
* Representative curriculum, terminology-focused lesson, BMI-driver lesson,
  glossary, source, final-assessment, and progress routes returned HTTP 200.
  Rendered CFE partitioning and SAC-SMA runoff lessons were contextually reviewed
  for ordinary-language first use, bounded examples, defined equation variables,
  units, and source-facing identifiers.
* The first rendered-text inspection attempted to import unavailable Beautiful
  Soup. A standard-library HTML-to-text fallback worked. An initial order
  assertion also looked for non-visible equation accessibility metadata; the
  corrected assertion used the rendered equation caption and passed.
* Both Target Repository and generated-product Git trees were clean after final
  promotion.

Automatic product discovery validation completed on 2026-09-09:

* Ruff formatting and lint passed. All 22 Django/unit tests passed. Django system
  checks and migration-drift checks passed.
* Both products were regenerated with entry-point metadata. The clean CFE
  product is `6ea878e9bde20f3fc0257edb1a501593cc38a27b`; the clean SAC-SMA product is
  `43143a0bb892ba1f14c63fb632f51d61d7961dc1`.
* Both wheels built and installed together into an isolated target directory.
  Each generated package's two provenance/entry-point tests passed.
* With `EDUCATION_PRODUCTS` explicitly unset, a new SQLite database discovered
  both products, applied both migration sets, and loaded `cfe-curriculum` and
  `sac-sma-curriculum`. Both curriculum detail routes returned HTTP 200.
* A real development server started with `EDUCATION_PRODUCTS` unset. A localhost
  request to its curriculum list rendered both CFE and SAC-SMA. The first server
  start inside the restricted sandbox could not bind a socket; the approved
  local-server retry passed.

Local project discovery update completed on 2026-09-09:

* The repository runner now cross-references each directory under `curricula/`
  with `target_repository_name` in generated-product provenance. Matching does
  not inspect or require `curriculum` in the generated repository, package, or
  curriculum name. Matched products use their declared `pyproject.toml` entry
  point and local `src/` directory; installed entry points and the legacy
  explicit setting remain additive.
* Discovery ignores generated directories without a reviewed curriculum match,
  rejects duplicate generated products for one project, and validates matched
  provenance and entry-point metadata before modifying the import path.
* `ruff format --check src tests tools manage.py` and `ruff check src tests tools
  manage.py` passed. All 24 Django/unit tests passed. `manage.py check` and
  `manage.py makemigrations --check --dry-run` passed with no changes.
* A clean temporary SQLite migration, with no product installation or explicit
  product setting, discovered and applied both CFE and SAC-SMA product
  migrations. The resulting curriculum identifiers were `cfe-curriculum` and
  `sac-sma-curriculum`.
* The root wheel built successfully with `python -m build --wheel
  --no-isolation`. Setuptools warned that ignored `__pycache__` directories
  beneath generator templates looked importable and included their bytecode;
  this pre-existing package-data hygiene issue did not fail the build.
* The first full test run exposed that repository-local product migrations
  invalidate a runtime test's one-total-curriculum assumption and that manifest
  static storage lacked a collected test manifest. Runtime tests were scoped to
  the CFE fixture and given ordinary static storage; the full rerun passed.

Installation refresh update completed on 2026-09-09:

* Added executable `install.sh`. It uses `set -euo pipefail`, resolves the
  repository root, supports a `PYTHON_BIN` override, and sequentially runs
  `migrate --noinput`, `load_curricula`, and `collectstatic --noinput`.
* Added the `load_curricula` management command and a typed product-loading
  service. The service deterministically scans installed Django applications
  for packaged `data/curriculum.json` resources and imports every current
  payload through the existing atomic, conflict-preserving baseline importer.
  Curriculum JSON changes therefore apply even when no migration is pending.
* A regression test changes a packaged lesson title after migrations and
  verifies that the explicit loader brings the new JSON value into the runtime
  database. A shell-workflow regression test verifies the migration, refresh,
  and static-collection command order.
* An end-to-end `install.sh` run against a fresh temporary SQLite database
  applied all runtime, CFE, and SAC-SMA migrations; explicitly loaded both
  curriculum payloads; and collected static assets. The database contained
  `cfe-curriculum` and `sac-sma-curriculum`, both at product version 1.1.0.
* `bash -n install.sh`, Ruff formatting and lint, all 26 Django/unit tests,
  Django system checks, migration-drift checks, and `git diff --check` passed.
  The root wheel also built successfully; setuptools repeated the previously
  recorded ignored-template-`__pycache__` package-data warnings.

LGAR-C continuation and finalization completed on 2026-09-10:

* Continued the user-provided ChatGPT Work review candidate without modifying
  its original ZIP or expanded draft. Canonical reviewed artifacts now live at
  `curricula/lgar-c/`, with the pinned configuration in
  `lgar-c.project.json`. The generated product remains outside root tracking at
  `generated/lgar-c-curriculum/`.
* LGAR-C 1.1.0 pins target commit
  `9166bcfa1d8c37af26a4f6329872400f07a33ff6`. It contains six sections, 18
  lessons, 156 independently scored questions, 160 terminology contracts, 21
  source-reference records, and 12 cumulative multi-contract final cases.
* The continuation reviewed the complete 2023 LGAR paper and Wang et al.
  frozen-soil paper. It added the published validity boundary, all four
  iterative front-correction branches, the exact freeze/thaw multiplier and
  bounded source-observed risks, every pinned configuration key, literal versus
  instructional identifier distinctions, and cumulative diagnosis.
* The runtime now preserves configured major-concept quotas and coverage of
  every major Mastery Contract. Midterm and final attempts additionally retain
  all represented sections and terminal outcomes. Pop quizzes retain randomized
  prior-lesson filtering. Tests cover each non-pop kind, repeated-attempt
  variation, configured quotas, and prior-lesson restriction.
* Canonical and packaged LGAR-C payloads match exactly. Schema 2.2 and pinned
  source-reference validation reported zero errors. All 332 lesson blocks
  rendered through the runtime template. Ten final attempts preserved the
  three-question-per-major-concept quota, major contracts, sections, and
  outcomes while varying the selected set.
* The product built a `py3-none-any` wheel, installed without dependencies into
  an isolated target, advertised the expected entry point, and passed all six
  portable tests from both source and the installed wheel. The final checked
  download is `generated/lgar-c-curriculum-1.1.0.zip` with SHA-256
  `598eefa2940a79617ed42138f9abfe9a96fedf98b454ef8039b93fb58ec0f517`.
* A clean `install.sh` run with no explicit product setting discovered CFE,
  LGAR-C, and SAC-SMA; applied every migration; refreshed all three payloads;
  and collected static assets. LGAR-C loaded one curriculum, six sections, 18
  lessons, and 156 questions. Repeat loading preserved counts, and changed
  incoming baseline validation preserved a human edit while recording a
  conflict.
* Ruff formatting and lint passed. All 31 Django/unit tests passed with all
  three local products discovered. Django system checks, migration-drift
  checks, and `git diff --check` passed. Representative LGAR-C curriculum,
  BMI-lesson, glossary, source, final-assessment, and progress routes returned
  HTTP 200.
* Initial validation invocations exposed three non-product issues: the
  restricted Ruff cache was read-only; a route check omitted `testserver` from
  allowed hosts; and its first corrected-host retry used an extra `/curricula/`
  prefix. Temporary Ruff caching and the actual root-mounted routes passed.
* Actual LGAR simulations and coupled model runs were not executed. Analytical
  examples remain explicitly instructional, and source-observed defect impacts
  remain unmeasured. No upstream repository was pushed, no release was
  published, and automated product commits remain disabled by the supplied
  configuration.

Source onboarding documentation completed on 2026-09-10:

* Added a Sphinx guide under ``docs/sphinx`` covering architecture and data
  flows, generator phases, runtime models/import/assessment behavior, runner
  discovery and settings, templates/static assets, generated-product templates,
  operations, specification traceability, every maintained source category, and
  autodoc API references including policy-bearing private helpers.
* Added ``docs/BUILDING_DOCUMENTATION.md``, an executable ``build-docs.sh``, and
  a ``docs`` project extra containing Sphinx. The build uses warnings as errors
  and configures an in-memory minimal Django registry for autodoc, so it neither
  reads the project database nor activates generated products.
* Documented the current schema-label discrepancy: the artifact contract and
  current terminology rules describe schema 2.2, while generator constants and
  generated agent templates still emit/describe schema 2.1.
* ``PYTHON_BIN=.venv/bin/python ./build-docs.sh`` built all 11 source pages and
  API/viewcode indices successfully with Sphinx 8.2.3. A separate warning-strict
  linkcheck build also passed. ``bash -n build-docs.sh``, Ruff check/format for
  all Python source plus ``docs/sphinx/conf.py``, and ``git diff --check``
  passed. All 31 Django/unit tests, Django system checks, and the migration-drift
  check also passed.

Next action: add browser-level WCAG 2.2 AA checks for MathJax output, responsive
tables, definition navigation, and pop-quiz navigation.

