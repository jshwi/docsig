E201: unknown-module-directive
==============================

Unknown module comment directive '{directive}'

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... # docsig: ena
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param param: Description of param1.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    3 in function
        E201: unknown module comment directive 'ena' (unknown-module-directive)
    1
