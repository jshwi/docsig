SIG403: spelling-error
======================

Spelling error found in documented parameter

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param) -> None:
    ...     """Docstring summary.
    ...
    ...     :param pram: Description of pram.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG403: spelling error found in documented parameter (spelling-error)
    1

.. code-block:: python

    >>> string = '''
    ... def function(param1) -> None:
    ...     """Docstring summary.
    ...
    ...     :param pram1: Description of pram1.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG403: spelling error found in documented parameter (spelling-error)
    1

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2) -> None:
    ...     """Docstring summary.
    ...
    ...     :param pram1: Description of pram1.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG203: parameters missing (params-missing)
        SIG403: spelling error found in documented parameter (spelling-error)
    1
