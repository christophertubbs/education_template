# DECISIONS

## 2026-09-03: Generated Repository Boundaries

Generated host and curriculum app outputs are independent Git repositories under
`generated/education` and `generated/education/lstm`. The parent generator
repository ignores generated output, while the generated host ignores the nested
curriculum app path. This preserves the specified dependency direction:

`Generator -> Generated Host Project -> Curriculum App`

The host integrates the app at runtime by adding the nested Curriculum App's
`src` directory to `sys.path` from host settings for standalone local use.
`manage.py` remains the unmodified artifact emitted by Django. The curriculum
app does not import from the host project.

For local forwarded development environments, the generated host uses
`ALLOWED_HOSTS = ["*"]` and is documented to run with
`./launch.sh`. The launcher binds to `0.0.0.0:8000` by default, selects Uvicorn,
Gunicorn, or Django's development server based on availability, and accepts
optional TLS paths. This permissive host configuration is development-only;
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

## 2026-09-03: File-Based Scaffold and Uploaded Curriculum Content

Reusable host and Curriculum App artifacts are stored in their natural formats
under `src/education_generator/templates`. The generator renders explicit
tokens in file paths and bodies; Python does not contain embedded Python, HTML,
CSS, JavaScript, or repository-specific curriculum records.

The standalone `launch.sh` artifact is stored at
`src/education_generator/launch.sh` and copied into each newly created host
with its executable mode preserved.

Repository-specific lessons, glossary entries, assessments, questions, and
coverage records are external JSON supplied by `curriculum_content_path`, its
conventional `curricula/<name>/curriculum.json` default, or the
`--curriculum-content` command-line override.
The generator validates the data shape and replaces supplied metadata with
current target-revision provenance before packaging it.

Generated code is parameterized by `name`, `curriculum_app_name`, and
`display_name` for host import paths, ignored nested repository paths, URL
namespaces, static asset paths, loader imports, progress storage keys, export
filenames, and documentation. Django `startproject` creates `manage.py`, and
Django `makemigrations` derives migration scripts from rendered models.

## 2026-09-03: Preserve Existing Standalone Hosts

When `generated/education` already exists, generation creates only the newly
configured independent Curriculum App. It does not recreate, render, commit, or
otherwise alter tracked host files. The nested app path is added to the host
repository's local `.git/info/exclude` so host status remains focused without a
tracked `.gitignore` change.

Curriculum migrations are derived with Django using generator-local minimal
settings rather than the existing host settings. This lets a new app obtain its
own migrations without first modifying the host's `INSTALLED_APPS`.
