# STATUS

Current objective: maintain the completed pivot rewrite to a shared Education
Runtime and independent Curriculum Products.

Requirements: `SPEC.md` sections 3-46, especially generation architecture,
completion state, product/runtime boundaries, assessment constraints, progress,
validation, and completion.

Implemented: shared runtime models/import/views/templates/admin/scoring/progress;
thin environment-configured runner; staged generator with v2 artifacts, source
integrity, durable phase state, regeneration impact, staging and promotion;
migrated CFE artifacts; updated packaging, documentation, agent policy, and
tests. The obsolete nested generated host, LSTM app, and CFE app repositories
were removed and replaced by the independent `generated/cfe-curriculum`; the
obsolete ignored LSTM Target Repository checkout was also removed.

Expected uncommitted state: the complete pivot rewrite on `project-pivot`.
Generated output remains ignored by the root and is clean at commit
`2321213b06dda5a70240ba64f218bd634da417e5`.

Validation completed on 2026-09-08:

* Ruff formatting and lint checks passed for `src`, `tests`, `tools`, and
  `manage.py`.
* All 9 Django/unit tests passed; Django reported no system issues.
* `makemigrations --check --dry-run` reported no changes.
* Generation resolved and detached CFE at exact commit
  `f9182dfb3d81c407c66c5b782114173893c30cf2`; every pipeline phase completed
  with no unresolved items.
* The generated product installed in editable form and built wheel
  `cfe_curriculum-1.0.0-py3-none-any.whl`.
* Runtime and product migrations applied to a new SQLite database. The result
  contained 1 curriculum, 7 concepts, 7 lessons, 7 assessments, and 64
  questions.
* Curriculum list/detail, lesson, final assessment, glossary, source, and
  progress routes all returned HTTP 200 with the product enabled.
* Generated product tests passed, both Target Repository and product Git trees
  were clean, and only `generated/cfe-curriculum/.git` exists under generated
  output.

Next action: add automated browser-level accessibility and pop-quiz navigation
coverage, or implement strict semantic-version runtime compatibility checks.
