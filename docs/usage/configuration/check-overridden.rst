Check overridden
================

check overridden methods

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... class Parent:
    ...     def method(self) -> None:
    ...         """Docstring summary."""
    ...
    ... class Child(Parent):
    ...     def method(self) -> None:
    ...         pass
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_overridden=True, no_ansi=True)
    7 in Child.method
        SIG101: function is missing a docstring (function-doc-missing)
    1
