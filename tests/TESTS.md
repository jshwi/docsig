<!--
This file is auto-generated and any changes made to it will be overwritten
-->
# tests

Test suite of docsig.

Most tests run with all the args that start with `check`, so passing
or failing of most tests depend on these passing. This means, by
default, that templates including classes, magic methods, overridden
methods, protected methods, and property returns, will be checked, even
though by default they aren’t.

There are separate tests written to exclude these particular flags.
Their templates contain a specific string to include them in these
special case tests.

Some tests overlap, which is why some templates are found by their
prefix, their suffix, or whether they simply contain a substring.

All templates ending with `S` are `Sphinx` style docstrings, all
templates ending with `N` are `NumPy` style docstrings, all
templates ending with `NI` are `NumPy` style docstrings with an
unusual indent, and all templates ending with `G` are `Google` style
docstrings.


### Disable rule

Test disabling of errors.

Confirm that templates testing specific error codes, passed as a
disable argument, do not result in a failed run.

Any of the tests that would normally raise the particular error
should pass with the error disabled.

This test only tests templates prefixed with `F<ERROR_CODE>`.

Expected result for these tests are derived from
`docsig.messages`.


### Error codes

Test expected error codes are emitted to stdout.

All templates containing `SingleError` are tested for error codes.

Expected result for these tests are derived from
`docsig.messages`.


### Exit status

Test for passing and failing checks.

All templates prefixed with `P` will be tested for zero exit
status.

All templates prefixed with `F` will be tested for non-zero exit
status.

All templates prefixed with `M` will be excluded from this test,
as this tests multiple functions in a file, some that may pass and
some that may fail.


### Ignore args

Test that for passing/failing tests with `-a/--ignore-args`.

Test that docs without args, where the signature contains args,
don’t fail with `-a/--ignore-args`.

All templates containing args in their signature must have WArgs in
their name.

Passing templates with `WArgs` will fail and failing tests with
`WArgs` will pass, as tests which pass will have args documented,
which shouldn’t be to pass with this check. All other tests will
have the usual result.

All templates prefixed with `M` will be excluded from this test,
as this tests multiple functions in a file, some that may pass and
some that may fail.


### Ignore kwargs

Test that for passing/failing tests with `-k/--ignore-kwargs`.

Test that docs without args, where the signature contains args,
don’t fail with `-k/--ignore-kwargs`.

All templates containing args in their signature must have
`WKwargs` their name.

Passing templates with `WKwargs` will fail and failing tests with
`WKwargs` will pass, as tests which pass will have args documented,
which shouldn’t be to pass with this check. All other tests will
have the usual result.

All templates prefixed with `M` will be excluded from this test,
as this tests multiple functions in a file, some that may pass and
some that may fail.


### Ignore no params

Test that failing funcs pass with -i/–ignore-no-params flag.

`E103`, `E105`, `E109`, and `H102` all indicate parameters
missing from docstring. These should not trigger with this argument.

All templates prefixed with `M` will be excluded from this test,
as this tests multiple functions in a file, some that may pass and
some that may fail.


### Multiple

Test for correct output for modules with multiple functions.

Only test templates prefixed with `M`, as these are designated
templates containing 2 or more functions. There templates are
generally excluded from other tests.


### No check property returns flag

Test that passing property fails without `-P` flag.

Only test templates prefixed with `PProperty` are collected for
this test, and all tests should fail.

All tests will be tested for `E108` and `H101`, which property
related errors.


### No flag

Test that failing tests pass without their corresponding flag.

All tests that fail such as with `--check-class` should be
prefixed with `FClass`, and these particular tests should all
pass.


### No stdout

Test that all tests emit no output.

Only test templates prefixed with P are collected for this test,
and all tests should pass.


### Single flag

Test that failing templates pass with only corresponding flag.

This tests that boolean expressions are all evaluated properly on
their own.

All tests that fail such as with –check-class should be prefixed
with FClass, and these particular tests should all fail.


### Stdout

Test stdout of failing tests.

Passing tests will not print to stdout.

All templates prefixed with `P` will be tested for no output.
As passing templates return an empty str as their expected results,
this test will confirm that tests that are not meant to pass do not
include this, as “” will always be True for being in a str object.

All templates prefixed with `F` will be tested for output.

All templates prefixed with `M` will be excluded from this test,
as this tests multiple functions in a file, some that may produce
output and some that may not.


### String argument

Test for passing and failing checks with `-s/--string`.

A combination of the test for exit status and the test for stdout.
As this test could be done for every single test where the file is
checked, without the `-s/--string` argument and with the path
positional argument, this will only test those two. As long as the
tests pass and are consistent with the result that the tests for a
file produce, this test should be enough.


### Summary

Test main for passing and failing checks with `--summary`.

Test for the differences and similarities in a standard run where
the full function diagram is emitted.


