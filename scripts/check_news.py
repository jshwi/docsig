"""Check for news fragment when making a production change."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import git

ALLOWED_KINDS = (
    "add",
    "change",
    "deprecate",
    "fix",
    "hack",
    "security",
    "remove",
)
COMMIT_FORMAT = "{type}: {description} (#{issue})"


def _main() -> int | str:
    commit_msg = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()[0]
    if any(commit_msg.startswith(i) for i in ALLOWED_KINDS):
        match = re.match(r"^(\w+):\s+(.+)\s+\(#(\d+)\)$", commit_msg)
        if match is None:
            return f"commit message not in the format of '{COMMIT_FORMAT}'"

        kind, desc, issue = match.group(1), match.group(2), match.group(3)
        repo = git.Repo(Path.cwd())
        diff = repo.git.diff("HEAD", cached=True, name_only=True)
        if not re.findall(r"^changelog/.*\.md$", diff, re.MULTILINE):
            name = f"{issue}.{kind}.md"
            output = subprocess.run(
                ["towncrier", "create", "-c", desc, name],
                capture_output=True,
                check=True,
                text=True,
            ).stdout
            diff = "\n".join(repo.untracked_files)
            news = Path(
                re.findall(r"^changelog/.*\.md$", diff, re.MULTILINE)[0]
            )
            if len(news.name.split(".")) == 4 and news.read_text(
                encoding="utf-8"
            ) == (Path("changelog") / name).read_text(encoding="utf-8"):
                news.unlink()
                return 0

            return output

    return 0


if __name__ == "__main__":
    sys.exit(_main())
