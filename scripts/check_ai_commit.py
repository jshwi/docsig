"""Check AI housekeeping commits carry their provenance."""

from __future__ import annotations

import re
import sys
from argparse import ArgumentParser
from pathlib import Path

import pytest

AI_COMMIT = re.compile(r"^chore\(ai\):\s+(.+)$")
TRAILER = re.compile(r"^[A-Za-z][A-Za-z0-9-]*:\s+.+$")
BATCH_DESCRIPTIONS = ("commit claude session",)


class E:  # pylint: disable=too-few-public-methods
    """Collection of errors."""

    NO_MESSAGE = "did not receive a commit message"
    BATCH = "'{description}' is a batch of rules, commit one at a time"
    NO_BODY = (
        "chore(ai) needs a body: the incident behind a changed rule, or "
        "the intent behind a new file"
    )


def get_paragraphs(lines: list[str]) -> list[list[str]]:
    """Group message lines into blank-line separated paragraphs.

    :param lines: Lines of the commit message below the subject.
    :return: Paragraphs, each a list of its non-blank lines.
    """
    paragraphs = []
    paragraph: list[str] = []
    for line in lines:
        if line.strip():
            paragraph.append(line)
        elif paragraph:
            paragraphs.append(paragraph)
            paragraph = []

    if paragraph:
        paragraphs.append(paragraph)

    return paragraphs


def get_body(lines: list[str]) -> list[list[str]]:
    """Get the prose paragraphs of a commit message.

    The trailing paragraph is dropped when it consists entirely of git
    trailers, so a message carrying nothing but ``Signed-off-by`` has no
    body.

    :param lines: Lines of the commit message below the subject.
    :return: Paragraphs which are not the trailer block.
    """
    paragraphs = get_paragraphs(lines)
    if paragraphs and all(TRAILER.match(i) for i in paragraphs[-1]):
        paragraphs.pop()

    return paragraphs


def main() -> int | str:
    """Entry point.

    Commit message file path (.git/COMMIT_EDITMSG) automatically passed
    as the first positional argument by the commit-msg pre-commit hook.

    Only ``chore(ai)`` commits are checked. They record how Claude works
    on this repo, and a rule whose cause is not written down cannot be
    reviewed later, so each carries one change and explains it.

    :return: 0 if successful, error message if unsuccessful.
    """
    p = ArgumentParser()
    p.add_argument("commit_msg_file", type=Path, help="commit msg file path")
    o = p.parse_args()
    lines = [
        i
        for i in o.commit_msg_file.read_text(encoding="utf-8").splitlines()
        if not i.startswith("#")
    ]
    if not lines:
        return E.NO_MESSAGE

    match = AI_COMMIT.match(lines[0])
    if match is None:
        return 0

    description = match.group(1)
    if description in BATCH_DESCRIPTIONS:
        return E.BATCH.format(description=description)

    if not get_body(lines[1:]):
        return E.NO_BODY

    return 0


class Test:
    """Tests for this script."""

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
        self.commit_file = tmp_path / "COMMIT_EDITMSG"
        monkeypatch.setattr("sys.argv", ["__main__.py", str(self.commit_file)])

    def write(self, message: str) -> None:
        """Write a commit message for the script to check.

        :param message: Contents of the commit message file.
        """
        self.commit_file.write_text(message, encoding="utf-8")

    def test_empty_message(self) -> None:
        """Test an empty commit message is rejected."""
        self.write("# please enter a commit message\n")
        assert main() == E.NO_MESSAGE

    def test_other_type(self) -> None:
        """Test commits of another type are not checked for a body."""
        self.write("fix: a bug (#1)\n\nSigned-off-by: A U <a@u.com>\n")
        assert main() == 0

    def test_other_scope(self) -> None:
        """Test chore commits of another scope are not checked."""
        self.write("chore(script): a change\n\nSigned-off-by: A U <a@u.com>\n")
        assert main() == 0

    def test_batch_description(self) -> None:
        """Test the batched session description is rejected."""
        self.write(
            "chore(ai): commit claude session\n"
            "\n"
            "Several unrelated rules.\n"
            "\n"
            "Signed-off-by: A U <a@u.com>\n",
        )
        assert main() == E.BATCH.format(description="commit claude session")

    def test_no_body(self) -> None:
        """Test a message with only a trailer block is rejected."""
        self.write("chore(ai): note a rule\n\nSigned-off-by: A U <a@u.com>\n")
        assert main() == E.NO_BODY

    def test_subject_only(self) -> None:
        """Test a message with no body at all is rejected."""
        self.write("chore(ai): note a rule\n")
        assert main() == E.NO_BODY

    def test_body(self) -> None:
        """Test a message stating its provenance is accepted."""
        self.write(
            "chore(ai): note stale git ls-files file lists\n"
            "\n"
            "`make lint` passed green on an unstaged module.\n"
            "\n"
            "Signed-off-by: A U <a@u.com>\n",
        )
        assert main() == 0

    def test_body_without_trailer(self) -> None:
        """Test a body is accepted when no trailer block follows it."""
        self.write("chore(ai): note a rule\n\nWhat went wrong.\n")
        assert main() == 0

    def test_comments_stripped(self) -> None:
        """Test commented template lines do not count as a body."""
        self.write(
            "chore(ai): note a rule\n"
            "\n"
            "# please enter a commit message\n"
            "\n"
            "Signed-off-by: A U <a@u.com>\n",
        )
        assert main() == E.NO_BODY


if __name__ == "__main__":
    sys.exit(main())
