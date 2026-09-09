#!/usr/bin/env bash

# Prepare the database and static assets for the current checkout or release.
set -euo pipefail

INSTALL_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"

cd "${INSTALL_ROOT}"

# Migrations establish schema; the explicit reload also applies JSON-only
# curriculum revisions when a product did not need a new migration.
"${PYTHON_BIN}" manage.py migrate --noinput
"${PYTHON_BIN}" manage.py load_curricula
"${PYTHON_BIN}" manage.py collectstatic --noinput
