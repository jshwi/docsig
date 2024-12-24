SIG304: bad-closing-token
=========================

bad token used to close parameter declaration '{token}'

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2, param3) -> None:
    ...     """Function summary.
    ...
    ...     :param param1: Description of param1.
    ...     :param param2. Description of param2.
    ...     :param param3: Description of param3.
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
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param param! Description of param.
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
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param param@ Description of param.
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
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param param# Description of param.
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
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param param$ Description of param.
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
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param param% Description of param.
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
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param param^ Description of param.
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
    ... def function(param) -> None:
    ...     """Function summary.
    ...
    ...     :param param& Description of param.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG304: bad token used to close parameter declaration '&' (bad-closing-token)
        hint: close a parameter declaration with ':'
    1
