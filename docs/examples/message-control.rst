Message Control
***************

To control checks ``docsig`` accepts disable and enable directives

To disable individual function checks add an inline comment similar to the example below

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = """
    ... def function_1(param1, param2, param3) -> None:  # docsig: disable
    ...     '''
    ...
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     :param param1: Fails.
    ...     '''
    ...
    ... def function_2(param1, param2) -> None:
    ...     '''
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     '''
    ...
    ... def function_3(param1, param2, param3) -> None:
    ...     '''
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     '''
    ... """
    >>> docsig(string=string)
    10
    --
    def function_2(✓param1, ✓param2, ✖None) -> ✓None:
        """
        :param param1: ✓
        :param param2: ✓
        :param param3: ✖
        """
    <BLANKLINE>
    E102: includes parameters that do not exist (params-do-not-exist)
    <BLANKLINE>
    18
    --
    def function_3(✓param1, ✓param2, ✖param3) -> ✓None:
        """
        :param param1: ✓
        :param param2: ✓
        :param None: ✖
        """
    <BLANKLINE>
    E103: parameters missing (params-missing)
    <BLANKLINE>
    1

To disable all function checks add a module level comment similar to the example below

.. code-block:: python

    >>> string = """
    ... # docsig: disable
    ... def function_1(param1, param2, param3) -> None:
    ...     '''
    ...
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     :param param1: Fails.
    ...     '''
    ...
    ... def function_2(param1, param2) -> None:
    ...     '''
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     '''
    ...
    ... def function_3(param1, param2, param3) -> None:
    ...     '''
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     '''
    ... """
    >>> docsig(string=string)
    0

To disable multiple function checks add a module level disable and enable comment similar to the example below

.. code-block:: python

    >>> string = """
    ... # docsig: disable
    ... def function_1(param1, param2, param3) -> None:
    ...     '''
    ...
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     :param param1: Fails.
    ...     '''
    ...
    ... def function_2(param1, param2) -> None:
    ...     '''
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     '''
    ... # docsig: enable
    ...
    ... def function_3(param1, param2, param3) -> None:
    ...     '''
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     '''
    ... """
    >>> docsig(string=string)
    20
    --
    def function_3(✓param1, ✓param2, ✖param3) -> ✓None:
        """
        :param param1: ✓
        :param param2: ✓
        :param None: ✖
        """
    <BLANKLINE>
    E103: parameters missing (params-missing)
    <BLANKLINE>
    1

The same can be done for disabling individual rules

.. code-block:: python

    >>> string = """
    ... # docsig: disable=E101
    ... def function_1(param1, param2, param3) -> int:
    ...     '''E105.
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     '''
    ...
    ... def function_2(param1, param2, param3) -> None:  # docsig: disable=E102,E106
    ...     '''E101,E102,E106.
    ...
    ...     :param param1: Fails.
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     '''
    ...
    ... def function_3(param1, param2, param3) -> None:
    ...     '''E101,E102,E106,E107.
    ...
    ...     :param param1: Fails.
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param: Fails.
    ...     '''
    ... """
    >>> docsig(string=string)
    3
    -
    def function_1(✓param1, ✓param2, ✓param3) -> ✖int:
        """
        :param param1: ✓
        :param param2: ✓
        :param param3: ✓
        :return: ✖
        """
    <BLANKLINE>
    E105: return missing from docstring (return-missing)
    <BLANKLINE>
    20
    --
    def function_3(✓param1, ✖param2, ✖param3, ✖None) -> ✓None:
        """
        :param param1: ✓
        :param param1: ✖
        :param param2: ✖
        :param None: ✖
        """
    <BLANKLINE>
    E102: includes parameters that do not exist (params-do-not-exist)
    E106: duplicate parameters found (duplicate-params-found)
    E107: parameter appears to be incorrectly documented (param-incorrectly-documented)
    <BLANKLINE>
    1

Individual rules can also be re-enabled

Module level directives will be evaluated separately to inline directives and providing no rules will disable and enable all rules

.. code-block:: python

    >>> string = """
    ... # docsig: disable
    ... def function_1(param1, param2, param3) -> int:
    ...     '''E105.
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     '''
    ...
    ... def function_2(param1, param2, param3) -> None:  # docsig: enable=E102,E106
    ...     '''E101,E102,E106.
    ...
    ...     :param param1: Fails.
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     '''
    ...
    ... def function_3(param1, param2, param3) -> None:
    ...     '''E101,E102,E106,E107.
    ...
    ...     :param param1: Fails.
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param: Fails.
    ...     '''
    ... """
    >>> docsig(string=string)
    11
    --
    def function_2(✓param1, ✖param2, ✖param3, ✖None) -> ✓None:
        """
        :param param1: ✓
        :param param1: ✖
        :param param2: ✖
        :param param3: ✖
        """
    <BLANKLINE>
    E102: includes parameters that do not exist (params-do-not-exist)
    E106: duplicate parameters found (duplicate-params-found)
    <BLANKLINE>
    1
