"""Bump version script."""

from __future__ import annotations

import re
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

import git


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
            rf"\s*{o.part}\s*─\s*(\S+)",
            subprocess.run(
                ["bump-my-version", "show-bump"],
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


if __name__ == "__main__":
    sys.exit(_main())
