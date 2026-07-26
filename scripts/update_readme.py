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
    shutil.get_terminal_size = lambda: os.terminal_size(  # type: ignore
        (93, 24),
    )
    helpio = io.StringIO()
    with contextlib.redirect_stdout(helpio), contextlib.suppress(SystemExit):
        sys.argv = ["docsig", "--help"]
        main()

    return helpio.getvalue()


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


if __name__ == "__main__":
    _main()
