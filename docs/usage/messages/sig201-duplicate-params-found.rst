SIG201: duplicate-params-found
==============================

Duplicate parameters found

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a: Description of a.
    ...     :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG201: duplicate parameters found (duplicate-params-found)
    1
