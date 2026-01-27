SIG503: return-missing
======================

Return missing from docstring

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a) -> int:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG503: return missing from docstring (return-missing)
    1

.. error::

    A return won't be recognised with the following syntax

.. code-block:: python

    >>> string = '''
    ... def function(a) -> int:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     :param return: Return value.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG202: includes parameters that do not exist (params-do-not-exist)
        SIG503: return missing from docstring (return-missing)
    1

.. note::

    Return mentioned in function or parameter description won't result in a hint

.. code-block:: python

    >>> string = '''
    ... def function(a) -> int:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG503: return missing from docstring (return-missing)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> int:
    ...     """Docstring summary.
    ...
    ...     This does return something.
    ...
    ...     :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG503: return missing from docstring (return-missing)
    1

.. note::

    A hint will be displayed if it looks as though a return document was
    attempted

.. code-block:: python

    >>> string = '''
    ... def function(a) -> int:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     :return Return description.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG503: return missing from docstring (return-missing)
        hint: it is possible a syntax error could be causing this
    1
