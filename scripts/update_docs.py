"""Update documentation when changes have been made to docsig."""

import contextlib
import io
import re
import sys
from pathlib import Path

from docsig import main

SCRIPTS_DIR = Path(__file__).parent
REPO = SCRIPTS_DIR.parent
DOCS_DIR = REPO / "docs"
USAGE = DOCS_DIR / "usage"
TOC = """\
.. toctree::
   :titlesonly:

   {option}\
"""
TEMPLATE = """\
{title}
{underline}

{description}

.. code-block:: python

    >>> from docsig import docsig
"""


def generate_configurations() -> None:
    """Generate documentation for help options."""
    categories = "check", "ignore"
    configuration_dir = USAGE / "configuration"
    configuration_dir.mkdir(exist_ok=True, parents=True)
    helpio = io.StringIO()
    with contextlib.redirect_stdout(helpio), contextlib.suppress(SystemExit):
        sys.argv = ["docsig", "--help"]
        main()

    for category in categories:
        toc_file = USAGE / f"{category}-configuration.rst"
        cur_content = toc_file.read_text(encoding="utf-8")
        tocs = []
        for line in helpio.getvalue().splitlines():
            try:
                parts = line.split()
                option = parts[1]
                if not option.startswith(f"--{category}"):
                    continue

                option = parts[1][2:]
                tocs.append(TOC.format(option=f"configuration/{option}"))
                doc_path = configuration_dir / f"{option}.rst"
                if not doc_path.is_file():
                    title = option.replace("-", " ").capitalize()
                    doc_path.write_text(
                        TEMPLATE.format(
                            title=title,
                            underline=len(title) * "=",
                            description=" ".join(parts[2:]),
                        ),
                        encoding="utf-8",
                    )
            except IndexError:
                continue

        content = "\n\n".join(sorted(tocs))
        content = f"{content}\n"
        if cur_content != content:
            toc_file.write_text(content)


def generate_messages() -> None:  # pylint: disable=too-many-locals
    """Generate documentation for messages."""
    categories = {1: "docstring", 2: "config"}
    messages_dir = USAGE / "messages"
    messages_dir.mkdir(exist_ok=True, parents=True)
    pattern = re.compile(r"([^:]+): ([^(]+) \(([^)]+)\)")
    msgio = io.StringIO()
    with contextlib.redirect_stdout(msgio), contextlib.suppress(SystemExit):
        sys.argv = ["docsig", "--list"]
        main()

    for index, category in categories.items():
        toc_file = USAGE / f"{category}-messages.rst"
        cur_content = toc_file.read_text(encoding="utf-8")
        tocs = []
        for message in msgio.getvalue().splitlines():
            match = pattern.search(message)
            if match is not None:
                code = match.group(1)
                symbolic = match.group(3)
                if code.startswith(f"E{index}"):
                    title = f"{code}: {symbolic}"
                    option = f"{code.lower()}-{symbolic}"
                    tocs.append(TOC.format(option=f"messages/{option}"))
                    path = messages_dir / f"{option}.rst"
                    if not path.is_file():
                        path.write_text(
                            TEMPLATE.format(
                                title=title.capitalize(),
                                underline=len(title) * "=",
                                description=match.group(2).capitalize(),
                            ),
                            encoding="utf-8",
                        )

        content = "\n\n".join(sorted(tocs))
        content = f"{content}\n"
        if cur_content != content:
            toc_file.write_text(content)


if __name__ == "__main__":
    generate_configurations()
    generate_messages()
