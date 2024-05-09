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

shutil.get_terminal_size = lambda: os.terminal_size((93, 24))  # type: ignore
helpio = io.StringIO()
with contextlib.redirect_stdout(helpio), contextlib.suppress(SystemExit):
    sys.argv = ["docsig", "--help"]
    main()

path = Path(__file__).parent.parent / "README.rst"
conflict_pattern = re.compile(
    r"^(<<<<<<<|=======|>>>>>>>).*\n?", flags=re.MULTILINE
)
commandline_pattern = re.compile(
    r"(Commandline\s*\*+\s*..\s*code-block::\s*console\s*\n)((?:\s{4}.*\n)+)"
)
# this won't work if there's a conflict in the file as it analyses
# indents
readme_content = conflict_pattern.sub("", path.read_text())
match = commandline_pattern.search(readme_content)
if match is not None:
    docsig_help = re.sub(r"^", "    ", helpio.getvalue(), flags=re.MULTILINE)
    updated_readme_content = (
        commandline_pattern.sub(rf"\1{docsig_help}", readme_content)
        .replace("    \n", "\n")
        .replace("\n\n\n", "\n\n")
    )
    if updated_readme_content != readme_content:
        path.write_text(updated_readme_content)
        # error if readme not correct to ensure ci knows about it
        sys.exit("readme was not up-to-date, fixed")
