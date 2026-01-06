SIG303: param-incorrectly-documented
====================================

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
        SIG303: parameter appears to be incorrectly documented (param-incorrectly-documented)
    1

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
        SIG201: duplicate parameters found (duplicate-params-found)
        SIG303: parameter appears to be incorrectly documented (param-incorrectly-documented)
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
        SIG303: parameter appears to be incorrectly documented (param-incorrectly-documented)
        SIG402: parameters out of order (params-out-of-order)
    1

But not if it is for a parameter that does not exist

.. code-block:: python

    >>> string = '''
    ... def function(param1) -> None:
    ...     """Function summary.
    ...
    ...     :param param1: Description of param1.
    ...     :param param2: Description of param2.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG202: includes parameters that do not exist (params-do-not-exist)
    1

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2) -> None:
    ...     """Function summary.
    ...
    ...     :param param2: Description of param2.
    ...     :param param1: Description of param1.
    ...     :param param3: Description of param3.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG202: includes parameters that do not exist (params-do-not-exist)
        SIG402: parameters out of order (params-out-of-order)
    1
