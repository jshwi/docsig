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

_TEMPLATE = "{code}: {description}"
_HINT_TEMPLATE = "hint: {hint}"


# Exxx: Error
E = _Messages(
    {
        # E1xx: Docstring
        101: _Message(
            "E101",
            "parameters out of order",
        ),
        102: _Message(
            "E102",
            "includes parameters that do not exist",
        ),
        103: _Message(
            "E103",
            "parameters missing",
        ),
        104: _Message(
            "E104",
            "return statement documented for None",
        ),
        105: _Message(
            "E105",
            "return missing from docstring",
            "it is possible a syntax error could be causing this",
        ),
        106: _Message(
            "E106",
            "duplicate parameters found",
        ),
        107: _Message(
            "E107",
            "parameter appears to be incorrectly documented",
        ),
        108: _Message(
            "E108",
            "return statement documented for property",
            "documentation is sufficient as a getter is the value returned",
        ),
        109: _Message(
            "E109",
            "cannot determine whether a return statement should exist or not",
        ),
        110: _Message(
            "E110",
            "documented parameter not equal to its respective argument",
        ),
        111: _Message(
            "E111",
            "return statement documented for class",
            "a class does not return a value during instantiation",
        ),
        112: _Message(
            "E112",
            "spelling error found in documented parameter",
        ),
        113: _Message(
            "E113",
            "function is missing a docstring",
        ),
        114: _Message(
            "E114",
            "class is missing a docstring",
        ),
        115: _Message(
            "E115",
            "syntax error in description",
        ),
        116: _Message(
            "E116",
            "param not indented correctly",
        ),
        # E2xx: Config
        201: _Message(
            "E201",
            "unknown module comment directive '{directive}'",
        ),
        202: _Message(
            "E202",
            "unknown inline comment directive '{directive}'",
        ),
        203: _Message(
            "E203",
            "unknown module comment option for {directive} '{option}'",
        ),
        204: _Message(
            "E204",
            "unknown inline comment option for {directive} '{option}'",
        ),
    }
)


# Exxx: Error
# E1xx: Docstring
E101 = str(E[101].fstring(_TEMPLATE))
E102 = str(E[102].fstring(_TEMPLATE))
E103 = str(E[103].fstring(_TEMPLATE))
E104 = str(E[104].fstring(_TEMPLATE))
E105 = str(E[105].fstring(_TEMPLATE))
E106 = str(E[106].fstring(_TEMPLATE))
E107 = str(E[107].fstring(_TEMPLATE))
E108 = str(E[108].fstring(_TEMPLATE))
E109 = str(E[109].fstring(_TEMPLATE))
E110 = str(E[110].fstring(_TEMPLATE))
E111 = str(E[111].fstring(_TEMPLATE))
E112 = str(E[112].fstring(_TEMPLATE))
E113 = str(E[113].fstring(_TEMPLATE))
E114 = str(E[114].fstring(_TEMPLATE))
E115 = str(E[115].fstring(_TEMPLATE))
E116 = str(E[116].fstring(_TEMPLATE))

# E2xx: Config
E201 = str(E[201].fstring(_TEMPLATE))
E202 = str(E[202].fstring(_TEMPLATE))
E203 = str(E[203].fstring(_TEMPLATE))
E204 = str(E[204].fstring(_TEMPLATE))

# Hxxx: Hint
# H1xx: Docstring
H101 = _HINT_TEMPLATE.format(hint=E[108].hint)
H102 = _HINT_TEMPLATE.format(hint=E[105].hint)
H103 = _HINT_TEMPLATE.format(hint=E[111].hint)
