|

.. image:: https://raw.githubusercontent.com/jshwi/docsig/master/docs/static/docsig.svg
   :alt: docsig logo
   :width: 50%
   :align: center

|

|License| |PyPI| |CI| |CodeQL| |pre-commit.ci status| |codecov.io| |readthedocs.org| |python3.8| |Black| |isort| |docformatter| |pylint| |Security Status| |Known Vulnerabilities| |docsig|

.. |License| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |PyPI| image:: https://img.shields.io/pypi/v/docsig
   :target: https://pypi.org/project/docsig/
   :alt: PyPI
.. |CI| image:: https://github.com/jshwi/docsig/actions/workflows/build.yaml/badge.svg
   :target: https://github.com/jshwi/docsig/actions/workflows/build.yaml
   :alt: CI
.. |CodeQL| image:: https://github.com/jshwi/docsig/actions/workflows/codeql-analysis.yml/badge.svg
   :target: https://github.com/jshwi/docsig/actions/workflows/codeql-analysis.yml
   :alt: CodeQL
.. |pre-commit.ci status| image:: https://results.pre-commit.ci/badge/github/jshwi/docsig/master.svg
   :target: https://results.pre-commit.ci/latest/github/jshwi/docsig/master
   :alt: pre-commit.ci status
.. |codecov.io| image:: https://codecov.io/gh/jshwi/docsig/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jshwi/docsig
   :alt: codecov.io
.. |readthedocs.org| image:: https://readthedocs.org/projects/docsig/badge/?version=latest
   :target: https://docsig.readthedocs.io/en/latest/?badge=latest
   :alt: readthedocs.org
.. |python3.8| image:: https://img.shields.io/badge/python-3.8-blue.svg
   :target: https://www.python.org/downloads/release/python-380
   :alt: python3.8
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black
.. |isort| image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
   :target: https://pycqa.github.io/isort/
   :alt: isort
.. |docformatter| image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg
   :target: https://github.com/PyCQA/docformatter
   :alt: docformatter
.. |pylint| image:: https://img.shields.io/badge/linting-pylint-yellowgreen
   :target: https://github.com/PyCQA/pylint
   :alt: pylint
.. |Security Status| image:: https://img.shields.io/badge/security-bandit-yellow.svg
   :target: https://github.com/PyCQA/bandit
   :alt: Security Status
.. |Known Vulnerabilities| image:: https://snyk.io/test/github/jshwi/docsig/badge.svg
   :target: https://snyk.io/test/github/jshwi/docsig/badge.svg
   :alt: Known Vulnerabilities
.. |docsig| image:: https://snyk.io/advisor/python/docsig/badge.svg
   :target: https://snyk.io/advisor/python/docsig
   :alt: docsig

Check signature params for proper documentation
-----------------------------------------------

Supports reStructuredText (``Sphinx``), ``NumPy``, and ``Google``

Contributing
------------
If you are interested in contributing to ``docsig`` please read about contributing `here <https://docsig.readthedocs.io/en/latest/development/contributing.html>`__

Installation
------------

.. code-block:: console

    $ pip install docsig

Usage
-----

Commandline
***********

