docsig
======
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/pypi/v/docsig
    :target: https://img.shields.io/pypi/v/docsig
    :alt: pypi
.. image:: https://github.com/jshwi/docsig/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/jshwi/docsig/actions/workflows/ci.yml
    :alt: CI
.. image:: https://codecov.io/gh/jshwi/docsig/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/docsig
    :alt: codecov.io
.. image:: https://readthedocs.org/projects/docsig/badge/?version=latest
    :target: https://docsig.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

Check signature params for proper documentation
-----------------------------------------------

Currently only supports reStructuredText (Sphinx)

Installation
------------

.. code-block:: console

    $ pip install docsig

`Error Codes <https://docsig.readthedocs.io/en/latest/docsig.html#docsig-messages>`_

Usage
-----

Commandline
***********

.. code-block:: console

    usage: docsig [-h] [-v] [-d LIST] [-t LIST] [path [path ...]]

    Check docstring matches signature

    positional arguments:
      path                     directories or files to check

    optional arguments:
      -h, --help               show this help message and exit
      -v, --version            show version and exit
      -d LIST, --disable LIST  comma separated list of rules to disable
      -t LIST, --target LIST   comma separated list of rules to target

Options can also be configured with the pyproject.toml file

.. code-block:: toml

    [tool.docsig]
    disable = [
        "E101",
        "E102",
        "E103",
    ]
    target = [
        "E102",
        "E103",
        "E104",
    ]
