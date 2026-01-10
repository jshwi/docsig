SIG203: params-missing
======================

Parameters missing

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a, b) -> None:
    ...     """Function summary.
    ...
    ...     :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG203: parameters missing (params-missing)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a, b, c, d) -> None:
    ...     """Function summary.
    ...
    ...     :param b: Description of b.
    ...     :param c: Description of c.
    ...     :param d: Description of d.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG203: parameters missing (params-missing)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a, b, c, d) -> None:
    ...     """Function summary.
    ...
    ...     :param b: Description of b.
    ...     :param c: Description of c.
    ...     :param d: Description of d.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG203: parameters missing (params-missing)
    1
