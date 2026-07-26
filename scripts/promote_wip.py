"""Promote a wip commit from dev/main to an issue branch.

Automates the promotion workflow documented in CLAUDE.md: create or
reuse the GitHub issue and its linked branch, check the finalized
subject against the commit policy before anything is touched,
cherry-pick the wip commit with that subject, run the commit hooks
(retrying once so the news fragment they create is included), push,
and open a pull request targeting master.

Merging is left to the maintainer once the pipeline passes.
"""

import re
import subprocess
import sys
import tempfile
import typing as t
from argparse import ArgumentParser
from pathlib import Path

import git
import pytest

WIP = re.compile(r"^wip: (\w+) (.+)$")


def gh(*args: str) -> str:
    """Run a gh command.

    :param args: Arguments to pass to gh.
    :return: Stripped stdout of the command.
    """
    proc = subprocess.run(
        ["gh", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def issue_branch(issue: int) -> str:
    """Get the branch linked to an issue, creating one if needed.

    Guards against running ``gh issue develop`` twice for the same
    issue, which would create a ``-1`` suffixed duplicate branch.

    :param issue: Issue number the branch belongs to.
    :return: Name of the linked branch.
    """
    branches = gh("issue", "develop", "--list", str(issue))
    if not branches:
        gh("issue", "develop", str(issue))
        branches = gh("issue", "develop", "--list", str(issue))

    return branches.splitlines()[0].split()[0]


def new_issue(title: str, body: str) -> int:
    """Open a GitHub issue for the fix.

    :param title: Title for the new issue.
    :param body: Body for the new issue.
    :return: Number of the issue that was opened.
    """
    url = gh("issue", "create", "--title", title, "--body", body)
    return int(url.rsplit("/", maxsplit=1)[1])


def policy_report(repo: git.Repo, subject: str) -> str | None:
    """Check a finalized subject against the commit policy.

    A wip subject clears conform's imperative mood check because ``wip:
    fix ...`` puts an imperative verb first. Finalizing strips that
    verb, so a description opening with a gerund, or with a capitalized
    message reference, is only rejected at commit time, once the
    working tree has been rearranged and the hooks have run. Check it
    up front against the policy the commit-msg hook applies, so a
    rewording costs nothing.

    :param repo: Repository whose sign-off identity signs the message.
    :param subject: Finalized commit subject.
    :return: Conform's report if the policy fails, else None.
    """
    name = repo.git.config("--get", "user.name")
    email = repo.git.config("--get", "user.email")
    with tempfile.NamedTemporaryFile(
        "w",
        delete=False,
        suffix=".txt",
    ) as file:
        file.write(f"{subject}\n\nSigned-off-by: {name} <{email}>\n")
        path = Path(file.name)

    try:
        proc = subprocess.run(
            [
                "conform",
                "enforce",
                "--commit-msg-file",
                str(path),
                "--reporter",
                "cli",
            ],
            capture_output=True,
            check=False,
            cwd=repo.working_dir,
            text=True,
        )
    except FileNotFoundError:
        print(
            "warning: conform not on PATH, subject unchecked",
            file=sys.stderr,
        )
        return None
    finally:
        path.unlink()

    if proc.returncode:
        return f"{proc.stdout}{proc.stderr}".strip()

    return None


def pull_request_body(
    commit: git.Commit,
    issue: int,
    body: str = "",
) -> str:
    """Construct the pull request body.

    A wip commit's message is only its sign-off trailer, so nothing
    survives to describe the change. Prefer an explicit body when one
    is given, and fall back to the commit's own paragraphs otherwise.

    :param commit: Commit being promoted.
    :param issue: Issue the pull request closes.
    :param body: Body to use in place of the commit's paragraphs.
    :return: Body text beginning with the closing reference.
    """
    lines = [f"Closes #{issue}"]
    text = body
    if not text:
        paragraphs = str(commit.message).split("\n", 1)[1:]
        if paragraphs:
            text = "\n".join(
                i
                for i in paragraphs[0].splitlines()
                if not i.startswith("Signed-off-by:")
            ).strip()

    if text:
        lines.extend(["", text])

    return "\n".join(lines)


def commit_staged(repo: git.Repo, subject: str) -> None:
    """Commit staged changes with sign-off.

    The commit-msg hook creates the news fragment and blocks the
    first attempt; stage the fragment and commit again.

    :param repo: Repository to commit to.
    :param subject: Finalized commit subject.
    """
    try:
        repo.git.commit("-s", "-m", subject)
    except git.GitCommandError:
        repo.git.add(".")
        repo.git.commit("-s", "-m", subject)


def main() -> int | str:  # pylint: disable=too-many-return-statements
    """Entry point.

    :return: 0 if successful, error message if unsuccessful.
    """
    p = ArgumentParser()
    p.add_argument("sha", help="wip commit to promote")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--issue", type=int, help="existing issue number")
    group.add_argument("--title", help="title for a new issue")
    p.add_argument("--body", default="", help="body for a new issue")
    p.add_argument(
        "--description",
        help="replace the description taken from the wip subject",
    )
    p.add_argument(
        "--pr-body",
        default="",
        help="body for the pull request, after the closing reference",
    )
    o = p.parse_args()
    repo = git.Repo(Path.cwd())
    if repo.is_dirty(untracked_files=True):
        return "working tree is not clean"

    try:
        wip_commit = repo.commit(o.sha)
    except (git.BadName, ValueError):
        return f"no such commit: {o.sha}"

    summary = str(wip_commit.summary)
    match = WIP.match(summary)
    if not match:
        return f"not a wip commit: {summary}"

    description = o.description or match[2]
    if " and " in description:
        return f"subject contains 'and', split the commit: {description}"

    try:
        issue = o.issue or new_issue(o.title, o.body)
        subject = f"{match[1]}: {description} (#{issue})"
        report = policy_report(repo, subject)
        if report is not None:
            return (
                f"subject fails the commit policy:\n{report}\n"
                f"reword it and rerun with --issue {issue} --description"
            )

        branch = issue_branch(issue)
        repo.git.fetch("origin", branch)
        repo.git.checkout(branch)
        repo.git.cherry_pick(wip_commit.hexsha)
        repo.git.reset("--soft", "HEAD~1")
        subprocess.run(["make"], check=True)
        repo.git.add(".")
        commit_staged(repo, subject)
        repo.git.push("--set-upstream", "origin", branch)
        print(
            gh(
                "pr",
                "create",
                "--base",
                "master",
                "--title",
                subject,
                "--body",
                pull_request_body(wip_commit, issue, o.pr_body),
            ),
        )
    except subprocess.CalledProcessError as err:
        return str(err.stderr or err)
    except git.GitCommandError as err:
        return str(err)

    print("wait for the pipeline, then merge with:")
    print(f"git checkout master; git merge {branch}; git push")
    return 0


class Test:
    """Tests for this script."""

    repo: git.Repo
    path: Path
    monkeypatch: pytest.MonkeyPatch

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
        self.monkeypatch = monkeypatch
        self.path = tmp_path
        self.repo = git.Repo.init(tmp_path)
        config = self.repo.config_writer()
        config.set_value("user", "name", "Test User")
        config.set_value("user", "email", "test.user@example.com")
        config.set_value("commit", "gpgsign", False)
        config.release()
        (tmp_path / "file.txt").write_text("", encoding="utf-8")
        self.repo.git.add(str(tmp_path))
        self.repo.git.commit(message="Initial commit")

    def wip(self, summary: str) -> str:
        """Add an empty commit with the given subject.

        :param summary: Subject line for the commit.
        :return: Hexsha of the created commit.
        """
        self.repo.git.commit("--allow-empty", "-m", summary)
        return str(self.repo.head.commit.hexsha)

    def argv(self, *args: str) -> None:
        """Set the commandline the script parses.

        :param args: Arguments following the program name.
        """
        self.monkeypatch.setattr("sys.argv", ["__main__.py", *args])

    def test_dirty_working_tree(self) -> None:
        """Test promotion refuses to run over uncommitted changes."""
        (self.path / "dirty.txt").write_text("x", encoding="utf-8")
        self.argv("HEAD", "--issue", "1")
        assert main() == "working tree is not clean"

    def test_unknown_commit(self) -> None:
        """Test an unresolvable revision is reported."""
        self.argv("nosuchref", "--issue", "1")
        assert main() == "no such commit: nosuchref"

    def test_not_a_wip_commit(self) -> None:
        """Test a commit of another type is refused."""
        sha = self.wip("fix: already promoted (#1)")
        self.argv(sha, "--issue", "1")
        assert str(main()).startswith("not a wip commit:")

    def test_description_contains_and(self) -> None:
        """Test a subject needing to be split is refused."""
        sha = self.wip("wip: fix this and that")
        self.argv(sha, "--issue", "1")
        assert "split the commit" in str(main())

    def test_description_override_contains_and(self) -> None:
        """Test the override is checked for 'and' as well."""
        sha = self.wip("wip: fix something")
        self.argv(sha, "--issue", "1", "--description", "fix this and that")
        assert "split the commit" in str(main())

    def test_policy_failure_reported(self) -> None:
        """Test a subject failing the commit policy stops promotion."""
        sha = self.wip("wip: fix something")
        self.monkeypatch.setattr(f"{__name__}.policy_report", lambda *_: "no")
        self.argv(sha, "--issue", "12")
        result = str(main())
        assert "subject fails the commit policy" in result
        assert "--issue 12 --description" in result

    def test_policy_skipped_without_conform(
        self,
        capsys: pytest.CaptureFixture,
    ) -> None:
        """Test a missing conform warns rather than failing.

        :param capsys: Capture sys out and err.
        """

        def _raise(*_: object, **__: object) -> None:
            raise FileNotFoundError

        self.monkeypatch.setattr("subprocess.run", _raise)
        assert policy_report(self.repo, "fix: a thing (#1)") is None
        assert "conform not on PATH" in capsys.readouterr().err

    def test_issue_branch_reuses_existing(self) -> None:
        """Test an existing linked branch is not created twice."""
        calls = []

        def _gh(*args: str) -> str:
            calls.append(args)
            return "1234-a-branch\tsomething"

        self.monkeypatch.setattr(f"{__name__}.gh", _gh)
        assert issue_branch(1) == "1234-a-branch"
        assert len(calls) == 1

    def test_issue_branch_created_when_missing(self) -> None:
        """Test a branch is created when the issue has none."""
        replies = ["", "", "1234-a-branch\tsomething"]
        calls = []

        def _gh(*args: str) -> str:
            calls.append(args)
            return replies.pop(0)

        self.monkeypatch.setattr(f"{__name__}.gh", _gh)
        assert issue_branch(1) == "1234-a-branch"
        assert calls[1] == ("issue", "develop", "1")

    def test_new_issue_parses_number(self) -> None:
        """Test the issue number is taken from the returned url."""
        url = "https://github.com/jshwi/docsig/issues/1234"
        self.monkeypatch.setattr(f"{__name__}.gh", lambda *_: url)
        assert new_issue("a title", "a body") == 1234

    def test_pull_request_body_from_commit(self) -> None:
        """Test the commit's own paragraphs describe the change."""
        self.repo.git.commit(
            "--allow-empty",
            "-m",
            "wip: fix a thing",
            "-m",
            "Why it was broken.\n\nSigned-off-by: T U <t@u.com>",
        )
        body = pull_request_body(self.repo.head.commit, 7)
        assert body.startswith("Closes #7")
        assert "Why it was broken." in body
        assert "Signed-off-by" not in body

    def test_pull_request_body_explicit(self) -> None:
        """Test an explicit body wins over the commit's paragraphs."""
        self.repo.git.commit(
            "--allow-empty",
            "-m",
            "wip: fix a thing",
            "-m",
            "From the commit.",
        )
        body = pull_request_body(self.repo.head.commit, 7, "From the flag.")
        assert body == "Closes #7\n\nFrom the flag."

    def test_pull_request_body_bare_commit(self) -> None:
        """Test a commit with no paragraphs yields only the reference."""
        self.wip("wip: fix a thing")
        assert pull_request_body(self.repo.head.commit, 7) == "Closes #7"

    def test_commit_staged_retries(self) -> None:
        """Test a commit blocked by a hook is retried once.

        The commit-msg hook writes the news fragment then fails the
        first attempt, so the fragment has to be staged and the commit
        remade. GitPython builds ``repo.git.commit`` dynamically, so
        this stubs the command namespace rather than patching it.
        """
        calls: list[str] = []

        class _Git:
            """Stand-in for the git command namespace."""

            @staticmethod
            def commit(*_: str) -> None:
                """Fail the first attempt, as the hook does.

                :param _: Arguments the caller passes to git commit.
                """
                calls.append("commit")
                if calls.count("commit") == 1:
                    raise git.GitCommandError("commit", 1)

            @staticmethod
            def add(*_: str) -> None:
                """Record that the fragment was staged.

                :param _: Arguments the caller passes to git add.
                """
                calls.append("add")

        class _Repo:  # pylint: disable=too-few-public-methods
            """Stand-in for the repository the function commits to."""

            git = _Git()

        commit_staged(t.cast(git.Repo, _Repo()), "fix: a thing (#1)")
        assert calls == ["commit", "add", "commit"]

    def test_commit_staged_first_attempt(self) -> None:
        """Test a commit which is not blocked is made only once."""
        self.repo.git.commit("--allow-empty", "-m", "wip: fix a thing")
        (self.path / "new.txt").write_text("x", encoding="utf-8")
        self.repo.git.add(str(self.path))
        commit_staged(self.repo, "wip: fix another thing")
        assert self.repo.head.commit.summary == "wip: fix another thing"


if __name__ == "__main__":
    sys.exit(main())
