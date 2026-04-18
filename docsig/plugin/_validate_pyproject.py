"""
docsig.plugin._validate_pyproject
=================================
"""

# pylint: disable=protected-access

import typing as _t

# noinspection PyFinal
from argparse import SUPPRESS as _SUPPRESS
from argparse import Action as _Action

import docsig as _docsig

from .._config import build_parser as _build_parser

_ID = "https://docsig.io/en/latest/usage/configuration/schema.json"
_SCHEMA = "http://json-schema.org/draft-07/schema#"
_DESCRIPTION_EXCLUDE = ("comma separated ",)
_NARGS = ("+", "*")
_EXCLUDED_OPTIONS = ("help", "list-checks", "string", "version")


class ValidatePyproject(dict[str, _t.Any]):
    """Schema for the docsig tool section in pyproject.toml.

    :param tool_name: The tool name to validate.
    """

    def __init__(self, tool_name: str = "docsig") -> None:
        assert tool_name == "docsig", "Only docsig is supported."
        self._parser = _build_parser()
        super().__init__(
            {
                "$comment": _CMT,
                "$id": _ID,
                "$schema": _SCHEMA,
                "type": "object",
                "additionalProperties": False,
            },
        )
        self._get_properties()
        self._get_mutually_exclusive_options()

    @staticmethod
    def _skip_action(action: _Action, name: str) -> bool:
        if not action.option_strings:
            return True

        if action.help == _SUPPRESS:
            return True

        if name in _EXCLUDED_OPTIONS:
            return True

        return False

    def _get_properties(self) -> None:
        self["properties"] = {}
        for action in self._parser._actions:
            name = action.dest.replace("_", "-")
            if self._skip_action(action, name):
                continue

            self["properties"][name] = {"default": action.default}
            if isinstance(action.default, bool):
                self["properties"][name]["type"] = "boolean"
            elif isinstance(action.default, list) or action.nargs in _NARGS:
                self["properties"][name]["type"] = "array"
                self["properties"][name]["items"] = {"type": "string"}
            elif action.type is None:
                self["properties"][name]["type"] = "string"

            if action.help:
                description = action.help
                for exclude in _DESCRIPTION_EXCLUDE:
                    description = description.replace(exclude, "")

                self["properties"][name]["description"] = description

    def _get_mutually_exclusive_options(self) -> None:
        for group in self._parser._mutually_exclusive_groups:
            names = []
            for action in group._group_actions:
                name = action.dest.replace("_", "-")
                if self._skip_action(action, name):
                    continue

                names.append(name)

            if len(names) > 1:
                if "allOf" not in self:
                    self["allOf"] = []

                self["allOf"].append({"not": {"required": names}})


_CMT = ValidatePyproject.__doc__.splitlines()[0].lower()[:-1]  # type: ignore

# for
# $ validate-pyproject --help
ValidatePyproject.__doc__ = _docsig.__doc__
