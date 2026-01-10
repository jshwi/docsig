SIG404: param-not-equal-to-arg
==============================

Documented parameter not equal to its respective argument

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Docstring summary.
    ...
    ...     :param b: Description of b.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG404: documented parameter not equal to its respective argument (param-not-equal-to-arg)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Docstring summary.
    ...
    ...     :param b: Description of b.
    ...     :return: Return description.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG404: documented parameter not equal to its respective argument (param-not-equal-to-arg)
        SIG502: return statement documented for None (return-documented-for-none)
    1

.. code-block:: python

    >>> string = '''
    ... def function(a, b) -> None:
    ...     """Docstring summary.
    ...
    ...     :param c: Description of c.
    ...     :param b: Description of b.
    ...     :param b: Description of b.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG201: duplicate parameters found (duplicate-params-found)
        SIG404: documented parameter not equal to its respective argument (param-not-equal-to-arg)
    1
