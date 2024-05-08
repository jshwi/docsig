E116: incorrect-indent
======================

Param not indented correctly

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     Function description.
    ...
    ...      :param param: This is indented one space too many.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E116: param not indented correctly (incorrect-indent)
    1

.. code-block:: python

    >>> string = '''
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...      :param param: This is indented one space too many.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E116: param not indented correctly (incorrect-indent)
    1

.. code-block:: python

    >>> string = '''
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...      Function description also indented one space too many.
    ...
    ...      :param param: This is indented one space too many.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E116: param not indented correctly (incorrect-indent)
    1
