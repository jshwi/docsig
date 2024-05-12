E110: param-not-equal-to-arg
============================

Documented parameter not equal to its respective argument

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param arg: This should be param.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E110: documented parameter not equal to its respective argument (param-not-equal-to-arg)
    1

.. code-block:: python

    >>> string = '''
    ... def function(param1) -> None:
    ...     """Function summary.
    ...
    ...     :param arg1: This should be param1.
    ...     :return: None.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E104: return statement documented for None (return-documented-for-none)
        E110: documented parameter not equal to its respective argument (param-not-equal-to-arg)
    1

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2) -> None:
    ...     """Function summary.
    ...
    ...     :param arg1: This should be param1.
    ...     :param param2: Documentation for param2.
    ...     :param param2: Documentation for param2.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E106: duplicate parameters found (duplicate-params-found)
        E110: documented parameter not equal to its respective argument (param-not-equal-to-arg)
    1
