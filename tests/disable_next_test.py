"""
tests.disable_next_test.py
==========================
"""

# pylint: disable=too-many-lines,duplicate-code
import pytest

from docsig.messages import E

from . import FixtureInitFile, FixtureMain

ES = (
    E[402].ref,
    E[202].ref,
    E[203].ref,
    E[502].ref,
    E[502].ref,
    E[201].ref,
    E[303].ref,
)
SYMBOLIC = [
    (E[402].ref, E[402].symbolic),
    (E[202].ref, E[202].symbolic),
    (E[203].ref, E[203].symbolic),
    (E[502].ref, E[502].symbolic),
    (E[503].ref, E[503].symbolic),
    (E[201].ref, E[201].symbolic),
]
MATRIX = [
    f"{ES[0]},{ES[1]}",
    f"{ES[0]},{ES[1]},{ES[2]}",
    f"{ES[0]},{ES[1]},{ES[2]},{ES[3]}",
    f"{ES[0]},{ES[1]},{ES[2]},{ES[3]},{ES[4]}",
    f"{ES[0]},{ES[1]},{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
    f"{ES[1]},{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
    f"{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
    f"{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
    f"{ES[4]},{ES[5]},{ES[6]}",
    f"{ES[5]},{ES[6]}",
]
DISABLE_FILE_1 = '''\
# docsig: disable-next
def function_1(a, b, c) -> None:
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
DISABLE_FILE_2 = '''\
def function_1(a, b, c) -> None:  # docsig: disable-next
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
DISABLE_FILE_3 = '''\
# docsig: disable-next=SIG402
def function_1(a, b, c) -> None:
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """

def function_4(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    :return: Return description.
    """

def function_5(a, b, c) -> int:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_6(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_7(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param a: Description of a.
    :param b: Description of b.
    :param: Description of d.
    """
'''
DISABLE_FILE_4 = '''\
# docsig: disable-next=SIG402,SIG202
def function_1(a, b, c) -> None:
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
DISABLE_FILE_5 = '''\
def function_1(a, b, c) -> None:  # docsig: disable-next=SIG402
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
DISABLE_FILE_6 = '''\
def function_1(a, b, c) -> None:
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
DISABLE_FILE_7 = '''\
# docsig: disable-next=SIG202
# docsig: disable-next=SIG402
def function_1(a, b, c):
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
ENABLE_FILE_1 = '''\
# docsig: disable-next
# docsig: enable-next
def function_1(a, b, c) -> None:
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """

def function_4(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    :return: Return description.
    """

def function_5(a, b, c) -> int:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_6(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_7(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param a: Description of a.
    :param b: Description of b.
    :param: Description of d.
    """
'''
ENABLE_FILE_2 = '''\
# docsig: disable-next
def function_1(a, b, c) -> None:  # docsig: enable-next
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
ENABLE_FILE_3 = '''\
# docsig: disable-next
# docsig: enable-next=SIG402
def function_1(a, b, c):
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
ENABLE_FILE_4 = '''\
# docsig: disable-next
# docsig: enable-next=SIG402,SIG202
def function_1(a, b, c) -> None:
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
ENABLE_FILE_5 = '''\
# docsig: disable-next
def function_1(a, b, c) -> None:  # docsig: enable-next=SIG402
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
ENABLE_FILE_6 = '''\
# docsig: disable-next
def function_1(a, b, c) -> None:
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """
'''
INLINE_DISABLE_TEMPLATE = '''\
def function_1(a, b, c) -> None:  # docsig: disable-next={rules}
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param a: Description of a.
    """

def function_2(a, b) -> None:  # docsig: disable-next={rules}
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_3(a, b, c) -> None:  # docsig: disable-next={rules}
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    """

def function_4(a, b, c) -> None:  # docsig: disable-next={rules}
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    :return: Return description.
    """

def function_5(a, b, c) -> int:  # docsig: disable-next={rules}
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_6(a, b, c) -> None:  # docsig: disable-next={rules}
    """Docstring summary.

    :param a: Description of a.
    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """

def function_7(a, b, c) -> None:  # docsig: disable-next={rules}
    """Docstring summary.

    :param a: Description of a.
    :param a: Description of a.
    :param b: Description of b.
    :param: Description of d.
    """
'''


def test_module_disables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test disabling entire module with `disable-next` comment.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_1)
    main(".")
    std = capsys.readouterr()
    assert "function_1" not in std.out
    assert all(f"function_{i}" in std.out for i in range(2, 4))


