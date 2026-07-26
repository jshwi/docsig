"""Update copyright year in license and docs."""

import re
from datetime import datetime
from pathlib import Path
from re import Match

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


if __name__ == "__main__":
    _main()
