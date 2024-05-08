E101: params-out-of-order
=========================

Parameters out of order

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2) -> None:
    ...     """Function summary.
    ...
    ...     :param param2: This should be param1.
    ...     :param param1: This should be param2.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E101: parameters out of order (params-out-of-order)
    1
