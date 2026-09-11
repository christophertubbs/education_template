# Target artifact profile

## Baseline and authority

Inspected baseline: `project-pivot`, commit
`6aea0519d9297049f371952915b011f7a51ba7f4`.
The repository's `src/education_generator/CONTENT_SCHEMA.md` describes contract
2.2. `constants.py` still emits curriculum schema 2.1. Existing auxiliary files
may carry 2.0 labels. These labels are inconsistent; this specification does not
silently fix application code or certify compatibility from a version string.

Before release, record an explicit profile tying the artifact loader, validator,
runtime importer, templates, assessment implementation and metadata together.
Reconcile the version mismatch through reviewed integration work. A serializer
may emit a candidate for inspection but MUST report the mismatch as a release
blocker. Do not simply change `schema_version` to make it look consistent.

Bounded implementation references in the generator repository:

| Contract concern | File |
| --- | --- |
| Five input objects and merged product payload | `src/education_generator/artifacts.py` |
| Required fields, supported blocks, relationships and release flags | `src/education_generator/validation.py` |
| Configuration and defaults | `src/education_generator/configuration.py` |
| Database field mapping and grading data | `src/education_runtime/importing.py` |
| Visible block fields | `src/education_runtime/templates/education_runtime/content_block.html` |
| Visible inline fields | `src/education_runtime/templates/education_runtime/inline_content.html` |
| Actual answer evaluation | `src/education_runtime/static/education_runtime/assessment.js` |
| Question selection and quotas | `src/education_runtime/services.py` |
| Product assembly and metadata | `src/education_generator/scaffold.py`, `metadata.py`, `constants.py` |

The tables below specify the mapping used by this refactor. They are not a claim
that the existing Python validator is an exhaustive formal JSON Schema. Unknown
fields require an explicit preservation/destination decision.

## Five JSON objects

| File | Top-level content |
| --- | --- |
| `knowledge-map.json` | `schema_version`; `concepts` array; `relationships` array |
| `mastery-contracts.json` | `schema_version`; `mastery_contracts` array |
| `curriculum.json` | `schema_version`; `curriculum` object; arrays `sections`, `lessons`, `glossary`, `sources`, `assessments`, `questions`, `terminology` |
| `coverage.json` | `schema_version`; `concepts` array of concept coverage records |
| `completion.json` | `schema_version`; `status`; `passes`; `terminal_learning_outcomes`; `unresolved_required_items`; `audit_evidence` |

The generated package's `data/curriculum.json` is a merged payload, not a copy of
the input curriculum.json alone. It has `knowledge_map` containing the whole
knowledge-map object, `mastery_contracts` containing its inner array, the contents
of the curriculum object file, `coverage` containing coverage's concepts array,
`completion` containing the whole completion object, and generated `metadata`.
Use `CurriculumArtifacts.as_product_payload()` and existing scaffolding.

## Entity field mapping

All IDs and prose are strings; sequences/counts are integers; relationships are
arrays of strings except where a typed object is explicitly described. Fields
listed here must be supplied by authoring unless declared mechanical in handoff.

| Record | Fields |
| --- | --- |
| curriculum | identifier, title, description; authored pop_quiz_probability and pop_quiz_cooldown |
| concept | identifier, title, description, importance; category retained in artifact |
| relationship | source, target, type; prerequisite direction is dependent → prerequisite |
| mastery contract | identifier, concept_identifier, competencies (array of explicit strings) |
| section | identifier, title, summary, sequence |
| lesson | identifier, section_identifier, sequence, title, summary, content (ordered blocks), concept_identifiers, source_identifiers, terminology_identifiers, introduced_terminology_identifiers |
| glossary | identifier, term, definition, aliases where applicable, concept_identifiers, lesson_identifiers |
| source | identifier, evidence_kind, citation, certainty; applicable file_path, symbol, start_line/end_line integers, url |
| assessment | identifier, title, kind, selection_count, time_limit_seconds or explicit null; section_identifier for section quizzes; configuration object |
| question | identifier, type, difficulty, prompt, concept_identifiers, mastery_contract_identifiers, assessment_identifiers, terminal_outcomes, feedback_correct, feedback_incorrect, review_lesson_identifier, terminology_identifiers; type-specific scoring below |
| coverage record | concept_identifier, dimensions object, lesson_identifiers, question_identifiers |
| terminology | Full record defined in common/handoff.md; behavior is an object; related_terms is an array of identifier/distinction objects; source_mappings is an array of code_identifier/source_identifier objects |

