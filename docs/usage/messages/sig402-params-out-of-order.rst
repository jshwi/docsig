SIG402: params-out-of-order
===========================

Parameters out of order

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a, b) -> None:
    ...     """Docstring summary.
    ...
    ...     :param b: Description of b.
    ...     :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG402: parameters out of order (params-out-of-order)
    1
