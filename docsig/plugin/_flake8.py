"""
docsig.plugin._flake8
=====================

Flake8 plugin entry point that runs docsig checks and reports as flake8
errors.
"""

import ast as _ast
import contextlib as _contextlib
import os as _os
import sys as _sys
import typing as _t
from argparse import Namespace as _Namespace
from pathlib import Path as _Path

from .._config import Check as _Check
from .._config import Config as _Config
from .._config import Ignore as _Ignore
from .._core import runner as _runner
from .._core import setup_logger as _setup_logger
from .._version import __version__
from ..messages import FLAKE8 as _FLAKE8
from ..messages import E as _E

_Flake8Error = tuple[int, int, str, type[_t.Any]]

#: boolean commandline options mirrored by this plugin, prefixed with
#: --sig- to avoid conflicts with other plugins
_OPTIONS = (
    ("verbose", "increase output verbosity"),
    ("check-class", "check class docstrings"),
    (
        "check-class-constructor",
        "check __init__ methods (mutually incompatible with"
        " --sig-check-class)",
    ),
    ("check-dunders", "check dunder methods"),
    ("check-nested", "check nested functions and classes"),
    ("check-overridden", "check overridden methods"),
    ("check-property-returns", "check property return values"),
    ("check-protected", "check protected functions and classes"),
    (
        "check-protected-class-methods",
        "check public methods belonging to protected classes",
    ),
    ("ignore-args", "ignore args prefixed with an asterisk"),
    ("ignore-kwargs", "ignore kwargs prefixed with two asterisks"),
    (
        "ignore-no-params",
        "ignore docstrings where parameters are not documented",
    ),
)


@_contextlib.contextmanager
def _cwd_on_sys_path() -> _t.Iterator[None]:
    # so astroid can resolve project packages for overridden checks
    # (#522) without mutating sys.path at import time
    cwd = _os.path.abspath(_os.getcwd())
    added = cwd not in _sys.path
    if added:
        _sys.path.append(cwd)
    try:
        yield
    finally:
        if added:
            with _contextlib.suppress(ValueError):
                _sys.path.remove(cwd)


class Flake8:
    """Plugin that runs docsig on a file and yields flake8 errors.

    :param tree: Parsed AST module (unused; flake8 requires it for the
        API).
    :param filename: Path to the file to check.
    """

    off_by_default = False
    name = __package__
    version = __version__
    a = _Namespace()

    def __init__(self, tree: _ast.Module, filename: str) -> None:
        _tree = tree  # noqa
        self.filename = filename

    # won't import flake8 type
    # conflicts with this module name
    # might require that flake8 actually be installed, which is not a
    # requirement for this package
    @classmethod
    def add_options(cls, parser: _t.Any) -> None:
        """Register CLI and config opts with the flake8 option parser.

        :param parser: Flake8 option manager to extend.
        """
        for option, help_text in _OPTIONS:
            parser.add_option(
                f"--sig-{option}",
                action="store_true",
                parse_from_config=True,
                help=help_text,
            )

    @classmethod
    def parse_options(cls, a: _Namespace) -> None:
        """Store parsed options on class state without the sig prefix.

        :param a: Argparse namespace from flake8.
        """
        cls.a.__dict__ = {
            k.replace("sig_", ""): v for k, v in a.__dict__.items()
        }

    def _build_config(self) -> _Config:
        options = self.a
        check = _Check(
            class_=options.check_class,
            class_constructor=options.check_class_constructor,
            dunders=options.check_dunders,
            protected_class_methods=options.check_protected_class_methods,
            nested=options.check_nested,
            overridden=options.check_overridden,
            protected=options.check_protected,
            property_returns=options.check_property_returns,
        )
        ignore = _Ignore(
            no_params=options.ignore_no_params,
            args=options.ignore_args,
            kwargs=options.ignore_kwargs,
        )
        return _Config(check=check, ignore=ignore, verbose=options.verbose)

    def run(self) -> _t.Generator[_Flake8Error, None, None]:
        """Run docsig on the file and yield flake8 errors per failure.

        If both class and class-constructor checks are enabled,
        yield one error and return, otherwise run checks with current
        config and yield one (line, col, message, checker_class) per
        failure.

        :return: Generator of flake8-style error tuples.
        """
        if self.a.check_class and self.a.check_class_constructor:
            line = "{msg}".format(
                msg=_FLAKE8.format(
                    ref=_E[5].ref,
                    description=_E[5].description,
                    symbolic=_E[5].symbolic,
                ),
            )
            yield 0, 0, line, self.__class__
        else:
            _setup_logger(self.a.verbose)
            with _cwd_on_sys_path():
                results = _runner(_Path(self.filename), self._build_config())

            for result in results:
                if not result.retcode:
                    continue

                for info in result:
                    line = "{msg} '{name}'".format(
                        msg=_FLAKE8.format(
                            ref=info.ref,
                            description=info.description,
                            symbolic=info.symbolic,
                        ),
                        name=info.name,
                    )
                    yield info.lineno, 0, line, self.__class__
