# DECISIONS

## 2026-09-08: Shared runtime and data-only products

Generic models, presentation, assessment execution, progress, administration,
and accessibility live in `education_runtime`. Products contain target
knowledge, provenance, and deterministic data migrations. `education_runner`
discovers installed products through package metadata without target-specific
edits.

## 2026-09-08: Fail-closed staged generation

Reviewed JSON artifacts connect expensive analysis to deterministic assembly.
The generator persists phase state under `.work`, verifies completion and source
references before assembly, compiles in staging, and promotes only passing
output to independent repositories under `generated/`.

## 2026-09-08: Baseline conflict preservation

Runtime records store a generated fingerprint and human-modification flag. An
incoming baseline that differs from a human-modified row creates an
`ImportConflict` and leaves the row unchanged.

## 2026-09-08: Versioned local learner state

IndexedDB records are keyed by stable curriculum identifiers and contain schema
and curriculum versions, completion, attempts, missed concepts, and preferences.
Portable JSON import rejects incompatible curriculum/schema identifiers.

## 2026-09-08: Semantic lessons and visible definitions

Curriculum Products store typed content blocks and typed inline spans, never
presentation-oriented lesson HTML. The runtime owns semantic rendering and
loads MathJax 4 for accessible LaTeX. Glossary-to-lesson relationships produce a
definition callout, while explicit glossary spans link the first pedagogically
useful occurrence. Validation rejects flattened technical lessons and any term
or configured alias mentioned without a visible lesson definition.

## 2026-09-08: Structured-content refresh migration

The schema 2.1/product 1.1 release includes product migration 0002 so databases
that already applied the original data migration receive regenerated baselines.
The importer continues to preserve human-modified rows and records conflicts.

## 2026-09-09: Explicit terminology closure

Curriculum schema 2.2 stores stable terminology contracts in each curriculum
payload. Lessons declare used and newly introduced terminology. Variable-table
rows and equation symbols map to those contracts, and questions declare the
terms they use. Validation fails when a contract is incomplete, an equation
precedes its variable definitions, assessment language is not taught in its
review lesson, either terminology/readability coverage dimension is incomplete,
or contextual audit evidence is absent. Glossary summaries render after the
lesson body so supplemental reference material does not introduce jargon before
the lesson's ordered teaching.

## 2026-09-09: Package-entry-point product discovery

Each Curriculum Product advertises its Django `AppConfig` through the
`education_curriculum.products` Python package entry-point group. The standalone
runner reads all entries before constructing `INSTALLED_APPS`, validates their
names and module ownership, rejects conflicting advertisements, and sorts them
for deterministic migration order. `EDUCATION_PRODUCTS` remains additive only
for compatibility with legacy products that lack entry-point metadata.

## 2026-09-09: Provenance-based local project discovery

The repository runner cross-references directory names under `curricula/` with
the `target_repository_name` recorded in each generated repository's provenance.
Only matched products are added to the local import path, and their package and
AppConfig names come from `pyproject.toml` entry-point metadata. Generated
repository names, package names, and curriculum identifiers are opaque and do
not need to contain `curriculum`. Installed entry-point discovery remains
additive for independently distributed products.

## 2026-09-09: Installation refreshes packaged curriculum data

Schema migrations are not used as the sole signal for curriculum content
updates. The runtime provides `load_curricula`, which imports every discovered
product's current packaged `data/curriculum.json` using the existing atomic,
conflict-preserving baseline importer. The root `install.sh` runs migrations,
that explicit refresh, and static-file collection in sequence and fails on the
first unsuccessful step.

## 2026-09-10: Coverage-preserving assessment selection

Non-pop assessment selection randomizes an oversized bank while enforcing each
configured major-concept quota and at least one item for every represented major
Mastery Contract. Midterm and final selection additionally retain every
represented curriculum section and terminal outcome. Pop-quiz selection remains
restricted to the eligible prior lessons supplied by learner progress. An
infeasible bank fails explicitly instead of silently dropping required coverage.

## 2026-09-10: Source-pinned LGAR-C stable product

LGAR-C product 1.1.0 is based on target commit
`9166bcfa1d8c37af26a4f6329872400f07a33ff6` and the complete reviewed 2023 LGAR
and Wang et al. frozen-soil papers. Literature comparisons retain their original
experimental boundaries. Suspected freeze/thaw implementation effects remain
source-observed and unmeasured because target code is read-only evidence and no
model runs were performed. The supplied configuration disables automated Git
commits, so no product history or external release is created automatically.

## 2026-09-10: Executable source-onboarding documentation

Source onboarding lives as Sphinx reStructuredText under ``docs/sphinx`` and
combines subsystem narratives, change-impact guidance, an exhaustive maintained
source inventory, and Python autodoc. Documentation imports use a minimal
in-memory Django configuration so builds cannot depend on or mutate a developer
database or activate local Curriculum Products. The root ``build-docs.sh`` is
the canonical warning-strict build interface, and ``docs/_build`` remains
disposable ignored output.
