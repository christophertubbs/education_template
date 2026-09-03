# STATUS

Current objective: generated the educational Django application for the target
repository configured in `project.json`.

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
* Initialized generated Git repositories with local repository identity:
  host commit `b0bf69c5d2cd9ec8e9032f70945b35704b32a50c`, curriculum app
  commit `aec8a494eae6367a6dc44cd2f3dcdae3f31939e4`.
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
* Added optional `project.json` field `curriculum_content_path` for external
  curriculum JSON, plus `src/education_generator/CONTENT_SCHEMA.md`.

Relevant files:

* `src/education_generator/generator.py`
* `src/education_generator/CONTENT_SCHEMA.md`
* `tests/test_generator_scaffold.py`
* `project.json`
* `generated/education/generation_metadata.json`
* `generated/education/lstm/generation_metadata.json`
* `generated/education/lstm/src/lstm/data/curriculum.json`
* `generated/education/lstm/src/lstm/models.py`
* `generated/education/lstm/src/lstm/services.py`
* `generated/education/lstm/src/lstm/static/lstm/js/progress.js`

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
* Reusable scaffold tests passed: optional content path loading, metadata
  injection, AppConfig class naming, and migration app-label rendering.

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
