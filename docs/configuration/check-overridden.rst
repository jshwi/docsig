Check overridden
================

check overridden methods

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... class Parent:
    ...     def method(self) -> None:
    ...         """This is documented."""
    ...         self._set: _t.Set[T] = set()
    ...
    ... class Child(Parent):
    ...     def method(self) -> None:
    ...         self._set: _t.Set[T] = set()
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_overridden=True, no_ansi=True)
    8 in Child.method
        E113: function is missing a docstring (function-doc-missing)
    1
