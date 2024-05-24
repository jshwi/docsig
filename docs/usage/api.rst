API
===

``docsig`` is a commandline program, but it can be imported and used in a
Python script

For this documentation, and to accurately outline what goes into each call,
we'll be using the API. The parameters are available to the commandline as
outlined in the next page.

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2, param3) -> None:
    ...     """
    ...
    ...     :param param1: About param1.
    ...     :param param2: About param2.
    ...     :param param3: About param3.
    ...     """
    ... '''
    >>> docsig(string=string, no_ansi=True)
    0

.. code-block:: python

    >>> string = '''
    ... def function(param1, param2) -> None:
    ...     """
    ...
    ...     :param param1: About param1.
    ...     :param param2: About param2.
    ...     :param param3: About param3.
    ...     """
    ... '''
    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG202: includes parameters that do not exist (params-do-not-exist)
    1
