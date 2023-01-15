docsig
======
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/pypi/v/docsig
    :target: https://pypi.org/project/docsig/
    :alt: PyPI
.. image:: https://github.com/jshwi/docsig/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/jshwi/docsig/actions/workflows/ci.yml
    :alt: CI
.. image:: https://results.pre-commit.ci/badge/github/jshwi/docsig/master.svg
   :target: https://results.pre-commit.ci/latest/github/jshwi/docsig/master
   :alt: pre-commit.ci status
.. image:: https://github.com/jshwi/docsig/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/docsig/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
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
    :alt: Black
.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/PyCQA/pylint
    :alt: pylint
.. image:: https://snyk.io/test/github/jshwi/docsig/badge.svg
    :target: https://snyk.io/test/github/jshwi/docsig/badge.svg
    :alt: Known Vulnerabilities

Check signature params for proper documentation
-----------------------------------------------

Supports reStructuredText (``Sphinx``), ``NumPy``, and ``Google``

Installation
------------

.. code-block:: console

    $ pip install docsig

Usage
-----

Commandline
***********

.. code-block:: console

    usage: docsig [-h] [-v] [-c] [-D] [-o] [-p] [-P] [-i] [-a] [-k] [-n] [-S] [-s STR]
                             [-d LIST] [-t LIST]
                             [path [path ...]]

    Check signature params for proper documentation

    positional arguments:
      path                          directories or files to check (default: .)

    optional arguments:
      -h, --help                    show this help message and exit
      -v, --version                 show program's version number and exit
      -c, --check-class             check class docstrings
      -D, --check-dunders           check dunder methods
      -o, --check-overridden        check overridden methods
      -p, --check-protected         check protected functions and classes
      -P, --check-property-returns  check property return values
      -i, --ignore-no-params        ignore docstrings where parameters are not documented
      -a, --ignore-args             ignore args prefixed with an asterisk
      -k, --ignore-kwargs           ignore kwargs prefixed with two asterisks
      -n, --no-ansi                 disable ansi output
      -S, --summary                 print a summarised report
      -s STR, --string STR          string to parse instead of files
      -d LIST, --disable LIST       comma separated list of rules to disable
      -t LIST, --target LIST        comma separated list of rules to target

Options can also be configured with the pyproject.toml file

If you find the output is too verbose then the report can be configured to display a summary

.. code-block:: toml

    [tool.docsig]
    check-dunders = false
    check-overridden = false
    check-protected = false
    summary = true
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
        """
        :param param1: ✓
        :param param2: ✓
        :param param3: ✖
        """
    <BLANKLINE>
    E102: includes parameters that do not exist
    <BLANKLINE>
    1

A full list of checks can be found `here <https://docsig.readthedocs.io/en/latest/docsig.html#docsig-messages>`_

Classes
#######
Checking a class docstring is not enabled by default, as this check is opinionated, and won't suite everyone

This check will check documentation of ``__init__`` under the class docstring, and not under ``__init__`` itself

.. code-block:: python

    >>> string = """
    ... class Klass:
    ...     '''Summary for failing docstring...
    ...
    ...     Explanation for failing docstring...
    ...
    ...     :param param1: About param1.
    ...     :param param2: About param2.
    ...     :param param3: About param3.
    ...     '''
    ...     def __init__(self, param1, param2) -> None:
    ...         pass
    ... """
    >>> docsig(string=string, check_class=True)
    11 in Klass
    -----------
    class Klass:
        """
        :param param1: ✓
        :param param2: ✓
        :param param3: ✖
        """
    <BLANKLINE>
        def __init__(✓param1, ✓param2, ✖None) -> ✓None:
    <BLANKLINE>
    E102: includes parameters that do not exist
    <BLANKLINE>
    1

Checking class docstrings can be permanently enabled in the pyproject.toml file

.. code-block:: toml

    [tool.docsig]
    check-class = true

pre-commit
**********

``docsig`` can be used as a `pre-commit <https://pre-commit.com>`_ hook

It can be added to your .pre-commit-config.yaml as follows:

.. code-block:: yaml

    repos:
      - repo: https://github.com/jshwi/docsig
        rev: v0.30.0
        hooks:
          - id: docsig
            args:
              - "--check-class"
              - "--check-dunders"
              - "--check-overridden"
              - "--check-protected"
              - "--summary"
