Ignore no params
================

ignore docstrings where parameters are not documented

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2, *args) -> None:
    ...     """Proper docstring."""
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG203: parameters missing (params-missing)
    1

.. code-block:: python

    >>> docsig(string=string, ignore_no_params=True, no_ansi=True)
    0
