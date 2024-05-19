E117: description-missing
=========================

Description missing from parameter

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param1) -> None:
    ...     """Function summary.
    ...
    ...     :param param1:
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        E117: description missing from parameter (description-missing)
    1
