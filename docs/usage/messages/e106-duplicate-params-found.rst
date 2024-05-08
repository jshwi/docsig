E106: duplicate-params-found
============================

Duplicate parameters found

.. code-block:: python

    >>> from docsig import docsig

.. todo::

    | E101 occurs, wrongly, when there are parameters that do not exist
    | E102 is occurring because of the duplicate parameter
    | Should see:
    | 2 in function
    |     E106: duplicate parameters found (duplicate-params-found)
    | 1

.. code-block:: python

    >>> string = '''
    ... def function(param1) -> None:
    ...     """Function summary.
    ...
    ...     :param param1: Description of param1.
    ...     :param param1: Description of param1.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E101: parameters out of order (params-out-of-order)
        E102: includes parameters that do not exist (params-do-not-exist)
        E106: duplicate parameters found (duplicate-params-found)
    1

.. todo::

    | Should see:
    | 2 in function
    |     E106: duplicate parameters found (duplicate-params-found)
    | 1

.. code-block:: python

    >>> string = '''
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param param: Description of param.
    ...     :param param: Another description of param.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E101: parameters out of order (params-out-of-order)
        E102: includes parameters that do not exist (params-do-not-exist)
        E106: duplicate parameters found (duplicate-params-found)
    1

.. todo::

    | Should see:
    | 2 in function
    |     E106: duplicate parameters found (duplicate-params-found)
    | 1

.. code-block:: python

    >>> string = '''
    ... def function(param1) -> None:
    ...     """Function summary.
    ...
    ...     :param param1: Description of param1.
    ...     :param param1: Another description of param1.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E101: parameters out of order (params-out-of-order)
        E102: includes parameters that do not exist (params-do-not-exist)
        E106: duplicate parameters found (duplicate-params-found)
    1
