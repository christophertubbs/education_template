Specification map
=================

The implementation is organized around the normative ``SPEC.md`` contract.
This map tells an onboarded maintainer where a behavior originates; it does not
replace reading the relevant specification section.

.. list-table::
   :header-rows: 1
   :widths: 22 34 44

   * - Specification concern
     - Primary implementation
     - Durable evidence or enforcement
   * - Architecture and boundaries (1--4, 23--26, 38)
     - Generator scaffold, runtime app, runner discovery.
     - Package entry points, dependency metadata, separate Git roots.
   * - Inputs and exact revision (6--8)
     - ``configuration``, ``repositories``, ``cli``.
     - Validated project config, detached commit, generation metadata.
   * - Knowledge and mastery (9--14)
     - Canonical artifact content; runtime models.
     - Knowledge map, mastery contracts, lessons, questions.
   * - Traceability and research (15--16, 36)
     - ``source_validation`` and artifact validator.
     - Source records, certainty, pinned URL/path/line evidence.
   * - Coverage and completion (17--19, 46)
     - ``validation`` and pipeline promotion gate.
     - Coverage/completion JSON and durable failed phase state.
   * - Assessments (20--21)
     - Validator, ``services``, assessment template and JavaScript.
     - Bank constraints, coverage-preserving attempts, explicit scoring data.
   * - Glossary and terminology (6.3, 22, 40.1)
     - Validator, lesson/glossary models, inline/block templates.
     - Terminology contracts, first-use ordering, visible definitions.
   * - Database and baseline edits (27, 30--31)
     - Runtime models/importer/admin and product migrations.
     - Fingerprints, human-modified flags, conflict records.
   * - Progress (28--29)
     - ``progress.js`` and body/template data attributes.
     - Versioned IndexedDB records and portable JSON validation.
   * - Metadata and intermediate state (32, 35)
     - ``metadata``, ``inventory``, ``PipelineState``, scaffold.
     - ``.work`` state and product ``provenance``.
   * - Generated documentation and procedure capture (33, 37)
     - Product README and agent-document templates.
     - Copied governing docs and rendered durable state.
   * - Validation and security (39, 44)
     - Configuration/source/artifact validation, clean-tree gates.
     - Failures block promotion; paths and names are constrained.
   * - UI, tone, accessibility, networking (40--43)
     - Runtime templates/static assets and thin HTTP views.
     - Semantic HTML, MathJax, browser progress, standard HTTP.

Known implementation follow-ups are authoritative only when also recorded in
``docs/agent/TASKS.md``.  In particular, browser-level WCAG coverage and
semantic runtime compatibility enforcement are currently ready work rather than
completed guarantees.
