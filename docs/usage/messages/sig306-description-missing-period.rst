SIG306: description-missing-period
==================================

Description does not end in a period

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG306: description does not end in a period (description-missing-period)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0
