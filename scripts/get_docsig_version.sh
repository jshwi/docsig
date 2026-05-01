#!/bin/bash
# use this instead of `$ poetry version --short` as the version may be
# needed before poetry is installed
grep -E '^version = ' pyproject.toml |
  sed 's/.*= *"\([^"]*\)".*/\1/' 2>/dev/null
