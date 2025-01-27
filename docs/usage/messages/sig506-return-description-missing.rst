SIG506: return-description-missing
==================================

Description missing from return

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = '''
    ... def normalize(ticker: str) -> str:
    ...     """Normalize ticket names.
    ...
    ...     :param ticker: Ticker to normalize.
    ...     :return:
    ...     """
    ... '''

.. code-block:: python

    >>> docsig(string=string, no_ansi=True)
    2 in normalize
        SIG506: description missing from return (return-description-missing)
    1
