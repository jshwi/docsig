Ignore kwargs
=============

ignore kwargs prefixed with two asterisks

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a, b, **kwargs) -> None:
    ...     """Proper docstring.
    ...
    ...     :param a: Description of a.
    ...     :param b: Description of b.
    ...     :param kwargs: Description of kwargs.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, ignore_kwargs=True, no_ansi=True)
    2 in function
        SIG202: includes parameters that do not exist (params-do-not-exist)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a, b, **kwargs) -> None:
    ...     """Proper docstring.
    ...
    ...     :param a: Description of a.
    ...     :param b: Description of b.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG203: parameters missing (params-missing)
    1

.. code-block:: python

    >>> docsig(string=string, ignore_kwargs=True, no_ansi=True)
    0

.. code-block:: python

    >>> string = '''
    ... def function(a, **kwargs) -> None:
    ...     """Proper docstring.
    ...
    ...     :param a: Description of a.
    ...     :key kwarg1: Description of kwarg1.
    ...     :keyword kwarg2: Description of kwarg2.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, ignore_kwargs=True, no_ansi=True)
    2 in function
        SIG202: includes parameters that do not exist (params-do-not-exist)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a, b, **kwargs) -> None:
    ...     """Proper docstring.
    ...
    ...     :param a: Description of a.
    ...     :param b: Description of b.
    ...     :param **kwargs: Description of **kwargs.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, ignore_kwargs=True, no_ansi=True)
    2 in function
        SIG202: includes parameters that do not exist (params-do-not-exist)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a, b, **kwargs) -> None:
    ...     """Proper docstring.
    ...
    ...     :param a: Description of a.
    ...     :param b: Description of b.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG203: parameters missing (params-missing)
    1

.. code-block:: python

    >>> docsig(string=string, ignore_kwargs=True, no_ansi=True)
    0
