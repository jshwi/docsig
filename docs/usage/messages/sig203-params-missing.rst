SIG203: params-missing
======================

Parameters missing

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2) -> None:
    ...     """Function summary.
    ...
    ...     :param param1: Missing param2 from docstring.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG203: parameters missing (params-missing)
    1

.. code-block:: python

    >>> string = '''
    ... def function(first, second, third, fourth) -> None:
    ...     """Function summary.
    ...
    ...     :param second: Second param.
    ...     :param third: Third param.
    ...     :param fourth: Fourth param.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG203: parameters missing (params-missing)
    1

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2, param3, param4) -> None:
    ...     """Function summary.
    ...
    ...     :param param2: Second param.
    ...     :param param3: Third param.
    ...     :param param4: Fourth param.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG203: parameters missing (params-missing)
    1
