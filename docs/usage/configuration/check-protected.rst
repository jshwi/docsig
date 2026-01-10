Check protected
===============

check protected functions and classes

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... class Class:
    ...     def _protected(self, a) -> None:
    ...         """Docstring summary."""
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_protected=True, no_ansi=True)
    3 in Class._protected
        SIG203: parameters missing (params-missing)
    1
