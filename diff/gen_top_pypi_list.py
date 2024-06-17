"""
gen_top_pypi_list
=================
"""

# inspiration from https://github.com/psf/black/tree/main/gallery

from __future__ import annotations

import json
from argparse import ArgumentParser, Namespace
from urllib.request import urlopen

PYPI_TOP_PACKAGES = (
    "https://hugovk.github.io/top-pypi-packages/"
    "top-pypi-packages-30-days.min.json"
)


def _parse_args() -> Namespace:
    p = ArgumentParser()
    p.add_argument(
        "-n",
        "--number",
        type=int,
        help="number of packages to fetch",
    )
    p.add_argument(
        "-e",
        "--exclude",
        nargs="+",
        help="packages to exclude",
    )
    return p.parse_args()


def _get_top_packages(exclude: list[str]) -> list[str]:
    # filter out exclusions here so that slicing the list later will
    # always return the desired number
    with urlopen(PYPI_TOP_PACKAGES) as page:
        return [
            i["project"]
            for i in json.load(page)["rows"]
            if i["project"] not in exclude
        ]


def _get_latest_version(package: str) -> str:
    with urlopen(f"https://pypi.org/pypi/{package}/json") as page:
        return list(json.load(page)["releases"].keys())[-1]


def _main() -> None:
    args = _parse_args()
    for package in _get_top_packages(args.exclude)[slice(None, args.number)]:

        # slice ahead of getting latest versions so as not to make
        # unnecessary requests
        print(f"{package}=={_get_latest_version(package)}")


if __name__ == "__main__":
    _main()
