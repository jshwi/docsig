SIG901: invalid-syntax
======================

Parsing python code failed

This is only raised for files ending in ``.py``, all other files will be ignored

.. note::

    ``docsig`` does not support ``python2``

.. code-block:: console

    $ docsig py2.py
    py2.py:0 in module
        SIG901: parsing python code failed: invalid syntax (syntax-error)
