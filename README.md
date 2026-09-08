# Education Template

The education template generates a standalone Django host and an independently
installable Curriculum App for the repository configured in `project.json`.

Repository-specific lessons, glossary entries, assessments, questions, and
coverage mappings are JSON data under `curricula/`. Reusable generated files
are editable in their natural formats under
`src/education_generator/templates/`. The Python modules in
`src/education_generator/` orchestrate configuration, repository acquisition,
rendering, metadata, Django scaffolding, and Git initialization.

Generate the configured project with:

```bash
PYTHONPATH=src python -m education_generator
```

`curriculum_content_path` in `project.json` selects the canonical curriculum
data. When omitted, it defaults to
`curricula/<repository-name>/curriculum.json`. Use `--curriculum-content PATH`
to upload a different curriculum JSON for one run. See
`src/education_generator/CONTENT_SCHEMA.md` for the data shape.

Django creates the generated host's `manage.py` through `startproject` and
derives Curriculum App migrations through `makemigrations`. New standalone
hosts also receive an executable `launch.sh` from the reusable host scaffold.
