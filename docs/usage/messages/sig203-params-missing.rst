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
    ...     :param param1: Description of param1.
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
    ...     :param second: Description of second.
    ...     :param third: Description of third.
    ...     :param fourth: Description of fourth.
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
    ...     :param param2: Description of param2.
    ...     :param param3: Description of param3.
    ...     :param param4: Description of param4.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG203: parameters missing (params-missing)
    1
