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

Usage
-----

Commandline
***********

.. code-block:: console

    usage: docsig [-h] [-v] [-s STR] [-d LIST] [-t LIST] [path [path ...]]

    Check docstring matches signature

    positional arguments:
      path                     directories or files to check (default: .)

    optional arguments:
      -h, --help               show this help message and exit
      -v, --version            show version and exit
      -s STR, --string STR     string to parse instead of files
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

API
***

.. code-block:: python

    >>> from docsig import docsig

.. code-block:: python

    >>> string = """
    ... def function(param1, param2, param3) -> None:
    ...     '''Summary for passing docstring...
    ...
    ...     Explanation for passing docstring...
    ...
    ...     :param param1: About param1.
    ...     :param param2: About param2.
    ...     :param param3: About param3.
    ...     '''
    ...     """
    >>> docsig(string=string)
    0

.. code-block:: python

    >>> string = """
    ... def function(param1, param2) -> None:
    ...     '''Summary for failing docstring...
    ...
    ...     Explanation for failing docstring...
    ...
    ...     :param param1: About param1.
    ...     :param param2: About param2.
    ...     :param param3: About param3.
    ...     '''
    ... """
    >>> docsig(string=string)
    2
    -
    def function(✓param1, ✓param2, ✖None) -> ✓None:
        """...
    <BLANKLINE>
        :param param1: ✓
        :param param2: ✓
        :param param3: ✖
        """
    <BLANKLINE>
    E102: includes parameters that do not exist
    <BLANKLINE>
    1

There are currently 9 other `errors <https://docsig.readthedocs.io/en/latest/docsig.html#docsig-messages>`_
