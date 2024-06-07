"""Update copyright year in license and docs."""

import re
from datetime import datetime
from pathlib import Path
from re import Match

repo = Path(__file__).parent.parent


def _replace_year(match: Match) -> str:
    return f"{match.group(0)[:-4]}{datetime.now().year}"


files = {
    repo / "LICENSE": re.compile(r"Copyright \(c\) (\d{4})"),
    repo / "docs" / "conf.py": re.compile(r'copyright = "(\d{4})'),
}

for file, pattern in files.items():
    text = file.read_text(encoding="utf-8")
    if not pattern.search(text):
        file.write_text(
            pattern.sub(_replace_year, file.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
