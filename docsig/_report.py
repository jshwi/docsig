"""
docsig._report
==============

Format and print docstring-check diagnostics for CLI and tooling.
"""

import json as _json
import os as _os
import sys as _sys
from dataclasses import dataclass as _dataclass
from warnings import warn as _warn

from ._config import Config as _Config
from ._diagnostic import Failures as _Failures
from ._diagnostic import RetCode as _RetCode
from .messages import NEW as _NEW
from .messages import TEMPLATE as _TEMPLATE


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


# TODO: make report json by default and wrap with a reporter for cli
def report(
    failures: _Failures,
    config: _Config,
    file: str | None = None,
) -> int:
    """Print failures and return the highest exit code.

    Builds a report payload from failures, prints each entry with path,
    line header, and messages, then returns the maximum retcode.

    :param failures: Failures to print (one FunctionResult per
        function).
    :param config: Config for ANSI and formatting.
    :param file: Module path when failures came from a file (optional).
    :return: Exit code (non-zero if any check failed).
    """
    payload = _build_report(failures, file)
    format_json = _os.getenv("_DOCSIG_FORMAT_JSON") is not None
    output = []
    obj = []
    for result in payload:
        header = result.header
        if not config.no_ansi and _sys.stdout.isatty():
            header = f"\033[35m{header}\033[0m"

        output.append(header)
        for item in result.diagnostics:
            output.append(f"    {item.message}")
            if item.extra is not None:
                output.append(f"    {item.extra}")

            obj.append(
                {
                    "line": None if result.retcode == 2 else item.line,
                    "message": item.message,
                    "exit": item.exit,
                },
            )

    if format_json:
        print(_json.dumps(obj).strip())  # pragma: no cover

    elif output:
        print("\n".join(output))

    return payload.retcode
