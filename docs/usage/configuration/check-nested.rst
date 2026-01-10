Check nested
============

check nested functions and classes

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a) -> int:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     :return: Return description.
    ...     """
    ...     def nested_function(a) -> int:
    ...         pass
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_nested=True, no_ansi=True)
    8 in function.nested_function
        SIG101: function is missing a docstring (function-doc-missing)
    1
