Message Control
===============

There are multiple levels that can be configured to achieve the desired results

Persistent
----------

The base configuration exists in the pyproject.toml file

.. todo::

    Mock the pyproject.toml here if possible

.. include:: ../_generated/pyproject-toml-example.rst

After this, messages available can also be achieved with the commandline and
with comment directives

Both commandline and comments can be used for finer configuration of signature
documentation policy

Directives work exactly the same as commandline arguments except they can be
used to configure lines of code in a module, or functions and classes using
inline syntax

Commandline
-----------

.. toctree::
   :titlesonly:

   message-control/commandline

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

This will just disable everything, as disable will disable one, and target will
disable everything else

.. code-block:: python

    >>> docsig(string=string, disable=["SIG203"], target=["SIG203"], no_ansi=True)
    0

Directives
----------

.. toctree::
   :titlesonly:

   message-control/directives

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
