# TASKS

## Complete

* Replace per-target Django generation with a shared runtime and data-oriented
  Curriculum Products. (`SPEC.md` sections 3, 23-27, 38)
* Implement staged generation, structured analysis, completion and evidence
  gates, staging, and promotion. (sections 6-19, 32-39, 44-46)
* Implement generic runtime data, baseline conflicts, deterministic assessments,
  and product migrations. (sections 20-31)
* Implement navigation, accessible content/assessment rendering, and versioned
  progress export/import. (sections 28-29, 40-43)
* Migrate CFE content into v2 knowledge, mastery, coverage, completion,
  assessment, and provenance artifacts.
* Record prior/current source revisions and changed-file impact during
  regeneration.
* Implement structured lesson blocks and inline semantics, accessible MathJax
  equations, source-aware code, variable tables, examples, diagnostics,
  callouts, and lesson-linked glossary definitions. Regenerate CFE lessons under
  schema 2.1 and product/runtime 1.1.
* Generate the SAC-SMA 1.1 Curriculum Product from target commit
  `975902e3d44785f3b3503f29adfb5755120f5bf5`, including conceptual hydrology,
  equations and units, HRUs, Fortran-to-C/C++/Python translation, BMI driver and
  ISO C interoperability, build/test guidance, and pinned source discrepancies.
* Add schema 2.2 terminology contracts, first-use/equation-order/assessment
  vocabulary gates, terminology-closure and contextual-readability audit
  evidence, and regenerate both CFE and SAC-SMA products. CFE product commit:
  `c6431330dd5e6330f539f869373ec0606ee4b1a8`; SAC-SMA product commit:
  `25cf18748f3906334f984098b7ee100f7ea481b7`.
* Automatically discover every installed Curriculum Product through package
  entry points so migration and server startup need no `EDUCATION_PRODUCTS`
  setting. Regenerated CFE product commit:
  `6ea878e9bde20f3fc0257edb1a501593cc38a27b`; SAC-SMA product commit:
  `43143a0bb892ba1f14c63fb632f51d61d7961dc1`.
* Discover repository-local products by cross-referencing `curricula/` project
  directories with generated provenance, without requiring `curriculum` in any
  generated repository, package, or curriculum name. Keep installed and legacy
  discovery additive and fail closed on conflicting matches.
* Add an idempotent `install.sh` workflow that migrates the configured database,
  imports current packaged curriculum JSON independently of migration state,
  and collects static assets.
* Continue and complete the source-pinned LGAR-C/CASAM curriculum begun in
  ChatGPT Work: review the primary literature and target source, close
  terminology and scientific-depth gaps, add cumulative assessments, synchronize
  the canonical and packaged artifacts, and validate stable product 1.1.0.
* Preserve section, major-concept, major-Mastery-Contract, and terminal-outcome
  coverage during randomized non-pop assessment selection while retaining
  prior-lesson filtering and variation for pop quizzes.
* Add warning-strict Sphinx onboarding documentation for every maintained source
  category, cross-package behavior and change effects, with an isolated Django
  autodoc setup, Markdown build guide, and executable build script.

## Ready

* Add browser-level WCAG 2.2 AA coverage for rendered mathematics, responsive
  tables, glossary-definition navigation, and pop-quiz navigation.
* Enforce semantic runtime compatibility before product migration.
