---
handoff_version: "1.0"
status: "draft"
identifier: "demo-lesson"
section_identifier: "demo-section"
sequence: 1
title: "An illustrative rate calculation"
summary: "Separate an amount from its rate using invented values."
concept_identifiers: ["demo-rate"]
source_identifiers: []
terminology_identifiers: ["demo-amount", "demo-duration", "demo-rate-term"]
introduced_terminology_identifiers: ["demo-amount", "demo-duration", "demo-rate-term"]
---

## Block: demo-introduction | paragraph
### inline
This is an invented arithmetic example. An amount and a rate answer **different questions**.

## Block: demo-variables | variable_table
```yaml
caption: "Symbols used in this example"
rows:
  - symbol: "A"
    accessible_symbol: "A"
    identifier: "amount"
    meaning: "The amount accumulated during the interval"
    units: "m"
    role: "input"
    constraints: "12 m in this invented example"
    terminology_identifier: "demo-amount"
  - symbol: "t"
    accessible_symbol: "t"
    identifier: "duration"
    meaning: "The duration of the interval"
    units: "s"
    role: "input"
    constraints: "4 s in this invented example; greater than zero"
    terminology_identifier: "demo-duration"
  - symbol: "r"
    accessible_symbol: "r"
    identifier: "rate"
    meaning: "The average amount per second during the interval"
    units: "m/s"
    role: "output"
    constraints: "3 m/s in this invented example"
    terminology_identifier: "demo-rate-term"
```

## Block: demo-equation | equation
```yaml
variable_identifiers: ["demo-amount", "demo-duration", "demo-rate-term"]
caption: "Average rate for the invented interval"
```
### latex
```latex
r = \frac{A}{t} = \frac{12\,\mathrm{m}}{4\,\mathrm{s}} = 3\,\mathrm{m/s}
```
### accessible_text
The average rate r equals amount A divided by duration t: twelve meters divided by four seconds is three meters per second.

## Block: demo-interpretation | paragraph
### inline
The calculation describes the average during this interval. It does not tell us whether the amount arrived steadily or in a short burst.

## References

Original illustrative arithmetic. No external or repository behavior is asserted.
