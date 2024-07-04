"""
check_diff
==========

Check if introduced change will result in an unexpected pipeline result.

This will not run if a commit indicates a breaking change is expected.
"""

# inspiration from https://github.com/psf/black/tree/main/gallery

from __future__ import annotations

import contextlib
import difflib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import venv
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen, urlretrieve

import git

BIN = "Scripts" if os.name == "nt" else "bin"
RETURNCODE_TOKENS = ("!:", "fix:")
DIFF_TOKENS = ("add:", "change:", "hack:", "remove:", *RETURNCODE_TOKENS)
CACHEDIR_TAG = """\
Signature: 8a477f597d28d172789f06886806bc55
# This file is a cache directory tag automatically created by check_diff.py.
# For information about cache directory tags see https://bford.info/cachedir/
"""


def _parse_args() -> Namespace:
    p = ArgumentParser()
    p.add_argument(
        "location",
        type=Path,
        help="location to store cache in",
    )
    p.add_argument(
        "packages",
        nargs="+",
        help="packages to test docsig against",
    )
    p.add_argument(
        "-d",
        "--diff",
        action="store_true",
        help="show diff",
    )
    p.add_argument(
        "-c",
        "--color",
        action="store_true",
        help="color output",
    )
    p.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="run regardless of commit messages",
    )
    return p.parse_args()


def _init_cachedir(location: Path) -> None:
    location.mkdir(exist_ok=True, parents=True)
    (location / "CACHEDIR.TAG").write_text(CACHEDIR_TAG, encoding="utf-8")
    (location / ".gitignore").write_text("*\n", encoding="utf-8")


def _fetch(path: Path) -> None:
    """Fetch the package."""
    name, version = path.name.rsplit("-", maxsplit=1)
    with urlopen(f"https://pypi.org/pypi/{name}/json") as page:
        for source in json.load(page)["releases"][version]:
            if source["python_version"] == "source":
                with tarfile.open(urlretrieve(source["url"])[0]) as src:
                    members = [
                        i for i in src.getmembers() if i.name.endswith(".py")
                    ]
                    src.extractall(path=path.parent, members=members)


def _init_env(env_dir: Path, rev: str) -> None:
    with TemporaryDirectory() as tmp_dir:
        docsig = Path(tmp_dir)
        shutil.copytree(Path.cwd() / ".git", docsig / ".git")
        repo = git.Repo(docsig)
        repo.git.reset(hard=True)
        repo.git.checkout(rev)
        venv.create(env_dir, with_pip=True)
        subprocess.run(
            [
                env_dir / BIN / "python",
                env_dir / BIN / "pip",
                "install",
                docsig,
                "--upgrade",
                "pip",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )


def _get_diff(a: str, b: str, color: bool) -> str:
    diff = list(difflib.ndiff(a.splitlines(), b.splitlines()))
    if color:
        tokens = {"-": "\033[91m", "+": "\033[92m", "?": "\033[94m"}
        for count, line in enumerate(diff):
            with contextlib.suppress(KeyError):
                diff[count] = f"{tokens[line[0]]}{line}\033[0m"

    return "\n".join(diff)


def _runner(env_dir: Path, package: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            env_dir / BIN / "python",
            env_dir / BIN / "docsig",
            "-cpoDPmNI",
            package,
        ],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
    )


def _ne_expected(this: git.Repo, rev: str) -> tuple[bool, bool]:
    returncode = diff = False
    for commit in this.git.rev_list(
        f"{rev}..HEAD", ancestry_path=True
    ).splitlines():
        msg = this.git.log(commit, format="%B", max_count=1).splitlines()[0]
        if any(i in msg for i in RETURNCODE_TOKENS):
            print(f"returncode variance expected in '{msg}'")
            returncode = True

        if any(i in msg for i in DIFF_TOKENS):
            print(f"output diff expected in '{msg}'")
            diff = True

    return returncode, diff


def _main() -> int:
    os.environ["PRE_COMMIT_ALLOW_NO_CONFIG"] = "1"
    returncode = 0
    this = git.Repo(Path.cwd())
    last_tag = this.git.describe(abbrev=0)
    args = _parse_args()
    retcode_expected = diff_expected = False
    if not args.force:
        retcode_expected, diff_expected = _ne_expected(this, last_tag)
        if retcode_expected and diff_expected:
            print(f"variances are expected between HEAD and {last_tag}")
            print("running this check is redundant")
            return returncode

    location = args.location.resolve()
    _init_cachedir(location)
    env_dir = location / last_tag
    if not env_dir.is_dir():
        print(f"creating {env_dir}")
        _init_env(env_dir, last_tag)

    packages = [location / i for i in args.packages]
    for package in packages:
        if not package.is_dir():
            print(f"creating {package}")
            _fetch(package)

        print(package)
        a = _runner(env_dir, package)
        b = _runner(Path(sys.executable).parent.parent, package)
        if not retcode_expected and a.returncode != b.returncode:
            print(f"HEAD returncode not equal to {last_tag}")
            returncode = 1

        diff = _get_diff(a.stdout, b.stdout, args.color)
        if diff:
            if not diff_expected:
                returncode = 1
                args.diff = True

            if args.diff:
                print(diff)

    return returncode


if __name__ == "__main__":
    sys.exit(_main())
