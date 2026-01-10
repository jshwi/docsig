Ignore args
===========

ignore args prefixed with an asterisk

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a, b, *args) -> None:
    ...     """Proper docstring.
    ...
    ...     :param a: Description of a.
    ...     :param b: Description of b.
    ...     :param args: Description of args.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, ignore_args=True, no_ansi=True)
    2 in function
        SIG202: includes parameters that do not exist (params-do-not-exist)
    1
