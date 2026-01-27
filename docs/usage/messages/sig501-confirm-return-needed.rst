SIG501: confirm-return-needed
=============================

Cannot determine whether a return statement should exist or not

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function():
    ...     """Docstring summary."""
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG501: cannot determine whether a return statement should exist (confirm-return-needed)
        hint: annotate type to indicate whether return documentation needed
    1

.. hint::

    This check requires that you annotate your function. If you don't type your code, this check can be disabled.

.. code-block:: python

    >>> string = '''
    ... def function():
    ...     """Docstring summary."""
    ... '''

.. code-block:: python

    >>> docsig(string=string, ignore_typechecker=True, no_ansi=True)
    0
