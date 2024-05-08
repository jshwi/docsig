E107: param-incorrectly-documented
==================================

Parameter appears to be incorrectly documented

.. code-block:: python

    >>> from docsig import docsig

This will be raised if it looks as though an existing parameter documentation was attempted

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2) -> None:
    ...     """Function summary.
    ...
    ...     :param param1: Description of param1.
    ...     :param: This is considered param3, but it is not named.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E107: parameter appears to be incorrectly documented (param-incorrectly-documented)
    1

.. todo::

    | Should be:
    | 2 in function
    |     E106: duplicate parameters found (duplicate-params-found)
    |     E107: parameter appears to be incorrectly documented (param-incorrectly-documented)
    | 1

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2, param3) -> None:
    ...     """Function summary.
    ...
    ...     :param param1: Description of param1.
    ...     :param param1: Description of param1.
    ...     :param param2: Description of param2.
    ...     :param: This is considered param3, but it is not named.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E102: includes parameters that do not exist (params-do-not-exist)
        E106: duplicate parameters found (duplicate-params-found)
        E107: parameter appears to be incorrectly documented (param-incorrectly-documented)
    1

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2, param3) -> None:
    ...     """Function summary.
    ...
    ...     :param param2: Description of param2.
    ...     :param param1: Description of param1.
    ...     :param: This is considered param3, but it is not named.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E101: parameters out of order (params-out-of-order)
        E107: parameter appears to be incorrectly documented (param-incorrectly-documented)
    1

But not if it is for a parameter that does not exist

.. todo::

    | Should be:
    | 2 in function
    |     E102: includes parameters that do not exist (params-do-not-exist)
    | 1

.. code-block:: python

    >>> string = '''
    ... def function(param1) -> None:
    ...     """Function summary.
    ...
    ...     :param param1: Description of param1.
    ...     :param: This is considered param3, but it is not named.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E102: includes parameters that do not exist (params-do-not-exist)
        E107: parameter appears to be incorrectly documented (param-incorrectly-documented)
    1

.. todo::

    | Should be:
    |     E101: parameters out of order (params-out-of-order)
    |     E102: includes parameters that do not exist (params-do-not-exist)
    | 1

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2) -> None:
    ...     """Function summary.
    ...
    ...     :param param2: Description of param2.
    ...     :param param1: Description of param1.
    ...     :param: This is an additional param and should be E102.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E101: parameters out of order (params-out-of-order)
        E102: includes parameters that do not exist (params-do-not-exist)
        E107: parameter appears to be incorrectly documented (param-incorrectly-documented)
    1
