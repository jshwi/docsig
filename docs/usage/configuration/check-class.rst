Check class
===========

check class docstrings

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... class Klass:
    ...     """Info about class.
    ...
    ...     :param b: Description of b.
    ...     :param a: Description of a.
    ...     """
    ...
    ...     def __init__(self, a, b) -> None:
    ...         pass
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_class=True, no_ansi=True)
    9 in Klass.__init__
        SIG402: parameters out of order (params-out-of-order)
    1
