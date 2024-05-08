Check dunders
=============

check dunder methods

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... class Klass:
    ...     def __get__(self, param1, param2) -> None:
    ...         """Info about class.
    ...
    ...         :param param2: Info about param2.
    ...         :param param1: Info about param1.
    ...         """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_dunders=True, no_ansi=True)
    3 in Klass.__get__
        E101: parameters out of order (params-out-of-order)
    1
