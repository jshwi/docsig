Check signature params for proper documentation
===============================================

Supports reStructuredText (``Sphinx``), ``NumPy``, and ``Google``
-----------------------------------------------------------------

``docsig`` a tool for ensuring signature parameters are correctly documented.

There is no one standard for how docstring parameters should be documented, and
so with ``docsig``, you can lay down a policy and stick to it, resulting in
more accurate documentation.

Documenting your parameters is important, but very easy to neglect, especially
when parameters belonging to a function or method change frequently.

``docsig`` will help you keep your docstrings up-to-date and informative

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
