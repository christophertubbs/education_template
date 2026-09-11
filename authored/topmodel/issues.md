---
handoff_version: "1.0"
status: "blocked"
---
# TOPMODEL authoring issues

## Record: topmodel-missing-revision

```yaml
severity: "blocking"
owner_stage: "authoring"
status: "resolved"
affected_records: ["topmodel.project.json", "MANIFEST.md"]
```

### evidence

On 2026-09-11, the repository configuration loader exited 1 with
`ValueError: Missing required project fields: ['revision']`:

```bash
PYTHONPATH=src .venv/bin/python -c 'from pathlib import Path; from education_generator.configuration import load_project_configuration; load_project_configuration(Path("topmodel.project.json"))'
```

The input SHA-256 is
`6e7a0cf35b8cb177b9e0191102ff3161d31600b5f949ad1f5253951e5ea81bcd`.
`spec/common/lifecycle.md` section 6.1 requires a configured revision and
configuration validation before generation. `spec/common/source_handling.md`
requires the requested revision and resolved commit to be recorded separately.
The configured `initial_branch` controls the generated repository branch; it
does not supply the source revision. No existing `repository/topmodel/` or
`authored/topmodel/` was present at startup.

### required_resolution

Resolved on 2026-09-11: user selected `master`; the updated configuration pins
`89e4dc529dfdf7f23b7365530973e9f238fb740d`. Remote branch resolution and the
cloned checkout both match that pin. Configuration validation passes.

### review

Model-assisted configuration review confirmed the missing field against the
actual loader and lifecycle contract. No source, science, lesson, assessment,
or authoring-acceptance review has passed. This file records a preflight failure,
not a complete authored packet.

## Record: topmodel-paper-readable-evidence

```yaml
severity: "blocking"
owner_stage: "authoring"
status: "open"
affected_records: ["MANIFEST.md", "completion.md", "research.md"]
```

### evidence

Configured required topic 23 requires paper-specific derivations, notation/sign
checks, nonlinear routing, measured-versus-estimated parameters, experiment
conditions, error measures, parameter response surfaces and paper/Fortran/current
code comparisons. The publisher PDF returned HTTP 403 through both browser
retrieval and direct curl. White Rose explicitly has no full-text download;
Lancaster points back to the DOI. A Scribd OCR copy was consulted, but contains
damaged mathematical text and does not provide readable response-surface plots
through the available text view. See `research.md` for exact retrieval evidence.

### required_resolution

Supply a readable full-text copy (local PDF path or accessible URL) of Beven
and Kirkby (1979), DOI `10.1080/02626667909491834`, printed pages 43–69.
Verify original equations 1–16 and figures, particularly the parameter response
surfaces, from page images. Complete the paper/code comparison and prerequisite
teaching before authoring acceptance. Do not infer exact equation glyphs or plot
values from damaged OCR, and do not silently replace the assigned paper with
a later TOPMODEL description.

### scope_of_blocker

This blocks completion of the required paper-specific review and hence the
authoring acceptance gate. It does not invalidate the static code findings.
The user has confirmed they have no copy. Subsequent legacy IAHS and NTUA
download checks returned HTTP 404. Do not repeat the request for a user copy.
Source analysis has been preserved for continued independent work; full lessons,
terminology, mastery, coverage, question banks and all twelve acceptance reviews
remain unfinished, not implicitly covered by this issue's resolution.
An initial evidence lesson and six-item pop-review bank are now written in_review;
their completion does not resolve the paper-specific obligation.

## Record: topmodel-schema-profile-mismatch

```yaml
severity: "release_blocking"
owner_stage: "serialization"
status: "open"
affected_records: ["MANIFEST.md"]
```

### evidence

`spec/serialization/schema.md` documents schema 2.2 versus the generator's 2.1
constant and limitations for conceptual terminology roles and not_applicable
coverage. This existing integration issue is distinct from the scientific
source blocker. It does not prevent writing substantive Markdown lessons.

### required_resolution

Before serialization release, reconcile the pinned profile as required by the
schema specification. Preserve truthful terminology roles and applicability;
do not relabel a concept or unknown field to force validator success.
