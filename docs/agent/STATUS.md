# STATUS

Current objective: generate an independent CFE curriculum from the newly
configured `project.json` without changing the existing standalone host.

Current requirements: generation lifecycle, target revision provenance,
curriculum app reusability, generated host project, packaged curriculum data,
client-side learner progress, assessment coverage, admin editing, generated Git
repository initialization, and validation (`GEN-001`-style lifecycle
requirements from `SPEC.md` sections 4-42).

Recently completed work:

* Added reproducible generator code under `src/education_generator`.
* Cloned target repository `https://github.com/NOAA-OWP/lstm.git` under
  `repository/lstm`.
* Resolved configured revision `master` to exact commit
  `9d21f2c2a5c93dae8a33796ed9bf63b790762e3c`.
* Generated standalone Django host project at `generated/education`.
* Generated independent reusable curriculum app repository at
  `generated/education/lstm`.
* Generated packaged curriculum data with 7 longer lessons, 10 glossary entries,
  10 assessments, 63 repository-only question records, and 7 coverage records.
* Adjusted generated development host settings for forwarded browser access:
  `ALLOWED_HOSTS = ["*"]` and documented `runserver 0.0.0.0:8000`.
* Addressed curriculum quality defects: removed generated-app leakage from
  assessment questions, replaced unrelated distractors with repository-adjacent
  alternatives, added explicit lesson-completion feedback, and wired completed
  lessons to the next relevant assessment.
* Addressed section-flow defects: each lesson now has a unique section quiz,
  lesson completion opens that lesson's quiz, and quiz submission navigates to
  the next lesson or the course index after the final section.
* Generalized the generator scaffold so new repositories can reuse the same
  Django host, curriculum app, admin models, loader, templates, static assets,
  progress behavior, section quiz flow, and Git initialization with different
  content.
* Added required `project.json` field `curriculum_content_path` for external
  curriculum JSON, plus `src/education_generator/CONTENT_SCHEMA.md`.
* Split the former 2,472-line generator into focused configuration, context,
  repository, process, rendering, curriculum, metadata, scaffold, and CLI
  modules. `generator.py` is now only a compatibility facade.
* Moved the canonical LSTM curriculum to
  `curricula/lstm/curriculum.json`; external curriculum data is now required and
  may be overridden with `--curriculum-content`.
* Moved reusable Python, HTML, CSS, JavaScript, TOML, and Markdown artifacts to
  `src/education_generator/templates` in their natural formats.
* Changed generation so Django `startproject` owns `manage.py` and Django
  `makemigrations` creates migrations from the rendered models.
* Added `src/education_generator/launch.sh` to newly created standalone hosts.
  File copying and template rendering preserve source modes so generated
  launchers remain executable.
* Regenerated clean repositories at host commit
  `e365943af19fe2da7f0b89bc21baa41679781006` and Curriculum App commit
  `ce60d6ed543b345442c1a400406c239bbaeb6e2d`.
* Cloned CFE under `repository/cfe` and resolved `master` to exact commit
  `f9182dfb3d81c407c66c5b782114173893c30cf2`.
* Added a source-traceable CFE curriculum with 7 lessons, 10 glossary entries,
  10 assessments, 36 CFE-only questions, and 7 coverage records under
  `curricula/cfe/curriculum.json`.
* Updated generation to preserve an existing host and derive Curriculum App
  migrations with generator-local Django settings.
* Generated the independent CFE Curriculum App at
  `generated/education/cfe`, commit
  `c608aa7eb1751d5b77691ac8c30c8aa013d2e7a0`.
* Verified the existing host stayed at commit
  `e365943af19fe2da7f0b89bc21baa41679781006`; its pre-existing
  `standalone/asgi.py` edit and complete tracked diff fingerprint remained
  unchanged.

Relevant files:

