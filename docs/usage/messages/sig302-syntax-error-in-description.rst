SIG302: syntax-error-in-description
===================================

Syntax error in description

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a:Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG302: syntax error in description (syntax-error-in-description)
    1
