# Generated Education Host

This standalone Django project hosts generated curriculum apps.

## Provenance

* Target repository: `__REPOSITORY_URL__`
* Configured revision: `__CONFIGURED_REVISION__`
* Resolved commit: `__RESOLVED_COMMIT__`
* Generated package: `__APP_NAME__`

## Run

```bash
python -m pip install -e ./__REPOSITORY_NAME__
python -m pip install -e .
python manage.py migrate
python manage.py load_curriculum
./launch.sh
```

Run `./launch.sh --help` for host, port, and optional TLS settings. The launcher
prefers Uvicorn, then Gunicorn, and falls back to Django's development server.

The curriculum app is an independent Git repository at
`./__REPOSITORY_NAME__`. The host keeps that path ignored so it does
not absorb curriculum app history.