.. code-block:: console

    usage: docsig [-h] [-V] [-l] [-c | -C] [-D] [-m] [-N] [-o] [-p] [-P] [-i] [-a] [-k] [-T]
                  [-I] [-n] [-v] [-s STR] [-d LIST] [-t LIST] [-e PATTERN] [-E PATH [PATH ...]]
                  [path [path ...]]

    Check signature params for proper documentation

    positional arguments:
      path                  directories or files to check

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -l, --list-checks     display a list of all checks and their messages
      -c, --check-class     check class docstrings
      -C, --check-class-constructor
                            check __init__ methods. Note: mutually incompatible with -c
      -D, --check-dunders   check dunder methods
      -m, --check-protected-class-methods
                            check public methods belonging to protected classes
      -N, --check-nested    check nested functions and classes
      -o, --check-overridden
                            check overridden methods
      -p, --check-protected
                            check protected functions and classes
      -P, --check-property-returns
                            check property return values
      -i, --ignore-no-params
                            ignore docstrings where parameters are not documented
      -a, --ignore-args     ignore args prefixed with an asterisk
      -k, --ignore-kwargs   ignore kwargs prefixed with two asterisks
      -T, --ignore-typechecker
                            ignore checking return values
      -I, --include-ignored
                            check files even if they match a gitignore pattern
      -n, --no-ansi         disable ansi output
      -v, --verbose         increase output verbosity
      -s STR, --string STR  string to parse instead of files
      -d LIST, --disable LIST
                            comma separated list of rules to disable
      -t LIST, --target LIST
                            comma separated list of rules to target
      -e PATTERN, --exclude PATTERN
                            regular expression of files or dirs to exclude from checks
      -E PATH [PATH ...], --excludes PATH [PATH ...]
                            path glob patterns to exclude from checks

Options can also be configured with the pyproject.toml file

.. code-block:: toml

    [tool.docsig]
    check-dunders = false
    check-overridden = false
    check-protected = false
    disable = [
        "SIG101",
        "SIG102",
        "SIG402",
    ]
    target = [
        "SIG202",
        "SIG203",
        "SIG201",
    ]

Flake8
******

``docsig`` can also be used as a ``flake8`` plugin. Install ``flake8`` and
ensure your installation has registered `docsig`

.. code-block:: console

    $ flake8 --version
    7.1.0 (docsig: 0.66.1, mccabe: 0.7.0, pycodestyle: 2.12.0, pyflakes: 3.2.0) CPython 3.8.13 on Darwin

And now use `flake8` to lint your files

.. code-block:: console

    $ flake8 example.py
    example.py:1:1: SIG202 includes parameters that do not exist (params-do-not-exist) 'function'

With ``flake8`` the pyproject.toml config will still be the base config, though the
`ini files <https://flake8.pycqa.org/en/latest/user/configuration.html#configuration-locations>`_ ``flake8`` gets it config from will override the pyproject.toml config.
For ``flake8`` all args and config options are prefixed with ``sig`` to
avoid any potential conflicts with other plugins

.. code-block:: ini

    [flake8]
    sig-check-dunders = True
    sig-check-overridden = True
    sig-check-protected = True

..
   end flake8

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
    >>> docsig(string=string, no_ansi=True)
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
    >>> docsig(string=string, no_ansi=True)
    2 in function
        SIG202: includes parameters that do not exist (params-do-not-exist)
    1

A full list of checks can be found `here <https://docsig.readthedocs.io/en/latest/usage/messages.html>`__

Message Control
***************

If you have been using ``docsig`` prior to ``v0.56.0``, please see
`updated messages <https://docsig.readthedocs.io/en/latest/deprecated/messages.html>`_

`Documentation on message control <https://docsig.readthedocs.io/en/latest/usage/message-control.html>`_

Classes
*******

`Documenting classes <https://docsig.readthedocs.io/en/latest/usage/configuration.html#classes>`_

pre-commit
**********

``docsig`` can be used as a `pre-commit <https://pre-commit.com>`_ hook

It can be added to your .pre-commit-config.yaml as follows:

Standalone

.. code-block:: yaml

    repos:
      - repo: https://github.com/jshwi/docsig
        rev: v0.66.1
        hooks:
          - id: docsig
            args:
              - "--check-class"
              - "--check-dunders"
              - "--check-overridden"
              - "--check-protected"

or integrated with ``flake8``

.. code-block:: yaml

    repos:
      - repo: https://github.com/PyCQA/flake8
        rev: "7.1.0"
        hooks:
          - id: flake8
            additional_dependencies:
              - docsig==0.66.1
            args:
              - "--sig-check-class"
              - "--sig-check-dunders"
              - "--sig-check-overridden"
              - "--sig-check-protected"
