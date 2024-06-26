"""Release script."""

from __future__ import annotations

import re
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

import git


def _main() -> int | str:
    p = ArgumentParser()
    p.add_argument(
        "part",
        choices=["patch", "minor", "major"],
        help="semver part to bump",
    )
    o = p.parse_args()
    repo = git.Repo(Path.cwd())
    try:
        repo.git.diff_index("HEAD", quiet=True)
    except git.exc.GitCommandError:
        return "there are uncommitted changes in the working directory"

    if len(list(Path("changelog").iterdir())) == 1:
        return "there are no release notes therefore nothing to release"

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
        ["bump-my-version", "bump", o.part],
        check=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(_main())