The current terminology role enum is input, parameter, state, flux, intermediate,
configuration, output. Missing roles for pure conceptual terms are an integration
limitation, not permission to assign a false scientific role. source_mappings must
be truthful; a source identifier cannot be manufactured to satisfy validation.

## Assessment data

Kinds: pop, section, midterm, final. Pop selects 3–8; section at least 10; midterm
at least 30; final at least 50. Eligible banks must exceed selection counts and
satisfy the stronger substantive variation/coverage requirements. A current
validator pass does not guarantee feasible randomized attempts.

| Type | Fields at question top level |
| --- | --- |
| single_choice | options array of identifier, text, correct; exactly one true |
| multiple_select | options array; explicit correct set with at least one true |
| true_false | exactly two unambiguous truth-value options; exactly one true |
| numeric | accepted_value finite number, tolerance finite nonnegative number |
| text | nonempty accepted_answers string array; explicit normalization policy |

Do **not** put `scoring` in the input question. The importer constructs its
internal scoring object from options, accepted_value, tolerance, accepted_answers
and normalization. The actual browser implementation currently trims, performs
locale-sensitive lowercasing and collapses whitespace unconditionally for text;
it does not apply configurable normalization options. Only compatible authored
policies can be released without a runtime fix. Case-sensitive grading is blocked.

## Lesson blocks and inline objects

Use the types listed in authoring/examples.md, matching validator constants.
Each block has `type`. Paragraph-like blocks use `inline`, an array of objects.
Each inline object has `type` and nonempty `text`; math additionally has latex and
accessible_text; glossary additionally has glossary_identifier and definition.
Supported inline types: text, code, math, glossary, emphasis, strong, file,
command, citation. The current renderer displays citation text in a cite element;
it does not use a source ID to create a hyperlink. Retain source links in the
lesson's source relationships and claim map, and include adjacent readable
citations. Do not claim clickable inline citations without implementing them.

| Block | Visible/validated field shape |
| --- | --- |
| heading | text; current renderer fixes h2 rather than accepting arbitrary level |
| paragraph | inline |
| definition | term, inline |
| theorem/rule/principle | title, inline |
| equation | latex, accessible_text, variable_identifiers; optional identifier, caption, number |
| code | code, language, kind; source_file, line_range, source_revision, caption when applicable |
| callout/warning/note | title, semantic_type, inline |
| ordered_list/unordered_list | items: array of inline arrays |
| table/comparison_table | caption, headers: strings, rows: array of rows, each row an array of inline-array cells |
| variable_table | caption, rows: objects with symbol, accessible_symbol, identifier, meaning, units, role, constraints, terminology_identifier |
| worked_example | title, scenario, known_values: name/value records when used, steps: inline arrays, result, interpretation |
| diagnostic_example | title, observed_behavior, conditions, candidate_causes, reasoning, recommended_action (strings) |
| procedure | title, steps: inline arrays |
| quote | text, citation |
| source_reference | file_path, symbol when applicable, line_range when applicable |

Callout semantic types are note, important, warning, implementation-detail,
scientific-assumption, common-mistake, performance-concern, debugging-tip,
source-discrepancy, model-limitation.

Write diagnostics' likely cause and rejected alternatives explicitly inside the
authored reasoning field when using this profile. Put procedure preconditions and
results in separately authored supported blocks; do not add invisible fields.
Figures/diagrams are required by the broader spec where useful but absent from
the current supported block set. Essential diagrams or nested math needing richer
fields require reviewed lowering or a runtime extension. No silent flattening.

## Coverage and completion

Required dimensions: foundational_explanation, prerequisite_closure, theory,
mathematics, assumptions, implementation_mapping, source_evidence,
operational_behavior, limitations, failure_modes, bias_reasoning,
worked_examples, diagnostic_exercises, assessment_coverage, terminology_closure,
readability_review. Preserve all sixteen and their evidence mappings.

Required pass keys: knowledge, prerequisite, mastery, structure, content,
assessment, adversarial, gap_review, remediation, competency_audit,
terminology_closure, readability_review. For accepted authoring they map to
complete only with evidence. terminal_learning_outcomes maps each declared ID to
covered only after audited teaching and assessment support. Never omit an outcome
to make the final exam appear complete.

audit_evidence contains terminology_closure and readability_review objects with
status, method, reviewed_lesson_identifiers and unresolved_items. The current
readability record requires manual_contextual_review true. This means an actual
contextual review rather than a readability score alone; record whether the
reviewer was human or model in retained provenance, without inventing human review.

The current validator accepts only true for every coverage dimension. A reviewed
not_applicable cannot be lowered faithfully under that restriction. Report and
resolve the incompatibility; do not change not_applicable to true or weaken the
scientific scope merely to satisfy the schema.
