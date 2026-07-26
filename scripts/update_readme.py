"""
update_readme.py
================

Updates the README.rst file with the latest help output.
"""

import contextlib
import io
import os
import re
import shutil
import sys
from pathlib import Path

import pytest

from docsig import main


def _normalize_for_alternate_argparse_versions(text: str) -> str:
    # requires-python is >=3.10, where argparse prints "options:" and
    # "[path ...]"; normalize help from older interpreters to that form
    text = text.replace("[path [path ...]]", "[path ...]")

    return text.replace("    optional arguments:", "    options:")


README = Path(__file__).parent.parent / "README.rst"
CONFLICT_PATTERN = re.compile(
    r"^(<<<<<<<|=======|>>>>>>>).*\n?",
    flags=re.MULTILINE,
)
COMMANDLINE_PATTERN = re.compile(
    r"(Commandline\s*\*+\s*..\s*code-block::\s*console\s*\n)((?:\s{4}.*\n)+)",
)


def _help() -> str:
    # argparse wraps to the terminal width, so pin it to keep the help
    # in README.rst stable no matter where the script runs
    size = os.terminal_size((93, 24))
    original = shutil.get_terminal_size
    shutil.get_terminal_size = lambda *_, **__: size  # type: ignore
    try:
        helpio = io.StringIO()
        with (
            contextlib.redirect_stdout(helpio),
            contextlib.suppress(
                SystemExit,
            ),
        ):
            sys.argv = ["docsig", "--help"]
            main()

        return helpio.getvalue()
    finally:
        shutil.get_terminal_size = original  # type: ignore


def _main() -> None:
    # this won't work if there's a conflict in the file as it analyzes
    # indents
    readme_content = CONFLICT_PATTERN.sub("", README.read_text())
    match = COMMANDLINE_PATTERN.search(readme_content)
    if match is not None:
        docsig_help = _normalize_for_alternate_argparse_versions(
            re.sub(r"^", "    ", _help(), flags=re.MULTILINE),
        )
        updated_readme_content = (
            COMMANDLINE_PATTERN.sub(rf"\1{docsig_help}", readme_content)
            .replace("    \n", "\n")
            .replace("\n\n\n", "\n\n")
        )
        if updated_readme_content != readme_content:
            README.write_text(updated_readme_content)
            # error if readme not correct to ensure ci knows about it
            sys.exit("readme was not up-to-date, fixed")


# the console block is followed by further content, as it is in the
# real README.rst; a block at the very end of a file is not a fixed
# point, since the trailing indent has no newline after it to collapse
SECTION = """\
Commandline
***********

.. code-block:: console

    {body}

Footer
======

tail
"""


class Test:
    """Tests for this script."""

    readme: Path

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
        self.readme = tmp_path / "README.rst"
        monkeypatch.setattr(f"{__name__}.README", self.readme)

    def test_stale_help_replaced(self) -> None:
        """Test an out-of-date console block is regenerated."""
        self.readme.write_text(SECTION.format(body="stale"), encoding="utf-8")
        with pytest.raises(SystemExit) as err:
            _main()

        assert str(err.value) == "readme was not up-to-date, fixed"
        assert "usage: docsig" in self.readme.read_text(encoding="utf-8")

    def test_current_help_untouched(self) -> None:
        """Test a regenerated block is a fixed point on a second run."""
        self.readme.write_text(SECTION.format(body="stale"), encoding="utf-8")
        with pytest.raises(SystemExit):
            _main()

        before = self.readme.read_text(encoding="utf-8")
        _main()
        assert self.readme.read_text(encoding="utf-8") == before

    def test_no_commandline_section(self) -> None:
        """Test a readme with no console block is left alone."""
        self.readme.write_text("Nothing to update here\n", encoding="utf-8")
        _main()
        assert self.readme.read_text(encoding="utf-8") == (
            "Nothing to update here\n"
        )

    def test_conflict_markers_stripped(self) -> None:
        """Test conflict markers do not defeat the section match."""
        section = SECTION.format(body="stale")
        self.readme.write_text(f"<<<<<<< HEAD\n{section}", encoding="utf-8")
        with pytest.raises(SystemExit):
            _main()

        assert "<<<<<<<" not in self.readme.read_text(encoding="utf-8")

    def test_normalizes_older_argparse(self) -> None:
        """Test help from an older interpreter is normalized."""
        text = _normalize_for_alternate_argparse_versions(
            "usage: docsig [path [path ...]]\n    optional arguments:\n",
        )
        assert text == "usage: docsig [path ...]\n    options:\n"


if __name__ == "__main__":
    _main()
