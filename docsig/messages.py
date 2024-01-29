"""
docsig.messages
===============
| E101: parameters out of order
| E102: includes parameters that do not exist
| E103: parameters missing
| E104: return statement documented for None
| E105: return missing from docstring
| E106: duplicate parameters found
| E107: parameter appears to be incorrectly documented
| E108: return statement documented for property
| E109: cannot determine whether a return statement should exist or not
| E110: documented parameter not equal to its respective argument
| E111: return statement documented for class
| E112: spelling error found in documented parameter
| E113: function is missing a docstring
| E114: class is missing a docstring
| E115: syntax error in description
| E116: param not indented correctly
| E201: unknown module comment directive '{directive}'
| E202: unknown inline comment directive '{directive}'
| E203: unknown module comment option for {directive} '{option}'
| E204: unknown inline comment option for {directive} '{option}'
"""

from ._message import Message as _Message
from ._message import Messages as _Messages

TEMPLATE = "{code}: {description} ({symbolic})"


# Exxx: Error
E = _Messages(
    {
        # E1xx: Docstring
        101: _Message(
            "E101",
            "parameters out of order",
            "params-out-of-order",
        ),
        102: _Message(
            "E102",
            "includes parameters that do not exist",
            "params-do-not-exist",
        ),
        103: _Message(
            "E103",
            "parameters missing",
            "params-missing",
        ),
        104: _Message(
            "E104",
            "return statement documented for None",
            "return-documented-for-none",
        ),
        105: _Message(
            "E105",
            "return missing from docstring",
            "return-missing",
            "it is possible a syntax error could be causing this",
        ),
        106: _Message(
            "E106",
            "duplicate parameters found",
            "duplicate-params-found",
        ),
        107: _Message(
            "E107",
            "parameter appears to be incorrectly documented",
            "param-incorrectly-documented",
        ),
        108: _Message(
            "E108",
            "return statement documented for property",
            "return-documented-for-property",
            "documentation is sufficient as a getter is the value returned",
        ),
        109: _Message(
            "E109",
            "cannot determine whether a return statement should exist or not",
            "confirm-return-needed",
        ),
        110: _Message(
            "E110",
            "documented parameter not equal to its respective argument",
            "param-not-equal-to-arg",
        ),
        111: _Message(
            "E111",
            "return statement documented for class",
            "class-return-documented",
            "a class does not return a value during instantiation",
        ),
        112: _Message(
            "E112",
            "spelling error found in documented parameter",
            "spelling-error",
        ),
        113: _Message(
            "E113",
            "function is missing a docstring",
            "function-doc-missing",
        ),
        114: _Message(
            "E114",
            "class is missing a docstring",
            "class-doc-missing",
        ),
        115: _Message(
            "E115",
            "syntax error in description",
            "syntax-error-in-description",
        ),
        116: _Message(
            "E116",
            "param not indented correctly",
            "incorrect-indent",
        ),
        # E2xx: Config
        201: _Message(
            "E201",
            "unknown module comment directive '{directive}'",
            "unknown-module-directive",
        ),
        202: _Message(
            "E202",
            "unknown inline comment directive '{directive}'",
            "unknown-inline-directive",
        ),
        203: _Message(
            "E203",
            "unknown module comment option for {directive} '{option}'",
            "unknown-module-directive-option",
        ),
        204: _Message(
            "E204",
            "unknown inline comment option for {directive} '{option}'",
            "unknown-inline-directive-option",
        ),
    }
)
