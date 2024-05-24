SIG302: syntax-error-in-description
===================================

Syntax error in description

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param param:There should be a space here.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG302: syntax error in description (syntax-error-in-description)
    1
