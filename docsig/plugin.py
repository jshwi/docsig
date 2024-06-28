"""Flake8 implementation of docsig."""

import ast
import contextlib
import io
import re
import sys
import typing as t
from argparse import Namespace

import docsig

Flake8Error = t.Tuple[int, int, str, t.Type]


class Docsig:
    """Flake8 implementation of docsig class.

    :param tree: Ast module, which will not be used by flake8 will
        provide.
    :param filename: Filename to pass to docsig.
    """

    off_by_default = False
    name = docsig.__name__
    version = docsig.__version__
    options_dict: t.Dict[str, bool] = {}

    def __init__(self, tree: ast.Module, filename: str) -> None:
        _tree = tree  # noqa
        self.filename = filename

    # won't import flake8 type
    # conflicts with this module name
    # might require that flake8 actually be installed, which is not a
    # requirement for this package
    @classmethod
    def add_options(cls, parser) -> None:
        """Add flake8 commandline and config options.sig_

        :param parser: Flake8 option manager.
        """
        parser.add_option(
            "--sig-check-class",
            action="store_true",
            parse_from_config=True,
            help="check class docstrings",
        )
        parser.add_option(
            "--sig-check-class-constructor",
            action="store_true",
            parse_from_config=True,
            help="check __init__ methods. Note: mutually incompatible with -c",
        )
        parser.add_option(
            "--sig-check-dunders",
            action="store_true",
            parse_from_config=True,
            help="check dunder methods",
        )
        parser.add_option(
            "--sig-check-protected-class-methods",
            action="store_true",
            parse_from_config=True,
            help="check public methods belonging to protected classes",
        )
        parser.add_option(
            "--sig-check-nested",
            action="store_true",
            parse_from_config=True,
            help="check nested functions and classes",
        )
        parser.add_option(
            "--sig-check-overridden",
            action="store_true",
            parse_from_config=True,
            help="check overridden methods",
        )
        parser.add_option(
            "--sig-check-protected",
            action="store_true",
            parse_from_config=True,
            help="check protected functions and classes",
        )
        parser.add_option(
            "--sig-check-property-returns",
            action="store_true",
            parse_from_config=True,
            help="check property return values",
        )
        parser.add_option(
            "--sig-ignore-no-params",
            action="store_true",
            parse_from_config=True,
            help="ignore docstrings where parameters are not documented",
        )
        parser.add_option(
            "--sig-ignore-args",
            action="store_true",
            parse_from_config=True,
            help="ignore args prefixed with an asterisk",
        )
        parser.add_option(
            "--sig-ignore-kwargs",
            action="store_true",
            parse_from_config=True,
            help="ignore kwargs prefixed with two asterisks",
        )
        parser.add_option(
            "--sig-ignore-typechecker",
            action="store_true",
            parse_from_config=True,
            help="ignore checking return values",
        )

    @classmethod
    def parse_options(cls, options: Namespace) -> None:
        """Parse flake8 options into am instance accessible dict.

        :param options: Argparse namespace.
        """
        cls.options_dict = {
            "check_class": options.sig_check_class,
            "check_class_constructor": options.sig_check_class_constructor,
            "check_dunders": options.sig_check_dunders,
            "check_protected_class_methods": (
                options.sig_check_protected_class_methods
            ),
            "check_nested": options.sig_check_nested,
            "check_overridden": options.sig_check_overridden,
            "check_protected": options.sig_check_protected,
            "check_property_returns": options.sig_check_property_returns,
            "ignore_no_params": options.sig_ignore_no_params,
            "ignore_args": options.sig_ignore_args,
            "ignore_kwargs": options.sig_ignore_kwargs,
            "ignore_typechecker": options.sig_ignore_typechecker,
        }

    def run(self) -> t.Generator[Flake8Error, None, None]:
        """Run docsig and possibly yield a flake8 error.

        :return: Flake8 error, if there is one.
        """
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            sys.argv = [
                __package__,
                self.filename,
                *[
                    f"--{k.replace('_', '-')}"
                    for k, v in self.options_dict.items()
                    if v
                ],
            ]
            docsig.main()

        results = re.split(r"^(?!\s)", buffer.getvalue(), flags=re.MULTILINE)
        for result in results:
            if not result:
                continue

            header, remainder = result.splitlines()[:2]
            lineno, func_name = header.split(":", 1)[1].split(" in ", 1)
            line = f"{remainder.lstrip().replace(':', '')} '{func_name}'"
            yield int(lineno), 0, line, self.__class__
