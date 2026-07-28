#!/bin/bash
# use this instead of `$ uv version --short` as the version may be
# needed before uv is installed
set -u
grep -m1 -E '^version *= *' "${1}" |
  sed -E 's/.*= *"?([^"]*)"?/\1/'
