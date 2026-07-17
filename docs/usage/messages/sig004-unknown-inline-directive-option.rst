SIG004: unknown-inline-directive-option
=======================================

Unknown inline comment option for {directive} '{option}'

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param1) -> None:  # docsig: enable=EIEIO
    ...     """Docstring summary.
    ...
    ...     :param param: Description of param.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG004: unknown inline comment option for enable 'EIEIO' (unknown-inline-directive-option)
        SIG403: spelling error found in documented parameter (spelling-error)
    1

Using a valid rule as the option resolves the check

.. code-block:: python

    >>> string = '''
    ... def function(param1) -> None:  # docsig: enable=SIG403
    ...     """Docstring summary.
    ...
    ...     :param param1: Description of param1.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0
