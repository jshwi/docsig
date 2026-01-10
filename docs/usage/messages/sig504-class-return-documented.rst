SIG504: class-return-documented
===============================

Return statement documented for class

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... class Klass:
    ...     """Function summary.
    ...
    ...     :param param: Description of param.
    ...     :returns: Return description.
    ...     """
    ...
    ...     def __init__(self, param) -> None:
    ...         pass
    ... '''

.. code-block:: python

    >>> docsig(string=string, check_class=True, no_ansi=True)
    9 in Klass.__init__
        SIG504: return statement documented for class (class-return-documented)
        hint: a class does not return a value during instantiation
    1
