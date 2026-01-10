SIG202: params-do-not-exist
===========================

Includes parameters that do not exist

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a: Description of a.
    ...     :param b: Description of b.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG202: includes parameters that do not exist (params-do-not-exist)
    1
