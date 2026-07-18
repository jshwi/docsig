---
orphan: true
---

# Logbook

Development notes and decisions that don't belong anywhere official yet.

## 2026-07-18 — flake8 plugin: delete the dead pyproject merge

Remove the never-functional `[tool.docsig]` lookup from
`Flake8.parse_options` (`docsig/plugin/_flake8.py`) and correct the flake8
doc sentence claiming "the pyproject.toml config will still be the base
config". Flake8 config then comes solely from flake8's native mechanisms:
`--sig-*` flags and ini files (`.flake8`/`tox.ini`/`setup.cfg`) via
`parse_from_config=True`.

Why:

- The lookup calls `get_config(__package__)` where `__package__` is
  `"docsig.plugin"`, so it reads `tool."docsig.plugin"` — a section nobody
  has. Verified empirically: it returns `{}` while `[tool.docsig]` is
  populated. It has never worked; nobody can be relying on it (issue
  tracker: zero).
- flake8 itself deliberately refuses pyproject.toml support; ini-only is
  the ecosystem norm and what `.flake8`/`tox.ini` users expect.
- Even if the key were fixed, only boolean flags plus `verbose` are
  consumed by `_build_config`, so `disable`/`exclude`/etc. would merge in
  and be silently ignored — an honest fix means full config support plus a
  frozen three-way precedence (pyproject → ini → CLI). Overengineering.
- Reversibility: adding a pyproject layer later is additive (a minor
  release); freezing it at 1.0 and regretting it forces 2.0. Deleting
  keeps the door open.
