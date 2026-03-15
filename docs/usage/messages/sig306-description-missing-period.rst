SIG306: description-missing-period
==================================


.. admonition:: New Violation

   SIG306 is a new violation and will error in a future version

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
        warning: please remember to fix this or disable it
    0

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
