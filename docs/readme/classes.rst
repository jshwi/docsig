Classes
*******

.. code-block:: python

    >>> from docsig import docsig

Checking class constructor

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

Checking class

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
