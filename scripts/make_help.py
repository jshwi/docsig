# /// script
# requires-python = ">=3.10"
# dependencies = ["pytest>=9.1.1,<10.0"]
# ///
"""Print help for makefile."""

import re
import textwrap
from pathlib import Path

import pytest


def _main() -> None:
    comment = "#:"
    file = Path("Makefile")
    targets = {}
    lines = [i.rstrip() for i in file.read_text(encoding="utf-8").splitlines()]
    for prev_line, line in zip([""] + lines[:-1], lines, strict=True):
        target_match = re.match(r"^([a-zA-Z_-]+):", line)
        if target_match:
            target = target_match.group(1)
            if comment in line:
                desc = line.split(comment, 1)[1].strip()
                targets[target] = desc
            elif prev_line and prev_line.startswith(comment):
                desc = prev_line[3:].strip()
                targets[target] = desc

    longest_target = max(map(len, targets))
    for target, desc in sorted(targets.items()):
        wrapped = textwrap.wrap(desc, width=64)
        for line in wrapped:
            tab = (longest_target - len(target) + 1) * " "
            print(f"\033[36m{target}\033[0m{tab} -- {line}")


class Test:
    """Tests for this script."""

    makefile: Path

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
        self.makefile = tmp_path / "Makefile"

    def run(self, contents: str, capsys: pytest.CaptureFixture) -> str:
        """Write a makefile, print its help, return the plain output.

        :param contents: Contents of the makefile to document.
        :param capsys: Capture sys out and err.
        :return: Printed help with its color escapes removed.
        """
        self.makefile.write_text(contents, encoding="utf-8")
        _main()
        return re.sub(r"\033\[\d+m", "", capsys.readouterr().out)

    def test_preceding_comment(self, capsys: pytest.CaptureFixture) -> None:
        """Test a target documented by the line above it.

        :param capsys: Capture sys out and err.
        """
        out = self.run("#: run the tests\ntests:\n\t@echo\n", capsys)
        assert out == "tests  -- run the tests\n"

    def test_inline_comment(self, capsys: pytest.CaptureFixture) -> None:
        """Test a target documented on its own line.

        :param capsys: Capture sys out and err.
        """
        out = self.run("tests: #: run the tests\n\t@echo\n", capsys)
        assert out == "tests  -- run the tests\n"

    def test_undocumented_target_omitted(
        self,
        capsys: pytest.CaptureFixture,
    ) -> None:
        """Test a target with no comment is not listed.

        :param capsys: Capture sys out and err.
        """
        out = self.run("#: run the tests\ntests:\n\nlint:\n\t@echo\n", capsys)
        assert "lint" not in out

    def test_targets_sorted(self, capsys: pytest.CaptureFixture) -> None:
        """Test targets are listed in alphabetical order.

        :param capsys: Capture sys out and err.
        """
        out = self.run("#: b\ntests:\n\n#: a\nlint:\n", capsys)
        assert out.splitlines() == ["lint   -- a", "tests  -- b"]

    def test_padded_to_longest_target(
        self,
        capsys: pytest.CaptureFixture,
    ) -> None:
        """Test descriptions align against the longest target name.

        :param capsys: Capture sys out and err.
        """
        out = self.run("#: a\nlint:\n\n#: b\ninstall-venv:\n", capsys)
        assert out.splitlines() == [
            "install-venv  -- b",
            "lint          -- a",
        ]

    def test_long_description_wrapped(
        self,
        capsys: pytest.CaptureFixture,
    ) -> None:
        """Test a description longer than the width spans lines.

        :param capsys: Capture sys out and err.
        """
        out = self.run(f"#: {'word ' * 20}\nlint:\n", capsys)
        lines = out.splitlines()
        assert len(lines) > 1
        assert all(i.startswith("lint  -- ") for i in lines)


if __name__ == "__main__":
    _main()
