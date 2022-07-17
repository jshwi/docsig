"""
tests.conftest
==============
"""
import warnings
from pathlib import Path

import pytest

import docsig

from . import InitFileFixtureType, MockMainType
from ._utils import NoColorCapsys


@pytest.fixture(name="environment", autouse=True)
def fixture_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Prepare environment for testing.

    :param monkeypatch: Mock patch environment and attributes.
    :param tmp_path: Create and return temporary directory.
    """
    monkeypatch.chdir(tmp_path)


@pytest.fixture(name="main")
def fixture_main(monkeypatch: pytest.MonkeyPatch) -> MockMainType:
    """Pass patched commandline arguments to package's main function.

    :param monkeypatch: Mock patch environment and attributes.
    :return: Function for using this fixture.
    """

    def _main(*args: str, catch_warnings: bool = True) -> int:
        """Run main with custom args."""
        monkeypatch.setattr(
            "sys.argv", [docsig.__name__, *[str(a) for a in args]]
        )
        with warnings.catch_warnings():
            if catch_warnings:
                warnings.simplefilter("ignore")

            return docsig.main()

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
