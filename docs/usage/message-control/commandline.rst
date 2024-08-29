More on commandline
===================

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def func(param, param2, param3, param4) -> int:
    ...     """Desc.
    ...
    ...      :param param1: About param1.
    ...      :param param2:A.
    ...      :param param3:
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in func
        SIG203: parameters missing (params-missing)
        SIG301: description missing from parameter (description-missing)
        SIG302: syntax error in description (syntax-error-in-description)
        SIG401: param not indented correctly (incorrect-indent)
        SIG503: return missing from docstring (return-missing)
    1

.. code-block:: python

    >>> docsig(string=string, disable=["SIG203"], no_ansi=True)
    2 in func
        SIG301: description missing from parameter (description-missing)
        SIG302: syntax error in description (syntax-error-in-description)
        SIG401: param not indented correctly (incorrect-indent)
        SIG503: return missing from docstring (return-missing)
    1

.. code-block:: python

    >>> docsig(string=string, target=["SIG203"], no_ansi=True)
    2 in func
        SIG203: parameters missing (params-missing)
    1

.. code-block:: python

    >>> docsig(string=string, target=["SIG303"], no_ansi=True)
    0

This has the same effect, but is quicker to write

.. code-block:: python

    >>> docsig(string=string, disable=["SIG203"], no_ansi=True)
    2 in func
        SIG301: description missing from parameter (description-missing)
        SIG302: syntax error in description (syntax-error-in-description)
        SIG401: param not indented correctly (incorrect-indent)
        SIG503: return missing from docstring (return-missing)
    1

than

.. todo::

    should be here
    SIG403: spelling error found in documented parameter (spelling-error)


.. code-block:: python

    >>> docsig(
    ...    string=string,
    ...    target=["SIG503", "SIG403", "SIG302", "SIG401", "SIG301"],
    ...    no_ansi=True,
    ... )
    2 in func
        SIG301: description missing from parameter (description-missing)
        SIG302: syntax error in description (syntax-error-in-description)
        SIG401: param not indented correctly (incorrect-indent)
        SIG503: return missing from docstring (return-missing)
    1

But this takes longer to write

.. code-block:: python

    >>> docsig(
    ...     string=string,
    ...     disable=["SIG503", "SIG403", "SIG302", "SIG401", "SIG301"],
    ...     no_ansi=True
    ... )
    2 in func
        SIG203: parameters missing (params-missing)
    1

than

.. code-block:: python

    >>> docsig(string=string, target=["SIG203"], no_ansi=True)
    2 in func
        SIG203: parameters missing (params-missing)
    1

There isn't any use in using these together, however

.. code-block:: python

    >>> docsig(
    ...     string=string,
    ...     disable=["SIG503", "SIG403", "SIG302", "SIG401", "SIG301"],
    ...     target=["SIG203"],
    ...     no_ansi=True,
    ... )
    2 in func
        SIG203: parameters missing (params-missing)
    1

.. code-block:: python

    >>> docsig(string=string, target=["SIG203"], no_ansi=True)
    2 in func
        SIG203: parameters missing (params-missing)
    1

This will just disable everything, as disable will disable one, and target will
disable everything else

.. code-block:: python

    >>> docsig(string=string, disable=["SIG203"], target=["SIG203"], no_ansi=True)
    0

.. code-block:: python

    >>> string = '''
    ... def func(  # docsig: disable=SIG301
    ...     param, param2, param3, param4
    ... ) -> int:
    ...     """Desc.
    ...
    ...      :param param1: About param1.
    ...      :param param2:A.
    ...      :param param3:
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, disable=["SIG203"], no_ansi=True)
    2 in func
        SIG302: syntax error in description (syntax-error-in-description)
        SIG401: param not indented correctly (incorrect-indent)
        SIG503: return missing from docstring (return-missing)
    1

.. code-block:: python

    >>> docsig(string=string, target=["SIG203"], no_ansi=True)
    2 in func
        SIG203: parameters missing (params-missing)
    1

.. code-block:: python

    >>> string = '''
    ... # docsig: disable
    ...
    ... def func(  # docsig: enable=SIG203
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
        SIG203: parameters missing (params-missing)
    1

.. code-block:: python

    >>> docsig(string=string, target=["SIG301"], no_ansi=True)
    0
