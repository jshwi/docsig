"""Ensure fix commits include a test."""

from __future__ import annotations

import sys
from pathlib import Path

import git


def main() -> int | str:
    """Entry point.

    :return: 0 if successful, error message if unsuccessful.
    """
    commit_msg = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()[0]
    if commit_msg.startswith("fix:"):
        repo = git.Repo(Path.cwd())
        diff = repo.git.diff(
            "HEAD", Path("tests") / "fix_test.py", cached=True, name_only=True
        )
        if not diff:
            return """\
a test should be written in tests/fix_test.py to avoid regressions
"""

    return 0


if __name__ == "__main__":
    sys.exit(main())
