# Building the Sphinx documentation

The documentation explains every maintained source category under `src/`, the
dependency direction between packages, end-to-end generation and installation,
and the effects of changing each subsystem. Its landing page is
`docs/sphinx/index.rst`.

## Quick build

Use Python 3.11 or newer from the same environment as the project:

```bash
python -m pip install -e '.[docs]'
./build-docs.sh
```

The HTML entry point is `docs/_build/html/index.html`. The script enables
Sphinx's warnings-as-errors mode so broken references and malformed source fail
the build.

## Script options

The first argument selects any installed Sphinx builder. The second argument
overrides the build root:

```bash
./build-docs.sh html
./build-docs.sh linkcheck /tmp/education-docs
PYTHON_BIN=.venv/bin/python ./build-docs.sh
```

The default builder is `html`, the default output root is `docs/_build`, and
`PYTHON_BIN` defaults to `python`. The script does not install dependencies; if
Sphinx is absent it prints the exact installation command and exits.

## Direct Sphinx invocation

The equivalent direct command is:

```bash
python -m sphinx -M html docs/sphinx docs/_build -W --keep-going
```

Sphinx autodoc imports Django models. `docs/sphinx/conf.py` configures an
in-memory minimal Django application, so building documentation neither opens
the project database nor activates local generated products.

## Editing checklist

When behavior under `src/` changes:

1. Update the relevant narrative page and `source-inventory.rst` if files moved.
2. Keep Python module/class/function docstrings accurate; `api.rst` reads them.
3. Run `./build-docs.sh` and inspect the affected HTML page.
4. Run `git diff --check` along with the code checks required by `AGENTS.md`.

Do not edit `docs/_build`; it is disposable generated output.
