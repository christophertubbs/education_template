# AGENTS.md

## Purpose and authority

This repository is designed for interchangeable CLI coding agents. Durable
state belongs in the repository, never only in a conversation.

When instructions conflict, follow this order: current user instructions,
`SPEC.md`, this file, `STYLE.md`, `docs/agent/DECISIONS.md`, tests, then code.

## Required startup and handoff

Before substantial work, read the task-relevant `SPEC.md` sections,
`docs/agent/STATUS.md`, `docs/agent/TASKS.md`, relevant decisions, `git status`,
the current diff, and recent relevant history. Inspect the configured Target
Repository only when required. Continue recorded work instead of reconstructing
settled context.

Before stopping, update `STATUS.md` and `TASKS.md` with current state, exact
validation, failures, blockers, and the next concrete action. Put long-lived
architecture choices in `DECISIONS.md`.

## Repository boundaries

The primary packages are:

* `education_generator`: staged analysis, validation, assembly, and promotion;
* `education_runtime`: generic Django models, views, administration,
  assessments, progress, templates, and static assets;
* `education_runner`: an optional thin Django host.

Reviewed generation artifacts live under `curricula/<target>/`. Promoted output
lives at `generated/<target>-curriculum` as an independent Git repository.
Target checkouts live at `repository/<target>` and are read-only evidence.

```text
Generator -> Curriculum Product -> Education Runtime <- Standalone Runner
```

The runtime must never import a particular product. A product must not duplicate
generic runtime behavior. The runner must not contain curriculum content.

## Generation workflow

Retain explicit phase boundaries and durable state. Validate configuration,
resolve the configured revision to an exact commit, and never execute arbitrary
Target Repository code merely to analyze it. Treat source paths, JSON, URLs,
and generated names as untrusted.

Required artifacts are documented in
`src/education_generator/CONTENT_SCHEMA.md`. Missing required fields remain
unresolved and fail promotion. Never turn an unknown into “complete” to make a
run terminate. Assemble in staging, verify, then promote. Refuse to update a
dirty generated repository. Do not overwrite human-modified runtime content;
record baseline conflicts explicitly.

## Target repositories and Git

Fetching and inspection under `repository/` are allowed. Do not modify source,
discard changes, rewrite history, or silently change the analyzed revision.
Do not cross Git boundaries. The root does not track generated products or
target checkouts. Use repository-local identity for automated product commits;
never change global Git configuration.

## Implementation and testing

Follow `STYLE.md`. Keep views thin and behavior in services. Add dependencies
only for clear technical reasons. Use structured logging and never log secrets.
Use stable IDs for every persisted curriculum entity.

Externally observable behavior needs tests. Before completion, run focused and
full Django tests, system checks, migration drift and clean migration checks,
package checks, and generator validation as applicable. Never delete, weaken,
or skip a failing test merely to report success.

## Completion

A task is complete only when relevant specification requirements pass,
documentation and agent state are current, repository boundaries remain valid,
and another agent can continue without conversation history. Curriculum
generation also requires every criterion in `SPEC.md` section 46.
