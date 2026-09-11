# JSON mapping examples

These are fixtures for field placement and content preservation, not complete
curricula or evidence of pedagogical sufficiency:

- [Markdown lesson fragment](../../examples/handoff/lesson.md)
- [Expected lesson record](../../examples/handoff/lesson.expected.json)
- [Markdown numeric question](../../examples/handoff/question.md)
- [Expected numeric question](../../examples/handoff/question.expected.json)

The fixture metadata deliberately says draft. It must not pass whole-packet
acceptance. The math example is original instructional arithmetic, with invented
values explicitly labeled; it makes no claim about a Target Repository.

The lesson's block anchors map to consecutive content indices. YAML front matter
`status` and `handoff_version` remain in packet provenance, not in the runtime
lesson. Paragraph Markdown becomes semantic inline objects; equation LaTeX and
accessible wording stay separate. The question's accepted_value and tolerance
remain at top level for the importer to collect into its internal scoring object.

The complete five-file wrapper layout is defined in schema.md. Do not infer
release completeness from these small examples, or fill missing relationships
with synthetic entities just to make a demonstration validate.
