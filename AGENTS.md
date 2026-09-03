# AGENTS.md

## 1. Purpose

This repository is intended to be developed by interchangeable CLI coding agents.

Assume that any development session may be performed by a different agent with no memory of previous conversations or sessions.

All information required to understand, continue, verify, and complete work must therefore be stored in the repository.

This file defines how agents must operate while working in this repository.

---

# 2. Source of Truth

When instructions conflict, use the following priority order:

1. Explicit instructions from the current user or session
2. `SPEC.md`
3. `AGENTS.md`
4. `STYLE.md`
5. `docs/agent/DECISIONS.md`
6. Existing automated tests
7. Existing implementation
8. Comments and secondary documentation

Existing code is evidence of current implementation, not necessarily evidence of intended behavior.

If implementation conflicts with `SPEC.md`, do not assume the implementation is correct.

Record significant conflicts or ambiguities before making architectural changes.

---

# 3. Required Startup Procedure

Before beginning substantial work:

1. Read `AGENTS.md`.
2. Read the relevant sections of `SPEC.md`.
3. Read `docs/agent/STATUS.md`.
4. Read `docs/agent/TASKS.md`.
5. Read only the relevant entries from `docs/agent/DECISIONS.md`.
6. Inspect repository state with:

   * `git status`;
   * `git diff`;
   * recent relevant Git history.
7. Inspect the Target Repository only when the current task depends upon it.
8. Identify the current objective and next unfinished task.
9. Continue from recorded state instead of re-analyzing the entire repository unless that state is missing, stale, contradictory, or insufficient.

Do not waste resources reconstructing information already recorded in repository state files.

Do not automatically change the resolved Target Repository revision merely because a new agent session has started.

---

# 4. Session Independence

Never rely on conversation history as the sole record of:

* architectural decisions;
* implementation status;
* assumptions;
* known failures;
* blockers;
* partially completed work;
* next actions;
* generated project state;
* Target Repository revision;
* regeneration state.

Repository state must be sufficient for another agent to resume work.

---

# 5. Specification

`SPEC.md` defines what the application must do.

Agents may:

* clarify implementation details;
* add references between requirements and tasks;
* identify missing or ambiguous requirements;
* propose specification changes.

Agents must not casually rewrite product intent or redefine requirements to make implementation easier.

When a requirement is ambiguous:

1. inspect related specification sections;
2. inspect relevant architectural decisions;
3. inspect existing tests and implementation;
4. prefer the smallest implementation consistent with documented intent;
5. record meaningful assumptions.

Requirement identifiers should be referenced where available.

Prefer identifiers such as:

* `GEN-001`;
* `CUR-004`;
* `ASM-002`;
* `UI-003`;

rather than informal references such as:

`the quiz persistence thing`.

---

# 6. Task Tracking

`docs/agent/TASKS.md` is the authoritative implementation task list.

Agents are expected to maintain it.

Agents must:

* derive implementation tasks from `SPEC.md`;
* reference applicable requirement identifiers;
* add newly discovered implementation tasks when necessary;
* split large tasks into smaller actionable tasks;
* record blockers and dependencies;
* mark work complete only after appropriate verification;
* preserve unfinished tasks;
* avoid changing priorities without a technical dependency or explicit user instruction.

Human edits to task ordering or priority take precedence over agent-generated planning.

Completed tasks should not contain detailed historical narratives. Git already provides implementation history.

---

# 7. Resumable Work

`docs/agent/STATUS.md` is the current working-memory checkpoint for the repository.

It should describe present state, not provide a chronological diary.

Keep it concise enough that a new agent can read it cheaply.

It should normally contain:

* current objective;
* current requirement identifiers;
* recently completed work;
* work currently in progress;
* relevant files;
* tests run;
* current failures;
* blockers;
* important assumptions;
* relevant decision references;
* next concrete actions;
* current Generator repository commit when useful;
* current Target Repository revision when relevant;
* expected uncommitted changes when applicable.

Update `STATUS.md` whenever:

