# Curriculum Artifact Contract 2.0

Each `curriculum_source_path` contains five JSON objects:

* `knowledge-map.json`: stable concepts and typed, acyclic relationships;
* `mastery-contracts.json`: competencies keyed to concepts;
* `curriculum.json`: curriculum, sections, lessons, glossary, evidence,
  assessments, and deterministically scored questions;
* `coverage.json`: required dimensions and lesson/question mappings per concept;
* `completion.json`: ten passes, terminal outcomes, unresolved items, and status.

All records use stable non-empty `identifier` values. A prerequisite relation's
`source` is the dependent concept and `target` is its prerequisite.

Lesson `content` is an ordered block list. Runtime types are `paragraph`,
`heading`, `equation`, `code`, and `callout`; equations include accessible text.

Assessment kinds are `pop`, `section`, `midterm`, and `final`. Questions list
eligible assessments, concepts, Mastery Contracts, outcomes, feedback, and a
review lesson. Types are `single_choice`, `multiple_select`, `true_false`,
`numeric`, and normalized `text`; all scoring criteria are explicit data.

Coverage dimensions are `foundational_explanation`, `prerequisite_closure`,
`theory`, `mathematics`, `assumptions`, `implementation_mapping`,
`source_evidence`, `operational_behavior`, `limitations`, `failure_modes`,
`bias_reasoning`, `worked_examples`, `diagnostic_exercises`, and
`assessment_coverage`. Applicable dimensions must be true before promotion.

Overall status, every generation/audit pass, and every terminal outcome must be
complete/covered with no unresolved required items. These declarations are
review records, not evidence substitutes; never set them optimistically.
