Checking a class docstring is not enabled by default, as there are two mutually exclusive choices to choose from.

This check will either check the documentation of ``__init__``, or check documentation of ``__init__`` under the class docstring, and not under ``__init__`` itself

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... class Klass:
    ...     def __init__(self, a, b) -> None:
    ...         """Docstring summary.
    ...
    ...         :param a: Description of a.
    ...         :param b: Description of b.
    ...         :param c: Description of c.
    ...         """
    ... '''
    >>> docsig(string=string, check_class_constructor=True, no_ansi=True)
    3 in Klass.__init__
        SIG202: includes parameters that do not exist (params-do-not-exist)
    1

.. code-block:: python

    >>> string = '''
    ... class Klass:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     :param b: Description of b.
    ...     :param c: Description of c.
    ...     """
    ...     def __init__(self, a, b) -> None:
    ...         pass
    ... '''
    >>> docsig(string=string, check_class=True, no_ansi=True)
    9 in Klass.__init__
        SIG202: includes parameters that do not exist (params-do-not-exist)
    1

Checking class docstrings can be permanently enabled in the pyproject.toml file

.. code-block:: toml

    [tool.docsig]
    check-class-constructor = true

Or

.. code-block:: toml

    [tool.docsig]
    check-class = true