* a requirement is completed;
* a significant milestone is reached;
* work moves to another subsystem;
* an architectural decision is made;
* an important blocker is discovered;
* a long or risky operation is about to begin;
* substantial work is about to stop.

The next agent should be able to resume useful work without reconstructing the previous session.

---

# 8. Durable Decisions

`docs/agent/DECISIONS.md` contains architectural and long-lived implementation decisions.

Use it for decisions such as:

* storage strategy;
* application boundaries;
* dependency choices;
* public API choices;
* template strategy;
* generated-project layout;
* regeneration behavior;
* human-edit preservation;
* client-side persistence;
* repository management behavior;
* curriculum provenance strategy.

Do not use `STATUS.md` for long-term architectural reasoning.

When a current task depends on a recorded decision, reference the relevant decision from `STATUS.md` or `TASKS.md`.

Do not reverse an existing documented decision casually.

If new information invalidates a decision:

1. document why the previous decision is no longer appropriate;
2. record the replacement decision;
3. update affected implementation;
4. update tests;
5. update relevant task and status state.

---

# 9. Programming Style

All generated or modified code must follow `STYLE.md`.

When existing code conflicts with `STYLE.md`:

1. preserve local conventions in unrelated code;
2. apply `STYLE.md` to new code and substantially modified code;
3. do not perform large formatting-only rewrites unless explicitly requested.

Prefer:

* clear code over clever code;
* explicit control flow;
* short, focused functions;
* strong typing where supported;
* descriptive names;
* automated verification;
* established libraries;
* framework conventions;
* abstractions only where they solve a real variation or testing problem.

Avoid speculative abstractions and unnecessary dependencies.

---

# 10. Development Workflow

Before implementation:

1. identify the requirement or task being addressed;
2. inspect relevant existing implementation;
3. inspect relevant tests;
4. identify affected interfaces and dependencies;
5. inspect relevant Target Repository material when required;
6. record important assumptions.

During implementation:

1. make incremental changes;
2. keep changes scoped to the current task;
3. run focused tests after meaningful changes;
4. preserve public APIs unless changing them is required;
5. avoid unrelated refactors;
6. update task and status state as milestones are reached.

Before considering a task complete:

1. verify relevant `SPEC.md` requirements;
2. verify applicable acceptance criteria;
3. run relevant automated tests;
4. run linting and formatting checks where configured;
5. update documentation when behavior changed;
6. update `TASKS.md`;
7. update `STATUS.md`.

---

# 11. Testing

New externally observable behavior should have automated tests where practical.

Bug fixes should include regression tests where practical.

Tests should primarily verify behavior rather than implementation details.

Do not:

* delete failing tests merely to make CI pass;
* weaken assertions without justification;
* disable validation to avoid fixing implementation;
* mark tests skipped solely because implementation is incomplete.

If tests cannot be made to pass, document:

* the exact failure;
* likely cause;
* affected requirement;
* next recommended action;

in `STATUS.md`.

---

# 12. System Architecture

The generated educational system consists of:

* one Generated Host Project; and
* one or more independently reusable Curriculum Apps.

The Generator is separate from both.

The intended relationship is:

```text
Generator
    |
    +-- produces --> Generated Host Project
                         |
                         +-- hosts --> Curriculum App
                         |
                         +-- hosts --> Curriculum App
```

The Generated Host Project may depend on Curriculum Apps.

Curriculum Apps must not depend on the Generated Host Project.

The Generator repository must not depend on generated repositories as source dependencies unless explicitly required.

---

# 13. Django Architecture

The Generated Host Project is responsible primarily for:

* Django settings;
* root URL configuration;
* ASGI configuration;
* WSGI configuration;
* shared database configuration;
* shared navigation;
* shared styles and static resources;
* deployment wiring;
* Django administration;
* Curriculum App integration.

Reusable domain and curriculum functionality belongs in Curriculum Apps.

Do not place Curriculum App functionality inside the Generated Host Project merely because it is convenient.

Keep all generated Django code under:

`./generated/education`

The expected standalone entry point is:

`./generated/education/manage.py`

---

# 14. Curriculum App Rules

