---
handoff_version: "1.0"
status: "draft"
identifier: "tm-curriculum"
title: "TOPMODEL: water, implementation and evidence"
pop_quiz_probability: 0.15
pop_quiz_cooldown: 3
---
# Curriculum design checkpoint

Teach a professional developer to understand TOPMODEL's science, trace its
historical and current implementation, and evaluate proposed changes with
appropriate evidence. The configured scope contains 26 topic groups, represented
by the draft knowledge map. The packet is not ready for publication: the
full learning sequence and all required assessments remain incomplete.

## Record: tm-foundations

```yaml
identifier: "tm-foundations"
title: "Evidence and quantitative foundations"
sequence: 1
```

### summary

Begin by distinguishing evidence from assertions. Build the units, functions,
rates and storage-accounting tools needed to read the model progressively.

### lesson_order

1. `tm-evidence-lesson` — `lessons/tm-evidence.md`.

This is the completed initial writing sequence only. Remaining foundation and
later domain lessons must be authored and ordered from `knowledge-map.md`.
It is not permission for a serializer to infer or write the missing sequence.

## Record: tm-verify-claims

```yaml
identifier: "tm-verify-claims"
status: "in_review"
```

### outcome

Verify a technical claim against an exact source revision or appropriate
observational evidence, state the scope supported by that evidence, and identify
the next discriminating check. This is an initial outcome, not the complete
set of terminal outcomes required by the specification.

## Navigation and review policy

The opening evidence review draws only after its review lesson is completed.
Its timing defaults to 300 seconds for three items; the runtime's timing-disable
and timing-extension accessibility controls must remain available. Randomize
eligible questions and answer order. Probability is 0.15 and cooldown is three
navigation events. Do not interrupt navigation before three taught review items
are available. This checkpoint's bank supports an initial pop review only;
it does not satisfy section, midterm or final examination requirements.
