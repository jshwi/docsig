"""Update documentation when changes have been made to docsig."""

import contextlib
import io
import re
import sys
import typing as t
from pathlib import Path

import pytest

from docsig import main
from docsig.messages import NEW

SCRIPTS_DIR = Path(__file__).parent
REPO = SCRIPTS_DIR.parent
DOCS_DIR = REPO / "docs"
USAGE = DOCS_DIR / "usage"
ADMONITION = f"""

.. admonition:: New Violation

   {NEW}
"""
TOC = """\
.. toctree::
   :titlesonly:

   {option}\
"""
TEMPLATE = """\
{title}
{underline}
{admonition}
{description}

.. code-block:: python

    >>> from docsig import docsig
"""
CATEGORIES = {
    0: "config",
    1: "missing",
    2: "signature",
    3: "description",
    4: "parameters",
    5: "returns",
    9: "error",
}


def generate_configurations() -> None:
    """Generate documentation for help options."""
    categories = "check", "ignore"
    configuration_dir = USAGE / "configuration"
    configuration_dir.mkdir(exist_ok=True, parents=True)
    helpio = io.StringIO()
    with contextlib.redirect_stdout(helpio), contextlib.suppress(SystemExit):
        sys.argv = ["docsig", "--help"]
        main()

    for category in categories:
        toc_file = USAGE / f"{category}-configuration.rst"
        cur_content = toc_file.read_text(encoding="utf-8")
        tocs = []
        for line in helpio.getvalue().splitlines():
            try:
                parts = line.split()
                option = parts[0]
                if not option.startswith(f"--{category}"):
                    continue

                option = parts[0][2:]
                tocs.append(TOC.format(option=f"configuration/{option}"))
                doc_path = configuration_dir / f"{option}.rst"
                if not doc_path.is_file():
                    title = option.replace("-", " ").capitalize()
                    doc_path.write_text(
                        TEMPLATE.format(
                            title=title,
                            underline=len(title) * "=",
                            admonition="",
                            description=" ".join(parts[2:]).capitalize(),
                        ),
                        encoding="utf-8",
                    )
            except IndexError:
                continue

        content = "\n\n".join(sorted(tocs))
        content = f"{content}\n"
        if cur_content != content:
            toc_file.write_text(content, encoding="utf-8")


def generate_messages() -> None:  # pylint: disable=too-many-locals
    """Generate documentation for messages."""
    messages_dir = USAGE / "messages"
    messages_dir.mkdir(exist_ok=True, parents=True)
    pattern = re.compile(r"(?:. )?([^:]+): ([^(]+) \(([^)]+)\)")
    msgio = io.StringIO()
    with contextlib.redirect_stdout(msgio), contextlib.suppress(SystemExit):
        sys.argv = ["docsig", "--list"]
        main()

    for index, category in CATEGORIES.items():
        toc_file = USAGE / f"{category}-messages.rst"
        cur_content = ""
        if toc_file.is_file():
            cur_content = toc_file.read_text(encoding="utf-8")

        tocs = []
        for message in msgio.getvalue().splitlines():
            match = pattern.search(message)
            if match is not None:
                code = match.group(1)
                symbolic = match.group(3)
                if code.startswith(f"SIG{index}"):
                    title = f"{code.upper()}: {symbolic}"
                    option = f"{code.lower()}-{symbolic}"
                    tocs.append(TOC.format(option=f"messages/{option}"))
                    path = messages_dir / f"{option}.rst"
                    if not path.is_file():
                        admonition = (
                            ADMONITION.format(ref=code)
                            if message.startswith("W")
                            else ""
                        )
                        path.write_text(
                            TEMPLATE.format(
                                title=title,
                                underline=len(title) * "=",
                                admonition=admonition,
                                description=match.group(2).capitalize(),
                            ),
                            encoding="utf-8",
                        )

        content = "\n\n".join(sorted(tocs))
        content = f"{content}\n"
        if cur_content != content:
            toc_file.write_text(content, encoding="utf-8")
            sys.exit("new docs generated that need to be added to commit")


