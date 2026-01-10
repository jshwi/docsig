SIG401: incorrect-indent
========================

Param not indented correctly

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Docstring summary.
    ...
    ...     Function description.
    ...
    ...      :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG401: param not indented correctly (incorrect-indent)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Docstring summary.
    ...
    ...      :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG401: param not indented correctly (incorrect-indent)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Docstring summary.
    ...
    ...      Function description also indented one space too many.
    ...
    ...      :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG401: param not indented correctly (incorrect-indent)
    1
