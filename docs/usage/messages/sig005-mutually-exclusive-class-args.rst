SIG005: mutually-exclusive-class-args
=====================================

both class args passed to commandline

This is only raised as a ``flake8`` violation so that it won't cause ``flake8`` to
totally crash and other plugins can continue to run

When running ``docsig`` on it's own an exception will be raised instead

.. code-block:: console

    $ flake8 example.py --sig-check-class --sig-check-class-constructor
    example.py:0:1: SIG005 both class and class constructor passed to commandline (mutually-exclusive-class-args)

.. code-block:: console

    $ docsig example.py --check-class --check-class-constructor 2>&1 | tail -n 1
    docsig: error: argument -C/--check-class-constructor: not allowed with argument -c/--check-class