* `src/education_generator/generator.py`
* `src/education_generator/scaffold.py`
* `src/education_generator/rendering.py`
* `src/education_generator/templates/`
* `src/education_generator/launch.sh`
* `curricula/lstm/curriculum.json`
* `curricula/cfe/curriculum.json`
* `src/education_generator/migration_settings.py`
* `src/education_generator/CONTENT_SCHEMA.md`
* `tests/test_generator_scaffold.py`
* `project.json`
* `generated/education/generation_metadata.json`
* `generated/education/lstm/generation_metadata.json`
* `generated/education/lstm/src/lstm/data/curriculum.json`
* `generated/education/lstm/src/lstm/models.py`
* `generated/education/lstm/src/lstm/services.py`
* `generated/education/lstm/src/lstm/static/lstm/js/progress.js`
* `generated/education/cfe/generation_metadata.json`
* `generated/education/cfe/src/cfe/data/curriculum.json`

Tests and validation run:

* `python -m compileall src generated/education/standalone generated/education/lstm/src/lstm`
* `python generated/education/manage.py check`
* `python generated/education/manage.py migrate`
* `python generated/education/manage.py makemigrations --check --dry-run`
* `python generated/education/manage.py load_curriculum`
* Django test-client smoke check for `/`, `/lstm/`, `/lstm/glossary/`,
  `/lstm/progress/`, `/lstm/lessons/lstm-purpose/`, and
  `/lstm/assessments/final/`.
* `curl -I --max-time 5 http://127.0.0.1:8000/lstm/` against the launched
  `0.0.0.0:8000 --noreload` development server.
* Content scan for generated-app leakage terms in
  `generated/education/lstm/src/lstm/data/curriculum.json`.
* Smoke check that lesson pages include `data-completion-feedback`,
  `data-next-assessment-url`, and the related assessment link.
* Database/navigation check that every section quiz maps to exactly one lesson,
  every lesson links to its own quiz, and every section quiz has the expected
  `data-next-url`.
* `PYTHONPATH=src python -m unittest discover -s tests`
* Full regeneration with `PYTHONPATH=src python -m education_generator`.
* `bash -n generated/education/launch.sh`
* `generated/education/launch.sh --help`
* CFE generation with `PYTHONPATH=src python -m education_generator`.
* Independent CFE `django check` and migration drift check using
  `education_generator.migration_settings`.
* Independent in-memory CFE migration and `load_curriculum` verification.

Current validation result:

* Django system check passed with no issues.
* Migrations applied successfully.
* Migration drift check reported no changes.
* Curriculum loader created expected record counts.
* Smoke routes returned expected statuses: `/` redirected with 302; curriculum
  pages returned 200.
* Launched server returned `HTTP/1.1 200 OK` for `/lstm/`.
* Generated curriculum JSON scan found no Django/CSS/browser/generated-app
  leakage terms in question content.
* Section quiz mapping check showed 7 unique section quizzes, each with 3
  questions, and correct next-lesson navigation for all lessons.
* Reusable scaffold tests passed: required content path loading, metadata
  injection, AppConfig class naming, natural artifact boundaries, renderer
  cache handling, and Django migration invocation.
* Generated `manage.py` matches Django's stock `startproject` artifact.
* Generated `launch.sh` is tracked with executable mode `100755`.
* Source scans found no embedded curriculum builders, assessment identifiers,
  migration bodies, or web-asset strings in generator Python.
* CFE loader created 7 lessons, 10 glossary entries, 10 assessments, 36
  questions, and 7 coverage records.
* All 7 CFE section assessments map one-to-one to their lessons, and every CFE
  lesson contains 241-284 words.
* Existing host tracked diff fingerprint remained
  `07182b710bed4721225dc600fa2a0be600e29dfe60ce3be95b2c5b947c140267`.

Current failures: none known.

Important assumptions:

* The generated curriculum is source-traceable and longer than the first pass,
  but future work can still deepen hydrology and neural-network prerequisites.
* Learner progress is stored client-side in versioned `localStorage` data with
  export/import support. This satisfies the current no-account persistence
  requirement at the smallest practical scope.
* The generated host ignores the nested curriculum repository path so host Git
  history does not absorb curriculum app history.

Next concrete actions:

* Review generated curriculum accuracy against the recorded source references.
* Add focused tests for `education_generator` configuration validation and
  full generated output structure.
* Add deeper curriculum modules for hydrologic domain concepts and LSTM math
  if maintainers need more complete prerequisite coverage.
