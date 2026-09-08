# __DISPLAY_NAME__ Curriculum Product

This independent package contains the generated curriculum and provenance for
`__REPOSITORY_URL__` at exact commit `__RESOLVED_COMMIT__`. It requires the
Education Runtime `__RUNTIME_COMPATIBILITY__` and contains no generic learning
views, models, or client-side application code.

Install it beside a compatible Education Runtime, add
`__APP_NAME__.apps.__APP_CONFIG_CLASS__` to `INSTALLED_APPS`, then run:

```bash
python manage.py migrate
python manage.py check
```

The data migration deterministically loads the generated baseline. Runtime
administrative overrides remain separate and are reported as conflicts when a
later baseline changes.

Run package tests with `python -m unittest discover -s tests`. Generation
evidence and completion records are under `provenance/`.

