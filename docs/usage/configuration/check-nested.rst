Check nested
============

check nested functions and classes

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def my_function(a: int = 42) -> int:
    ...     """
    ...     Function that prints a message and returns the argument + 1
    ...
    ...     :param a: Description of a.
    ...     :return: Return description.
    ...     """
    ...     def my_external_function(argument: int = 42) -> int:
    ...         pass
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_nested=True, no_ansi=True)
    9 in my_function.my_external_function
        SIG101: function is missing a docstring (function-doc-missing)
    1
