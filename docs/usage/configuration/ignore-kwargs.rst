Ignore kwargs
=============

ignore kwargs prefixed with two asterisks

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2, **kwargs) -> None:
    ...     """Proper docstring.
    ...
    ...     :param param1: Pass.
    ...     :param param2: Pass.
    ...     :param kwargs: Pass
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, ignore_kwargs=True, no_ansi=True)
    2 in function
        E102: includes parameters that do not exist (params-do-not-exist)
    1

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2, **kwargs) -> None:
    ...     """Proper docstring.
    ...
    ...     :param param1: Pass.
    ...     :param param2: Pass.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E103: parameters missing (params-missing)
    1

.. code-block:: python

    >>> docsig(string=string, ignore_kwargs=True, no_ansi=True)
    0

.. code-block:: python

    >>> string = '''
    ... def function(param1, **kwargs) -> None:
    ...     """Proper docstring.
    ...
    ...     :param param1: Passes
    ...     :key kwarg1: Pass
    ...     :keyword kwarg2: Pass
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, ignore_kwargs=True, no_ansi=True)
    2 in function
        E102: includes parameters that do not exist (params-do-not-exist)
    1

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2, **kwargs) -> None:
    ...     """Proper docstring.
    ...
    ...     Parameters
    ...     ----------
    ...         param1 : int
    ...             Pass.
    ...         param2 : int
    ...             Pass.
    ...         **kwargs : int
    ...             Pass
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, ignore_kwargs=True, no_ansi=True)
    2 in function
        E102: includes parameters that do not exist (params-do-not-exist)
    1

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2, **kwargs) -> None:
    ...     """Proper docstring.
    ...
    ...     Parameters
    ...     ----------
    ...         param1 : int
    ...             Pass.
    ...         param2 : int
    ...             Pass.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E103: parameters missing (params-missing)
    1

.. code-block:: python

    >>> docsig(string=string, ignore_kwargs=True, no_ansi=True)
    0
