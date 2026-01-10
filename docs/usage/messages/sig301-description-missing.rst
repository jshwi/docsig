SIG301: description-missing
===========================

Description missing from parameter

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Docstring summary.
    ...
    ...     :param a:
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG301: description missing from parameter (description-missing)
    1
