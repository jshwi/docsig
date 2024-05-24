More on commandline
===================

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def func(param, param2, param3, param4) -> int:
    ...     """Desc.
    ...
    ...     :param param1: About param1.
    ...     :param param2:A.
    ...     :param param3:
    ...      """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in func
        E103: parameters missing (params-missing)
        E105: return missing from docstring (return-missing)
        E112: spelling error found in documented parameter (spelling-error)
        E115: syntax error in description (syntax-error-in-description)
        E116: param not indented correctly (incorrect-indent)
        E117: description missing from parameter (description-missing)
    1

.. code-block:: python

    >>> docsig(string=string, disable=["E103"], no_ansi=True)
    2 in func
        E105: return missing from docstring (return-missing)
        E112: spelling error found in documented parameter (spelling-error)
        E115: syntax error in description (syntax-error-in-description)
        E116: param not indented correctly (incorrect-indent)
        E117: description missing from parameter (description-missing)
    1

.. code-block:: python

    >>> docsig(string=string, targets=["E103"], no_ansi=True)
    2 in func
        E103: parameters missing (params-missing)
    1

.. code-block:: python

    >>> docsig(string=string, targets=["E107"], no_ansi=True)
    0

This has the same effect, but is quicker to write

.. code-block:: python

    >>> docsig(string=string, disable=["E103"], no_ansi=True)
    2 in func
        E105: return missing from docstring (return-missing)
        E112: spelling error found in documented parameter (spelling-error)
        E115: syntax error in description (syntax-error-in-description)
        E116: param not indented correctly (incorrect-indent)
        E117: description missing from parameter (description-missing)
    1

than

.. code-block:: python

    >>> docsig(
    ...    string=string,
    ...    targets=["E105", "E112", "E115", "E116", "E117"],
    ...    no_ansi=True,
    ... )
    2 in func
        E105: return missing from docstring (return-missing)
        E112: spelling error found in documented parameter (spelling-error)
        E115: syntax error in description (syntax-error-in-description)
        E116: param not indented correctly (incorrect-indent)
        E117: description missing from parameter (description-missing)
    1

But this takes longer to write

.. code-block:: python

    >>> docsig(
    ...     string=string,
    ...     disable=["E105", "E112", "E115", "E116", "E117"],
    ...     no_ansi=True
    ... )
    2 in func
        E103: parameters missing (params-missing)
    1

than

.. code-block:: python

    >>> docsig(string=string, targets=["E103"], no_ansi=True)
    2 in func
        E103: parameters missing (params-missing)
    1

There isn't any use in using these together, however

.. code-block:: python

    >>> docsig(
    ...     string=string,
    ...     disable=["E105", "E112", "E115", "E116", "E117"],
    ...     targets=["E103"],
    ...     no_ansi=True,
    ... )
    2 in func
        E103: parameters missing (params-missing)
    1

.. code-block:: python

    >>> docsig(string=string, targets=["E103"], no_ansi=True)
    2 in func
        E103: parameters missing (params-missing)
    1

This will just disable everything, as disable will disable one, and target will
disable everything else

.. code-block:: python

    >>> docsig(string=string, disable=["E103"], targets=["E103"], no_ansi=True)
    0

.. code-block:: python

    >>> string = '''
    ... def func(  # docsig: disable=E117
    ...     param, param2, param3, param4
    ... ) -> int:
    ...     """Desc.
    ...
    ...     :param param1: About param1.
    ...     :param param2:A.
    ...     :param param3:
    ...      """
    ... '''

.. code-block:: python

    >>> docsig(string=string, disable=["E103"], no_ansi=True)
    2 in func
        E105: return missing from docstring (return-missing)
        E112: spelling error found in documented parameter (spelling-error)
        E115: syntax error in description (syntax-error-in-description)
        E116: param not indented correctly (incorrect-indent)
    1

.. code-block:: python

    >>> docsig(string=string, targets=["E103"], no_ansi=True)
    2 in func
        E103: parameters missing (params-missing)
    1

.. code-block:: python

    >>> string = '''
    ... # docsig: disable
    ...
    ... def func(  # docsig: enable=E103
    ...     param, param2, param3, param4
    ... ) -> int:
    ...     """Desc.
    ...
    ...     :param param1: About param1.
    ...     :param param2:A.
    ...     :param param3:
    ...      """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    4 in func
        E103: parameters missing (params-missing)
    1

.. code-block:: python

    >>> docsig(string=string, targets=["E117"], no_ansi=True)
    0
