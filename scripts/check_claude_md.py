"""Check CLAUDE.md is not stale relative to the working tree."""

import re
import sys
from pathlib import Path

import pytest

SEARCH_DIRS = (
    "",
    "docsig",
    "docsig/plugin",
    "scripts",
    "docs",
    "tests",
    "tests/plugins",
)
UNDOCUMENTED_MODULES = ("_version.py",)


def _main() -> int:
    text = Path("CLAUDE.md").read_text(encoding="utf-8")
    errors = []
    for token in sorted(set(re.findall(r"[\w./-]*\w\.py\b", text))):
        if not any(Path(d, token).is_file() for d in SEARCH_DIRS):
            errors.append(f"CLAUDE.md references {token} which does not exist")

    for path in sorted(Path("docsig").glob("*.py")):
        if path.name.startswith("__") or path.name in UNDOCUMENTED_MODULES:
            continue

        if path.name not in text:
            errors.append(f"{path} exists but CLAUDE.md does not mention it")

    for error in errors:
        print(error, file=sys.stderr)

    return len(errors)


class Test:
    """Tests for this script."""

    claude_md: Path
    package: Path

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
        self.claude_md = tmp_path / "CLAUDE.md"
        self.package = tmp_path / "docsig"
        self.package.mkdir()

    def module(self, name: str) -> None:
        """Add a module to the temporary package.

        :param name: Name of the module file, including its suffix.
        """
        (self.package / name).write_text("", encoding="utf-8")

    def test_documented_module(self) -> None:
        """Test no error when every module is documented."""
        self.module("_core.py")
        self.claude_md.write_text("`_core.py` runs it", encoding="utf-8")
        assert _main() == 0

    def test_undocumented_module(self, capsys: pytest.CaptureFixture) -> None:
        """Test a module missing from CLAUDE.md is reported.

        :param capsys: Capture sys out and err.
        """
        self.module("_core.py")
        self.claude_md.write_text("nothing here", encoding="utf-8")
        assert _main() == 1
        assert (
            f"{Path('docsig') / '_core.py'} exists but"
            in capsys.readouterr().err
        )

    def test_stale_reference(self, capsys: pytest.CaptureFixture) -> None:
        """Test a reference to a deleted file is reported.

        :param capsys: Capture sys out and err.
        """
        self.claude_md.write_text("see `scripts/gone.py`", encoding="utf-8")
        assert _main() == 1
        assert "references scripts/gone.py" in capsys.readouterr().err

    def test_reference_in_search_dir(self) -> None:
        """Test a reference resolves against any of the search dirs."""
        (Path.cwd() / "scripts").mkdir()
        (Path.cwd() / "scripts" / "here.py").write_text("", encoding="utf-8")
        self.claude_md.write_text("see `here.py`", encoding="utf-8")
        assert _main() == 0

    def test_dunder_module_skipped(self) -> None:
        """Test dunder modules need no mention."""
        self.module("__init__.py")
        self.claude_md.write_text("nothing here", encoding="utf-8")
        assert _main() == 0

    def test_undocumented_module_skipped(self) -> None:
        """Test explicitly undocumented modules need no mention."""
        self.module("_version.py")
        self.claude_md.write_text("nothing here", encoding="utf-8")
        assert _main() == 0

    def test_multiple_errors(self, capsys: pytest.CaptureFixture) -> None:
        """Test the return value counts every error.

        :param capsys: Capture sys out and err.
        """
        self.module("_core.py")
        self.module("_config.py")
        self.claude_md.write_text("see `gone.py`", encoding="utf-8")
        assert _main() == 3
        assert len(capsys.readouterr().err.splitlines()) == 3


if __name__ == "__main__":
    sys.exit(_main())
