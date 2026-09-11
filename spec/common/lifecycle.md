# Lifecycle

Normative retained requirements. Original section numbers are stable migration anchors, not a required reading order. The stage ownership and explicit amendments in the root SPEC.md and common/handoff.md govern the two-stage workflow.

## 1. Purpose

This repository defines a system for producing deeply technical educational curricula from configured target Git repositories.

The system is intentionally split into two major concerns:

1. a reusable **Education Runtime** that provides the Django application, user interface, persistence, assessment behavior, progress tracking, administration, and curriculum rendering; and
2. independently versioned **Curriculum Products** that contain the knowledge, lessons, assessments, provenance, and database population logic for a specific Target Repository.

The Generator must not recreate a complete Django application for every Target Repository when equivalent behavior can be provided by the shared Education Runtime.

The primary generated artifact is therefore a Curriculum Product, not a bespoke educational website.

A Curriculum Product must teach its Target Repository deeply enough that a successful Learner can independently inspect, explain, build, diagnose, modify, evaluate, and contribute to the Target Repository. For scientific, mathematical, engineering, or modeling software, the Learner must also understand the governing domain concepts deeply enough to evaluate when the implementation is appropriate, when its assumptions are violated, how those violations affect results, and what forms of bias or failure should be expected.

The system must prioritize durable knowledge extraction and validated curriculum design over repeated generation of application boilerplate.

---

# 3. Design Principles

## 3.1 Shared behavior belongs in the Education Runtime

Functionality that does not materially vary between Target Repositories should be implemented once in the Education Runtime.

Examples include:

* Django models representing generic curriculum concepts;
* lesson rendering;
* glossary presentation;
* assessment execution;
* question randomization;
* scoring;
* progress tracking;
* client-side progress persistence;
* administrative editing;
* shared navigation;
* accessibility behavior;
* common templates and static assets;
* curriculum import and validation;
* source-reference presentation.

Curriculum Products must not duplicate these facilities without a documented requirement.

## 3.2 Generated products should primarily contain knowledge, not application infrastructure

The Generator should produce structured curriculum content, source mappings, assessments, metadata, and deterministic database population logic.

Where Django data migrations are a suitable representation, a Curriculum Product may consist primarily of migrations and packaged supporting data that populate Education Runtime models.

The Generator must not repeatedly generate equivalent views, models, templates, URLs, or JavaScript merely because a new Target Repository is being taught.

## 3.3 Expensive reasoning should create reusable leverage

High-capability model compute should be concentrated on work that genuinely requires substantial reasoning, such as:

* repository understanding;
* scientific and mathematical analysis;
* prerequisite discovery;
* architectural reconstruction;
* identifying assumptions and validity regimes;
* identifying model-form limitations and expected biases;
* designing mastery requirements;
* resolving contradictory evidence;
* reviewing and auditing curriculum completeness;
* discovering reusable analysis procedures.

Routine transformation, formatting, structured expansion, deterministic validation, and repetitive implementation should be delegated to ordinary code or lower-cost/local models where practical.

## 3.4 Completion must be defined structurally

The Generator must not consider a curriculum complete merely because it has produced a plausible quantity of prose.

Completion must be determined from explicit mastery requirements, prerequisite closure, concept coverage, source traceability, assessment coverage, and machine-readable completion criteria.

---

# 6. Generator Input

## 6.1 `project.json`

Generation is controlled by `project.json`.

The file must identify at least:

* Target Repository name;
* Target Repository Git URL;
* configured revision;
* Curriculum Product package or identifier;
* human-readable display name.

A minimal conceptual structure is:

```json
{
    "name": "t-route",
    "repository_url": "https://github.com/NOAA-OWP/t-route.git",
    "revision": "main",
    "curriculum_product_name": "t_route_curriculum",
    "display_name": "t-route"
}
```

Optional configuration may include:

* description;
* excluded paths;
* explicitly required topics;
* source documentation URLs;
* authoritative external references;
* known build instructions;
* source repository submodule behavior;
* assumed learner prerequisites;
* desired curriculum emphasis;
* runtime compatibility requirements;
* standalone packaging behavior;
* generation model or execution policy.

The Generator must validate `project.json` before generation begins.

## 6.2 Entry knowledge

Assumed Learner knowledge must be explicit where it materially affects prerequisite generation.

The Generator must not silently assume undergraduate or graduate-level domain education merely because the Target Repository implements scientific software.

If no domain prerequisites are configured, the default assumption is a competent professional software developer with general programming knowledge but no specialized scientific or mathematical training beyond ordinary secondary-school mathematics.


## 6.3 Learner Language and Terminology Contract

Unless configured otherwise, the Learner is proficient in general-purpose
software development but has no specialized knowledge of the Target
Repository's scientific domain, mathematical notation, numerical methods, or
implementation language.

Ordinary explanatory prose should target approximately a United States grade
8–10 reading level. This requirement does not apply mechanically to source
code, equations, citations, or unavoidable proper names.

The curriculum must use progressive disclosure:

1. explain the idea in ordinary language;
2. provide a concrete example or analogy;
3. introduce the precise technical term;
4. define its variables, units, and constraints;
5. present the mathematics;
6. map the mathematics to source code;
7. translate relevant implementation logic into familiar C++ and Python
   concepts; and
8. explain assumptions, limitations, failure signatures, and common mistakes.

A glossary entry elsewhere does not satisfy the first-use requirement.

---

# 8. Generation Architecture

Generation must be treated as a multi-stage knowledge-production pipeline rather than a single prompt that asks a model to produce a course.

At minimum, the lifecycle must distinguish:

