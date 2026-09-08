# STATUS

Current objective: maintain structured, accessible technical lesson rendering
in the shared Education Runtime and independent Curriculum Products.

Requirements: `SPEC.md` sections 3-46, especially generation architecture,
completion state, product/runtime boundaries, assessment constraints, progress,
validation, and completion.

Implemented: shared runtime models/import/views/templates/admin/scoring/progress;
thin environment-configured runner; staged generator with v2 artifacts, source
integrity, durable phase state, regeneration impact, staging and promotion;
migrated CFE artifacts; updated packaging, documentation, agent policy, and
tests. Lesson schema 2.1 supports semantic inline content, MathJax equations,
source-aware code, callouts, definitions, variable/comparison tables, worked and
diagnostic examples, procedures, and glossary-linked terms. The CFE 1.1 lessons
were regenerated with these structures, including explicit and visually
prominent Schaake/Xinanjiang parameter contracts. The obsolete nested generated
host, LSTM app, and CFE app repositories
were removed and replaced by the independent `generated/cfe-curriculum`; the
obsolete ignored LSTM Target Repository checkout was also removed.

Expected uncommitted state: structured-rendering and regenerated-lesson changes
on `project-pivot`. Generated output remains ignored by the root and is clean at
independent commit `eeceb90af9ad46631a663881f196999be55b1460`.

Validation completed on 2026-09-08:

* Ruff formatting and lint checks passed for `src`, `tests`, `tools`, and
  `manage.py`.
* All 13 Django/unit tests passed; Django reported no system issues.
* `makemigrations --check --dry-run` reported no changes.
* Generation resolved and detached CFE at exact commit
  `f9182dfb3d81c407c66c5b782114173893c30cf2`; every pipeline phase completed
  with no unresolved items.
* The generated product installed in editable form and built wheel
  `cfe_curriculum-1.1.0-py3-none-any.whl`.
* Runtime and product migrations applied to a new SQLite database. The result
  contained 1 curriculum, 7 concepts, 7 lessons, 7 assessments, and 64
  questions.
* An upgrade test stopped at product migration 0001, installed a stale generated
  baseline, then verified migration 0002 replaced it with structured content.
* Curriculum list/detail, lesson, final assessment, glossary, source, and
  progress routes all returned HTTP 200 with the product enabled.
* Generated product tests passed, both Target Repository and product Git trees
  were clean, and only `generated/cfe-curriculum/.git` exists under generated
  output.

Next action: add browser-level WCAG 2.2 AA checks for MathJax output, responsive
tables, definition navigation, and pop-quiz navigation.
