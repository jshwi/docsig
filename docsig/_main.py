"""
docsig._main
============

Contains package entry point.
"""
from ._core import FailedDocData as _FailedDocData
from ._core import MissingDocList as _MissingDocList
from ._core import Parser as _Parser
from ._core import PathList as _PathList
from ._core import construct_func as _construct_func
from ._core import get_files as _get_files
from ._core import get_members as _get_members
from ._core import print_failures as _print_failures
from ._core import warn as _warn


def main() -> int:
    """Main function for package."""
    failed = False
    paths: _PathList = []
    failures: _FailedDocData = {}
    missing: _MissingDocList = []
    parser = _Parser()
    _get_files(parser.args.path, paths)
    members = _get_members(paths)
    for module, func_data in members:
        failures[module] = []
        if func_data:
            for func, args, (is_doc, docstring) in func_data:
                if not is_doc:
                    missing.append((module, func))
                else:
                    func_str = _construct_func(func, args, docstring)
                    if func_str is not None:
                        failures[module].append(func_str)
                        failed = True

    _print_failures(failures)
    _warn(missing)
    return int(failed)
