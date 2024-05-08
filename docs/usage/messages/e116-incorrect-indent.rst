E116: incorrect-indent
======================

Param not indented correctly

.. code-block:: python

    >>> from docsig import docsig

.. todo::

    | This is buggy as it only works when a description line is correct
    | If description is also incorrect then this doesn't work, so it's measured against the description and probably shouldn't be

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

.. todo::
    | Should see:
    | 2 in function
    |     E116: param not indented correctly (incorrect-indent)
    | 1

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
    0

.. todo::
    | Should see:
    | 2 in function
    |     E116: param not indented correctly (incorrect-indent)
    | 1

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
    0
