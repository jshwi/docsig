#!/bin/bash
set -euo pipefail
src="${1}"
dst="${2}"
rm -rf "${dst}"
git clone --no-hardlinks "${src}" "${dst}" >/dev/null 2>&1
cd "${dst}"
unset VIRTUAL_ENV
unset POETRY_ACTIVE
hash -r 2>/dev/null || true
make build
