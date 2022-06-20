"""
docsig._core
============
"""
import ast as _ast
import sys as _sys
import typing as _t
from argparse import ArgumentParser as _ArgumentParser
from itertools import zip_longest as _zip_longest
from pathlib import Path as _Path

from ._function import Docstring as _Docstring
from ._report import Report as _Report
from ._repr import FuncStr as _FuncStr
from ._utils import color as _color
from ._utils import get_index as _get_index
from ._version import __version__

NAME = __name__.split(".", maxsplit=1)[0]

DocArgs = _t.Tuple[_t.Optional[str], ...]
SigArgs = _t.Tuple[_t.Tuple[str, ...], _t.Optional[str]]
DocstringData = _t.Tuple[bool, DocArgs, bool]
FuncData = _t.Tuple[str, SigArgs, _Docstring]
FailedFunc = _t.Tuple[_FuncStr, _Report]
FailedDocData = _t.Dict[str, _t.List[FailedFunc]]


class Parser(_ArgumentParser):
    """Parse commandline arguments."""

    def __init__(self) -> None:
        super().__init__(
            prog=_color.cyan.get(NAME),
            description="Check docstring matches signature",
        )
        self._add_arguments()
        self._version_request()
        self.args = self.parse_args()
        self._version_request()

    def _add_arguments(self) -> None:
        self.add_argument(
            "path",
            action="store",
            type=_Path,
            help="directory or file to check",
        )
        self.add_argument(
            "-v",
            "--version",
            action="store_true",
            help="show version and exit",
        )

    @staticmethod
    def _version_request() -> None:
        if len(_sys.argv) > 1 and _sys.argv[1] == "--version":
            print(__version__)
            _sys.exit(0)


def _get_returns(func: _ast.FunctionDef) -> _t.Optional[str]:
    if func.returns is not None:
        if isinstance(func.returns, _ast.Name):
            return func.returns.id

        if isinstance(func.returns, _ast.Subscript):
            if isinstance(func.returns.value, _ast.Name):
                return func.returns.value.id

            if isinstance(func.returns.value, _ast.Attribute):
                return func.returns.value.attr

    return None


def _get_args(func: _ast.FunctionDef) -> _t.Tuple[str, ...]:
    args = [a.arg for a in func.args.args if a.arg != "_"]
    if func.args.vararg is not None:
        args.append(f"*{func.args.vararg.arg}")

    if func.args.kwarg is not None:
        args.append(f"**{func.args.kwarg.arg}")

    return tuple(args)


# collect a tuple of function information values
def _get_func_data(path: _Path) -> _t.List[FuncData]:
    node = _ast.parse(path.read_text(), filename=str(path))
    # noinspection PyUnresolvedReferences
    return [
        (
            f.name,
            (_get_args(f), _get_returns(f)),
            _Docstring(f),  # type: ignore
        )
        for f in node.body
        if isinstance(f, _ast.FunctionDef) and not str(f.name).startswith("_")
    ]


def get_members(
    paths: _t.List[_Path],
) -> _t.Tuple[_t.Tuple[str, _t.List[FuncData]], ...]:
    """Get a tuple of module names paired with function information.

    :param paths: Paths to parse for function information.
    :return: A tuple of module level function values.
    """
    return tuple((str(p), _get_func_data(p)) for p in paths)


def get_files(root: _Path, paths: _t.List[_Path]) -> None:
    """Get files belonging to the provided package.

    :param root: The path where to check for files.
    :param paths: List to populate.
    """
    if root.is_file() and str(root.name).endswith(".py"):
        paths.append(root)

    if root.is_dir():
        for path in root.iterdir():
            get_files(path, paths)


def _compare_args(arg: _t.Optional[str], doc: _t.Optional[str]) -> bool:
    if isinstance(arg, str):
        arg = arg.replace("*", "")

    return arg == doc and arg is not None and doc is not None


def construct_func(
    func: str, args: SigArgs, docstring: _Docstring
) -> _t.Optional[FailedFunc]:
    """Construct a string representation of function and docstring info.

    Return None if the test passed.

    :param func: Function name.
    :param args: Tuple of signature parameters.
    :param docstring: Docstring parameters.
    :return: String if test fails else None.
    """
    report = _Report()
    func_str = _FuncStr(func)
    params, arg_returns = args
    report.exists(params, docstring.args)
    report.missing(params, docstring.args)
    report.duplicates(docstring.args)
    for count, _ in enumerate(_zip_longest(params, docstring.args)):
        longest = max([len(params), len(docstring.args)])
        arg = _get_index(count, params)
        doc = _get_index(count, docstring.args)
        if _compare_args(arg, doc):
            func_str.add_param(arg, doc)
        else:
            func_str.add_param(arg, doc, failed=True)
            report.order(arg, doc, params, docstring.args)
            report.incorrect(arg, doc)

        if count + 1 != longest:
            func_str.add_comma()

    func_str.set_mark()
    if docstring.returns and arg_returns:
        func_str.add_return()
    elif (
        docstring.returns
        and not arg_returns
        or arg_returns
        and not docstring.returns
    ):
        func_str.add_return(failed=True)

    func_str.close_sig(arg_returns)
    report.extra_return(docstring.returns, arg_returns)
    report.missing_return(docstring.returns, arg_returns)
    func_str.close_docstring()
    func_str.render()
    if report:
        return func_str, report

    return None


def print_failures(failures: FailedDocData) -> None:
    """Print failed tests.

    :param failures: Tuple of module names containing a list of failed
        functions.
    """
    for module, funcs in failures.items():
        for func, summary in funcs:
            _color.magenta.print(module)
            print(len(module) * "-")
            print(f"{func}\n{summary.get_report()}")
