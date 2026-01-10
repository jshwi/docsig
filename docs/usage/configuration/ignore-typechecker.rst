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
    ...     :return: Return description.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG502: return statement documented for None (return-documented-for-none)
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
        SIG503: return missing from docstring (return-missing)
    1

.. code-block:: python

    >>> docsig(string=string, ignore_typechecker=True, no_ansi=True)
    0

.. code-block:: python

    >>> string = '''
    ... def function(*_, **__):
    ...     """Proper docstring.
    ...
    ...     :return: Return description.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG501: cannot determine whether a return statement should exist (confirm-return-needed)
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
    ...         :return: Return description.
    ...         """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    3 in Klass.function
        SIG505: return statement documented for property (return-documented-for-property)
        hint: documentation is sufficient as a getter is the value returned
    1

.. code-block:: python

    >>> docsig(string=string, ignore_typechecker=True, no_ansi=True)
    0
