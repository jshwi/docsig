"""
docsig._main
============

Contains package entry point.
"""

from __future__ import annotations as _

from ._config import Parser as _Parser
from ._core import docsig as _docsig
from ._hooks import excepthook as _excepthook


def main() -> str | int:
    """Main function for package.

    Collect config and arguments for the commandline.

    :return: Exit status for whether test failed or not.
    """
    p = _Parser()
    _excepthook(p.args.no_ansi)
    return _docsig(
        *p.args.path,
        string=p.args.string,
        list_checks=p.args.list_checks,
        check_class=p.args.check_class,
        check_class_constructor=p.args.check_class_constructor,
        check_dunders=p.args.check_dunders,
        check_protected_class_methods=p.args.check_protected_class_methods,
        check_nested=p.args.check_nested,
        check_overridden=p.args.check_overridden,
        check_protected=p.args.check_protected,
        check_property_returns=p.args.check_property_returns,
        include_ignored=p.args.include_ignored,
        ignore_no_params=p.args.ignore_no_params,
        ignore_args=p.args.ignore_args,
        ignore_kwargs=p.args.ignore_kwargs,
        no_ansi=p.args.no_ansi,
        summary=p.args.summary,
        verbose=p.args.verbose,
        targets=p.args.target,
        disable=p.args.disable,
        exclude=p.args.exclude,
    )
