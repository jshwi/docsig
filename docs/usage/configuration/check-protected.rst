Check protected
===============

check protected functions and classes

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... class Parent:
    ...     def _protected(self, param1) -> None:
    ...         """This is documented."""
    ...         self._set: _t.Set[T] = set()
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_protected=True, no_ansi=True)
    3 in Parent._protected
        SIG203: parameters missing (params-missing)
    1
