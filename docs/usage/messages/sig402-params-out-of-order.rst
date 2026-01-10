SIG402: params-out-of-order
===========================

Parameters out of order

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2) -> None:
    ...     """Function summary.
    ...
    ...     :param param2: Description of param2.
    ...     :param param1: Description of param1.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG402: parameters out of order (params-out-of-order)
    1
