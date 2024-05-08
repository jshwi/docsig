E112: spelling-error
====================

Spelling error found in documented parameter

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param pram: Misspelled.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E112: spelling error found in documented parameter (spelling-error)
    1
