SIG902: unicode-decode-error
============================

Failed to read file

This is only raised for files ending in ``.py``, all other files will be ignored

.. code-block:: console

    $ docsig py2.py
    py2.py:0 in module
        SIG902: failed to read file (unicode-decode-error)
