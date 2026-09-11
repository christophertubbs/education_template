# Review

Normative retained requirements. Original section numbers are stable migration anchors, not a required reading order. The stage ownership and explicit amendments in the root SPEC.md and common/handoff.md govern the two-stage workflow.

# 18. Multi-Pass Generation and Auditing

Curriculum generation must use iterative review rather than trusting the first generated pass.

The expected logical passes are:

1. **Knowledge pass**: determine what must be understood.
2. **Prerequisite pass**: recursively identify what must be taught first.
3. **Mastery pass**: define what competent understanding of each major concept means.
4. **Structure pass**: order concepts and construct curriculum sections.
5. **Content pass**: produce lessons, examples, and references.
6. **Assessment pass**: create questions and exercises mapped to Mastery Contracts.
7. **Adversarial pass**: identify cases, counterexamples, assumption violations, and likely failure signatures.
8. **Gap-review pass**: determine what a successful Learner could still misunderstand.
9. **Remediation pass**: generate missing or inadequate material.
10. **Competency-audit pass**: verify every terminal learning outcome has sufficient instructional and assessment support.
11. **Terminology-closure pass**: verify every specialized item is inventoried,
    taught before use, distinguished from related items, and closed across
    lessons and assessments.
12. **Readability-review pass**: review ordinary prose for grade 8–10 clarity,
    short sentences, jargon load, progressive disclosure, and retained
    scientific and mathematical depth.

These twelve passes do not require twelve separate model invocations if an implementation can achieve equivalent independence and verification more efficiently.

Where practical, final review should be performed with fresh context or an independent reviewing agent so that the author is not the sole judge of its own completeness.

---

# 19. Machine-Readable Completion State

The Generator must maintain machine-readable generation state sufficient to determine whether a Curriculum Product is actually complete.

For each major concept, state should record applicable fields such as:

* prerequisite status;
* mastery-contract status;
* theory coverage;
* mathematical coverage;
* assumptions coverage;
* implementation mapping;
* source verification;
* validity-regime coverage;
* failure-mode coverage;
* bias-analysis coverage;
* example coverage;
* diagnostic-exercise coverage;
* assessment coverage;
* unresolved uncertainty.

Generation must continue while required fields remain incomplete unless generation cannot proceed because evidence is unavailable or another explicit failure condition has been reached.

Inability to complete a required field must be surfaced as an unresolved issue. It must not be converted to "complete" merely to terminate generation.

---

## Authoring acceptance gate

Review all twelve passes with evidence, not a checklist copied into complete
state. Every required outcome and major contract needs sufficient teaching and
assessment links. Check prerequisite closure, full depth, model criticism,
terminology first use, source fidelity, valid examples and answer keys, bank
variation, accessibility and contextual readability. Record reviews against
content hashes and identify the review method honestly.

Resolve defects while progress is possible. If an applicable requirement cannot
be fulfilled, preserve the partial product with exact unresolved items. If a
dimension genuinely does not apply, record the scientific/pedagogical reason and
review it; unknown is not inapplicable. Do not claim JSON, migrations, package or
runtime tests ran during authoring. Those are serialization/release checks.
