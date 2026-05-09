#!/bin/bash
# use this instead of `$ poetry version --short` as the version may be
# needed before poetry is installed
set -u
grep -E '^version *= *' "${1}" |
  sed -E 's/.*= *"?([^"]*)"?/\1/' 2>/dev/null
