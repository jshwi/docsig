Check class constructor
=======================

check __init__ methods. Note: mutually incompatible with -c

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... class Class:
    ...     def __init__(self, a, b) -> None:
    ...         """Docstring summary.
    ...
    ...         :param b: Description of b.
    ...         :param a: Description of a.
    ...         """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> docsig(string=string, check_class_constructor=True, no_ansi=True)
    3 in Class.__init__
        SIG402: parameters out of order (params-out-of-order)
    1
