SIG506: return-description-missing
==================================

Description missing from return

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(a) -> int:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     :return:
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG506: description missing from return (return-description-missing)
    1

Describing the return resolves the check

.. code-block:: python

    >>> string = '''
    ... def function(a) -> int:
    ...     """Docstring summary.
    ...
    ...     :param a: Description of a.
    ...     :return: Return description.
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    0
