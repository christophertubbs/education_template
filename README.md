# Education Curriculum System

This repository implements a shared Django Education Runtime, a thin optional
runner, and a staged generator that produces independently installable
Curriculum Products instead of duplicated websites.

Install dependencies, then prepare and launch the runtime:

```bash
python -m pip install -e .
./install.sh
python manage.py test
python manage.py runserver
```

`install.sh` applies migrations, reloads every discovered product's current
packaged curriculum JSON, and collects static assets. The explicit reload means
a JSON-only curriculum update is applied even when all migrations were already
recorded as complete. Set `PYTHON_BIN` to select a different Python executable.

Generate the product configured by `project.json`:

```bash
PYTHONPATH=src python -m education_generator
```

The generator resolves an exact Target Repository commit, inventories source
without executing it, validates the artifacts under `curricula/<target>/`,
assembles in `.work/`, and promotes only passing output to `generated/`.

From this repository, the runner automatically loads products whose generated
provenance matches a project directory under `curricula/`. Product directory,
package, and curriculum names do not need a `curriculum` suffix. Install a
generated product when using it outside this repository; installed products are
also discovered automatically:

```bash
python -m pip install -e generated/cfe-curriculum
./install.sh
python manage.py runserver
```

`EDUCATION_PRODUCTS` remains an optional comma-separated compatibility setting
for legacy product packages that do not yet advertise the standard entry point.

See `docs/ARCHITECTURE.md`,
`src/education_generator/CONTENT_SCHEMA.md`, and `docs/agent/STATUS.md`.
