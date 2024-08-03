"""Check for news fragment when making a production change."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import typing as t
from pathlib import Path

import git
import pytest
import tomli
import tomli_w

MSG = re.compile(r"^(\w+):\s+(.+)\s+\(#(\d+)\)$", re.MULTILINE)
NEWS = re.compile(r"^changelog/.*\.md$", re.MULTILINE)
CREATED_NEWS = "Created news fragment at {path}"


class E:  # pylint: disable=too-few-public-methods
    """Collection of errors."""

    FORMAT = "commit message not in the format of '{pattern}'"
    CHANGED_NAME = "issue or type changed, {src} -> {dst}"
    CHANGED_DESC = "commit description changed, updated {name}"
    REMOVED = "no news for commit type, removed {name}"


def get_last_issue_fragment(default: Path) -> Path:
    """Get the last created news fragment related to the current name.

    .. code-block:: console

        # would return 1.add.1.md
        $ git commit -m 'add: commit message (#1)'
        $ ls changelog
        1.add.md
        $ git commit -m 'add: new commit message for same issue (#1)'
        1.add.md  1.add.1.md

    If no other fragments exist apart from the default one, return that.

    :param default: Default name for news fragment e.g. 1.add.md.
    :return: Latest news fragment.
    """
    files = [(default.name, 0)]
    for path in default.parent.iterdir():
        if path.name.startswith(default.stem):
            parts = path.name.split(".")
            # default has 3 parts (1.add.md), new commit for same issue
            # has 4 (1.add.1.md)
            if len(parts) == 4:
                files.append((path.name, int(parts[2])))

    return default.parent / max(files, key=lambda x: x[1])[0]


def create_news_fragment(
    desc: str, name: Path, repo: git.Repo, last: Path
) -> int | str:
    """Create news files and ensure it's not a duplicate.

    A duplicate will occur in situations such as an amendment to the
    commit. As this script only reads the .git/COMMIT_EDITMSG file it is
    unable to determine whether the commit is an amendment and will
    create an unwanted duplicate as if it was a new commit for the same
    issue.

    Check the latest untracked news fragment (the name is not know yet),
    and confirm its contents aren't identical to the last news fragment
    before it.

    :param desc: Description to write to file.
    :param name: Name of new file.
    :param repo: Repository to check for diff.
    :param last: Last new file created, before the current one.
    :return: 0 if successful, error message if unsuccessful.
    """
    output = subprocess.run(
        ["towncrier", "create", "-c", desc, name],
        capture_output=True,
        check=True,
        text=True,
    ).stdout
    untracked = NEWS.findall("\n".join(repo.untracked_files))
    if untracked:
        latest = Path(untracked[0])
        if (last.name != latest.name) and (
            last.read_text(encoding="utf-8")
            == latest.read_text(encoding="utf-8")
        ):
            latest.unlink()
            return 0

    return output


def main() -> int | str:
    """Entry point.

    This script reads the commit message file and cannot determine the
    commit from the commandline.

    :return: 0 if successful, error message if unsuccessful.
    """
    conf = (Path.cwd() / "pyproject.toml").read_text(encoding="utf-8")
    allowed_kinds = tuple(tomli.loads(conf)["tool"]["towncrier"]["fragment"])
    commit_msg = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()[0]
    repo = git.Repo(Path.cwd())
    diff = repo.git.diff("HEAD", cached=True, name_only=True)
    unversioned_news = NEWS.findall(diff)

    # only allowed commit types will be logged
    # commit types such as refactor will not
    if any(commit_msg.startswith(i) for i in allowed_kinds):
        match = MSG.match(commit_msg)
        if match is None:
            # if commit message does not have the correct pattern it
            # cannot be parsed
            return E.FORMAT.format(pattern=MSG.pattern)

        kind, desc, issue = match.group(1), match.group(2), match.group(3)
        name = Path(f"{issue}.{kind}.md")
        last = get_last_issue_fragment(Path.cwd() / "changelog" / name)
        if unversioned_news:
            latest = Path(unversioned_news[0])
            if desc != latest.read_text(encoding="utf-8").strip():
                # description changed, update file contents
                latest.write_text(desc, encoding="utf-8")
                return E.CHANGED_DESC.format(name=latest.name)

            if not latest.name.startswith(name.stem):
                # issue or commit type changed, rename file
                os.rename(latest, last)
                return E.CHANGED_NAME.format(src=latest.name, dst=last.name)
        else:
            return create_news_fragment(desc, name, repo, last)
    elif unversioned_news:
        # if a news fragment was created for a loggable commit, and the
        # commit is no longer loggable, remove the news fragment
        latest = Path(unversioned_news[0])
        try:
            latest.unlink()
            return E.REMOVED.format(name=latest.name)
        except FileNotFoundError:
            # the file does not exist, maybe the diff is a removal for
            # a version bump
            pass

    return 0


class Test:
    """Tests for this script."""

    fragments: Path
    pyproject: Path
    commit_file: Path
    repo: git.Repo

    @classmethod
    @pytest.fixture(autouse=True)
    def setup_class(
        cls, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Set up the test environment.

        :param tmp_path: Create and return temporary directory.
        :param monkeypatch: Mock patch environment and attributes.
        """
        monkeypatch.chdir(tmp_path)
        this_pyproject = Path(__file__).parent.parent / "pyproject.toml"
        conf = tomli.loads(this_pyproject.read_text(encoding="utf-8"))
        cls.fragments = tmp_path / "changelog"
        cls.fragments.mkdir(exist_ok=True, parents=True)
        cls.pyproject = tmp_path / "pyproject.toml"
        cls.repo = git.Repo.init(tmp_path)
        config = cls.repo.config_writer(config_level="repository")
        config.set_value("user", "name", "Test User")
        config.set_value("user", "email", "test.user@example.com")
        conf["tool"]["towncrier"]["directory"] = str(cls.fragments)
        del conf["tool"]["towncrier"]["template"]
        cls.pyproject.write_text(tomli_w.dumps(conf), encoding="utf-8")
        cls.repo.git.add(tmp_path)
        cls.repo.git.commit(message="Initial commit")
        cls.commit_file = tmp_path / ".git" / "COMMIT_EDITMSG"
        monkeypatch.setattr("sys.argv", ["__main__.py", str(cls.commit_file)])

    def _touch_unique_file(self) -> None:
        Path(self.repo.git.rev_parse("HEAD")).touch()

    def _ci(self, **kwargs: t.Any) -> int | str:
        # simulate pre-commit hook which blocks unstaged fragments
        assert "??" not in self.repo.git.status(self.fragments, porcelain=True)

        message = kwargs.get("message")
        if message is not None:
            # if a commit message provided, prepare the message as would
            # be done before the `commit-msg` hook
            self.commit_file.write_text(message, encoding="utf-8")

        # main in this context is the pre-commit hook
        returncode = main()
        if not returncode:
            # if main passes, the commit hook is successful, so proceed
            # to actually making the commit
            self.repo.git.commit(**kwargs)

        # return int if int, strip str if str
        return (
            returncode
            if isinstance(returncode, int)
            else str(returncode).strip()
        )

    def test_no_log(self) -> None:
        """Test non loggable commit."""
        self._touch_unique_file()
        self.repo.git.add(Path.cwd())
        assert not self._ci(message="ci: not loggable")
        assert len(list(self.fragments.iterdir())) == 0

    def test_log_bad_format(self) -> None:
        """Test loggable commit with bad commit message format."""
        expected = E.FORMAT.format(pattern=MSG.pattern)
        self._touch_unique_file()
        self.repo.git.add(Path.cwd())
        assert self._ci(message="add: feature") == expected
        assert len(list(self.fragments.iterdir())) == 0

    def test_log(self) -> None:
        """Test loggable commit."""
        news = self.fragments / "1.add.md"
        expected = CREATED_NEWS.format(path=news)
        self._touch_unique_file()
        self.repo.git.add(Path.cwd())
        out = self._ci(message="add: feature (#1)")
        self.repo.git.add(Path.cwd())
        self._ci(message="add: feature (#1)")
        assert out == expected
        assert news.is_file()
        assert len(list(self.fragments.iterdir())) == 1

    def test_log_commit_amend(self) -> None:
        """Test commit amend doesn't add an extra fragment."""
        self.test_log()
        assert not self._ci(amend=True, no_edit=True)
        assert len(list(self.fragments.iterdir())) == 1

    def test_log_commit_same_issue(self) -> None:
        """Test new fragment allowed if it's a commit for same issue."""
        news = self.fragments / "1.add.1.md"
        expected = CREATED_NEWS.format(path=news)
        self.test_log()
        assert self._ci(message="add: to feature (#1)") == expected
        assert news.is_file()
        assert len(list(self.fragments.iterdir())) == 2

    def test_log_commit_same_issue_amend(self) -> None:
        """Test git commit amend with already existing news.

        This amend is different because it requires finding the latest
        file to compare against.
        """
        self.test_log_commit_same_issue()
        self._touch_unique_file()
        self.repo.git.add(Path.cwd())
        assert not self._ci(amend=True, no_edit=True)
        assert len(list(self.fragments.iterdir())) == 2

    def test_log_commit_change_desc(self) -> None:
        """Test fragment updated when the commit description changes."""
        expected = E.CHANGED_DESC.format(name="1.add.md")
        self._ci(message="add: feature (#1)")
        self.repo.git.add(Path.cwd())
        assert self._ci(message="add: new desc (#1)") == expected

    def test_log_commit_change_type(self) -> None:
        """Test fragment updated when the commit type is changed."""
        expected = E.CHANGED_NAME.format(src="1.add.md", dst="1.change.md")
        self._ci(message="add: feature (#1)")
        self.repo.git.add(Path.cwd())
        assert self._ci(message="change: feature (#1)") == expected

    def test_log_commit_change_issue(self) -> None:
        """Test fragment updated when the commit issue is changed."""
        expected = E.CHANGED_NAME.format(src="1.add.md", dst="2.add.md")
        self._ci(message="add: feature (#1)")
        self.repo.git.add(Path.cwd())
        assert self._ci(message="add: feature (#2)") == expected

    def test_log_commit_no_news_anymore(self) -> None:
        """Test fragment removed when no longer needed."""
        expected = E.REMOVED.format(name="1.add.md")
        self._ci(message="add: commit message (#1)")
        self.repo.git.add(Path.cwd())
        assert self._ci(message="ci: feature (#1)") == expected

    def test_bump(self) -> None:
        """Test removal ok when building changelog for bump.."""
        news = self.fragments / "1.add.md"
        self._ci(message="add: commit message (#1)")
        self.repo.git.add(Path.cwd())
        self._ci(message="add: commit message (#1)")
        news.unlink()
        self.repo.git.add(Path.cwd())
        self._ci(message="bump: version 0.56.0 → 0.57.0")
        assert not news.is_file()


if __name__ == "__main__":
    sys.exit(main())
