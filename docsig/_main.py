"""
docsig._main
============

Contains package entry point.
"""
from ._config import Parser as _Parser
from ._config import get_config as _get_config
from ._core import docsig as _docsig


def main() -> int:
    """Main function for package.

    Collect config and arguments for the commandline.

    :return: Exit status for whether test failed or not.
    """
    config = _get_config()
    parser = _Parser(config)
    return _docsig(
        *parser.args.path,
        string=parser.args.string,
        check_class=parser.args.check_class,
        targets=parser.args.target,
        disable=parser.args.disable
    )
