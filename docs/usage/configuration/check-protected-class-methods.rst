Check protected class methods
=============================

check public methods belonging to protected classes

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... class _Klass:
    ...     @property
    ...     def prop(self, param1) -> str:
    ...         """This is documented."""
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_protected_class_methods=True, no_ansi=True)
    3 in _Klass.prop
        E103: parameters missing (params-missing)
    1
