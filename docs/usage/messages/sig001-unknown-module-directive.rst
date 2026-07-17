SIG001: unknown-module-directive
================================

Unknown module comment directive '{directive}'

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... # docsig: ena
    ... def function(a) -> None:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    3 in function
        SIG001: unknown module comment directive 'ena' (unknown-module-directive)
    1

Using a valid directive resolves the check

.. code-block:: python

    >>> string = '''
    ... # docsig: enable
    ... def function(a) -> None:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0
