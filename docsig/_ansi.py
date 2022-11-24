"""
docsig._ansi
============
"""
import typing as _t

from object_colors import Color as _Color
from pygments import highlight as _highlight
from pygments.formatters.terminal256 import (
    Terminal256Formatter as _Terminal256Formatter,
)

# noinspection PyUnresolvedReferences
from pygments.lexers.python import PythonLexer as _PythonLexer

color = _Color()

color.populate_colors()


class ANSI:
    """Get ANSI strings.

    :param no_ansi: Return string without color if True.
    """

    def __init__(self, no_ansi: bool = False) -> None:
        self._no_ansi = no_ansi

    def get_color(self, obj: _t.Any, color_obj: _Color) -> str:
        """Get string with selected color.

        :param obj: Any object, represented as ``__str__``.
        :param color_obj: Instantiated ``Color`` object.
        :return: Colored string or string as was supplied.
        """
        string = str(obj)
        if not self._no_ansi:
            return color_obj.get(obj)

        return string

    def get_syntax(self, value: str) -> str:
        """Get code representation with syntax highlighting.

        :param value: String object to highlight.
        :return: Colored string or string as was supplied.
        """
        if self._no_ansi:
            return value

        formatter = _Terminal256Formatter(style="monokai")
        return _highlight(value, _PythonLexer(), formatter).strip()
