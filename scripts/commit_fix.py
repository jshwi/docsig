"""Ensure fix commits include a test."""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from pathlib import Path

import git
import pytest


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
    try:
        commit_msg = o.commit_msg_file.read_text(
            encoding="utf-8",
        ).splitlines()[0]
    except IndexError:
        return "did not receive a commit message"

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


class Test:
    """Tests for this script."""

    repo: git.Repo
    tests: Path
    commit_file: Path

    @pytest.fixture(autouse=True)
    def setup(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Set up the test environment.

        :param tmp_path: Create and return a temporary directory.
        :param monkeypatch: Mock patch environment and attributes.
        """
        monkeypatch.chdir(tmp_path)
        self.repo = git.Repo.init(tmp_path)
        config = self.repo.config_writer()
        config.set_value("user", "name", "Test User")
        config.set_value("user", "email", "test.user@example.com")
        config.set_value("commit", "gpgsign", False)
        config.release()
        self.tests = tmp_path / "tests"
        self.tests.mkdir()
        (self.tests / "fix_test.py").write_text("", encoding="utf-8")
        self.repo.git.add(tmp_path)
        self.repo.git.commit(message="Initial commit")
        self.commit_file = tmp_path / "COMMIT_EDITMSG"
        monkeypatch.setattr("sys.argv", ["__main__.py", str(self.commit_file)])

    def write(self, message: str) -> None:
        """Write the commit message the script checks.

        :param message: Contents of the commit message file.
        """
        self.commit_file.write_text(message, encoding="utf-8")

    def stage_fix_test(self) -> None:
        """Stage a change to the fix test module."""
        path = self.tests / "fix_test.py"
        path.write_text("def test_fix_thing() -> None:\n    ...\n", "utf-8")
        self.repo.git.add(str(path))

    def test_empty_message(self) -> None:
        """Test an empty commit message is rejected."""
        self.write("")
        assert main() == "did not receive a commit message"

    def test_other_type(self) -> None:
        """Test a commit of another type needs no fix test."""
        self.write("feat: a feature (#1)\n")
        assert main() == 0

    def test_fix_without_test(self) -> None:
        """Test a fix commit with no staged fix test is rejected."""
        self.write("fix: a bug (#1)\n")
        assert "tests/fix_test.py" in str(main())

    def test_fix_with_test(self) -> None:
        """Test a fix commit with a staged fix test is accepted."""
        self.stage_fix_test()
        self.write("fix: a bug (#1)\n")
        assert main() == 0

    def test_fix_test_unstaged(self) -> None:
        """Test an unstaged fix test does not satisfy the check."""
        path = self.tests / "fix_test.py"
        path.write_text("def test_fix_thing() -> None:\n    ...\n", "utf-8")
        self.write("fix: a bug (#1)\n")
        assert "tests/fix_test.py" in str(main())


if __name__ == "__main__":
    sys.exit(main())
