"""
tests._test
===========
"""
import warnings

import pytest
import templatest
from templatest import Template, templates

import docsig.messages

from . import InitFileFixtureType, MockMainType
from ._utils import NoColorCapsys


def test_print_version(
    monkeypatch: pytest.MonkeyPatch,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
) -> None:
    """Test printing of version on commandline.

    :param monkeypatch: Mock patch environment and attributes.
    :param main: Patch package entry point.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    """
    monkeypatch.setattr("docsig._core.__version__", "1.0.0")
    with pytest.raises(SystemExit):
        main("--version")

    out = nocolorcapsys.stdout().strip()
    assert out == "1.0.0"


@pytest.mark.parametrize(
    "contents,expected",
    [
        (templates.registered[0].template, 0),
        (templates.registered[1].template, 1),
        (templates.registered[2].template, 1),
    ],
    ids=["pass", "fail-too-many-in-docs", "fail-too-many-in-sig"],
)
def test_main_args(
    init_file: InitFileFixtureType,
    main: MockMainType,
    contents: str,
    expected: int,
) -> None:
    """Test main for passing and failing checks.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param contents: Contents to write to file.
    :param expected: Expected returncode.
    """
    file = init_file(contents)
    assert main(str(file.parent)) == expected


@pytest.mark.parametrize(
    "template",
    templatest.templates.registered,
    ids=templates.registered.getids(),
)
def test_main_output(
    init_file: InitFileFixtureType,
    main: MockMainType,
    nocolorcapsys: NoColorCapsys,
    template: Template,
) -> None:
    """Test main for stdout.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param nocolorcapsys: Capture system output while stripping ANSI
        color codes.
    :param template: String data.
    """
    file = init_file(template.template)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main(str(file.parent))

    assert template.expected in nocolorcapsys.readouterr()[0]


def test_no_docstring(
    init_file: InitFileFixtureType, main: MockMainType
) -> None:
    """Test main for function with no docstring.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    file = init_file(
        templates.registered.getbyname("function-no-docstring").template
    )
    with pytest.warns(
        UserWarning,
        match=docsig.messages.W101.format(module=file, func="function_4"),
    ):
        main(str(file.parent))


def test_routed_function(
    init_file: InitFileFixtureType, main: MockMainType
) -> None:
    """Test main for function without params.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    file = init_file(
        templates.registered.getbyname("function-no-params").template
    )
    with pytest.warns(None) as record:  # type: ignore
        main(str(file.parent))

    assert len(record) == 0
