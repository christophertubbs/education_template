Build the curriculum described by `topmodel.project.json` using the authoring pipeline in this repository.

Before authoring:

1. Read `SPEC.md`.
2. Read `spec/authoring/SPEC.md` and every document in its required reading route.
3. Follow `spec/common/handoff.md`.
4. Read any applicable `AGENTS.md` files.
5. Validate `topmodel.project.json` before generating curriculum.
6. Resolve every configured source repository and revision to an exact commit when possible. Record the resolved revision in the authored packet.
7. Inspect source repositories selectively and record the files, directories, tests, examples, documentation and build configuration that materially inform the curriculum. Avoid indiscriminate ingestion of generated files, fixtures or repetitive data.

This run is the authoring stage only.

Treat `topmodel.project.json` as configuration and source-selection input—not as curriculum content. Produce the complete, detailed intermediate Markdown curriculum under the configured `authored/<target>/` location.

The authored packet must contain all substantive educational content needed by the later serializer, including:

* audience assumptions and required starting knowledge;
* concepts, terminology and notation;
* prerequisite relationships and learning progression;
* measurable learning objectives;
* complete lesson explanations;
* equations explained without assuming calculus unless the configuration explicitly permits it;
* worked examples and code examples;
* connections between domain theory and the source implementation;
* misconceptions, failure modes and debugging guidance;
* diagnostics and prerequisite remediation;
* complete assessment banks;
* correct answers, scoring rules and actionable feedback;
* mastery and coverage records;
* claim-level citations and source evidence;
* review and acceptance evidence.

The serializer must never need to invent, expand, reinterpret or repair the curriculum. Do not leave placeholders, TODOs, skeletal lesson summaries or instructions telling a later model to write missing content.

Match the audience, scope, reading level, programming background, mathematical background and other constraints in `project.json`. When the requested subject depends on an unstated prerequisite, teach or remediate that prerequisite rather than silently assuming it.

Maintain durable progress records as you work. Save a checkpoint after each completed lesson, assessment-question batch and review pass. Record decisions, unresolved issues and validation results in the authored packet so another Codex session can resume without relying on conversation history.

Perform every review required by `spec/authoring/SPEC.md`. Validate:

* concept and objective coverage;
* prerequisite ordering;
* pedagogical completeness;
* technical accuracy;
* source fidelity;
* citation completeness;
* examples and exercises;
* assessment coverage and answer correctness;
* terminology consistency;
* audience and difficulty fit;
* cross-record consistency;
* handoff readiness.

Do not generate the final project JSON, normalize identifiers for publication, or assemble the runtime project structure during this run.

Continue until either:

1. the complete authored packet satisfies the authoring acceptance gate and is marked `authoring_ready`; or
2. progress is genuinely blocked.

If blocked, preserve all completed work and report the exact unmet requirement, affected files and evidence needed to continue. Do not mark incomplete work as ready.

At the end, report:

* authored target and output location;
* source revisions used;
* lessons and assessments completed;
* validation and review commands run, with results;
* remaining warnings or blockers;
* whether the packet is `authoring_ready`;
* the exact next command or prompt to use for serialization.
