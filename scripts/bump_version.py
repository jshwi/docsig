"""Bump version script."""

from __future__ import annotations

import re
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

import git
import pytest
import tomli
import tomli_w


def _main() -> int | str:
    p = ArgumentParser()
    p.add_argument("part", choices=["patch", "minor", "major"])
    o = p.parse_args()
    repo = git.Repo(Path.cwd())
    try:
        repo.git.diff_index("HEAD", quiet=True)
    except git.exc.GitCommandError:
        return "there are uncommitted changes in the working directory"

    try:
        subprocess.run(
            ["towncrier", "build", "--draft"],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        return "there are no release notes therefore nothing to release"

    # all pre-flight checks passed, start making changes to files
    try:
        new_version = re.search(  # type: ignore
            rf"{o.part}\s*-\s*(\d+\.\d+\.\d+)",
            subprocess.run(
                ["bump-my-version", "show-bump", "--ascii"],
                stdout=subprocess.PIPE,
                text=True,
                check=True,
            ).stdout,
        ).group(1)
        subprocess.run(
            ["towncrier", "build", "--version", new_version, "--yes"],
            check=True,
        )
        subprocess.run(
            ["bump-my-version", "bump", o.part, "--verbose"],
            check=True,
        )
    except (KeyboardInterrupt, subprocess.CalledProcessError):
        # this is ok as the script will not run if the working tree is
        # dirty beforehand
        # just remove any changes this script has made
        repo.git.reset(hard=True)
        return "version bump failed"

    return 0


def test_bump(  # pylint: disable=too-many-locals
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test bump.

    :param tmp_path: Create and return temporary directory.
    :param monkeypatch: Mock patch environment and attributes.
    """
    this = Path(__file__).parent.parent
    path = tmp_path / this.name
    repo = git.Repo.clone_from(this, path)
    config = repo.config_writer(config_level="repository")
    config.set_value("user", "name", "Test User")
    config.set_value("user", "email", "test.user@example.com")
    changelog = path / "changelog"
    fragment = changelog / "1.add.md"
    fragment.write_text("add something")
    pyproject = path / "pyproject.toml"
    conf = tomli.loads(pyproject.read_text(encoding="utf-8"))
    del conf["tool"]["bumpversion"]["commit_args"]
    del conf["tool"]["bumpversion"]["sign_tags"]
    pyproject.write_text(tomli_w.dumps(conf), encoding="utf-8")
    repo.git.add(path)
    repo.git.commit(message="Initial commit")
    monkeypatch.chdir(path)
    monkeypatch.setattr("sys.argv", [__file__, "patch"])
    assert not _main()


if __name__ == "__main__":
    sys.exit(_main())
