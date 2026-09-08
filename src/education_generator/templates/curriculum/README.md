# __DISPLAY_NAME__ Curriculum App

This is a reusable Django app containing source-traceable curriculum for
`__REPOSITORY_URL__` at commit `__RESOLVED_COMMIT__`.

## Install in a Django Project

```bash
python -m pip install -e .
```

Add `__APP_NAME__` to `INSTALLED_APPS`, include
`__APP_NAME__.urls`, run migrations, and load the
packaged curriculum:

```bash
python manage.py migrate
python manage.py load_curriculum
```

Packaged data lives in `src/__APP_NAME__/data/curriculum.json`.
Administrative edits are tracked with `is_human_modified` and generated
fingerprints so later regeneration can detect preservation requirements.
