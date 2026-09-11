# Normalization and fidelity

## Representation-only transformations

Output UTF-8 JSON with two-space indentation and a terminal newline. Use a JSON
encoder with finite numbers only; reject NaN and infinities. Object key ordering
may be deterministic, but array ordering follows authored semantics. Preserve
code, LaTeX, text, signs, units, decimal values and option wording after decoding.
Do not normalize Unicode, punctuation or significant whitespace in source code,
identifiers, accepted answers or math without an explicit field-specific rule.

Strip only Markdown delimiters consumed by a known mapping. Convert inline code,
emphasis, math and citations into their supported semantic types. Preserve spaces
around adjacent inline elements. Reject raw HTML and executable markup; do not
silently sanitize away content whose meaning would change. Escape at JSON encoding
and let the runtime own safe HTML presentation.

Do not flatten tables, examples, diagnostics or equations into paragraphs. Do not
replace source excerpts with paraphrases. A unsupported figure, nested content
structure or citation location requires an explicit supported lowering that
preserves meaning and accessibility, or an integration issue.

## Numeric grading

The baseline numeric check uses an absolute tolerance. Preserve accepted_value
and tolerance from the author; require finite numeric values and tolerance >= 0.
Units belong in the prompt/teaching and must be unambiguous. Relative tolerance,
unit conversion or significant-figure rules need actual runtime support; do not
pretend absolute tolerance implements them. Test accepted boundary values and
rejected values just outside the boundary, including empty or nonnumeric input.

## Text grading

Copy accepted_answers and normalization options exactly. The pinned importer and
assessment implementation determine supported operations; inspect them before
lowering. Do not assume case folding equals lowercasing, or trim equals whitespace
collapse. Reject contradictory policies, such as case-insensitive grading of a
case-sensitive source identifier, for authoring review. Test accepted and rejected
responses after the actual runtime normalization path.

## Completion and reproducibility

Never normalize unknown, missing, blocked, false, not_applicable or unreviewed to
true/complete. Map completion flags only from accepted review evidence. Separate
authoring acceptance from executable release validation in the report.

A second serialization of identical inputs and profile must produce identical
content artifacts; exclude declared timestamps/build provenance from byte-level
reproducibility comparisons and document those exclusions. Keep input hashes,
tool/profile versions and all transformations so a subsequent serializer can
reproduce the same result without research.

## Inspected text-grading limitation

At the baseline commit, the browser always uses trim, toLocaleLowerCase and
whitespace collapse. It ignores configurable normalization data retained by the
importer. Record this exact behavior in the profile. Other authored policies
require integration changes; merely serializing a normalization field cannot
make the browser obey it.
