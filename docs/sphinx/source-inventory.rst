Authored source inventory
=========================

This page accounts for every maintained source category under ``src/``.  Python
bytecode directories and ``education_curriculum_system.egg-info`` are generated
build/install artifacts: delete and recreate them through normal tooling rather
than treating them as architecture or editing them by hand.

Generator Python
----------------

.. csv-table::
   :header: "File", "Purpose"
   :widths: 35, 65

   "``education_generator/__init__.py``", "Package identity."
   "``education_generator/__main__.py``", "Supports ``python -m education_generator`` by calling the CLI."
   "``education_generator/generator.py``", "Stable public re-export surface."
   "``education_generator/cli.py``", "Top-level configuration, Git resolution, context, and pipeline entry."
   "``education_generator/configuration.py``", "Validated untrusted project configuration and AppConfig naming."
   "``education_generator/context.py``", "Immutable per-run paths and provenance."
   "``education_generator/constants.py``", "Generator, schema, runtime, template, and product versions and template root."
   "``education_generator/processes.py``", "Checked argument-list subprocess execution."
   "``education_generator/repositories.py``", "Target clone/fetch/checkout and generated-product Git operations."
   "``education_generator/inventory.py``", "Non-executing file inventory and revision-change impact."
   "``education_generator/artifacts.py``", "Five-artifact loader and runtime payload composition."
   "``education_generator/validation.py``", "Complete structural, referential, content, terminology, assessment, coverage, and completion gate."
   "``education_generator/source_validation.py``", "Resolved-checkout source path, line, and pinned URL checks."
   "``education_generator/metadata.py``", "Serializable generation provenance."
   "``education_generator/rendering.py``", "Token-aware scaffold rendering and governing-document copying."
   "``education_generator/scaffold.py``", "Product assembly, provenance writing, and staged promotion."
   "``education_generator/pipeline.py``", "Durable phase orchestration and generated Python compilation."
   "``education_generator/CONTENT_SCHEMA.md``", "Human-readable artifact contract 2.2 used by curriculum authors and reviewers."

Generator templates
-------------------

``templates/product`` contains the generated README, package metadata,
``.gitignore``, Django package/AppConfig, initial and refresh migrations, and
portable product tests.  ``templates/agent`` contains the generated product's
durable ``STATUS``, ``TASKS``, and ``DECISIONS`` state.  Placeholder directories
and symbols such as ``__APP_NAME__`` are valid template tokens, not unfinished
root-package modules.  See :doc:`generated-products` for each file's effects.

Runtime Python and database schema
----------------------------------

.. csv-table::
   :header: "File", "Purpose"
   :widths: 38, 62

   "``education_runtime/__init__.py``", "Package identity."
   "``education_runtime/apps.py``", "Django app registration."
   "``education_runtime/models.py``", "Generic persisted curriculum, assessment, provenance, baseline, and conflict types."
   "``education_runtime/migrations/0001_initial.py``", "Creates the complete initial runtime schema, relations, ordering, and constraints."
   "``education_runtime/migrations/__init__.py``", "Marks the runtime migration package."
   "``education_runtime/importing.py``", "Atomic stable-ID upserts, fingerprints, relations, and conflict preservation."
   "``education_runtime/product_loading.py``", "Deterministic packaged-resource scanning and current-payload import."
   "``education_runtime/services.py``", "Assessment selection and curriculum assessment queries."
   "``education_runtime/views.py``", "Learner request coordination and next-destination rules."
   "``education_runtime/urls.py``", "Target-independent named route declarations."
   "``education_runtime/admin.py``", "Human-edit marking and import-conflict inspection."
   "``education_runtime/management/__init__.py``", "Management extension package."
   "``education_runtime/management/commands/__init__.py``", "Runtime command package."
   "``education_runtime/management/commands/load_curricula.py``", "Explicit database-selectable product refresh command."

Runtime presentation
--------------------

All nine files in ``templates/education_runtime`` are covered in
:doc:`frontend`: ``base``, curriculum list/detail, lesson, assessment, glossary,
sources, progress, content-block, and inline-content templates.  The static
directory contains ``assessment.js`` (client scoring and attempts),
``progress.js`` (IndexedDB progress and pop navigation), ``runtime.css``
(shared responsive/accessibility presentation), and ``favicon.ico`` (site icon).

Runner
------

.. csv-table::
   :header: "File", "Purpose"
   :widths: 38, 62

   "``education_runner/__init__.py``", "Package identity and boundary statement."
   "``education_runner/product_discovery.py``", "Validated local, installed, and legacy Curriculum Product discovery."
   "``education_runner/settings.py``", "Environment-driven standalone Django composition."
   "``education_runner/urls.py``", "Admin and root runtime URL mounting."
   "``education_runner/asgi.py``", "ASGI application callable."
   "``education_runner/wsgi.py``", "WSGI application callable."
