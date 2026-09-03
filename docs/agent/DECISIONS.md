# DECISIONS

## 2026-09-03: Generated Repository Boundaries

Generated host and curriculum app outputs are independent Git repositories under
`generated/education` and `generated/education/lstm`. The parent generator
repository ignores generated output, while the generated host ignores the nested
curriculum app path. This preserves the specified dependency direction:

`Generator -> Generated Host Project -> Curriculum App`

The host integrates the app at runtime by adding `generated/education/lstm/src`
to `sys.path` from `manage.py` for standalone local use. The curriculum app does
not import from the host project.

For local forwarded development environments, the generated host uses
`ALLOWED_HOSTS = ["*"]` and is documented to run with
`python manage.py runserver 0.0.0.0:8000`. This is development-only behavior;
deployment should replace it with explicit host names.

## 2026-09-03: Curriculum Persistence and Regeneration Tracking

The generated curriculum app stores lessons, glossary entries, assessments,
questions, feedback, source references, and coverage records in Django models.
Canonical generated curriculum content is packaged as
`src/lstm/data/curriculum.json` and loaded through `python manage.py
load_curriculum`.

Generated content models include `baseline_fingerprint` and
`is_human_modified`. The loader updates generated-owned records but preserves
records flagged as human modified, giving later regeneration work a reliable
conflict-detection boundary.

## 2026-09-03: Learner Progress Storage

Learner progress is stored client-side using versioned browser `localStorage`
under a generated app-specific key such as `lstm-curriculum-progress-v1`. The
generated UI supports lesson completion, assessment-attempt storage, reset,
export, and import without user accounts or server-side learner identity.

## 2026-09-03: Reusable Scaffold With Replaceable Curriculum Content

The generator owns the Django project/app scaffold and can generate the same
architecture for repositories other than `lstm`. Repository-specific content is
replaceable through optional `project.json` field `curriculum_content_path`.
When provided, that JSON supplies course, lesson, glossary, assessment,
question, and coverage records; the generator replaces any supplied metadata
with current target-revision provenance.

Generated code is parameterized by `name`, `curriculum_app_name`, and
`display_name` for host import paths, ignored nested repository paths, URL
namespaces, static asset paths, migration app labels, loader imports, progress
storage keys, export filenames, and documentation.
