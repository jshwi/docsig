"""Print help for makefile."""

import re
import textwrap
from pathlib import Path


def _main() -> None:
    comment = "#:"
    file = Path("Makefile")
    targets = {}
    lines = [i.rstrip() for i in file.read_text(encoding="utf-8").splitlines()]
    for prev_line, line in zip([""] + lines[:-1], lines):
        target_match = re.match(r"^([a-zA-Z_-]+):", line)
        if target_match:
            target = target_match.group(1)
            if comment in line:
                desc = line.split(comment, 1)[1].strip()
                targets[target] = desc
            elif prev_line and prev_line.startswith(comment):
                desc = prev_line[3:].strip()
                targets[target] = desc

    longest_target = max(map(len, targets))
    for target, desc in sorted(targets.items()):
        wrapped = textwrap.wrap(desc, width=64)
        for line in wrapped:
            tab = (longest_target - len(target) + 1) * " "
            print(f"\033[36m{target}\033[0m{tab} -- {line}")


if __name__ == "__main__":
    _main()
