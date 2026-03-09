SIG006: unknown-module-directive-flag
=====================================

Unknown module comment option for {directive} '{option}'

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... # docsig: enable-nexto=SIG204
    ... def function(a) -> None:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    3 in function
        SIG006: unknown module comment flag for enable 'nexto' (unknown-module-directive-flag)
    1
