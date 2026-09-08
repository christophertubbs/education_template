# Education Curriculum System

This repository implements a shared Django Education Runtime, a thin optional
runner, and a staged generator that produces independently installable
Curriculum Products instead of duplicated websites.

Install, migrate, test, and launch the runtime:

```bash
python -m pip install -e .
python manage.py migrate
python manage.py test
python manage.py runserver
```

Generate the product configured by `project.json`:

```bash
PYTHONPATH=src python -m education_generator
```

The generator resolves an exact Target Repository commit, inventories source
without executing it, validates the artifacts under `curricula/<target>/`,
assembles in `.work/`, and promotes only passing output to `generated/`.

Install a generated product and enable it without modifying runner source:

```bash
python -m pip install -e generated/cfe-curriculum
EDUCATION_PRODUCTS=cfe_curriculum python manage.py migrate
EDUCATION_PRODUCTS=cfe_curriculum python manage.py runserver
```

See `docs/ARCHITECTURE.md`,
`src/education_generator/CONTENT_SCHEMA.md`, and `docs/agent/STATUS.md`.
