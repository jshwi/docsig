#!/bin/bash
grep -E '^version = ' pyproject.toml |
  sed 's/.*= *"\([^"]*\)".*/\1/' 2>/dev/null
