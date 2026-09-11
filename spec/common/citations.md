# Citations

Normative retained requirements. Original section numbers are stable migration anchors, not a required reading order. The stage ownership and explicit amendments in the root SPEC.md and common/handoff.md govern the two-stage workflow.

# 15. Source Traceability and Evidence

Important technical claims must be traceable to evidence whenever practical.

Curriculum provenance should include:

* Target Repository revision;
* source files;
* relevant symbols;
* relevant line ranges where useful;
* repository documentation;
* standards and specifications;
* primary scientific literature;
* official framework or library documentation;
* other authoritative references.

The Target Repository at the recorded revision is authoritative for claims about actual implementation behavior.

External scientific or mathematical claims should be supported by appropriate authoritative sources.

The curriculum must distinguish:

* facts directly observed in source;
* claims supported by upstream documentation;
* claims supported by external references;
* reasonable interpretations;
* unresolved uncertainties.

Unverified generated assumptions must not be presented as unquestionable fact.

---

# 16. External Research

The Generator may and should use external research when repository material is insufficient to teach domain or prerequisite knowledge correctly.

Preferred source order is:

1. official project documentation;
2. standards and formal specifications;
3. primary scientific literature;
4. official framework and library documentation;
5. reputable academic or professional secondary sources;
6. other reputable secondary sources when necessary.

The Generator should prefer primary sources for governing equations, numerical methods, model validity, and scientific claims.

External research must retain enough provenance for later verification.

## 16.1 Source and Citation Requirements

All externally derived factual claims MUST be explicitly cited.

This includes, but is not limited to:

- equations, formulas, and mathematical notation;
- definitions of variables, symbols, objective functions, and metrics;
- numerical constants, thresholds, coefficients, parameter ranges, and defaults;
- descriptions of algorithms, models, physical processes, calibration methods, and optimization methods;
- statements about model behavior, limitations, assumptions, accuracy, or computational characteristics;
- historical claims or claims about how a method is commonly implemented;
- terminology or notation attributed to a particular field, publication, software package, or modeling framework.

### 16.1.1 Citation placement

Citations MUST appear adjacent to the claim they support. Do not rely solely on a bibliography or "Sources" section at the end of a document.

For example:

> The calibration objective can be represented as a mean-squared-error loss,
> \(J(\theta) = \frac{1}{N}\sum_{i=1}^{N}(y_i-\hat{y}_i(\theta))^2\) [Smith et al., 2024].

If the source defines the objective function but does NOT use the symbol `J`, do not imply that it does. Instead state explicitly that the notation is being introduced for the curriculum:

> Using `J` here as curriculum notation, define the mean-squared-error objective as ...

### 16.1.2 Source fidelity

Never invent, infer, or fabricate a citation.

A citation MUST correspond to a source that was actually consulted and that materially supports the associated claim.

If no authoritative source can be found for a factual claim:

1. omit the claim;
2. qualify it as an interpretation or illustrative example; or
3. explicitly state that no supporting source was identified.

Do not present uncited external knowledge as established fact.

### 16.1.3 Original synthesis

Reasoning, explanations, examples, analogies, exercises, and pedagogical simplifications created by the curriculum generator do not require citations merely because they are original synthesis.

However, any factual premises used by that synthesis MUST still be cited.

### 16.1.4 References

Every generated curriculum document containing cited material MUST include a `References` section containing enough information to identify and retrieve each cited source.

Where available, include:

- author or organization;
- title;
- publication or documentation name;
- publication year or version;
- DOI or stable URL;
- date accessed for mutable web documentation.

Prefer primary sources, official documentation, peer-reviewed literature, standards, and authoritative technical reports over secondary summaries.

---

# 36. Hallucination Resistance and Uncertainty

The Generator and generated curriculum must teach and enforce verification rather than treating generated prose as authority.

Learners should be taught to:

* inspect relevant source code;
* inspect repository history where useful;
* consult official documentation;
* consult authoritative external references;
* identify conflicts between curriculum statements and source behavior;
* distinguish implementation facts from interpretive explanations.

The Generator must not fabricate certainty where evidence is incomplete.

Important unresolved questions should be represented explicitly in generation state and, when appropriate, surfaced in generated material.

---
