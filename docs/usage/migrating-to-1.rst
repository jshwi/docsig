Migrating to 1.0
================

v1.0.0 makes the stability promise described in :doc:`versioning` and is
functionally identical to the final 0.x release. The changes below landed in
the 0.x releases leading up to it, so upgrading through the latest 0.x
release is all that migrating requires

``--excludes`` renamed to ``--exclude-glob``
--------------------------------------------

The option takes path glob patterns, while ``-e/--exclude`` takes regular
expressions, and the near-identical names hid that distinction. The short
option ``-E`` is unchanged

.. code-block:: console

    $ docsig . --exclude-glob "docs/*"

The pyproject.toml key and the API keyword follow the new name

.. code-block:: toml

    [tool.docsig]
    exclude-glob = ["docs/*"]

Exclude patterns now combine
----------------------------

Previously an ``exclude`` pattern configured in pyproject.toml silently
replaced one passed on the commandline. Patterns now merge across all
sources: the default exclusions, pyproject.toml, and the commandline.
``-e/--exclude`` can be repeated, and pyproject.toml accepts a single
pattern or a list

.. code-block:: toml

    [tool.docsig]
    exclude = ["docs/conf.py", '.*[\\/]_[a-z]*']

``python -m docsig`` reads configuration
----------------------------------------

Previously ``[tool.docsig]`` was only read when invoked as ``docsig``.
Configuration now loads no matter how the program is invoked

The flake8 plugin is configured through flake8
----------------------------------------------

The documentation previously stated that pyproject.toml was the plugin's
base configuration. It never was, and the plugin now makes no attempt to
read it. Configure the plugin with its ``--sig-`` prefixed options through
`flake8's configuration
<https://flake8.pycqa.org/en/latest/user/configuration.html#configuration-locations>`_

``docsig()`` message arguments are typed as strings
---------------------------------------------------

The ``disable`` and ``target`` parameters were annotated with an internal
type even though the documented calling convention has always been a list of
codes or symbolic names, which type checkers flagged. The annotations are
now ``list[str] | None``, so the documented form checks cleanly

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Docstring summary.
    ...
    ...     :param b: Description of b.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(
    ...     string=string,
    ...     disable=["SIG203", "param-not-equal-to-arg"],
    ...     no_ansi=True,
    ... )
    0
