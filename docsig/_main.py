"""
docsig._main
============

Contains package entry point.
"""
from ._config import Parser as _Parser
from ._config import get_config as _get_config
from ._core import populate as _populate
from ._core import print_failures as _print_failures
from ._module import Modules as _Modules


def main() -> int:
    """Main function for package.

    :return: Exit status for whether test failed or not.
    """
    failed = False
    config = _get_config()
    parser = _Parser(config)
    modules = _Modules(*parser.args.path)
    for module in modules:
        for top_level in module:
            module_data = _populate(
                top_level, parser.args.target, parser.args.disable
            )
            if module_data:
                failed = True
                _print_failures(top_level.name, module_data)

    return failed
