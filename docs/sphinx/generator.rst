Generator subsystem
===================

The generator turns reviewed, machine-readable curriculum artifacts into an
independent installable product.  It deliberately does not author missing
curriculum during ``run_pipeline`` and does not execute target code.

Inputs and durable outputs
--------------------------

``project.json`` (or ``--project``) supplies the target URL/revision, safe local
name, Python product package name, display name, artifact directory, runtime
compatibility, learner prerequisites, required topics, initial Git branch, and
automatic-commit choice.  :mod:`education_generator.configuration` treats all
of these values as untrusted.

The artifact directory must contain the five JSON objects described by
``src/education_generator/CONTENT_SCHEMA.md``:

* ``knowledge-map.json``: concepts and acyclic typed relationships;
* ``mastery-contracts.json``: measurable competencies per concept;
* ``curriculum.json``: lessons, terminology, evidence, assessments, questions;
* ``coverage.json``: concept-to-teaching and concept-to-assessment coverage;
* ``completion.json``: required passes, terminal outcomes, and unresolved work.

The workspace under ``.work`` contains phase state, a non-executing source file
inventory, source revision impact, and staging.  The promoted repository under
``generated`` contains the packaged payload and copied provenance.

Phase ownership
---------------

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * - Module
     - What it does
     - What it affects
   * - ``cli``
     - Parses the project path, enforces repository containment, resolves the
       target, and creates the run context.
     - Starts every generation and determines paths and prior source revision.
   * - ``configuration``
     - Validates names, URL schemes, arrays, branch text, and local paths.
     - Security boundary before filesystem or Git operations.
   * - ``repositories``
     - Clones/fetches clean targets, resolves and checks out an exact commit,
       and manages product-local Git identity and commits.
     - Read-only target evidence and independent generated repository history.
   * - ``inventory``
     - Records target files without imports and diffs prior/current commits.
     - Re-audit scope and durable evidence; it does not decide content changes.
   * - ``artifacts``
     - Loads all required JSON and combines it into the runtime payload shape.
     - Boundary between reviewed artifacts and assembly.
   * - ``validation``
     - Enforces identifiers, references, closure, content structures,
       terminology, assessments, coverage, and completion.
     - Promotion gate; failures remain unresolved rather than being normalized.
   * - ``source_validation``
     - Checks target-source paths, line ranges, containment, and commit-pinned
       URLs against the resolved checkout.
     - Claim traceability and resistance to stale or escaping references.
   * - ``rendering``
     - Replaces explicit tokens in template paths and UTF-8 text files and
       copies durable agent instructions.
     - Generated package names, metadata, documentation, and migration code.
   * - ``scaffold``
     - Renders templates, writes payload/provenance, and promotes staging while
       preserving an existing ``.git`` directory.
     - The entire product working tree except its independent Git metadata.
   * - ``pipeline``
     - Orders phases, persists status, compiles generated Python, gates
       promotion, and optionally commits.
     - Transaction-like lifecycle of a generation run.
   * - ``metadata`` and ``constants``
     - Publish generator/product/schema/runtime versions and pinned provenance.
     - Product compatibility, audit trails, and local discovery matching.
   * - ``processes``
     - Runs explicit argument-list subprocesses with inherited plus optional env.
     - Git failures propagate immediately through ``check=True``.
   * - ``generator``
     - Re-exports the supported integration API.
     - External Python callers should prefer it over internal modules.

Important failure behavior
--------------------------

Existing target and generated Git trees must be clean.  Staging is discarded
and rebuilt, but a destination is not touched until validation and Python
compilation pass.  Promotion replaces all non-``.git`` destination content.
Consequently, human edits belong in canonical artifacts or the runtime admin,
not directly in a clean generated product tree.

``CURRICULUM_SCHEMA_VERSION`` is emitted into provenance and must agree with the
artifact contract and validation rules.  Changing a template changes future
generation only; regenerate affected products to propagate it.

.. warning::

   The current tree contains a version-label discrepancy that maintainers must
   understand before the next generation: ``CONTENT_SCHEMA.md`` and the newer
   terminology validation describe artifact contract 2.2, while
   ``constants.py`` and the generated agent-state templates still label output
   as schema 2.1.  Validation behavior and emitted provenance can therefore
   describe different revisions.  Resolve this as a coordinated schema release;
   do not conceal it by changing only the documentation label.
