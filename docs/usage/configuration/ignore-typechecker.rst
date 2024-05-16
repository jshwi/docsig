Ignore typechecker
==================

ignore checking return values

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function() -> None:
    ...     """Proper docstring.
    ...
    ...     :return: Returncode.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E104: return statement documented for None (return-documented-for-none)
    1

.. code-block:: python

    >>> docsig(string=string, ignore_typechecker=True, no_ansi=True)
    0

.. code-block:: python

    >>> string = '''
    ... def function(*_, **__) -> int:
    ...     """Proper docstring."""
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E105: return missing from docstring (return-missing)
    1

.. code-block:: python

    >>> docsig(string=string, ignore_typechecker=True, no_ansi=True)
    0

.. code-block:: python

    >>> string = '''
    ... def function(*_, **__):
    ...     """Proper docstring.
    ...
    ...     Returns
    ...     -------
    ...         int
    ...             Returncode.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E109: cannot determine whether a return statement should exist (confirm-return-needed)
        hint: annotate type to indicate whether return documentation needed
    1

.. code-block:: python

    >>> docsig(string=string, ignore_typechecker=True, no_ansi=True)
    0

.. code-block:: python

    >>> string = '''
    ... class Klass:
    ...     @property
    ...     def function() -> int:
    ...         """Proper docstring.
    ...
    ...         Returns
    ...         -------
    ...         int
    ...         Returncode.
    ...         """
    ...
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    3 in Klass.function
        E108: return statement documented for property (return-documented-for-property)
        hint: documentation is sufficient as a getter is the value returned
    1

.. code-block:: python

    >>> docsig(string=string, ignore_typechecker=True, no_ansi=True)
    0
