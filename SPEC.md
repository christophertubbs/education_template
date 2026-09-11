# Curriculum production specification

Contract version: **3.0 — two-stage workflow**. Markdown handoff version: **1.0**.
This is a specification change; it does not claim a Markdown importer already exists.

## Purpose and authority

Produce deeply technical, source-traceable Curriculum Products for the shared
Education Runtime. A successful learner must be able to inspect, explain, build,
diagnose, modify, evaluate, and contribute to the target software, including
criticism of scientific assumptions and outputs where applicable.

This root file routes work and defines ownership. Normative requirements live in
the linked specification tree. MUST, MUST NOT, and REQUIRED are mandatory;
SHOULD requires a documented reason for deviation. Examples illustrate contracts
and never override them. Repository code is evidence of current capabilities,
not permission to weaken a requirement that the code does not yet enforce.

## Two activities and their boundary

| Activity | Primary executor | Required result | Authority |
| --- | --- | --- | --- |
| Author curriculum | GPT-6/frontier model, supported by deterministic tools | Reviewed, detailed Markdown teaching content, complete question banks and answer keys, evidence, terminology, mastery and coverage records | [Authoring SPEC](spec/authoring/SPEC.md) |
| Serialize and assemble | GPT-5.6/lower-cost model, preferring deterministic tools | Five project JSON artifacts, independently installable product structure, fidelity and validation reports | [Serialization SPEC](spec/serialization/SPEC.md) |

Authoring settles what is taught and why. Serialization preserves that content
and its semantics while changing its representation. Missing explanations,
scientific judgments, answer keys, distractors, terminology, or citations return
to authoring. Serialization MUST NOT invent them or silently reduce depth.

`project.json` configures generation; it is not the curriculum payload. The five
reviewed artifacts live at `curricula/<target>/` by default. The installable
product lives at `generated/<target>-curriculum/` under the existing generator.
Authored Markdown lives at `authored/<target>/` and remains independently useful.

## Required reading routes

Start with this file, the selected stage SPEC, and
[the handoff contract](spec/common/handoff.md). Then load only relevant topic
files using the stage's checklist. Keep an inventory of applicable requirements
and their review evidence so limited context does not become lost obligations.

| Concern | Specification |
| --- | --- |
| Learner baseline, mastery and instructional tone | [Pedagogy](spec/common/pedagogy.md), [lifecycle §6](spec/common/lifecycle.md) |
| Shared vocabulary and terminology ownership | [Terminology](spec/common/terminology.md) |
| Claim-level citations and uncertainty | [Citations](spec/common/citations.md) |
| Revision pinning, bounded source inspection, security | [Source handling](spec/common/source_handling.md) |
| Configuration, architecture, provenance and regeneration | [Lifecycle](spec/common/lifecycle.md) |
| Authored packet and stage acceptance | [Handoff](spec/common/handoff.md) |
| Runtime, database, progress, accessibility and networking implementation | [Runtime SPEC](spec/runtime/SPEC.md) |
| Original section locations | [Requirement map](docs/agent/REQUIREMENT_MAP.md) |

The runtime reference preserves application requirements; it is not a third
curriculum-generation activity. Authors read its content/accessibility constraints
when relevant. Serializers read integration requirements when assembling and
verifying products. Neither stage recreates the Django application per target.

## Explicit amendments to retained requirements

These amendments resolve the old single-Generator wording; they are not optional.

1. In retained sections, Generator responsibilities are allocated by this file.
   Analysis, research, substantive content expansion, new assessment variants,
   and competency judgment belong to authoring. The lower-cost expansion and
   variant permissions formerly described in §34 do not apply to serialization.
2. The machine-readable knowledge map, coverage, mastery and completion state
   required before and during authoring may use the constrained Markdown records
   in the handoff contract. Their project JSON representations are stage-two outputs.
3. Structured content requirements in §40.1 apply semantically during authoring:
   tagged Markdown preserves equations, variables, code, examples and citations.
   Serialization materializes supported runtime block and inline records.
4. Authoring completion and release completion are separate. `authoring_ready`
   means the packet passed substantive review. It does not claim installation,
   migrations or runtime validation passed. Final release still requires §46.
5. The twelve named authoring review passes are all required. References to ten
   passes in previous prose or schema documentation are a counting defect.
6. Current runtime assessment types are limited to `single_choice`,
   `multiple_select`, `true_false`, `numeric`, and `text`. Other formats listed
   as possibilities in §4.8 require a separately reviewed runtime extension or an
   author-designed supported representation; the serializer cannot redesign them.
7. `not_applicable` requires an author rationale and review evidence. It is never
   equivalent to unknown or complete. If the target schema cannot represent it,
   serialization is blocked until the contract incompatibility is resolved.
8. Stage acceptance is based on recorded evidence, not merely flags, prose volume,
   a validator exit code, or a model's confidence. All stage-two transformations
   need a content-preservation account as well as existing executable checks.

## Stop, resume and change rules

Save completed records and update stage state at each lesson, assessment batch,
audit, and validation boundary. Record concise decisions, supporting evidence,
open issues, exact validation results, and the next action. Do not depend on chat
history or preserve private internal deliberation as an artifact.

On a target revision change, identify affected claims, lessons, questions and
terminology through the source map, re-author/review affected records, and retain
stable identifiers for semantically unchanged entities. On a schema-only change,
repeat serialization from the same accepted authoring packet and revalidate.

A blocked stage MUST leave its useful outputs and failure report available. It
MUST NOT mark a release complete, overwrite accepted content with guesses, or
rewrite success criteria to make validation pass.
