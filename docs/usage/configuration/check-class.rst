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
    ...     :param param2: Info about param2.
    ...     :param param1: Info about param1.
    ...     """
    ...
    ...     def __init__(self, param1, param2) -> None:
    ...         pass
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_class=True, no_ansi=True)
    9 in Klass.__init__
        E101: parameters out of order (params-out-of-order)
    1
