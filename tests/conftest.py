"""
tests.conftest
==============
"""

from __future__ import annotations

import io
import logging
import os
from pathlib import Path

import pytest
from flake8.main.application import Application

import docsig

from . import (
    FixtureFlake8,
    FixtureMakeTree,
    FixturePatchArgv,
    InitFileFixtureType,
    MockMainType,
    long,
)


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
    # make sure no pyproject.toml files past this point get parsed
    (tmp_path / "pyproject.toml").touch()


@pytest.fixture(name="flake8")
def fixture_flake8() -> FixtureFlake8:
    """Flake8 plugin fixture.

    :return: Function for using this fixture.
    """

    def _flake8(*args: str) -> int:
        """Run main with custom args."""
        app = Application()
        app.initialize(["--select=SIG", *args])
        app.run_checks()
        app.report()
        return app.exit_code()

    return _flake8


@pytest.fixture(name="main")
def fixture_main(
    monkeypatch: pytest.MonkeyPatch, flake8: FixtureFlake8
) -> MockMainType:
    """Pass patched commandline arguments to package's main function.

    :param monkeypatch: Mock patch environment and attributes.
    :param flake8: Flake8 plugin fixture.
    :return: Function for using this fixture.
    """

    def _main(
        *args: str, test_flake8: bool = True, no_ansi: bool = True
    ) -> str | int:
        """Run main with custom args."""
        argv = [docsig.__name__, *[str(a) for a in args]]
        if no_ansi:
            argv.append(long.no_ansi)

        monkeypatch.setattr("sys.argv", argv)
        retcode = docsig.main()
        if test_flake8:
            flake8_retcode = flake8(
                *[str(a).replace("--", "--sig-") for a in args]
            )
            assert flake8_retcode == retcode

        return retcode

    return _main


@pytest.fixture(name="init_file")
def fixture_init_file(tmp_path: Path) -> InitFileFixtureType:
    """Initialize a test file.

    :param tmp_path: Create and return temporary directory.
    :return: Function for using this fixture.
    """

    def _init_file(contents: str, path: Path | None = None) -> Path:
        file = tmp_path / (path or Path("module") / "file.py")
        file.parent.mkdir(exist_ok=True)
        file.write_text(contents)
        return file

    return _init_file


@pytest.fixture(name="make_tree")
def fixture_make_tree() -> FixtureMakeTree:
    """Recursively create directory tree from dict mapping.

    :return: Function for using this fixture.
    """

    def _make_tree(root: Path, obj: dict[str, object]) -> None:
        for key, value in obj.items():
            fullpath = root / key
            if isinstance(value, dict):
                fullpath.mkdir(exist_ok=True)
                _make_tree(fullpath, value)
            elif isinstance(value, list):
                fullpath.write_text("\n".join(value), encoding="utf-8")

    return _make_tree


@pytest.fixture(name="bench")
def bench(request: pytest.FixtureRequest) -> MockMainType:
    """A fixture that returns a benchmark function or a no-op function.

    Depends on whether benchmarking is enabled.

    :param request: Fixture request.
    :return: Function for using this fixture.
    """
    return (
        request.getfixturevalue("benchmark")
        if os.getenv("RUN_BENCHMARK", "false").lower() == "true"
        else lambda func, *args, **kwargs: func(*args, **kwargs)
    )


@pytest.fixture(name="patch_argv")
def fixture_patch_argv(monkeypatch: pytest.MonkeyPatch) -> FixturePatchArgv:
    """Patch commandline arguments.

    :param monkeypatch: Mock patch environment and attributes.
    :return: Function for using this fixture.
    """

    def _patch_argv(*args: str) -> None:
        monkeypatch.setattr("sys.argv", [str(a) for a in args])

    return _patch_argv


@pytest.fixture(name="patch_logger")
def fixture_patch_logger() -> io.StringIO:
    """Logs as an io instance.

    logging this amount output is ridiculously slow and results in an io
    bottleneck

    :return: Logging as IO instance.
    """
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger(docsig.__name__)
    logger.addHandler(handler)
    return log_stream
