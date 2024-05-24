SIG101: function-doc-missing
============================

Function is missing a docstring

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function() -> None:
    ...     pass
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG101: function is missing a docstring (function-doc-missing)
    1
