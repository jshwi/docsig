"""
tests._test
===========
"""
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

    assert nocolorcapsys.stdout().strip() == "1.0.0"


@pytest.mark.parametrize(
    "name,template,_", templates.registered, ids=templates.registered.getids()
)
def test_main_args(
    init_file: InitFileFixtureType,
    main: MockMainType,
    name: str,
    template: str,
    _: str,
) -> None:
    """Test main for passing and failing checks.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param name: Name of test.
    :param template: Contents to write to file.
    """
    file = init_file(template)
    assert main(file.parent) == int(name.startswith("fail"))


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
    main(file.parent)
    assert template.expected in nocolorcapsys.readouterr()[0]


def test_no_docstring(
    init_file: InitFileFixtureType, main: MockMainType
) -> None:
    """Test main for function with no docstring.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    contents = templates.registered.getbyname("pass-no-docstring").template
    file = init_file(contents)
    with pytest.warns(
        UserWarning,
        match=docsig.messages.W101.format(module=file, func="function"),
    ):
        main(file.parent, catch_warnings=False)


def test_no_params(init_file: InitFileFixtureType, main: MockMainType) -> None:
    """Test main for function without params.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    contents = templates.registered.getbyname("pass-no-params").template
    file = init_file(contents)
    with pytest.warns(None) as record:  # type: ignore
        main(file.parent)

    assert len(record) == 0
