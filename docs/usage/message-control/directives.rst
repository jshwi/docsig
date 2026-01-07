More on directives
==================

To control checks ``docsig`` accepts disable and enable directives

To disable individual function checks add an inline comment similar to the example below

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function_1(param1, param2, param3) -> None:  # docsig: disable
    ...     """
    ...
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     :param param1: Fails.
    ...     """
    ...
    ... def function_2(param1, param2) -> None:
    ...     """
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     """
    ...
    ... def function_3(param1, param2, param3) -> None:
    ...     """
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     """
    ... '''
    >>> docsig(string=string, no_ansi=True)
    10 in function_2
        SIG202: includes parameters that do not exist (params-do-not-exist)
    18 in function_3
        SIG203: parameters missing (params-missing)
    1

To disable all function checks add a module level comment similar to the example below

.. code-block:: python

    >>> string = '''
    ... # docsig: disable
    ... def function_1(param1, param2, param3) -> None:
    ...     """
    ...
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     :param param1: Fails.
    ...     """
    ...
    ... def function_2(param1, param2) -> None:
    ...     """
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     """
    ...
    ... def function_3(param1, param2, param3) -> None:
    ...     """
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     """
    ... '''
    >>> docsig(string=string, no_ansi=True)
    0

To disable multiple function checks add a module level disable and enable comment similar to the example below

.. code-block:: python

    >>> string = '''
    ... # docsig: disable
    ... def function_1(param1, param2, param3) -> None:
    ...     """
    ...
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     :param param1: Fails.
    ...     """
    ...
    ... def function_2(param1, param2) -> None:
    ...     """
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     """
    ... # docsig: enable
    ...
    ... def function_3(param1, param2, param3) -> None:
    ...     """
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     """
    ... '''
    >>> docsig(string=string, no_ansi=True)
    20 in function_3
        SIG203: parameters missing (params-missing)
    1

The same can be done for disabling individual rules

.. code-block:: python

    >>> string = '''
    ... # docsig: disable=SIG402
    ... def function_1(param1, param2, param3) -> int:
    ...     """SIG503.
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     """
    ...
    ... def function_2(param1, param2, param3) -> None:  # docsig: disable=SIG202,SIG201
    ...     """SIG402,SIG202,SIG201.
    ...
    ...     :param param1: Fails.
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     """
    ...
    ... def function_3(param1, param2, param3) -> None:
    ...     """SIG402,SIG202,SIG502,SIG303.
    ...
    ...     :param param1: Fails.
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param: Fails.
    ...     """
    ... '''
    >>> docsig(string=string, no_ansi=True)
    3 in function_1
        SIG503: return missing from docstring (return-missing)
    20 in function_3
        SIG201: duplicate parameters found (duplicate-params-found)
        SIG303: parameter appears to be incorrectly documented (param-incorrectly-documented)
    1

Individual rules can also be re-enabled

Module level directives will be evaluated separately to inline directives and providing no rules will disable and enable all rules

.. code-block:: python

    >>> string = '''
    ... # docsig: disable
    ... def function_1(param1, param2, param3) -> int:
    ...     """E105.
    ...
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     """
    ...
    ... def function_2(param1, param2, param3) -> None:  # docsig: enable=SIG202,SIG201
    ...     """SIG402,SIG202,SIG201.
    ...
    ...     :param param1: Fails.
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param param3: Fails.
    ...     """
    ...
    ... def function_3(param1, param2, param3) -> None:
    ...     """SIG402,SIG202,SIG201,SIG303.
    ...
    ...     :param param1: Fails.
    ...     :param param1: Fails.
    ...     :param param2: Fails.
    ...     :param: Fails.
    ...     """
    ... '''
    >>> docsig(string=string, no_ansi=True)
    11 in function_2
        SIG201: duplicate parameters found (duplicate-params-found)
    1
