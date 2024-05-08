E203: unknown-module-directive-option
=====================================

Unknown module comment option for {directive} '{option}'

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... # docsig: enable=EIEIO
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param param: Description of param1.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    3 in function
        E203: unknown module comment option for enable 'EIEIO' (unknown-module-directive-option)
    1
