"""
docsig._parsers
===============
"""

from __future__ import annotations as _

import logging as _logging
import os as _os
from pathlib import Path as _Path

import astroid as _ast

from ._config import Config as _Config
from ._directives import Directives as _Directives
from ._files import FILE_INFO as _FILE_INFO
from ._module import Error as _Error
from ._module import Parent as _Parent


def parse_from_string(
    code: str,
    config: _Config,
    module_name: str = "",
    file: _Path | None = None,
) -> _Parent:
    """Build a Parent from a string of Python code.

    Parses AST and comment directives (AST does not include comments,
    so directives are parsed separately). On syntax error, returns a
    Parent with an error set.

    :param code: Python source to parse.
    :param config: Configuration object.
    :param module_name: Module name, or empty string.
    :param file: Path for the source (or None for stdin).
    :return: Parent for the parsed code or syntax error.
    """
    logger = _logging.getLogger(__package__)
    source_name = file or "stdin"
    try:
        node = _ast.parse(code, module_name, str(file))
        directives = _Directives.from_text(code, config.disable)
        parent = _Parent(
            node,
            directives,
            file,
            config,
        )
        msg = "parsing python code successful"
    except _ast.AstroidSyntaxError as err:
        parent = _Parent(error=_Error.SYNTAX)
        msg = str(err).replace("\n", " ").lower()

    logger.debug(_FILE_INFO, source_name, msg)
    return parent


def parse_from_file(file: _Path, config: _Config) -> _Parent:
    """Build a Parent from a file containing Python code.

    Reads the file and delegates to parse_from_string. On UnicodeError,
    returns a Parent with a Unicode error. On syntax error and a non-.py
    path, returns an empty Parent (not treated as Python).

    :param file: Path to the file to parse.
    :param config: Configuration object.
    :return: Parent for the parsed file or an error/empty Parent.
    """
    try:
        code = file.read_text(encoding="utf-8")
        module_name = str(file)[:-3].replace(_os.sep, ".").replace("-", "_")
        parent = parse_from_string(code, config, module_name, file)
    except UnicodeDecodeError as err:
        logger = _logging.getLogger(__package__)
        logger.debug(_FILE_INFO, file, str(err).replace("\n", " "))
        parent = _Parent(error=_Error.UNICODE)

    if parent.error is not None and not file.name.endswith(".py"):
        parent = _Parent()

    return parent
