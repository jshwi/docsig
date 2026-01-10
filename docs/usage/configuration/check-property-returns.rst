Check property returns
======================

check property return values

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... class Klass:
    ...     @property
    ...     def prop(self) -> str:
    ...         """Docstring summary."""
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_property_returns=True, no_ansi=True)
    3 in Klass.prop
        SIG503: return missing from docstring (return-missing)
    1