Each Curriculum App must be installable independently as a Python package and usable by another Django project.

Curriculum Apps must not import from the Generated Host Project.

Reusable resources must be namespaced, including:

* URL names;
* templates;
* static files;
* settings;
* template tags where applicable.

App-local URLs should expose:

* `urlpatterns`;
* `app_name`.

The host project must control URL mounting through Django's `include()` mechanism.

Do not hard-code deployment URL prefixes.

Use Django URL reversing for internal navigation.

Models and migrations belong to the Curriculum App.

Do not depend directly on Django's concrete built-in `User` model.

Use Django-supported configurable user-model mechanisms where authentication integration is needed.

Curriculum App settings should be read through Django configuration and provide reasonable defaults where appropriate.

Do not import Generated Host Project settings directly.

---

# 15. Django Domain Logic

Keep HTTP views reasonably thin.

Prefer separating application and domain logic into reusable services or domain modules.

Where practical, structure request handling approximately as:

`request -> view -> service/domain logic -> model/storage`

This allows other Django projects to reuse behavior without depending on the original HTTP interface.

Use Django signals sparingly.

Prefer explicit behavior over hidden global side effects.

---

# 16. Packaging

Curriculum Apps must be independently installable through Python packaging configuration.

Package configuration must include runtime resources such as:

* templates;
* static files;
* migrations;
* packaged curriculum data;
* other required application resources.

Do not assume a source checkout will always be the runtime environment.

A Curriculum App must remain usable when installed as a normal dependency.

---

# 17. Target Repository

Use `project.json` to identify the Target Repository.

Store Target Repository checkouts under:

`./repository/<repository-name>`

Treat repositories under `./repository` as read-only source material.

Agents may perform non-destructive Git operations required to:

* clone repositories;
* fetch remote references;
* inspect history;
* inspect tags and branches;
* inspect differences;
* resolve configured revisions.

Agents must not:

* modify tracked source files;
* create commits;
* push changes;
* discard local modifications;
* alter upstream history;
* perform destructive resets;
* run destructive cleanup operations.

If local modifications prevent safe revision changes, record the condition rather than silently discarding them.

---

# 18. Target Repository Revision

Generation must be tied to an exact resolved Target Repository commit.

Do not treat a moving branch name such as `main` as sufficient provenance.

When generation begins:

1. load the configured revision from `project.json`;
2. fetch relevant remote state if necessary;
3. resolve the configured revision to an exact commit;
4. record that exact commit in generated metadata.

Do not silently change the resolved revision during an in-progress generation cycle.

A new revision should be treated as a regeneration or update operation.

---

# 19. Generator Helper Code

Store reusable Generator logic under:

`./src`

This includes code that:

* clones or inspects Target Repositories;
* analyzes source;
* generates curriculum;
* generates Django applications;
* renders templates;
* initializes repositories;
* validates generated output;
* performs repeatable transformations;
* supports future Target Repositories.

Significant generation behavior should be human reproducible through code stored in the repository.

Do not rely on undocumented manual steps for important generation behavior.

---

# 20. Generation Lifecycle

Generation should follow the lifecycle defined in `SPEC.md`.

Agents should preserve phase boundaries between:

* input validation;
* Target Repository acquisition;
* revision resolution;
* source analysis;
* prerequisite analysis;
* external research;
* curriculum planning;
* curriculum generation;
* assessment generation;
* Django generation;
* validation;
* Git initialization;
* metadata recording;
* promotion to final output.

Generation should occur in a temporary or staging workspace where practical.

Do not treat partial failed output as a completed Generated Project.

---

# 21. Generated Repository Types

The Generator produces two categories of generated Git repositories.

## 21.1 Generated Host Project Repository

Located at:

`./generated/education`

This repository contains:

* standalone Django configuration;
* shared host resources;
* integration of Curriculum Apps;
* host-level documentation;
* host-level agent state.

## 21.2 Curriculum App Repositories

Each Target Repository receives its own independent Curriculum App repository.

For example:

`./generated/education/t-route`

A Curriculum App repository is independent from the Generated Host Project repository even when checked out inside it.

