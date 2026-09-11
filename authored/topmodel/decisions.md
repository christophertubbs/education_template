---
handoff_version: "1.0"
status: "in_review"
---
# Authoring decisions

## Record: decision-master-pin

```yaml
status: "accepted"
requested_revision: "master"
resolved_revision: "89e4dc529dfdf7f23b7365530973e9f238fb740d"
```

### decision

Retain the user's updated exact revision in `topmodel.project.json`. The user
requested master, and `git ls-remote` confirms that master resolves to this
commit. Record the branch request separately from the exact pin. The checkout
was newly cloned from master; it is clean and matches the pin. No source file
or existing checkout revision was changed.

## Record: decision-analysis-boundary

```yaml
status: "accepted"
```

### decision

Use static source reading, bounded samples, Git metadata and independent
arithmetic only. Running the science or build is not necessary to establish
the recorded source facts. Do not treat test source as a successful test run.
Record configuration-provided bug descriptions as hypotheses until verified
at the pin. The additional uninitialized `fx` finding was independently located
and compared with Fortran `FC`.

## Record: decision-paper-fidelity

```yaml
status: "accepted"
```

### decision

Do not certify the paper-specific requirement from abstracts or damaged OCR.
A readable source is necessary for its requested equation/figure review.
Preserve the completed source analysis rather than fabricating citations,
equation signs, plot readings, or a complete authoring status.

## Record: decision-entry-baseline

```yaml
status: "accepted"
```

### decision

Treat `topmodel.project.json` as the specific configuration selected by the
prompt. Its mention of `project.json` is generic, not an instruction to mix
another target's configuration into TOPMODEL. Teach calculus from algebra
and rates because it is requested but explicitly not assumed. The 26 topic
groups are scope obligations, not prewritten lessons or source citations.
