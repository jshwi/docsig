Versioning
==========

``docsig`` follows `semantic versioning <https://semver.org/>`_

From v1.0.0 the public interface is stable: anything that would break it will
only land in a new major version. Most releases are patches; minor releases
are less common, and what they may change is documented here so version pins
can be chosen with confidence

Public interface
----------------

The following make up the public interface

- The commandline interface: options, their semantics, and exit statuses
- The pyproject.toml ``[tool.docsig]`` configuration keys
- The Python API: ``docsig``, ``main``, and the ``messages`` module
- The flake8 plugin's ``--sig-`` prefixed options
- Message codes: SIG numbers, their symbolic names, and their meanings

Anything prefixed with an underscore is internal, including the environment
variable and json format the editor plugins use to communicate with
``docsig``, and may change in any release

Release types
-------------

- Patch releases fix bugs, with output changing only insofar as a fix
  demands it
- Minor releases may add new options, add new checks, promote previously
  warned checks to errors, and extend the default exclusions
- Major releases are reserved for changes that break the public interface

Pin to a minor version for output that only changes when a bug is fixed, or
to a major version to also receive new checks as they stabilise

New checks
----------

New checks are introduced in two stages, so a minor upgrade never fails a
previously passing run without warning first

A new check begins life as a warning: it is prefixed with ``W``, announces
that it will error in a future version, and does not affect the exit status.
In a later minor release, at least one minor version after the warning first
shipped, the check is promoted to a regular violation and begins to affect
the exit status

To opt out of a check, at either stage, disable it

.. code-block:: toml

    [tool.docsig]
    disable = ["SIG101"]

Configuration precedence
------------------------

Configuration merges additively across its sources: built-in defaults,
pyproject.toml, then the commandline. List options combine, so a commandline
``--disable`` adds to any rules already disabled in pyproject.toml, and
``--exclude`` patterns join the default exclusions as well as any patterns
configured in pyproject.toml

The default exclusions may gain new entries in minor releases as new tool
cache directories become conventional