1. configuration validation;
2. repository acquisition;
3. exact revision resolution;
4. repository inventory and architecture analysis;
5. domain and algorithm identification;
6. knowledge-map construction;
7. prerequisite discovery and recursive expansion;
8. external research where necessary;
9. mastery-contract construction;
10. curriculum ordering and lesson planning;
11. lesson generation;
12. assessment generation;
13. model-criticism and adversarial-case generation where applicable;
14. source and evidence verification;
15. curriculum coverage auditing;
16. gap detection and additional generation;
17. final competency auditing;
18. Curriculum Product assembly;
19. migration or structured-data generation;
20. runtime compatibility validation;
21. metadata and provenance recording;
22. release promotion.

These stages may be implemented by one agent, multiple agents, deterministic tooling, local models, frontier models, or combinations thereof.

The implementation should choose the least expensive reliable mechanism for each stage.

Failed or incomplete generation must not be promoted as a completed Curriculum Product.

---

# 31. Regeneration and Incremental Updates

Each Curriculum Product must record the exact Target Repository revision used during its most recent successful generation.

When generation occurs against a newer revision, the Generator should compare the previously analyzed revision with the new revision and determine which concepts, source mappings, lessons, assessments, or assumptions may be affected.

Unchanged validated content should be preserved where practical.

Affected content must be re-audited rather than mechanically copied forward.

Stable concept and curriculum identifiers should be preserved where concepts remain semantically equivalent.

The Generator must distinguish changes caused by:

* Target Repository changes;
* Generator changes;
* Skill or methodology changes;
* Education Runtime schema changes;
* human curriculum modifications.

---

# 32. Generation Metadata

Each Curriculum Product must contain machine-readable generation metadata.

Metadata should include, where applicable:

* Generator name and version;
* generation timestamp;
* Target Repository name and URL;
* configured revision;
* resolved Target Repository commit;
* Curriculum Product name and version;
* curriculum schema version;
* compatible Education Runtime version or range;
* analysis methodology or Skill versions where useful;
* generation model information where reproducibility policy permits;
* prior source revision for incremental generations.

---

# 33. Reusable Skills and Agent Procedure Capture

The Generator may create or update reusable Skills when generation reveals a procedure that is likely to recur across Target Repositories.

Examples include procedures for:

* CMake analysis;
* Fortran module tracing;
* Python package analysis;
* BMI interface analysis;
* scientific model derivation review;
* source-provenance extraction;
* curriculum coverage auditing;
* assessment validation.

A reusable procedure should be captured as a Skill when doing so is expected to reduce repeated reasoning, improve consistency, or enable a lower-cost/local model to perform future work reliably.

Skills must be version controlled.

A Skill must not silently encode Target Repository-specific conclusions as universal rules.

Skills should contain, where applicable:

* a concise description usable for discovery without loading the full Skill;
* applicability conditions;
* required inputs;
* procedure;
* deterministic scripts or tools;
* expected outputs;
* validation rules;
* known limitations;
* failure conditions;
* escalation conditions.

When deterministic code can reliably replace repeated model reasoning, the Skill should prefer invoking that code.

Agents may propose or generate Skill changes as part of work, but a current task must not be declared successful merely by rewriting its own success criteria or weakening a Skill's validation requirements.

Changes that alter project policy belong in `SPEC.md` or `AGENTS.md`, not in a task-specific Skill.

---

# 34. Frontier, Local, and Deterministic Work Allocation

The architecture should allow generation tasks to be executed by different compute tiers.

Frontier-model work should focus on tasks whose failure would materially reduce correctness or educational depth and that require substantial synthesis or judgment.

Local or lower-cost models may be used for tasks such as:

* expanding content from already validated knowledge artifacts;
* applying established Skills;
* generating schema-conforming routine material;
* mechanical source mapping;
* repetitive assessment variants;
* formatting or migration generation;
* routine code changes.

Deterministic tooling should be preferred for tasks such as:

* repository inventories;
* symbol extraction where reliable parsers exist;
* schema validation;
* migration checks;
* link and provenance verification;
* coverage accounting;
* package installation tests;
* Django system checks.

Local or lower-capability execution must have explicit escalation criteria for cases that violate Skill assumptions, contain contradictory evidence, require unfamiliar scientific reasoning, or otherwise exceed established procedures.

The purpose of reusable Skills and intermediate artifacts is to reduce repeated frontier reasoning without lowering correctness standards.

---

# 35. Intermediate Artifacts

Significant analysis should produce persistent structured artifacts where they improve reproducibility or prevent repeated work.

Useful artifacts may include:

* repository inventories;
* architecture maps;
* concept graphs;
* prerequisite graphs;
* source maps;
* Mastery Contracts;
* coverage matrices;
* unresolved-question registers;
* scientific-model analyses;
* regeneration impact analyses.

Expensive, validated, or human-reviewed analysis may be version controlled.

Cheap deterministic caches should normally be regenerated rather than committed.

Transient agent scratch state, raw logs, and disposable plans should not be treated as canonical project knowledge.

Reusable Python and shell tooling must be stored in an appropriate source or tooling directory and version controlled.

---

# 45. Non-Goals

The system is not intended to:

* generate a complete duplicate Django application for every Target Repository when a shared runtime is sufficient;
* replace the Target Repository's authoritative source code;
* replace official upstream documentation or scientific literature;
* require a user account;
* require centralized progress tracking;
* hide source evidence from Learners;
* silently overwrite human-authored curriculum changes;
* assume generated explanations are infallible;
* optimize for short curricula at the expense of expert understanding;
* treat superficial exposure to terminology as mastery;
* use frontier-model compute for routine work that reliable local or deterministic mechanisms can perform.

---
