"""
docsig._report
==============

Format and print docstring-check diagnostics for CLI and tooling.
"""

import json as _json
import os as _os
import sys as _sys
import typing as _t
from dataclasses import dataclass as _dataclass
from warnings import warn as _warn

from ._config import Config as _Config
from ._diagnostic import Failures as _Failures
from ._diagnostic import RetCode as _RetCode
from .messages import NEW as _NEW
from .messages import TEMPLATE as _TEMPLATE
from .messages import E as _E


# pylint: disable=too-few-public-methods
@_dataclass(frozen=True)
class _ReportDiagnostic:
    line: int
    message: str
    exit: int
    extra: str | None = None


# pylint: disable=too-few-public-methods
@_dataclass(frozen=True)
class _ReportEntry:
    name: str
    lineno: int
    file: str | None
    retcode: int
    header: str
    diagnostics: tuple[_ReportDiagnostic, ...]


class _Report(list[_ReportEntry]):
    """Sequence of report entries built from check failures."""

    @property
    def retcode(self) -> int:
        """Maximum exit code across entries."""
        codes = _RetCode()
        for entry in self:
            codes.add(entry.retcode)
        return codes.result


#: values switching the json format off, so that setting the variable
#: to a falsy value reads as off rather than merely as set
_JSON_OFF = frozenset({"", "0", "false", "no", "off"})


def _format_json() -> bool:
    # the private contract editor plugins consume, off unless the
    # variable holds something other than a falsy value
    return _os.getenv("_DOCSIG_FORMAT_JSON", "").lower() not in _JSON_OFF


def _build_report(
    failures: _Failures,
    file: str | None = None,
) -> _Report:
    payload = _Report()
    for result in failures:
        path_prefix = f"{file}:" if file is not None else ""
        header = f"{path_prefix}{result.lineno} in {result.name}"
        diagnostics: list[_ReportDiagnostic] = []
        for item in result:
            extra = None
            if item.hint:
                extra = f"hint: {item.hint}"

            if item.new:
                extra = "warning: please remember to fix this or disable it"
                _warn(
                    _NEW.format(ref=item.ref),
                    FutureWarning,
                    stacklevel=3,
                )

            msg = _TEMPLATE.format(
                ref=item.ref,
                description=item.description,
                symbolic=item.symbolic,
            )
            diagnostics.append(
                _ReportDiagnostic(
                    line=item.lineno,
                    message=msg,
                    exit=result.retcode,
                    extra=extra,
                ),
            )

        payload.append(
            _ReportEntry(
                name=result.name,
                lineno=result.lineno,
                file=file,
                retcode=result.retcode,
                header=header,
                diagnostics=tuple(diagnostics),
            ),
        )

    return payload


def print_checks() -> None:
    """Print all available docstring-check codes and descriptions.

    Output goes to stdout.
    """
    for msg in _E.values():
        print(msg.fstring(_TEMPLATE))


def pretty_print_error(
    exception_type: type[BaseException],
    msg: str,
    no_ansi: bool,
) -> None:
    """Print exception type and message to stderr (ANSI color if tty).

    :param exception_type: Exception class.
    :param msg: Exception message.
    :param no_ansi: If True, do not use ANSI escape codes.
    """
    exception_type_name = exception_type.__name__
    if not no_ansi and _sys.stdout.isatty():
        exception_type_name = f"\033[1;31m{exception_type_name}\033[0m"

    print(f"{exception_type_name}: {msg}", file=_sys.stderr)


def print_error(message: str, retcode: int) -> None:
    """Print an error which cannot be attributed to a line.

    Rendered as json when _DOCSIG_FORMAT_JSON is enabled (the contract
    editor plugins consume), otherwise as text to stderr.

    :param message: Error message to print.
    :param retcode: Exit status the run will finish with.
    """
    if _format_json():
        obj = [{"line": None, "message": message, "exit": retcode}]
        print(_json.dumps(obj).strip())
    else:
        print(message, file=_sys.stderr)


def _to_json(payload: _Report) -> list[dict[str, _t.Any]]:
    # the shape editor plugins consume: a null line number marks a
    # whole-file error
    return [
        {
            "line": None if entry.retcode >= 2 else item.line,
            "message": item.message,
            "exit": item.exit,
        }
        for entry in payload
        for item in entry.diagnostics
    ]


def _to_text(payload: _Report, config: _Config) -> list[str]:
    output: list[str] = []
    for entry in payload:
        header = entry.header
        if not config.no_ansi and _sys.stdout.isatty():
            header = f"\033[35m{header}\033[0m"

        output.append(header)
        for item in entry.diagnostics:
            output.append(f"    {item.message}")
            if item.extra is not None:
                output.append(f"    {item.extra}")

    return output


# TODO: make report json by default and wrap with a reporter for cli
def report(
    failures: _Failures,
    config: _Config,
    file: str | None = None,
) -> int:
    """Print failures and return the highest exit code.

    Builds a report payload from failures, renders it as json when
    _DOCSIG_FORMAT_JSON is enabled (the contract editor plugins
    consume), otherwise as text, then returns the maximum retcode.

    :param failures: Failures to print (one FunctionResult per
        function).
    :param config: Config for ANSI and formatting.
    :param file: Module path when failures came from a file (optional).
    :return: Exit code (non-zero if any check failed).
    """
    payload = _build_report(failures, file)
    if _format_json():
        print(_json.dumps(_to_json(payload)).strip())
    else:
        lines = _to_text(payload, config)
        if lines:
            print("\n".join(lines))

    return payload.retcode
