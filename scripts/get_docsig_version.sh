#!/bin/bash
# use this instead of `$ poetry version --short` as the version may be
# needed before poetry is installed
set -u
grep -m1 -E '^version *= *' "${1}" |
  sed -E 's/.*= *"?([^"]*)"?/\1/'
