# Difficulty and assessment design

Difficulty describes reasoning demands, not obscure vocabulary, long prompts,
trick wording, time pressure or deliberately confusing distractors.

| Label | Required demand | Example task |
| --- | --- | --- |
| foundational | Explain or apply one taught idea in a familiar setting | Distinguish storage from a rate, with units already taught |
| intermediate | Combine taught ideas or trace a concrete implementation path | Diagnose a unit conversion error from values and a code excerpt |
| advanced | Integrate concepts, reject plausible alternatives, or analyze stressed assumptions | Distinguish forcing error from a structural limitation using supplied evidence |

These are handoff labels; the serializer preserves the authored `difficulty`
string. The inspected validator does not enforce a difficulty enum. Existing
products using other labels need an explicit author-approved mapping, not guessing.

For each major contract, record how it is taught and assessed, the item demands,
why distractors are plausible, and the misconception each distractor represents.
Foundational, high-risk and difficult concepts need multiple meaningful items.
Midterm/final items must integrate sections and include diagnosis, prediction,
comparison, source tracing, application and model criticism as applicable.

Specify the assessed scope and quotas for every attempt, not merely a large bank.
The bank must substantially exceed the selected count and contain meaningful
variants across required competencies. Document sufficiency through feasible
coverage-preserving selections and review; no arbitrary new fixed multiplier is
introduced here. A bank with one spare item may pass the current validator but
does not demonstrate substantial variation.

Do not create variants by changing only names or shuffling option order. Numeric
variants need independently checked answers, units and tolerances. Scenario
variants need reviewed premises and equivalent cognitive demand. The serializer
must return insufficient banks to authoring rather than generate filler.
