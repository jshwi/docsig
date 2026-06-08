"""
docsig._report
==============

Format and print docstring-check diagnostics for CLI and tooling.
"""

import json as _json
import os as _os
import sys as _sys
from warnings import warn as _warn

from ._config import Config as _Config
from ._diagnostic import Failures as _Failures
from ._diagnostic import FunctionResult as _FunctionResult
from ._diagnostic import RetCode as _RetCode
from ._function_checks import FunctionChecker as _FunctionChecker
from ._module import Function as _Function
from .messages import NEW as _NEW
from .messages import TEMPLATE as _TEMPLATE


def check_function(func: _Function, config: _Config) -> _FunctionResult:
    """Run configured checks for one function and return the result.

    :param func: Function under check.
    :param config: Configuration object.
    :return: Collected diagnostics for the function.
    """
    return _FunctionChecker(func, config).run()


# TODO: make report json by default and wrap with a reporter for cli
def report(
    failures: _Failures,
    config: _Config,
    file: str | None = None,
) -> int:
    """Print failures and return the highest exit code.

    Iterates over failures, prints each with path, line header, and
    messages, then returns the maximum retcode (0 or non-zero).

    :param failures: Failures to print (one FunctionResult per
        function).
    :param config: Config for ANSI and formatting.
    :param file: Module path when failures came from a file (optional).
    :return: Exit code (non-zero if any check failed).
    """
    format_json = _os.getenv("_DOCSIG_FORMAT_JSON") is not None
    retcodes = _RetCode()
    output = []
    obj = []
    for result in failures:
        retcodes.add(result.retcode)
        path_prefix = f"{file}:" if file is not None else ""
        header = f"{path_prefix}{result.lineno} in {result.name}"
        if not config.no_ansi and _sys.stdout.isatty():
            header = f"\033[35m{header}\033[0m"

        output.append(header)
        for item in result:
            extra = None
            if item.hint:
                extra = f"hint: {item.hint}"

            if item.new:
                extra = "warning: please remember to fix this or disable it"
                _warn(_NEW.format(ref=item.ref), FutureWarning, stacklevel=3)

            msg = _TEMPLATE.format(
                ref=item.ref,
                description=item.description,
                symbolic=item.symbolic,
            )
            output.append(f"    {msg}")
            if extra is not None:
                output.append(f"    {extra}")

            obj.append(
                {
                    "line": None if result.retcode == 2 else item.lineno,
                    "message": msg,
                    "exit": result.retcode,
                },
            )

    if format_json:
        print(_json.dumps(obj).strip())  # pragma: no cover

    elif output:
        print("\n".join(output))

    return retcodes.result