---

# 22. Git Submodules

Curriculum Apps may be incorporated into the Generated Host Project as Git submodules when required by `SPEC.md`.

If submodules are used:

* `.gitmodules` must be valid;
* submodule paths must be stable;
* generated documentation must explain initialization;
* generated documentation must explain updates;
* the Generator must not confuse the submodule working tree with ordinary host-owned files.

Do not make generated Curriculum Apps submodules of the Generator repository.

---

# 23. Generated Git Repository Initialization

After successful generation and validation, a new generated repository should normally:

1. be initialized as a Git repository;
2. use `main` as the initial branch unless otherwise configured;
3. use repository-local Git identity if an automated commit requires one;
4. stage generated files;
5. create an initial generation commit;
6. record generation metadata;
7. remain ready for independent human or agent development.

Do not modify global Git configuration merely to support generated commits.

Prefer explicitly targeted Git commands such as:

`git -C <repository-path> ...`

over process-wide current-directory changes where practical.

---

# 24. Repository Boundaries

Do not accidentally cross repository boundaries.

When working in the Generator repository:

* do not commit generated project contents;
* do not treat generated repositories as Generator source dependencies;
* do not alter generated repository history unless the current task requires it.

When working in the Generated Host Project:

* do not absorb Curriculum App repository contents into host history when those apps are intended to remain independent;
* treat Curriculum App repositories according to their configured relationship, including submodule rules.

When working inside a Curriculum App repository:

* treat that repository's own specification and agent state as authoritative;
* do not modify the Generator repository unless explicitly instructed;
* do not depend on Generated Host Project internals.

---

# 25. Regeneration

Regeneration is an update operation, not an assumption that existing generated output may be deleted.

Before regenerating an existing Curriculum App:

1. identify the previously recorded Target Repository revision;
2. identify the new resolved Target Repository revision;
3. inspect generated metadata;
4. identify relevant source differences;
5. identify human-modified curriculum content;
6. identify stable curriculum identifiers that must be preserved.

Regeneration should update curriculum affected by Target Repository changes without rewriting unrelated material merely for consistency.

Agents must not silently overwrite human-authored curriculum changes.

If generated content conflicts with human-modified content:

* preserve the human modification unless `SPEC.md` explicitly requires another behavior;
* record the conflict;
* avoid silently choosing one side.

Stable curriculum identifiers should be preserved when concepts remain equivalent.

---

# 26. Curriculum Provenance

Technical claims about the Target Repository should retain sufficient provenance for verification.

Where practical, record:

* exact Target Repository commit;
* source file;
* relevant symbol;
* relevant line range;
* relevant repository documentation;
* authoritative external source.

Do not invent source references.

Do not represent generated assumptions as verified repository behavior.

When generated curriculum contradicts the Target Repository at the recorded revision, treat the source as authoritative and correct the curriculum.

---

# 27. External Research

Use authoritative external sources when the Target Repository alone is insufficient to teach necessary prerequisite or domain knowledge.

Prefer:

1. official project documentation;
2. standards and specifications;
3. primary scientific literature;
4. official library and framework documentation;
5. reputable secondary sources.

Retain provenance for externally derived technical claims where practical.

Do not fill important gaps with unsupported assumptions merely to complete generation.

---

# 28. Curriculum Coverage

The generated curriculum must cover significant Target Repository concepts.

Maintain traceability between important repository concepts and:

* lessons;
* prerequisite material;
* glossary entries;
* assessments.

Do not omit difficult components merely because they require substantial explanation.

Pay particular attention to:

* unfamiliar languages;
* scientific algorithms;
* mathematical logic;
* build infrastructure;
* data flow;
* external interfaces;
* performance-sensitive code;
* known defects;
* runtime lifecycle.

---

# 29. Curriculum Data

Curriculum Apps must remain self-contained.

Although deployed curriculum is stored in Django models and may be edited through Django admin, a fresh installation must be able to populate the database deterministically from content stored within the Curriculum App repository.

Do not make an existing deployed database the only surviving source of curriculum content.

