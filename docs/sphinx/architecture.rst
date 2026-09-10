Architecture and data flow
==========================

Responsibilities
----------------

.. list-table::
   :header-rows: 1
   :widths: 20 38 42

   * - Component
     - Owns
     - Must not own
   * - ``education_generator``
     - Configuration safety, target acquisition, artifact validation, product
       assembly, provenance, staging, and promotion.
     - Learner-facing runtime behavior or target execution during analysis.
   * - Curriculum Product
     - Target-specific JSON, provenance, package metadata, and data migrations.
     - Generic models, views, templates, scoring, or progress code.
   * - ``education_runtime``
     - Generic Django schema, import conflict policy, queries, assessment
       selection, rendering, administration, and local learner progress.
     - Imports or special cases for a particular product.
   * - ``education_runner``
     - Environment-derived Django settings, product discovery, and URL mounting.
     - Curriculum content or duplicated runtime behavior.

Generation flow
---------------

.. code-block:: text

   project.json
       |
       v
   validate configuration --> clone/fetch target --> resolve exact commit
                                                   |
                                                   v
   curricula/<target>/*.json --> validate structure + pinned source evidence
                                                   |
                                                   v
   .work/<product>/staging --> compile Python --> verify destination is clean
                                                   |
                                                   v
   generated/<product>/ (independent Git repository, optional auto-commit)

``cli.main`` constructs a :class:`~education_generator.context.GenerationContext`.
``pipeline.run_pipeline`` records each phase in ``.work/<product>/state.json``.
The inventory and regeneration-impact files are durable evidence, while the
five files in the configured curriculum source directory are the reviewed input
contract.  Validation is fail-closed: errors are copied into ``unresolved`` and
promotion does not occur.

Installation and refresh flow
-----------------------------

.. code-block:: text

   runner startup
      |-- discover local generated products by provenance
      |-- discover installed package entry points
      `-- add explicitly configured legacy packages
                         |
                         v
                  Django INSTALLED_APPS
                         |
             migrate --> load_curricula --> collectstatic
                         |
                         v
       packaged data/curriculum.json --> atomic baseline importer --> runtime DB

Product migrations establish initial data and schema history.  The explicit
``load_curricula`` command is still required on installation because packaged
JSON may change without a new migration.  Both routes use the same importer.

Baseline update semantics
-------------------------

Every generated runtime row has a SHA-256 fingerprint and a
``is_human_modified`` flag.  The admin marks edited rows as human modified.
On refresh:

* an untouched row is updated and receives the incoming fingerprint;
* an edited row with the same baseline remains untouched;
* an edited row whose incoming baseline changed remains untouched and creates
  an :class:`~education_runtime.models.ImportConflict`;
* generated many-to-many relationships are synchronized only when the row was
  not preserved as a human override.

This is preservation, not conflict resolution.  An administrator must review
and resolve recorded conflicts.

Learner request flow
--------------------

URLs dispatch to thin functions in :mod:`education_runtime.views`.  Views query
runtime models, delegate selection to :mod:`education_runtime.services`, and
render shared templates.  Semantic JSON blocks become HTML in
``content_block.html`` and inline spans become HTML in ``inline_content.html``.
The browser then performs assessment scoring and IndexedDB progress updates.
No account or server-side learner-progress model is involved.

Change-impact guide
-------------------

.. list-table::
   :header-rows: 1
   :widths: 28 36 36

   * - If you change
     - Directly affected
     - Revalidate
   * - Artifact schema or validation
     - Generator constants, validation, canonical curricula, product payloads.
     - Every artifact set, generated products, clean product install.
   * - Runtime model fields
     - Runtime migrations, importer mappings, admin, views/templates.
     - Migration drift, clean migration, refresh, runtime tests.
   * - Import fingerprint fields
     - Baseline comparison and conflict behavior.
     - Untouched update, human override, relation preservation, repeat import.
   * - Product entry-point format
     - Generator template and runner discovery.
     - Local, installed, legacy, duplicate, and malformed discovery cases.
   * - Assessment configuration
     - Generator validation and runtime coverage-preserving selection.
     - Pop eligibility plus section/midterm/final coverage and infeasible banks.
   * - Semantic content blocks
     - Schema validator, importer storage, content template, CSS, accessibility.
     - Every supported block, unsafe/invalid input, responsive and keyboard use.
   * - Progress schema
     - ``progress.js`` imports, exports, attempts, pop navigation.
     - Version rejection, curriculum mismatch, upgrade/migration behavior.
   * - Product template
     - All subsequently generated products, not existing products automatically.
     - Rendered scaffold, package build, migrations, entry point, product tests.
