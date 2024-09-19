"""Persistent runtime config."""

from __future__ import annotations

import os as _os
import re as _re
import typing as _t
from argparse import Action as _Action
from argparse import ArgumentParser as _ArgumentParser
from argparse import HelpFormatter as _HelpFormatter
from argparse import Namespace as _Namespace
from pathlib import Path as _Path

import mergedeep as _mergedeep
import tomli as _tomli

PYPROJECT_TOML = "pyproject.toml"
ANSI_ESCAPE = _re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


class _FormatterClass(_t.Protocol):  # pylint: disable=too-few-public-methods
    def __call__(self, prog: str) -> _HelpFormatter:
        """Callable type for ``ArgumentParser.formatter_class``."""


# split str by comma, but allow for escaping
def _split_comma(value: str) -> list[str]:
    return [i.replace("\\,", ",") for i in _re.split(r"(?<!\\),", value)]


# attempt to locate a pyproject.toml file if one exists in parents
def _find_pyproject_toml(path: _Path | None = None) -> _Path | None:
    if not path:
        path = _Path.cwd()

    pyproject_toml = path / PYPROJECT_TOML
    if pyproject_toml.is_file():
        return pyproject_toml

    if str(path) == _os.path.abspath(_os.sep):
        return None

    return _find_pyproject_toml(path.parent)


# Get config dict object from package's tool section in toml file.
def _get_config(prog: str) -> dict[str, _t.Any]:
    pyproject_file = _find_pyproject_toml()
    if pyproject_file is None:
        return {}

    return (
        _tomli.loads(pyproject_file.read_text()).get("tool", {}).get(prog, {})
    )


class _DictAction(_Action):  # pylint: disable=too-few-public-methods
    def __call__(
        self,
        parser: _ArgumentParser,
        namespace: _Namespace,
        values: str | _t.Sequence[_t.Any] | None = None,
        _: str | None = None,
    ) -> None:
        if values is not None:
            try:
                dest = {
                    k: _split_comma(v)
                    for i in values
                    for k, v in [i.split("=")]
                }
                setattr(namespace, self.dest, dest)
            except ValueError:
                pass


class ArgumentParser(_ArgumentParser):
    """Parse commandline arguments.

    :param version: Version of package, if there is one.
    :param prog: The name of the program (default: sys.argv[0]).
    :param usage: A usage message (default: auto-generated from
        arguments).
    :param description: A description of what the program does.
    :param epilog: Text following the argument descriptions.
    :param parents: Parsers whose arguments should be copied into this
        one.
    :param formatter_class: HelpFormatter class for printing help
        messages.
    :param prefix_chars: Characters that prefix optional arguments.
    :param fromfile_prefix_chars: Characters that prefix files
        containing additional arguments.
    :param argument_default: The default value for all arguments.
    :param conflict_handler: String indicating how to handle conflicts.
    :param add_help: Add a -h/-help option.
    :param allow_abbrev: Allow long options to be abbreviated
        unambiguously.
    :param config: A dict object containing default values for parser.
        If no dict object provided than a pyproject.toml file will be
        loaded.
    :param version_short_form: Alternative short form for version.
    """

    # noinspection PyDefaultArgument
    # pylint: disable=dangerous-default-value,too-many-arguments
    # pylint: disable=too-many-locals
    def __init__(
        self,
        version: str,
        prog: str | None = None,
        usage: str | None = None,
        description: str | None = None,
        epilog: str | None = None,
        parents: _t.Sequence[ArgumentParser] = [],  # noqa
        formatter_class: _FormatterClass = _HelpFormatter,
        prefix_chars: str = "-",
        fromfile_prefix_chars: str | None = None,
        argument_default: _t.Any = None,
        conflict_handler: str = "error",
        add_help: bool = True,
        allow_abbrev: bool = True,
        config: dict[str, _t.Any] | None = None,
        version_short_form: str = "-v",
    ) -> None:
        super().__init__(
            prog,
            usage,
            description,
            epilog,
            parents,
            formatter_class,
            prefix_chars,
            fromfile_prefix_chars,
            argument_default,
            conflict_handler,
            add_help,
            allow_abbrev,
        )
        self.add_argument(
            version_short_form, "--version", action="version", version=version
        )
        self._config = {
            k.replace("-", "_"): v
            for k, v in _mergedeep.merge(
                _get_config(ANSI_ESCAPE.sub("", self.prog)),
                config or {},
                strategy=_mergedeep.Strategy.ADDITIVE,
            ).items()
        }

    def parse_known_args(  # type: ignore
        self,
        args: _t.Sequence[str] | None = None,
        namespace: _Namespace | None = None,
    ) -> tuple[_Namespace | None, list[str]]:
        namespace, args = super().parse_known_args(args, namespace)
        namedict = namespace.__dict__
        for key, value in self._config.items():
            if key in namedict and namedict[key] in (None, False):
                namedict[key] = value

        namespace.__dict__ = _mergedeep.merge(
            self._config, namedict, strategy=_mergedeep.Strategy.ADDITIVE
        )
        return namespace, args

    def add_list_argument(self, *args: str, **kwargs: _t.Any) -> None:
        """Parse a comma separated list of strings into a list.

        :param args: Long and/or short form argument(s).
        :param kwargs: Kwargs to pass to ``add_argument``.
        """
        kwargs.update(
            {
                "action": "store",
                "type": _split_comma,
                "default": kwargs.get("default", []),
            }
        )
        self.add_argument(*args, **kwargs)

    def add_dict_argument(
        self, *args: str, nargs: str = "*", **kwargs: _t.Any
    ) -> None:
        """Parse key(s) of comma separated lists of strings into a dict.

        :param args: Long and/or short form argument(s).
        :param nargs: Nargs to pass to ``add_argument``.
        :param kwargs: Kwargs to pass to ``add_argument``.
        """
        kwargs.update(
            {
                "action": _DictAction,
                "default": kwargs.get("default", {}),
                "nargs": nargs,
            }
        )
        self.add_argument(*args, **kwargs)
