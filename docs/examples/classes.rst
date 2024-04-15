Classes
*******
Checking a class docstring is not enabled by default, as there are two mutually exclusive choices to choose from.

This check will either check the documentation of ``__init__``, or check documentation of ``__init__`` under the class docstring, and not under ``__init__`` itself

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = """
    ... class Klass:
    ...     def __init__(self, param1, param2) -> None:
    ...         '''
    ...
    ...         :param param1: About param1.
    ...         :param param2: About param2.
    ...         :param param3: About param3.
    ...         '''
    ... """
    >>> docsig(string=string, check_class_constructor=True, no_ansi=True)
    3 in Klass
    ----------
    class Klass:
        """
        :param param1: ✓
        :param param2: ✓
        :param param3: ✖
        """
    <BLANKLINE>
        def __init__(✓param1, ✓param2, ✖None) -> ✓None:
    <BLANKLINE>
    E102: includes parameters that do not exist (params-do-not-exist)
    <BLANKLINE>
    1

.. code-block:: python

    >>> string = """
    ... class Klass:
    ...     '''
    ...
    ...     :param param1: About param1.
    ...     :param param2: About param2.
    ...     :param param3: About param3.
    ...     '''
    ...     def __init__(self, param1, param2) -> None:
    ...         pass
    ... """
    >>> docsig(string=string, check_class=True, no_ansi=True)
    9 in Klass
    ----------
    class Klass:
        """
        :param param1: ✓
        :param param2: ✓
        :param param3: ✖
        """
    <BLANKLINE>
        def __init__(✓param1, ✓param2, ✖None) -> ✓None:
    <BLANKLINE>
    E102: includes parameters that do not exist (params-do-not-exist)
    <BLANKLINE>
    1

Checking class docstrings can be permanently enabled in the pyproject.toml file

.. code-block:: toml

    [tool.docsig]
    check-class-constructor = true

Or

.. code-block:: toml

    [tool.docsig]
    check-class = true
