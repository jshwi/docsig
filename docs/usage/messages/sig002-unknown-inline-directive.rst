SIG002: unknown-inline-directive
================================

Unknown inline comment directive '{directive}'

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param) -> None:  # docsig: ena
    ...     """Function summary.
    ...
    ...     :param param: Description of param.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG002: unknown inline comment directive 'ena' (unknown-inline-directive)
    1
