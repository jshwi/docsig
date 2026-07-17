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

Documenting parameters in signature order resolves the check

.. code-block:: python

    >>> string = '''
    ... def function(a, b) -> None:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     :param b: Description of b.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0
