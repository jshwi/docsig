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

Installation
------------

.. code-block:: console

    $ pip install docsig

Usage
-----

Commandline
***********

.. code-block:: console

    usage: docsig [-h] [-c INT] [-l INT] [-s STR] [-i LIST] [-I LIST]usage: docsig [-h] [-v] path

    Check docstring matches signature

    positional arguments:
      path           directory or file to check

    optional arguments:
      -h, --help     show this help message and exit
      -v, --version  show version and exit
