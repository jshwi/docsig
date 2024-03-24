"""
tests.conftest
==============
"""

from __future__ import annotations

from pathlib import Path

import pytest

import docsig

from . import InitFileFixtureType, MockMainType, long


@pytest.fixture(name="environment", autouse=True)
def fixture_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Prepare environment for testing.

    :param monkeypatch: Mock patch environment and attributes.
    :param tmp_path: Create and return temporary directory.
    """
    monkeypatch.setenv("DOCSIG_DEBUG", "0")
    monkeypatch.chdir(tmp_path)


@pytest.fixture(name="main")
def fixture_main(monkeypatch: pytest.MonkeyPatch) -> MockMainType:
    """Pass patched commandline arguments to package's main function.

    :param monkeypatch: Mock patch environment and attributes.
    :return: Function for using this fixture.
    """

    def _main(*args: str) -> str | int:
        """Run main with custom args."""
        monkeypatch.setattr(
            "sys.argv",
            [docsig.__name__, long.no_ansi, *[str(a) for a in args]],
        )
        return docsig.main()

    return _main


@pytest.fixture(name="init_file")
def fixture_init_file(tmp_path: Path) -> InitFileFixtureType:
    """Initialize a test file.

    :param tmp_path: Create and return temporary directory.
    :return: Function for using this fixture.
    """

    def _init_file(contents: str) -> Path:
        file = tmp_path / "module" / "file.py"
        file.parent.mkdir(exist_ok=True)
        file.write_text(contents)
        return file

    return _init_file
