# Integration issues and adoption work

This is the remaining application work identified while splitting specifications.
It is separate from completion of the documentation refactor. Baseline commit:
6aea0519d9297049f371952915b011f7a51ba7f4.

| ID | Observed gap | Required disposition |
| --- | --- | --- |
| SPLIT-01 | No Markdown handoff reader exists in the inspected generator pipeline | Implement a data-only parser/adapter and the manifest/fidelity gates, or follow the spec manually with explicit validated conversion artifacts |
| SPLIT-02 | CONTENT_SCHEMA says 2.2; constants emit 2.1; auxiliary examples include 2.0 | Reconcile schema labels and document compatibility before release |
| SPLIT-03 | Coverage validator requires every dimension true | Add reviewed applicability semantics and evidence validation; never silently coerce not_applicable |
| SPLIT-04 | Terminology role/source mapping constraints do not fit every pure conceptual term | Define truthful supported representation or extend schema; do not manufacture code symbols |
| SPLIT-05 | General spec allows richer assessment/figure content than current renderer supports | Use author-approved supported forms or implement missing runtime semantics |
| SPLIT-06 | Browser text grading ignores stored normalization configuration | Restrict accepted policy to actual behavior or implement policy-driven grading with tests |
| SPLIT-07 | Pipeline checks structural/source validity and Python compilation before promotion | Add pre-promotion package, migration, rendering and grading gates; use isolated candidates meanwhile |
| SPLIT-08 | Replacement of an existing product deletes files before moving staged files | Provide recoverable/transactional promotion; existing function docstring overstates atomicity |
| SPLIT-09 | Agent document copying previously assumed a monolithic SPEC.md | Copy the linked spec tree or emit a self-contained product contract |
| SPLIT-10 | Current scaffold does not retain authored Markdown or field mappings | Package accepted packet and conversion provenance; verify distribution inclusion |
| SPLIT-11 | Validator checks are not exhaustive, e.g. exactly-one choice, reference types, numeric validity and pop upper bound | Add missing deterministic checks without treating a passing validator as pedagogical review |
| SPLIT-12 | Greedy randomized assessment selection can fail despite a feasible bank | Verify actual selection behavior and strengthen feasibility/selection handling; preserve authored coverage quotas |

Adopt documentation first; then implement the handoff adapter and fidelity checks
against the paired fixtures and real accepted packets. Resolve profile/version
and representability gaps before releasing a newly serialized product. Test the
adapter independently before touching accepted curricula or generated repositories.
