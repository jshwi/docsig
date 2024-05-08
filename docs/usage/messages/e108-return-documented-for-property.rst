E108: return-documented-for-property
====================================

Return statement documented for property

.. code-block:: python

    >>> from docsig import docsig


.. code-block:: python

    >>> string = '''
    ... class Klass:
    ...     @property
    ...     def function() -> int:
    ...         """Return an integer.
    ...
    ...         :return: An integer.
    ...         """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    3 in Klass.function
        E108: return statement documented for property (return-documented-for-property)
        hint: documentation is sufficient as a getter is the value returned
    1

.. hint::

    A hint will be displayed as to why this check is implemented, but this check can disabled


.. code-block:: python

    >>> string = '''
    ... class Klass:
    ...     @property
    ...     def function() -> int:
    ...         """Return an integer.
    ...
    ...         :return: An integer.
    ...         """
    ... '''

.. code-block:: python

    >>> docsig(string=string, check_property_returns=True, no_ansi=True)
    0
