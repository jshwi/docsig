E110: param-not-equal-to-arg
============================

Documented parameter not equal to its respective argument

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param arg: This should be param.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E110: documented parameter not equal to its respective argument (param-not-equal-to-arg)
    1
