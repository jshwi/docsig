SIG305: description-not-capitalized
===================================

Description does not begin with a capital letter

This needs to be manually enabled

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a: description of param.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, enforce_capitalization=True, no_ansi=True)
    2 in function
        SIG305: description does not begin with a capital letter (description-not-capitalized)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a: Description of param. and another sentence.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, enforce_capitalization=True, no_ansi=True)
    2 in function
        SIG305: description does not begin with a capital letter (description-not-capitalized)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a: Describing a pyproject.toml where toml is the type.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, enforce_capitalization=True, no_ansi=True)
    0

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a: Description of param e.g. not a new sentence.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, enforce_capitalization=True, no_ansi=True)
    0
