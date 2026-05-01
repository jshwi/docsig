"""Ensure fix commits include a test."""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from pathlib import Path

import git


def main() -> int | str:
    """Entry point.

    Commit message file path (.git/COMMIT_EDITMSG) automatically
    passed as the first positional argument by the commit-msg pre-commit
    hook.

    :return: 0 if successful, error message if unsuccessful.
    """
    p = ArgumentParser()
    p.add_argument("commit_msg_file", type=Path, help="commit msg file path")
    o = p.parse_args()
    commit_msg = o.commit_msg_file.read_text(encoding="utf-8").splitlines()[0]
    if commit_msg.startswith("fix:"):
        repo = git.Repo(Path.cwd())
        diff = repo.git.diff(
            "HEAD",
            Path("tests") / "fix_test.py",
            cached=True,
            name_only=True,
        )
        if not diff:
            return """\
a test should be written in tests/fix_test.py to avoid regressions
"""

    return 0


if __name__ == "__main__":
    sys.exit(main())
