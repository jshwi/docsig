E106: duplicate-params-found
============================

Duplicate parameters found

.. code-block:: python

    >>> from docsig import docsig

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
        E106: duplicate parameters found (duplicate-params-found)
    1

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
        E106: duplicate parameters found (duplicate-params-found)
    1

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
        E106: duplicate parameters found (duplicate-params-found)
    1
