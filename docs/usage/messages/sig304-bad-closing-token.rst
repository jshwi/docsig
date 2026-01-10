SIG304: bad-closing-token
=========================

bad token used to close parameter declaration '{token}'

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a, b, c) -> None:
    ...     """Function summary.
    ...
    ...     :param a: Description of a.
    ...     :param b. Description of b.
    ...     :param c: Description of c.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG304: bad token used to close parameter declaration '.' (bad-closing-token)
        hint: close a parameter declaration with ':'
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a! Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG304: bad token used to close parameter declaration '!' (bad-closing-token)
        hint: close a parameter declaration with ':'
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a@ Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG304: bad token used to close parameter declaration '@' (bad-closing-token)
        hint: close a parameter declaration with ':'
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a# Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG304: bad token used to close parameter declaration '#' (bad-closing-token)
        hint: close a parameter declaration with ':'
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a$ Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG304: bad token used to close parameter declaration '$' (bad-closing-token)
        hint: close a parameter declaration with ':'
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a% Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG304: bad token used to close parameter declaration '%' (bad-closing-token)
        hint: close a parameter declaration with ':'
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a^ Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG304: bad token used to close parameter declaration '^' (bad-closing-token)
        hint: close a parameter declaration with ':'
    1

.. code-block:: python

    >>> string = '''
    ... def function(a) -> None:
    ...     """Function summary.
    ...
    ...     :param a& Description of a.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG304: bad token used to close parameter declaration '&' (bad-closing-token)
        hint: close a parameter declaration with ':'
    1
