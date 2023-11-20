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
# Exxx: Error
# E1xx: Docstring
E101 = "E101: parameters out of order"
E102 = "E102: includes parameters that do not exist"
E103 = "E103: parameters missing"
E104 = "E104: return statement documented for None"
E105 = "E105: return missing from docstring"
E106 = "E106: duplicate parameters found"
E107 = "E107: parameter appears to be incorrectly documented"
E108 = "E108: return statement documented for property"
E109 = "E109: cannot determine whether a return statement should exist or not"
E110 = "E110: documented parameter not equal to its respective argument"
E111 = "E111: return statement documented for class"
E112 = "E112: spelling error found in documented parameter"
E113 = "E113: function is missing a docstring"
E114 = "E114: class is missing a docstring"
E115 = "E115: syntax error in description"
E116 = "E116: param not indented correctly"

# E2xx: Config
E201 = "E201: unknown module comment directive '{directive}'"
E202 = "E202: unknown inline comment directive '{directive}'"
E203 = "E203: unknown module comment option for {directive} '{option}'"
E204 = "E204: unknown inline comment option for {directive} '{option}'"

# Hxxx: Hint
# H1xx: Docstring
H101 = "hint: documentation is sufficient as a getter is the value returned"
H102 = "hint: it is possible a syntax error could be causing this"
H103 = "hint: a class does not return a value during instantiation"
