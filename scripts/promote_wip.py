"""Promote a wip commit from dev/main to an issue branch.

Automates the promotion workflow documented in CLAUDE.md: create or
reuse the GitHub issue and its linked branch, cherry-pick the wip
commit with its finalized subject, run the commit hooks (retrying
once so the news fragment they create is included), push, and open a
pull request targeting master.

Merging is left to the maintainer once the pipeline passes.
"""

import re
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

import git

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


def pull_request_body(commit: git.Commit, issue: int) -> str:
    """Construct the pull request body.

    :param commit: Commit being promoted.
    :param issue: Issue the pull request closes.
    :return: Body text beginning with the closing reference.
    """
    lines = [f"Closes #{issue}"]
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

    if " and " in match[2]:
        return f"subject contains 'and', split the commit: {match[2]}"

    try:
        issue = o.issue
        if issue is None:
            url = gh("issue", "create", "--title", o.title, "--body", o.body)
            issue = int(url.rsplit("/", maxsplit=1)[1])

        subject = f"{match[1]}: {match[2]} (#{issue})"
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
                pull_request_body(wip_commit, issue),
            ),
        )
    except subprocess.CalledProcessError as err:
        return str(err.stderr or err)
    except git.GitCommandError as err:
        return str(err)

    print("wait for the pipeline, then merge with:")
    print(f"git checkout master; git merge {branch}; git push")
    return 0


if __name__ == "__main__":
    sys.exit(main())