The repository must contain either:

* canonical curriculum data; or
* another deterministic representation sufficient to rebuild database state.

---

# 30. Human-Modified Curriculum

Administrator-modified curriculum must not be silently overwritten.

The system must distinguish:

* generated baseline content;
* human-modified content.

Agents working on regeneration must preserve this distinction.

Do not assume that current database content can safely be regenerated from scratch.

---

# 31. Learner State

Learner progress must follow the persistence rules defined in `SPEC.md`.

Do not introduce user accounts or server-side learner identity merely as a shortcut for progress persistence.

Learner progress must remain client-side unless the specification explicitly changes.

Persisted curriculum entities must use stable identifiers.

Changes to client-side persistence formats must account for:

* schema versioning;
* migration;
* backward compatibility where practical;
* existing learner progress.

Progress behavior must survive ordinary page reloads and browser restarts.

---

# 32. Client-Side Communication

Use the simplest communication mechanism that satisfies the feature.

Do not introduce WebSockets solely for:

* lesson navigation;
* ordinary quiz interaction;
* glossary access;
* client-side progress persistence.

WebSockets may be used when persistent bidirectional communication is materially required.

Other mechanisms such as:

* normal HTTP requests;
* asynchronous HTTP;
* Server-Sent Events;

may be more appropriate depending on the feature.

---

# 33. Generated Project Agent State

Generated repositories may themselves be agent-driven workspaces.

Where applicable, generated repositories should contain their own copies or generated equivalents of:

* `AGENTS.md`;
* `SPEC.md`;
* `STYLE.md`;
* `docs/agent/STATUS.md`;
* `docs/agent/TASKS.md`;
* `docs/agent/DECISIONS.md`.

Generated project agent state belongs to that generated repository.

A CLI agent should be able to enter a generated repository and resume work using only repository-local state.

---

# 34. Generated Project Metadata

Generated repositories should contain machine-readable metadata describing their origin.

Metadata should include where applicable:

* Generator name;
* Generator version;
* template name;
* template version;
* generation timestamp;
* Target Repository name;
* Target Repository URL;
* configured Target Repository revision;
* exact resolved Target Repository commit;
* generated package name;
* curriculum schema version.

Use a structured format such as JSON for machine-readable metadata.

Use Markdown for human and agent instructions.

---

# 35. Generated Documentation

Every generated repository must contain sufficient documentation to:

* build;
* install;
* run;
* test;
* configure;
* continue development.

Generated documentation should not require access to the Generator repository.

Where applicable, documentation should include:

* `README.md`;
* `AGENTS.md`;
* `SPEC.md`;
* `STYLE.md`;
* migration instructions;
* curriculum loading instructions;
* Git submodule instructions;
* provenance information.

---

# 36. Dependencies

Do not add dependencies without a clear technical reason.

Before introducing a dependency:

1. inspect whether the repository already has an appropriate dependency;
2. determine whether a common, established ecosystem library is appropriate;
3. determine whether the standard library provides an equally clear and maintainable implementation;
4. consider maintenance activity;
5. consider deployment impact;
6. consider supported runtime environments.

Prefer established Django and Python ecosystem libraries over unnecessary custom infrastructure.

Do not choose low-level standard-library facilities merely to avoid a well-established dependency when the higher-level library materially improves clarity, reliability, or maintainability.

---

# 37. Logging

Follow `STYLE.md` logging requirements.

Application diagnostics should use structured logging rather than `print()`.

Logging configuration should remain centralized and externally configurable.

Do not log:

* credentials;
* tokens;
* private keys;
* authentication headers;
* sensitive learner data.

Generated applications should provide enough logging to diagnose important failures and generation behavior.

---

# 38. Security

Generated projects and Generator automation must treat external input as untrusted.

Do not:

* construct shell commands through unsafe string concatenation;
* trust project names as filesystem paths without validation;
* permit path traversal outside configured generation roots;
* write secrets into generated repositories;
* execute arbitrary Target Repository code merely because it exists;
* execute generated code without a concrete validation requirement and appropriate controls;
* mutate global Git configuration;
* modify unrelated repositories.

