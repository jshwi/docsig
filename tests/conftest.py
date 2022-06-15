"""
tests.conftest
==============
"""
# pylint: disable=too-many-arguments,too-many-locals,too-few-public-methods
# pylint: disable=protected-access,no-member,too-many-statements
from pathlib import Path

import pytest

import docsig

from . import InitFileFixtureType, MockMainType
from ._utils import NoColorCapsys


@pytest.fixture(name="main")
def fixture_main(monkeypatch: pytest.MonkeyPatch) -> MockMainType:
    """Pass patched commandline arguments to package's main function.

    :param monkeypatch: Mock patch environment and attributes.
    :return: Function for using this fixture.
    """

    def _main(*args: str) -> int:
        """Run main with custom args."""
        # noinspection PyProtectedMember
        # pylint: disable=protected-access,import-outside-toplevel
        from docsig.__main__ import main

        monkeypatch.setattr("sys.argv", [docsig.__name__, *args])
        return main()

    return _main


@pytest.fixture(name="nocolorcapsys")
def fixture_nocolorcapsys(capsys: pytest.CaptureFixture) -> NoColorCapsys:
    """Instantiate capsys with the regex method.

    :param capsys: Capture ``sys`` stdout and stderr..
    :return: Instantiated ``NoColorCapsys`` object for capturing output
        stream and sanitizing the string if it contains ANSI escape
        codes.
    """
    return NoColorCapsys(capsys)


@pytest.fixture(name="init_file")
def fixture_init_file(tmp_path: Path) -> InitFileFixtureType:
    """Initialize a test file.

    :param tmp_path: Create and return temporary directory.
    :return: Function for using this fixture.
    """

    def _init_file(contents: str) -> Path:
        file = tmp_path / "module" / "file.py"
        file.parent.mkdir()
        file.write_text(contents)
        return file

    return _init_file
