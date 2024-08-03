---
orphan: true
---

# New Messages

The messages have been updated in v0.56.0

Messages have been grouped more logically after accumulating for a period of
time incrementally

The prefix has also been changed to make migration easier. This way old messages
can still be used without conflict

Old messages are no longer documented, apart from here, and are now considered
deprecated

If any old disable or target rules are used for your pipeline (as well as any
old comment directives), please update them with the help of the below table to
avoid any issues once the old messages are removed

| New    | Old  | Description                                               |
|--------|------|-----------------------------------------------------------|
| SIG001 | E201 | unknown module comment directive '{directive}'            |
| SIG002 | E202 | unknown inline comment directive '{directive}'            |
| SIG003 | E203 | unknown module comment option for {directive} '{option}'  |
| SIG004 | E204 | unknown inline comment option for {directive} '{option}'  |
| SIG101 | E113 | function is missing a docstring                           |
| SIG102 | E114 | class is missing a docstring                              |
| SIG201 | E106 | duplicate parameters found                                |
| SIG202 | E102 | includes parameters that do not exist                     |
| SIG203 | E103 | parameters missing                                        |
| SIG301 | E117 | description missing from parameter                        |
| SIG302 | E115 | syntax error in description                               |
| SIG303 | E107 | parameter appears to be incorrectly documented            |
| SIG401 | E116 | param not indented correctly                              |
| SIG402 | E101 | parameters out of order                                   |
| SIG403 | E112 | spelling error found in documented parameter              |
| SIG404 | E110 | documented parameter not equal to its respective argument |
| SIG501 | E109 | cannot determine whether a return statement should exist  |
| SIG502 | E104 | return statement documented for None                      |
| SIG503 | E105 | return missing from docstring                             |
| SIG504 | E111 | return statement documented for class                     |
| SIG505 | E108 | return statement documented for property                  |
