#!/bin/bash
# use this instead of `$ poetry version --short` as the version may be
# needed before poetry is installed
grep -E '^version = ' "${1}" |
  sed 's/.*= *"\([^"]*\)".*/\1/' 2>/dev/null
