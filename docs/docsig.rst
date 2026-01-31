Check Python signature params for proper documentation
=======================================================

Supports reStructuredText (``Sphinx``), ``NumPy``, and ``Google``
-----------------------------------------------------------------

**docsig** is a Python documentation linter that ensures function and method
signature parameters are properly documented in docstrings. It supports multiple
docstring formats including reStructuredText (``Sphinx``), ``NumPy``, and
``Google`` styles.

Maintain accurate and up-to-date Python documentation by automatically checking
that all parameters in function signatures match their docstring documentation.
Use docsig as a standalone tool, integrate it with ``flake8``, or add it as a
``pre-commit`` hook to catch documentation issues before they reach your
repository.

Installation
------------

To begin using ``docsig`` simply install it from
`PyPI <https://pypi.org/project/docsig/>`_ with ``pip``

.. code-block:: console

    $ pip install docsig

pre-commit
----------

``docsig`` can be used as a `pre-commit <https://pre-commit.com>`_ hook

It can be added to your .pre-commit-config.yaml as follows:

.. include:: _generated/pre-commit-example.rst
