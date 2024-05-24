SIG404: param-not-equal-to-arg
==============================

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
        SIG404: documented parameter not equal to its respective argument (param-not-equal-to-arg)
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
        SIG404: documented parameter not equal to its respective argument (param-not-equal-to-arg)
        SIG502: return statement documented for None (return-documented-for-none)
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
        SIG201: duplicate parameters found (duplicate-params-found)
        SIG404: documented parameter not equal to its respective argument (param-not-equal-to-arg)
    1
