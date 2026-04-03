SIG007: unknown-inline-directive-flag
=====================================

Unknown inline comment flag for {directive} '{flag}'

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param1) -> None:  # docsig: disable-nexto=SIG403
    ...     """Docstring summary.
    ...
    ...     :param param: Description of param.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG007: unknown inline comment flag for disable 'nexto' (unknown-inline-directive-flag)
    1
