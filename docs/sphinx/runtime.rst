Education Runtime
=================

The runtime is a reusable Django application.  It persists any compatible
Curriculum Product, renders its semantic content, chooses assessments, and
protects administrative edits during generated baseline refreshes.

Data model
----------

.. code-block:: text

   Curriculum
      |-- Section -- Lesson --< SourceReference
      |                |  `--< GlossaryEntry
      |                `-----< Concept >----- Concept prerequisites
      |                                `----- MasteryContract
      |-- Assessment >-- Question -- review Lesson
      |                    |--< Concept
      |                    `--< MasteryContract
      `-- Concept -------- CoverageRecord

Most content models inherit ``BaselineContent`` and therefore carry the
generated fingerprint and human-edit flag.  Stable identifiers are primary
keys so product upgrades and learner progress do not depend on database IDs.
``ImportConflict`` is operational history rather than curriculum content.

Import order and effects
------------------------

:func:`education_runtime.importing.import_product_payload` runs atomically and
loads records in dependency order: curriculum, sections, concepts,
prerequisites, contracts, sources, lessons, glossary, assessments, questions,
and coverage.  Foreign keys and many-to-many relationships are resolved from
stable identifiers.  Question scoring fields are condensed into the model's
``scoring`` JSON field; lesson semantic blocks remain in ``Lesson.content``.

:func:`education_runtime.product_loading.load_installed_product_payloads`
scans Django applications in deterministic name order and imports those with a
``data/curriculum.json`` resource.  The ``load_curricula`` management command
exposes that service and supports Django's ``--database`` selection.

Assessment behavior
-------------------

The service first restricts pop quizzes to eligible completed-lesson IDs when
the view receives ``?lessons=...``.  It shuffles the bank and answer options
with ``SystemRandom``.  Pop quizzes take the requested number directly from the
eligible shuffled bank.

For section, midterm, and final assessments, selection greedily preserves:

* the configured minimum per represented major concept;
* at least one question per represented major Mastery Contract;
* for midterms and finals, every represented section and terminal outcome.

Remaining slots are random.  If required coverage cannot fit in
``selection_count``, selection raises ``ValueError`` rather than silently
dropping a requirement.  Artifact validation must therefore keep bank design
and selection configuration mutually feasible.

Views and navigation
--------------------

Views remain thin.  They enforce curriculum ownership in object lookups, build
template context, and determine learning destinations.  Lesson navigation goes
to the next lesson or the current section quiz.  Section quizzes may lead to a
midterm at the midpoint, the next section's first lesson, or the final.  A
midterm resumes at the first lesson of the second half; a pop quiz returns to
the curriculum page.

Administration
--------------

The admin's shared ``BaselineAdmin`` marks saved generated records as human
modified.  It exposes identifying and baseline state for curriculum models.
Conflicts are separately listed with timestamps, fingerprints, and resolution
state.  Admin editing does not mutate packaged JSON, so resolution policy must
account for the next refresh.

Runtime compatibility constraints
---------------------------------

Product dependency metadata expresses a compatible runtime version, and the
importer records it on ``Curriculum``.  At present, product discovery and
migration do not independently enforce semantic compatibility before loading;
that gap is recorded in ``docs/agent/TASKS.md``.  Treat compatibility changes as
release and migration work, not a string-only metadata edit.
