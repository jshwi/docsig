SIG303: param-incorrectly-documented
====================================

Parameter appears to be incorrectly documented

.. code-block:: python

    >>> from docsig import docsig

This will be raised if it looks as though an existing parameter documentation was attempted

.. code-block:: python

    >>> string = '''
    ... def function(a, b) -> None:
    ...     """Function summary.
    ...
    ...     :param a: Description of a.
    ...     :param: Description of unnamed param.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG303: parameter appears to be incorrectly documented (param-incorrectly-documented)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a, b, c) -> None:
    ...     """Function summary.
    ...
    ...     :param a: Description of a.
    ...     :param a: Description of a.
    ...     :param b: Description of b.
    ...     :param: Description of unnamed param.
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
    ... def function(a, b, c) -> None:
    ...     """Function summary.
    ...
    ...     :param b: Description of b.
    ...     :param a: Description of a.
    ...     :param: Description of unnamed param.
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
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a: Description of a.
    ...     :param b: Description of b.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG202: includes parameters that do not exist (params-do-not-exist)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a, b) -> None:
    ...     """Function summary.
    ...
    ...     :param b: Description of b.
    ...     :param a: Description of a.
    ...     :param c: Description of c.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG202: includes parameters that do not exist (params-do-not-exist)
        SIG402: parameters out of order (params-out-of-order)
    1
