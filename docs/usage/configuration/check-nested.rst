Check nested
============

check nested functions and classes

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def my_function(argument: int = 42) -> int:
    ...     """
    ...     Function that prints a message and returns the argument + 1
    ...
    ...     Parameters
    ...     ----------
    ...     argument : int, optional
    ...         The input argument, by default 42
    ...
    ...     Returns
    ...     -------
    ...     int
    ...         The input argument + 1
    ...     """
    ...     def my_external_function(argument: int = 42) -> int:
    ...         pass
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_nested=True, no_ansi=True)
    16 in my_function.my_external_function
        SIG101: function is missing a docstring (function-doc-missing)
    1
