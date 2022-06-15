"""
docsig._core
============
"""
import ast as _ast
import sys as _sys
import typing as _t
import warnings as _warnings
from argparse import ArgumentParser as _ArgumentParser
from itertools import zip_longest as _zip_longest
from pathlib import Path as _Path

from object_colors import Color as _Color
from pygments import highlight as _highlight
from pygments.formatters.terminal256 import (
    Terminal256Formatter as _Terminal256Formatter,
)

# noinspection PyUnresolvedReferences
from pygments.lexers.python import PythonLexer as _PythonLexer

from ._version import __version__

color = _Color()

color.populate_colors()

NAME = __name__.split(".", maxsplit=1)[0]
CHECK = color.green.get("\u2713")
CROSS = color.red.get("\u2716")
TRIPLE_QUOTES = '"""'
TAB = "    "

DocArgs = _t.Tuple[_t.Optional[str], ...]
SigArgs = _t.Tuple[str, ...]
DocstringData = _t.Tuple[bool, DocArgs]
FuncData = _t.Tuple[str, SigArgs, DocstringData]
FuncDataList = _t.List[FuncData]
ModuleData = _t.Tuple[str, FuncDataList]
FailedDocData = _t.Dict[str, _t.List[str]]
MissingDocList = _t.List[_t.Tuple[str, str]]
MemberData = _t.Tuple[ModuleData, ...]
PathList = _t.List[_Path]


class Parser(_ArgumentParser):
    """Parse commandline arguments."""

    def __init__(self) -> None:
        super().__init__(
            prog=color.cyan.get(NAME),
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


# get index without throwing an error if index does not exist
def _get_index(index: int, params: _t.Sequence) -> _t.Optional[str]:
    try:
        return params[index]
    except IndexError:
        return None


# parse docstring into a tuple of documentation and parameters
def _parse_docstring(docstring: _t.Optional[str] = None) -> DocstringData:
    if docstring is None:
        # noinspection PyRedundantParentheses
        return False, tuple()

    return True, tuple(
        _get_index(1, s.split())
        for s in docstring.split(":")
        if s.startswith("param")
    )


# collect a tuple of function information values
def _get_func_data(path: _Path) -> _t.List[FuncData]:
    node = _ast.parse(path.read_text(), filename=str(path))
    return [
        (
            f.name,
            tuple(a.arg for a in f.args.args),
            _parse_docstring(_ast.get_docstring(f)),
        )
        for f in node.body
        if isinstance(f, _ast.FunctionDef) and not str(f.name).startswith("_")
    ]


# Add syntax highlighting to string.
def _lexer(value: str) -> str:
    formatter = _Terminal256Formatter(style="monokai")
    return _highlight(value, _PythonLexer(), formatter).strip()


def get_members(paths: PathList) -> MemberData:
    """Get a tuple of module names paired with function information.

    :param paths: Paths to parse for function information.
    :return: A tuple of module level function values.
    """
    return tuple((str(p), _get_func_data(p)) for p in paths)


def get_files(root: _Path, paths: PathList) -> None:
    """Get files belonging to the provided package.

    :param root: The path where to check for files.
    :param paths: List to populate.
    """
    if root.is_file() and str(root.name).endswith(".py"):
        paths.append(root)

    if root.is_dir():
        for path in root.iterdir():
            get_files(path, paths)


def construct_func(
    func: str, args: SigArgs, docstring: DocArgs
) -> _t.Optional[str]:
    """Construct a string representation of function and docstring info.

    Return None if the test passed.

    :param func: Function name.
    :param args: Tuple of signature parameters.
    :param docstring: Tuple of docstring parameters.
    :return: String if test fails else None.
    """
    failed = False
    func_str = _lexer(f"def {func}(").strip()
    doc_str = f"{_lexer(f'{TAB}{TRIPLE_QUOTES}...')}\n"
    for count, _ in enumerate(_zip_longest(args, docstring)):
        longest = max([len(args), len(docstring)])
        arg = _get_index(count, args)
        doc = _get_index(count, docstring)
        (mark, failed) = (CHECK, False) if arg == doc else (CROSS, True)
        func_str += f"{mark}{arg}"
        doc_str += f"\n{TAB}:param {doc}: {mark}"
        if count + 1 != longest:
            func_str += _lexer(", ")

    func_str += "):"
    doc_str += f"\n{TAB}{_lexer(TRIPLE_QUOTES)}\n"
    if failed:
        return f"{func_str}\n{doc_str}"

    return None


def print_failures(failures: FailedDocData) -> None:
    """Print failed tests.

    :param failures: Tuple of module names containing a list of failed
        functions.
    """
    for module, funcs in failures.items():
        if funcs:
            color.magenta.print(module)
            print(len(module) * "-")
            print("\n".join(funcs))


def warn(missing: MissingDocList) -> None:
    """Warn if function does not contain a docstring.

    :param missing: Tuple of module names containing a list of function
        to warn for.
    """
    for module, func in missing:
        _warnings.warn(f"{module}::{func} is missing a docstring")
