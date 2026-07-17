"""Check CLAUDE.md is not stale relative to the working tree."""

import re
import sys
from pathlib import Path

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


if __name__ == "__main__":
    sys.exit(_main())
