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


if __name__ == "__main__":
    sys.exit(main())
