# Validation

Normative retained requirements. Original section numbers are stable migration anchors, not a required reading order. The stage ownership and explicit amendments in the root SPEC.md and common/handoff.md govern the two-stage workflow.

# 39. Validation

A Curriculum Product must not be considered successfully generated solely because files or migrations were produced.

Validation must include applicable checks for:

* Curriculum Product package installation;
* Python syntax;
* Django system checks;
* migration consistency;
* migration application into a clean database;
* Education Runtime compatibility;
* stable identifier integrity;
* source-reference integrity;
* coverage-matrix completeness;
* Mastery Contract coverage;
* prerequisite closure;
* required assessment presence;
* final competency coverage;
* unresolved required fields;
* automated tests;
* static analysis and formatting where configured.

For scientific or numerical curricula, validation must also ensure that major methods have adequate assumptions, validity, failure-mode, and bias-analysis coverage.

Validation failure must prevent incomplete output from being promoted as a successful release.

Validation must include a terminology-closure and readability audit.

The audit must verify that:

* every specialized term and identifier is present in a terminology inventory;
* every acronym is expanded on first use;
* every variable is defined before it appears in an equation or worked example;
* definitions do not rely on terms that are introduced later;
* related variables with similar names are explicitly contrasted;
* every parameter definition includes role, units, range, behavior, and source;
* every lesson has been reviewed against the configured reading-level target;
* unexplained terminology remains an unresolved required item.

Automated readability scores may support this audit but must not be its sole
evidence, because equations, identifiers, and scientific names can distort such
scores.

## 39.1 Citation Verification During Generation

Before finalizing each lesson, maintain an internal claim-source mapping for externally derived factual content.

For each factual claim, record:

- the claim or concept;
- the supporting source;
- the exact section, page, heading, equation, or other locator when available;
- whether the curriculum is quoting, paraphrasing, synthesizing, or introducing its own notation.

Before emitting the final lesson, verify that every externally derived factual claim has at least one supporting citation.

The final curriculum need not expose this internal ledger unless requested.

---

# 46. Completion Criteria

Generation is complete only when all applicable criteria below are satisfied.

* The configured Target Repository revision has been resolved to an exact commit.
* Repository analysis required for the curriculum has completed.
* A machine-readable knowledge map exists.
* Required prerequisite knowledge has been recursively identified and closed against configured entry knowledge.
* Major concepts have explicit Mastery Contracts.
* Curriculum content satisfies required concept-depth requirements.
* Scientific and numerical concepts include adequate governing theory, assumptions, validity regimes, limitations, failure modes, and bias reasoning where applicable.
* Major theoretical concepts are mapped to implementation evidence where possible.
* Curriculum coverage has been validated through the coverage matrix.
* Required assessments exist and map to Mastery Contracts.
* Adversarial, marginal, and inappropriate-use cases exist where applicable.
* A gap-review pass has completed.
* A final competency audit shows sufficient support for every terminal learning outcome.
* Required source provenance has been recorded.
* Required unresolved issues are explicitly represented rather than hidden.
* The Curriculum Product can be installed or loaded into a compatible Education Runtime.
* Curriculum migrations or equivalent deterministic data-loading mechanisms apply successfully to a clean database.
* Stable identifier and progress-compatibility requirements pass validation.
* Generated documentation is sufficient for independent use.
* Generation metadata has been recorded.
* Automated validation passes.
* Terminology closure and first-use auditing pass with no unresolved terms.
* A contextual readability and jargon review has completed; automated readability
  scores, if used, are supporting evidence rather than the sole criterion.

The Generator must continue generating, researching, reviewing, or remediating while required completion fields remain incomplete and further progress is possible.

A Curriculum Product is not complete merely because the generated material is coherent, useful, or long. It is complete when the defined competencies are actually taught, traceable, and assessed.

## Stage-two release gates and current gaps

Run gates in order and record exact commands, versions, results and limitations.
All required gates must pass before production promotion; a blocked candidate is
still a useful handoff artifact.

1. Packet acceptance: verify file hashes, reviewed statuses, required fields,
   evidence and unresolved issues. Rejected inputs remain unchanged.
2. Serialization fidelity: compare protected decoded fields, references, order,
   equations/code, option flags, units and tolerances against authoring; verify
   every entity/block/field has a declared runtime or provenance destination.
3. Structural validation: use load_artifacts and validate_artifacts on all five
   JSON files. Add contract checks absent from the baseline validator: every
   cross-reference kind, exactly-one-answer constraints, finite numeric values,
   pop upper limit, full question scope and declaration/evidence consistency.
4. Source validation: verify exact target commit, paths and line ranges with
   validate_source_references. Citation existence is not claim support; retained
   authoring review must establish that support. Ensure learner-visible citations
   remain adjacent and complete source information remains accessible.
5. Assessment behavior: verify actual browser grading for every used item type,
   normalization, empty input, tolerances and option identity under shuffling.
   Check that selected attempts can satisfy every required quota/outcome/section
   and have meaningful variation. The current greedy selector can fail on a
   particular ordering even when a feasible selection exists; exercise the actual
   selection path and report the limitation rather than equating bank size with
   feasibility. Do not weaken authored quotas to evade selection failure.
6. Product/runtime integration: verify Python syntax, wheel build and package
   installation, entry-point discovery, compatible runtime, Django system checks,
   migration drift, clean database migration, explicit curriculum refresh,
   repeated import and human-baseline conflict preservation as applicable.
7. Rendering/accessibility: render every used block/inline type and representative
   full lessons and assessments; inspect equations, code, tables, definitions,
   citations, feedback and keyboard/timing controls. Hidden but retained JSON
   fields do not count as learner-visible content.
8. Final review: evaluate retained §46, archive completeness, independent product
   use, documentation links, provenance, identifier/progress compatibility and
   all unresolved items. Mark release complete only now.

Use the repository's documented commands for applicable implementation tests:
`python manage.py test`, `python manage.py check`,
`python manage.py makemigrations --check --dry-run`, and a clean isolated
installation workflow. Package build needs its declared build dependencies;
report missing dependencies without claiming success. Documentation-only changes
do not require application tests; validate their links, retained requirements,
examples and archive instead.

Known baseline limitations requiring explicit handling include schema labels,
not-applicable coverage, pure-concept terminology roles/source mappings,
unsupported figures/nesting, fixed heading levels, plaintext citation links,
unconditional text normalization, weak structural checks, non-transactional
replacement of existing product files, and insufficient built-in pre-promotion
checks. These are implementation observations, not authoring exemptions.
