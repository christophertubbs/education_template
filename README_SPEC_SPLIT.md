# Using the two-stage specifications

This directory is a reviewable overlay for the education_template `project-pivot`
branch at commit `6aea0519d9297049f371952915b011f7a51ba7f4`.

Copy `SPEC.md`, `spec/`, `examples/handoff/` and the included documentation into
the repository after reviewing the diff. The included AGENTS.md changes only
spec navigation/completion references. Agent status/tasks/decisions retain their
previous contents with a new task-specific update. If the repository has advanced,
merge those updates rather than overwriting newer work.

For curriculum authoring, start at `SPEC.md`, then `spec/authoring/SPEC.md`.
For conversion and assembly, start at `SPEC.md`, then
`spec/serialization/SPEC.md`. Both stages must read `spec/common/handoff.md`.

The author writes complete Markdown under `authored/<target>/`. The serializer
consumes its accepted manifest, emits the existing five JSON artifacts and uses
the current generator's packaging workflow in isolation. Read the integration
issues before treating the workflow as an automated command: this delivery changes
specifications, not the CLI, Markdown parsing or runtime implementation.

The requested common/authoring/serialization layout is retained. Additional files
make the handoff, review, lifecycle, product assembly and retained runtime contract
explicit. Original numbered requirements are preserved and mapped in
`docs/agent/REQUIREMENT_MAP.md`; obsolete monolithic navigation is replaced.

The archive also includes work records outside this overlay: source snapshots,
decision summaries, an intermediate draft checkpoint, validation output and
reproduction utilities. They are review evidence, not files to copy into the
application. Source snapshots include existing content examples for schema
inspection, not endorsements of their pedagogical quality.

No upstream repository was modified, no PR was opened, and no product was deployed.