def test_single_function_disable(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test disabling single function with `disable-next` comment.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_2)
    main(".")
    std = capsys.readouterr()
    assert "function_1" not in std.out
    assert all(f"function_{i}" in std.out for i in range(2, 4))


def test_module_single_error_disables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test disabling entire module with specific `disable-next` comment.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_3)
    main(".")
    std = capsys.readouterr()
    assert E.from_ref(ES[0]).ref not in std.out
    assert all(E.from_ref(i).ref in std.out for i in ES if i != ES[0])


def test_module_comma_separated_error_disables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test disabling module with comment of several specific errors.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_4)
    main(".")
    std = capsys.readouterr()
    assert "function_1" not in std.out
    assert all(f"function_{i}" in std.out for i in range(2, 4))


def test_single_function_single_error_disable(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test disabling single function with specific `disable-next` comment.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_5)
    main(".")
    std = capsys.readouterr()
    assert "function_1" not in std.out
    assert all(f"function_{i}" in std.out for i in range(2, 4))


def test_single_function_comma_separated_error_disable(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test disabling function with comment of several specific errors.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_6)
    main(".")
    std = capsys.readouterr()
    assert "function_6" not in std.out
    assert all(f"function_{i}" in std.out for i in range(1, 4) if i != 6)


def test_module_enables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test individual checks.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_1)
    main(".")
    std = capsys.readouterr()
    assert all(E.from_ref(i).ref in std.out for i in ES)


def test_single_function_enable(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test enabling entire module with enable-next comment.

    Prior to `enable-next` add the `disable-next` directive.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_2)
    main(".")
    std = capsys.readouterr()
    assert all(f"function_{i}" in std.out for i in range(1, 4))


def test_module_single_error_enables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test enabling entire module with enable-next comment.

    Prior to `enable-next` add the `disable-next` directive.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_3)
    main(".")
    std = capsys.readouterr()
    assert E.from_ref(ES[0]).ref in std.out
    assert all(f"function_{i}" in std.out for i in range(1, 4))


def test_module_comma_separated_error_enables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test enabling entire module with specific enable-next comment.

    Prior to `enable-next` add the `disable-next` directive.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_4)
    main(".")
    std = capsys.readouterr()
    assert all(f"function_{i}" in std.out for i in range(1, 4))


def test_single_function_single_error_enable(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test enabling single function with specific enable-next comment.

    Prior to `enable-next` add the `disable-next` directive.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_5)
    main(".")
    std = capsys.readouterr()
    assert """\
module/file.py:2 in function_1
    SIG402: parameters out of order (params-out-of-order)
""" in std.out
    assert """\
module/file.py:2 in function_1
    SIG402: parameters out of order (params-out-of-order)
    SIG501: cannot determine whether a return statement should exist (\
confirm-return-needed)
    hint: annotate type to indicate whether return documentation needed
""" not in std.out
    assert all(f"function_{i}" in std.out for i in range(1, 4))


def test_single_function_comma_separated_error_enable(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test enabling function with comment of several specific errors.

    Prior to `enable-next` add the `disable-next` directive.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_6)
    main(".")
    std = capsys.readouterr()
    assert "function_1" not in std.out
    assert all(f"function_{i}" in std.out for i in range(2, 4))


@pytest.mark.parametrize("rules", MATRIX)
def test_comma_separated_inline_disable_checks(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    rules: str,
) -> None:
    """Test multiple inline `disable-next` checks.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param rules: Rules to comment.
    """
    all_rules = list(ES)
    comma_separated_rules = rules.split(",")
    enabled_rules = [i for i in all_rules if i not in comma_separated_rules]
    init_file(INLINE_DISABLE_TEMPLATE.format(rules=rules))
    main(".")
    std = capsys.readouterr()
    assert not any(E.from_ref(i).ref in std.out for i in comma_separated_rules)
    assert all(E.from_ref(i).ref in std.out for i in enabled_rules)


def test_disable_stacked(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test new can be stacked.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_7)
    main(".")
    std = capsys.readouterr()
    assert """\
module/file.py:3 in function_1
    SIG501: cannot determine whether a return statement should exist \
(confirm-return-needed)
    hint: annotate type to indicate whether return documentation needed
""" in std.out
    assert """\
module/file.py:3 in function_1
    SIG202: includes parameters that do not exist (params-do-not-exist)
    SIG402: parameters out of order (params-out-of-order)
    SIG501: cannot determine whether a return statement should exist \
(confirm-return-needed)
    hint: annotate type to indicate whether return documentation needed
""" not in std.out
    assert all(f"function_{i}" in std.out for i in range(2, 4))
