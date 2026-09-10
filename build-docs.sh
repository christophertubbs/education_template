#!/usr/bin/env bash
set -euo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python_bin="${PYTHON_BIN:-python}"
builder="${1:-html}"
build_root="${2:-${repository_root}/docs/_build}"
source_root="${repository_root}/docs/sphinx"

if ! "${python_bin}" -c 'import sphinx' >/dev/null 2>&1; then
    echo "Sphinx is not installed for ${python_bin}." >&2
    echo "Install it with: ${python_bin} -m pip install -e '${repository_root}[docs]'" >&2
    exit 2
fi

exec "${python_bin}" -m sphinx \
    -M "${builder}" \
    "${source_root}" \
    "${build_root}" \
    -W \
    --keep-going