def remove_outdated_messages() -> None:
    """Remove the outdated messages file."""
    for path in USAGE.glob("*-messages.rst"):
        if not any(path.name.startswith(v) for v in CATEGORIES.values()):
            path.unlink()


class Test:
    """Tests for this script."""

    usage: Path

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
        self.usage = tmp_path / "usage"
        self.usage.mkdir()
        monkeypatch.setattr(f"{__name__}.USAGE", self.usage)

    @staticmethod
    def run_until_stable(generate: t.Callable[[], None]) -> int:
        """Run a generator until it stops rewriting a toctree.

        generate_messages exits on the first category it changes, so a
        full scaffold takes as many runs as there are categories.
        generate_configurations writes without exiting, so it settles on
        the first run.

        :param generate: Generator function to run.
        :return: Number of runs which rewrote something.
        """
        for run in range(len(CATEGORIES) + 2):
            try:
                generate()
            except SystemExit:
                continue

            return run

        raise AssertionError("generator never settled")

    def toc(self, name: str, content: str = "") -> Path:
        """Create a toctree file for a category.

        :param name: File name of the toctree, without its suffix.
        :param content: Initial content of the file.
        :return: Path to the created file.
        """
        path = self.usage / f"{name}.rst"
        path.write_text(content, encoding="utf-8")
        return path

    def test_configurations_generated(self) -> None:
        """Test a page is scaffolded for every check option."""
        self.toc("check-configuration")
        self.toc("ignore-configuration")
        generate_configurations()

        pages = list((self.usage / "configuration").glob("*.rst"))
        assert pages
        assert all(i.name.startswith(("check-", "ignore-")) for i in pages)

    def test_configurations_listed_in_toc(self) -> None:
        """Test generated pages are referenced by the toctree."""
        toc = self.toc("check-configuration")
        self.toc("ignore-configuration")
        generate_configurations()

        content = toc.read_text(encoding="utf-8")
        assert ".. toctree::" in content
        assert "configuration/check-" in content

    def test_existing_page_not_overwritten(self) -> None:
        """Test a page that already exists is left as it is."""
        self.toc("check-configuration")
        self.toc("ignore-configuration")
        directory = self.usage / "configuration"
        directory.mkdir()
        page = directory / "check-dunders.rst"
        page.write_text("hand written", encoding="utf-8")
        generate_configurations()

        assert page.read_text(encoding="utf-8") == "hand written"

    def test_configurations_write_without_exiting(self) -> None:
        """Test scaffolding configurations never fails the caller.

        generate_messages exits so the hook blocks until the new pages
        are committed; this one writes silently. Pin the difference, so
        restoring the exit is a deliberate change rather than a silent
        one.
        """
        toc = self.toc("check-configuration")
        self.toc("ignore-configuration")

        generate_configurations()

        written = toc.read_text(encoding="utf-8")
        assert written != ""

        # a second pass finds everything current, writes nothing more
        generate_configurations()

        assert toc.read_text(encoding="utf-8") == written

    def test_messages_generated(self) -> None:
        """Test a page is scaffolded for every message."""
        with pytest.raises(SystemExit):
            generate_messages()

        pages = list((self.usage / "messages").glob("sig*.rst"))
        assert pages

    def test_messages_split_by_category(self) -> None:
        """Test each message page is filed under its code range."""
        self.run_until_stable(generate_messages)
        toc = self.usage / "signature-messages.rst"
        assert "messages/sig2" in toc.read_text(encoding="utf-8")

    def test_messages_exit_once_per_category(self) -> None:
        """Test a full scaffold takes one run for each category."""
        assert self.run_until_stable(generate_messages) == len(CATEGORIES)

    def test_outdated_messages_removed(self) -> None:
        """Test a toctree outside the categories is deleted."""
        stale = self.toc("gone-messages")
        kept = self.toc("returns-messages")
        remove_outdated_messages()
        assert not stale.is_file()
        assert kept.is_file()


if __name__ == "__main__":
    generate_configurations()
    generate_messages()
    remove_outdated_messages()
