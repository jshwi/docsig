SIG502: return-documented-for-none
==================================

Return statement documented for none

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function() -> None:
    ...     """Function summary.
    ...
    ...     :return: Return description.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG502: return statement documented for None (return-documented-for-none)
    1