Filesystem and process operations should be explicit and scoped.

---

# 39. Validation

A Generated Project is not complete merely because files were created.

Run appropriate validation before treating generation as successful.

Validation should include where applicable:

* Python syntax checks;
* Django system checks;
* migration consistency checks;
* automated tests;
* static analysis;
* formatting checks;
* package installation checks;
* independent Curriculum App import checks;
* Generated Host Project integration checks.

Validation failures must prevent incomplete output from being treated as a successful generated release.

---

# 40. Git

Use Git as the authoritative record of implementation history.

Do not duplicate Git history inside `STATUS.md`.

Use `STATUS.md` to describe:

* unfinished work;
* current intent;
* blockers;
* important context;
* next actions.

Before substantial work, inspect repository state.

Before stopping substantial work, ensure repository state is accurately represented in `STATUS.md`.

Do not commit:

* secrets;
* credentials;
* tokens;
* private keys;
* generated authentication material;
* environment-specific sensitive configuration.

---

# 41. Ambiguity

When requirements are incomplete:

1. inspect `SPEC.md`;
2. inspect relevant decisions;
3. inspect existing implementation and tests;
4. inspect Target Repository evidence where relevant;
5. prefer the smallest implementation consistent with documented intent;
6. record meaningful assumptions.

Do not invent major product features merely to fill gaps.

Do not redesign unrelated portions of the system while solving a local problem.

Do not use architectural ambiguity as permission to discard existing work.

---

# 42. Prohibited Actions

Agents must not:

* silently redefine requirements;
* commit secrets;
* disable tests merely to obtain a passing build;
* perform large unrelated refactors;
* rewrite unrelated files for formatting consistency;
* modify vendor code unless required;
* create hidden dependencies on the Generated Host Project;
* make generated repositories part of the Generator repository unintentionally;
* depend solely on conversation history for project state;
* erase unfinished tasks because they are inconvenient;
* mark work complete without appropriate verification;
* silently overwrite human-authored curriculum;
* silently discard Target Repository local modifications;
* silently change the Target Repository revision during in-progress work;
* treat a deployed database as the only source of curriculum content;
* introduce server-side learner accounts to avoid implementing client-side progress requirements.

---

# 43. Suggested Repository Structure

The repository may resemble:

```text
.
├── AGENTS.md
├── SPEC.md
├── STYLE.md
├── README.md
├── project.json
├── pyproject.toml
├── src/
├── docs/
│   ├── ARCHITECTURE.md
│   └── agent/
│       ├── STATUS.md
│       ├── TASKS.md
│       └── DECISIONS.md
├── tests/
├── repository/
│   └── <target-repository-name>/
│       └── <Target Repository checkout>
└── generated/
    └── education/
        ├── <Generated Host Project Git repository>
        ├── manage.py
        ├── pyproject.toml
        ├── README.md
        ├── AGENTS.md
        ├── SPEC.md
        ├── STYLE.md
        ├── standalone/
        │   ├── settings.py
        │   ├── urls.py
        │   ├── asgi.py
        │   └── wsgi.py
        ├── templates/
        ├── static/
        └── <curriculum-repository-name>/
            ├── <independent Git repository or submodule>
            └── src/
                └── <python_package_name>/
                    ├── apps.py
                    ├── models.py
                    ├── urls.py
                    ├── views.py
                    ├── services/
                    ├── migrations/
                    ├── templates/
                    └── static/
```

The Target Repository name, generated repository name, and Python package name are separate concepts and must not be assumed to be identical.

The exact layout may differ when documented by `SPEC.md` or an architectural decision.

---

# 44. Completion Standard

A task is not complete merely because code was written.

A task is complete when:

* the implementation satisfies the relevant specification;
* applicable acceptance criteria are met;
* relevant tests pass;
* required documentation is updated;
* `TASKS.md` reflects completion;
* `STATUS.md` accurately describes remaining work;
* repository boundaries remain valid;
* generated output remains reproducible where required.

Leave the repository in a state where another agent can continue without access to previous conversational context.
