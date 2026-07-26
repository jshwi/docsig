"""Update copyright year in license and docs."""

import re
from datetime import datetime
from pathlib import Path
from re import Match

import pytest

REPO = Path(__file__).parent.parent
PATTERNS = {
    Path("LICENSE"): re.compile(r"Copyright \(c\) (\d{4})"),
    Path("docs") / "conf.py": re.compile(r'copyright = "(\d{4})'),
}


def _replace_year(match: Match) -> str:
    return f"{match.group()[:-4]}{datetime.now().year}"


def _main() -> None:
    for relpath, pattern in PATTERNS.items():
        file = REPO / relpath
        text = file.read_text(encoding="utf-8")
        new = pattern.sub(_replace_year, text)
        if text != new:
            file.write_text(new, encoding="utf-8")


class Test:
    """Tests for this script."""

    year: int
    license_file: Path
    conf: Path

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
        monkeypatch.setattr(f"{__name__}.REPO", tmp_path)
        self.year = datetime.now().year
        self.license_file = tmp_path / "LICENSE"
        self.conf = tmp_path / "docs" / "conf.py"
        self.conf.parent.mkdir()

    def test_stale_license_year(self) -> None:
        """Test an out-of-date license year is replaced."""
        self.license_file.write_text("Copyright (c) 1999 S", encoding="utf-8")
        self.conf.write_text('copyright = "1999"', encoding="utf-8")
        _main()
        assert self.license_file.read_text("utf-8") == (
            f"Copyright (c) {self.year} S"
        )

    def test_stale_docs_year(self) -> None:
        """Test an out-of-date docs year is replaced."""
        self.license_file.write_text("Copyright (c) 1999 S", encoding="utf-8")
        self.conf.write_text('copyright = "1999"', encoding="utf-8")
        _main()
        assert self.conf.read_text("utf-8") == f'copyright = "{self.year}"'

    def test_current_year_untouched(self) -> None:
        """Test a file already on the current year is not rewritten."""
        self.license_file.write_text(
            f"Copyright (c) {self.year} S",
            encoding="utf-8",
        )
        self.conf.write_text(
            f'copyright = "{self.year}"',
            encoding="utf-8",
        )
        before = self.license_file.stat().st_mtime_ns
        _main()
        assert self.license_file.stat().st_mtime_ns == before

    def test_unrelated_year_untouched(self) -> None:
        """Test a year outside the copyright notice is left alone."""
        self.license_file.write_text(
            "Copyright (c) 1999 S\nreleased in 1998",
            encoding="utf-8",
        )
        self.conf.write_text('copyright = "1999"', encoding="utf-8")
        _main()
        assert "released in 1998" in self.license_file.read_text("utf-8")


if __name__ == "__main__":
    _main()
