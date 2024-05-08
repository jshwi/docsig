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
    ...     print("Hello from a function")
    ...     print(argument)
    ...
    ...     def my_external_function(argument: int = 42) -> int:
    ...         print("Hello from an external function")
    ...         print(argument)
    ...         return argument + 42
    ...
    ...     return argument + 1
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_nested=True, no_ansi=True)
    19 in my_function.my_external_function
        E113: function is missing a docstring (function-doc-missing)
    1
