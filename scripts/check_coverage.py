# /// script
# requires-python = ">=3.10"
# dependencies = ["pytest>=9.1.1,<10.0"]
# ///
"""Check coverage summary meets a line-coverage threshold."""

import json
import sys
from argparse import ArgumentParser
from pathlib import Path

import pytest


def _main() -> int | str:
    parser = ArgumentParser(description="check coverage meets threshold.")
    parser.add_argument(
        "--coverage-file",
        type=Path,
        default=Path("coverage") / "coverage-summary.json",
        help="path to coverage-summary.json",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.0,
        help="minimum line coverage percent",
    )
    args = parser.parse_args()
    try:
        obj = json.loads(args.coverage_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return f"missing coverage summary at {args.coverage_file}"

    pct = obj.get("total", {}).get("lines", {}).get("pct")
    if not isinstance(pct, (int, float)):
        return f"could not parse coverage percentage: {type(pct)}({pct})"

    if pct < args.threshold:
        return f"line coverage {pct}% is below the {args.threshold}% threshold"

    print(f"line coverage {pct}% meets the {args.threshold}% threshold")
    return 0


class Test:
    """Tests for this script."""

    summary: Path
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
        self.summary = tmp_path / "coverage-summary.json"

    def argv(self, *args: str) -> None:
        """Set the commandline the script parses.

        :param args: Arguments following the program name.
        """
        self.monkeypatch.setattr("sys.argv", ["__main__.py", *args])

    def write(self, pct: object) -> None:
        """Write a coverage summary reporting a line percentage.

        :param pct: Value to report as the line coverage percentage.
        """
        self.summary.write_text(
            json.dumps({"total": {"lines": {"pct": pct}}}),
            encoding="utf-8",
        )

    def test_missing_file(self) -> None:
        """Test a missing summary is reported, not raised."""
        self.argv("--coverage-file", str(self.summary))
        assert str(_main()).startswith("missing coverage summary at")

    def test_invalid_json(self) -> None:
        """Test an unparsable summary is reported, not raised."""
        self.summary.write_text("{", encoding="utf-8")
        self.argv("--coverage-file", str(self.summary))
        assert str(_main()).startswith("missing coverage summary at")

    def test_missing_percentage(self) -> None:
        """Test a summary without a percentage is reported."""
        self.summary.write_text("{}", encoding="utf-8")
        self.argv("--coverage-file", str(self.summary))
        assert "could not parse coverage percentage" in str(_main())

    def test_percentage_not_a_number(self) -> None:
        """Test a non-numeric percentage is reported."""
        self.write("100")
        self.argv("--coverage-file", str(self.summary))
        assert "could not parse coverage percentage" in str(_main())

    def test_below_threshold(self) -> None:
        """Test coverage under the threshold fails."""
        self.write(99.5)
        self.argv("--coverage-file", str(self.summary), "--threshold", "100")
        assert _main() == "line coverage 99.5% is below the 100.0% threshold"

    def test_meets_threshold(self, capsys: pytest.CaptureFixture) -> None:
        """Test coverage at the threshold passes.

        :param capsys: Capture sys out and err.
        """
        self.write(100)
        self.argv("--coverage-file", str(self.summary), "--threshold", "100")
        assert _main() == 0
        assert "meets the 100.0% threshold" in capsys.readouterr().out

    def test_default_threshold(self) -> None:
        """Test the default threshold accepts any coverage."""
        self.write(0)
        self.argv("--coverage-file", str(self.summary))
        assert _main() == 0

    def test_default_coverage_file(self) -> None:
        """Test the summary is looked for under coverage by default."""
        directory = Path.cwd() / "coverage"
        directory.mkdir()
        self.summary = directory / "coverage-summary.json"
        self.write(100)
        self.argv()
        assert _main() == 0


if __name__ == "__main__":
    sys.exit(_main())
