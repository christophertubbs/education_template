# Authoring examples and syntax

The paired fixture at [lesson fragment](../../examples/handoff/lesson.md) and
[expected JSON](../../examples/handoff/lesson.expected.json) illustrates lossless
lowering of a short instructional example. It is not a complete lesson, accepted
packet, scientific curriculum or replacement for the required audits.

## Lesson record skeleton

```markdown
---
handoff_version: "1.0"
identifier: "lesson-stable-id"
section_identifier: "section-stable-id"
sequence: 1
title: "Explicit lesson title"
summary: "Author-written summary."
status: "draft"
concept_identifiers: ["concept-stable-id"]
source_identifiers: ["source-stable-id"]
terminology_identifiers: ["term-stable-id"]
introduced_terminology_identifiers: ["term-stable-id"]
---
## Block: block-stable-id | paragraph
### inline
Complete teaching prose goes here. Cite the factual premise beside its claim
using [Source label](citation:source-stable-id).
## References
Full consulted source citation, locator and stable source ID go here.
```

The skeleton contains placeholders and MUST fail authoring acceptance. Replace
them with complete material; do not ask serialization to expand them.

## Content requirements by semantic block

| Block | Author supplies |
| --- | --- |
| paragraph, definition, theorem, rule, principle | Complete inline prose; term/title where appropriate; adjacent citations |
| heading | Text and heading level; preserve location in lesson |
| equation | Exact LaTeX, accessible text, caption/number if used, variable IDs already defined in an earlier variable table |
| code | Exact fenced code, language, kind (exact source/simplified/pseudocode), applicable commit/file/line provenance and explanatory context |
| callout, warning, note | Supported semantic type, title and complete inline text |
| ordered_list, unordered_list | Separate ordered/unordered inline items |
| table, comparison_table | Caption, headers, complete separate cells and citations |
| variable_table | Caption and complete variable rows including terminology ID, literal identifier, symbol, accessible symbol, meaning, units, role and constraints |
| worked_example | Title, scenario, inputs/assumptions, separately reasoned steps, result with units, interpretation and code connection |
| diagnostic_example | Title, observed behavior, conditions, candidate causes, reasoning, likely cause, rejected alternatives and investigation |
| procedure | Title, preconditions, separate actionable steps and expected result |
| source_reference, quote | Exact source reference or permitted quotation, citation and supporting locator |

Fields that the pinned runtime cannot preserve require the explicit mapping or
extension decision described in serialization/schema.md. For example, preserve
known inputs and assumptions in authored scenario text if that is the reviewed
runtime field, rather than inventing unsupported nested structures.

## What sufficient teaching looks like

An author must explain how a conclusion follows. “Smaller timesteps improve
accuracy” alone is neither a derivation nor a diagnostic lesson. Teach the
relevant discretization, state assumptions, cite the applicable result, show a
bounded worked case, and distinguish accuracy from stability. Do not assert that
generic statement universally. A serializer cannot recover these missing steps.

A terminology example must use actual values and explain behavior; “a worked
value must satisfy its constraints” is an instruction to write an example, not
an example. “Defined by the governing equation” is not an adequate valid-range
explanation unless the equation and resulting constraint are taught explicitly.

## Question records

Put typed relationships and scoring values in front matter; put `prompt`,
`feedback_correct`, and `feedback_incorrect` in named Markdown fields. Options
have immutable identifiers, verbatim text and explicit boolean correctness.
Numeric items state response units, accepted_value and nonnegative tolerance.
Text items state accepted_answers and normalization explicitly. Supply option
explanations and review evidence even where they must also be retained as
instructor-side material. See the paired question fixture for exact field placement.
