SIG003: unknown-module-directive-option
=======================================

Unknown module comment option for {directive} '{option}'

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... # docsig: enable=EIEIO
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    3 in function
        SIG003: unknown module comment option for enable 'EIEIO' (unknown-module-directive-option)
    1
