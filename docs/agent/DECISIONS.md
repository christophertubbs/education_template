# DECISIONS

## 2026-09-08: Shared runtime and data-only products

Generic models, presentation, assessment execution, progress, administration,
and accessibility live in `education_runtime`. Products contain target
knowledge, provenance, and deterministic data migrations. `education_runner`
discovers products through `EDUCATION_PRODUCTS` without target-specific edits.

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
