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

## Add Curriculum Apps from GitHub

Run these commands from the directory containing `manage.py`. Clone each
repository into a directory whose name matches its Django package. The explicit
destination names below are important: the GitHub repository is named
`lstm_onboarding`, but its importable Django package is named `lstm`; the same
rule applies to `cfe_onboarding` and `cfe`.

```bash
git clone https://github.com/christophertubbs/lstm_onboarding.git lstm
git clone https://github.com/christophertubbs/cfe_onboarding.git cfe
python -m pip install -e ./lstm -e ./cfe
```

Each Curriculum App must be a Git checkout directly under this host, contain
`generation_metadata.json`, and provide `src/<package-name>/urls.py`. The host
uses that layout to discover installed curricula. Do not clone either project
inside `standalone/`.

Apply the migrations for all installed apps:

```bash
python manage.py migrate
```

Both apps provide a management command named `load_curriculum`. Because Django
can resolve only one command with a given name, load each package explicitly
when both are installed:

```bash
python manage.py shell -c "from lstm.services import load_packaged_curriculum; print(load_packaged_curriculum())"
python manage.py shell -c "from cfe.services import load_packaged_curriculum; print(load_packaged_curriculum())"
```

Confirm the integration and launch the host:

```bash
python manage.py check
./launch.sh
```

The curricula are then mounted at `/lstm/` and `/cfe/`. Restart the host after
adding or removing a Curriculum App so Django rebuilds its application and URL
registries.

To update an existing checkout, pull it, refresh the editable installation,
apply migrations, and run that package's loader again. The loader preserves
records marked as human-modified.

```bash
git -C lstm pull --ff-only
python -m pip install -e ./lstm
python manage.py migrate
python manage.py shell -c "from lstm.services import load_packaged_curriculum; print(load_packaged_curriculum())"
```

For another onboarding repository, inspect its `generation_metadata.json` for
`generated_package_name`, use that value as the clone destination, and follow
the same installation and loading sequence.
