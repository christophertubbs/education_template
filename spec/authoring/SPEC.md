# Authoring activity

## Mission

Produce an accepted [Markdown Authoring Packet](../common/handoff.md) that teaches
the target deeply and is sufficiently explicit for faithful serialization by a
lower-cost model. Own all scientific and pedagogical decisions. GPT-6 is the
intended authoring executor; deterministic extraction and checks should conserve
its context and effort.

## Inputs and required reading

Read the root SPEC, handoff, common pedagogy, terminology, citations and source
handling; read lifecycle configuration and provenance requirements. Then use:

| Work | Read |
| --- | --- |
| Scope, prerequisites, knowledge and mastery | [Curriculum structure](curriculum_structure.md) |
| Full lessons, theory, failure analysis and semantic content | [Lesson content](lesson_content.md) |
| Question banks, scoring answers and feedback | [Assessments](assessments.md) |
| Difficulty and variation decisions | [Difficulty](difficulty.md) |
| Packet syntax and sufficient content examples | [Examples](examples.md) |
| Closure, remediation and acceptance | [Review](review.md) |

The serializer's field profile is a bounded capability reference when needed.
Do not load runtime views, CSS or migration internals to write lessons.

## Procedure and deliverables

1. Validate configuration; pin the target and generator/schema revisions. Save
   learner entry knowledge and scope decisions in the packet manifest.
2. Inventory the repository with bounded source inspection. Save architecture,
   code paths and evidence locators. Inspect representative data only when a
   specific teaching question requires its shape or values.
3. Build knowledge/prerequisite records and mastery contracts. Recursively close
   prerequisites against the learner baseline. Set importance and risk before
   planning assessments, so easy-to-write material does not dominate coverage.
4. Research missing foundations using consulted authoritative sources. Retain
   claim-level evidence and uncertainty; separate implementation from theory.
5. Order lessons; write the complete teaching text, equations, variable tables,
   examples, diagnostics, code explanations and references. Save each lesson as
   it becomes reviewable. Outlines and prose generation instructions are drafts.
6. Write the full assessment bank, explicit answers, scoring rules, feedback,
   review links, difficulty and outcome mappings. All variants require authoring
   review; a serializer is not an assessment author.
7. Perform the twelve logical review passes, remediate gaps, and record evidence
   by concept, field and lesson. Check the assembled learning sequence, not just
   independently plausible files.
8. Verify the packet grammar and references, hash accepted files, and mark
   authoring_ready only after all applicable teaching requirements are satisfied.

## Budget exhaustion and return from serialization

At every completed lesson, question batch or audit boundary, update completion,
issues and decisions. If work cannot finish, preserve a blocked/draft packet and
an exact next-action list. Never shorten remaining content or fill coverage flags
to fit a turn. An accepted packet should survive a model change without relying
on conversation memory.

Handle serializer issues narrowly. Repair only affected records and dependencies,
explain the decision with evidence, invalidate affected acceptance hashes and
repeat the relevant reviews. New substantive content always re-enters authoring.
