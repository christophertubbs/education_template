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

Lesson `content` is an ordered semantic block list. Supported runtime types are
`paragraph`, `heading`, `equation`, `code`, `callout`, `worked_example`,
`diagnostic_example`, `warning`, `note`, `definition`, `theorem`, `rule`,
`principle`, `ordered_list`, `unordered_list`, `table`, `comparison_table`,
`quote`, `procedure`, `source_reference`, and `variable_table`.

Text-bearing blocks use an `inline` list rather than presentation-oriented HTML.
Inline item types are `text`, `code`, `math`, `glossary`, `emphasis`, `strong`,
`file`, `command`, and `citation`. Math items contain `latex` and
`accessible_text`. Glossary items contain `glossary_identifier`, display `text`,
and a short `definition`; the referenced entry must exist. Each lesson's glossary
relationships drive its visible definition callout. Glossary entries may list
`aliases`; validation requires a lesson relationship whenever a term or alias is
mentioned so the definition is visibly available at least once in that lesson.

Equations contain `latex`, `accessible_text`, and optional `caption` and `number`.
Code blocks contain `code`, `language`, `kind`, and applicable source metadata.
Callouts contain a supported `semantic_type`, a `title`, and semantic inline
content. Tables contain a `caption`, `headers`, and rows whose cells are inline
lists. Variable tables contain definitions for symbol, accessible symbol,
source-code or configuration identifier, meaning, units, role, and constraints.
Worked and diagnostic examples keep scenarios, reasoning steps, results, and
investigation guidance structurally separate.

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
