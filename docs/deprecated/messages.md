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

| Old  | New    | Description                                               |
|------|--------|-----------------------------------------------------------|
| E101 | SIG402 | parameters out of order                                   |
| E102 | SIG202 | includes parameters that do not exist                     |
| E103 | SIG203 | parameters missing                                        |
| E104 | SIG502 | return statement documented for None                      |
| E105 | SIG503 | return missing from docstring                             |
| E106 | SIG201 | duplicate parameters found                                |
| E107 | SIG303 | parameter appears to be incorrectly documented            |
| E108 | SIG505 | return statement documented for property                  |
| E109 | SIG501 | cannot determine whether a return statement should exist  |
| E110 | SIG404 | documented parameter not equal to its respective argument |
| E111 | SIG504 | return statement documented for class                     |
| E112 | SIG403 | spelling error found in documented parameter              |
| E113 | SIG101 | function is missing a docstring                           |
| E114 | SIG102 | class is missing a docstring                              |
| E115 | SIG302 | syntax error in description                               |
| E116 | SIG401 | param not indented correctly                              |
| E117 | SIG301 | description missing from parameter                        |
| E201 | SIG001 | unknown module comment directive '{directive}'            |
| E202 | SIG002 | unknown inline comment directive '{directive}'            |
| E203 | SIG003 | unknown module comment option for {directive} '{option}'  |
| E204 | SIG004 | unknown inline comment option for {directive} '{option}'  |
