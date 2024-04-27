|

.. image:: https://raw.githubusercontent.com/jshwi/docsig/master/docs/static/docsig.svg
   :alt: docsig logo
   :width: 50%
   :align: center

|

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. image:: https://img.shields.io/pypi/v/docsig
   :target: https://pypi.org/project/docsig/
   :alt: PyPI
.. image:: https://github.com/jshwi/docsig/actions/workflows/build.yaml/badge.svg
   :target: https://github.com/jshwi/docsig/actions/workflows/build.yaml
   :alt: CI
.. image:: https://github.com/jshwi/docsig/actions/workflows/codeql-analysis.yml/badge.svg
   :target: https://github.com/jshwi/docsig/actions/workflows/codeql-analysis.yml
   :alt: CodeQL
.. image:: https://results.pre-commit.ci/badge/github/jshwi/docsig/master.svg
   :target: https://results.pre-commit.ci/latest/github/jshwi/docsig/master
   :alt: pre-commit.ci status
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
.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
   :target: https://pycqa.github.io/isort/
   :alt: isort
.. image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg
   :target: https://github.com/PyCQA/docformatter
   :alt: docformatter
.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
   :target: https://github.com/PyCQA/pylint
   :alt: pylint
.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
   :target: https://github.com/PyCQA/bandit
   :alt: Security Status
.. image:: https://snyk.io/test/github/jshwi/docsig/badge.svg
   :target: https://snyk.io/test/github/jshwi/docsig/badge.svg
   :alt: Known Vulnerabilities
.. image:: https://snyk.io/advisor/python/docsig/badge.svg
   :target: https://snyk.io/advisor/python/docsig
   :alt: docsig

Check signature params for proper documentation
-----------------------------------------------

Supports reStructuredText (``Sphinx``), ``NumPy``, and ``Google``

Contributing
------------
If you are interested in contributing to ``docsig`` please read about contributing `here <https://github.com/jshwi/docsig/blob/master/CONTRIBUTING.md>`__

Installation
------------

.. code-block:: console

    $ pip install docsig

Usage
-----

Commandline
***********

.. code-block:: console

    usage: docsig [-h] [-V] [-l] [-c | -C] [-D] [-m] [-N] [-o] [-p] [-P] [-i] [-a]
                           [-k] [-I] [-n] [-S] [-v] [-s STR] [-d LIST] [-t LIST]
                           [-e PATTERN]
                           [path [path ...]]

    Check signature params for proper documentation

    positional arguments:
      path                                 directories or files to check

    optional arguments:
      -h, --help                           show this help message and exit
      -V, --version                        show program's version number and exit
      -l, --list-checks                    display a list of all checks and their messages
      -c, --check-class                    check class docstrings
      -C, --check-class-constructor        check __init__ methods. Note: mutually
                                           incompatible with -c
      -D, --check-dunders                  check dunder methods
      -m, --check-protected-class-methods  check public methods belonging to protected
                                           classes
      -N, --check-nested                   check nested functions and classes
      -o, --check-overridden               check overridden methods
      -p, --check-protected                check protected functions and classes
      -P, --check-property-returns         check property return values
      -i, --ignore-no-params               ignore docstrings where parameters are not
                                           documented
      -a, --ignore-args                    ignore args prefixed with an asterisk
      -k, --ignore-kwargs                  ignore kwargs prefixed with two asterisks
      -I, --include-ignored                check files even if they match a gitignore
                                           pattern
      -n, --no-ansi                        disable ansi output
      -S, --summary                        print a summarised report
      -v, --verbose                        increase output verbosity
      -s STR, --string STR                 string to parse instead of files
      -d LIST, --disable LIST              comma separated list of rules to disable
      -t LIST, --target LIST               comma separated list of rules to target
      -e PATTERN, --exclude PATTERN        regular expression of files or dirs to exclude
                                           from checks

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
    ...     '''
    ...
    ...     :param param1: About param1.
    ...     :param param2: About param2.
    ...     :param param3: About param3.
    ...     '''
    ...     """
    >>> docsig(string=string, summary=True, no_ansi=True)
    0

.. code-block:: python

    >>> string = """
    ... def function(param1, param2) -> None:
    ...     '''
    ...
    ...     :param param1: About param1.
    ...     :param param2: About param2.
    ...     :param param3: About param3.
    ...     '''
    ... """
    >>> docsig(string=string, summary=True, no_ansi=True)
    2 in function
        E102: includes parameters that do not exist (params-do-not-exist)
    1

A full list of checks can be found `here <https://docsig.readthedocs.io/en/latest/docsig.html#docsig-messages>`__

Message Control
***************

`Documentation on message control <https://github.com/jshwi/docsig/blob/master/docs/examples/message-control.rst>`_

Classes
*******

`Documenting classes <https://github.com/jshwi/docsig/blob/master/docs/examples/classes.rst>`_

pre-commit
**********

``docsig`` can be used as a `pre-commit <https://pre-commit.com>`_ hook

It can be added to your .pre-commit-config.yaml as follows:

.. code-block:: yaml

    repos:
      - repo: https://github.com/jshwi/docsig
        rev: v0.51.1
        hooks:
          - id: docsig
            args:
              - "--check-class"
              - "--check-dunders"
              - "--check-overridden"
              - "--check-protected"
              - "--summary"
