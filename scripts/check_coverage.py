"""Check coverage summary meets a line-coverage threshold."""

import json
import sys
from argparse import ArgumentParser
from pathlib import Path


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


if __name__ == "__main__":
    sys.exit(_main())
