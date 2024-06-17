"""
check_diff
==========
"""

# inspiration from https://github.com/psf/black/tree/main/gallery

from __future__ import annotations

import difflib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import typing as t
import venv
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen, urlretrieve

import git

BIN = "Scripts" if os.name == "nt" else "bin"
BREAKING_TOKEN = "!:"
CHANGES_MSG = """\
diffs are expected between HEAD and {tag}
running this script is redundant\
"""
CREATE_MSG = "creating {path}"
SUCCESS_MSG = "HEAD results equal to {tag}"
CACHEDIR_TAG = """\
Signature: 8a477f597d28d172789f06886806bc55
# This file is a cache directory tag automatically created by check_diff.py.
# For information about cache directory tags see https://bford.info/cachedir/
"""
DIFF_EXPECTED = "diff expected in '{msg}'"


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
        "-v",
        "--verbose",
        action="store_true",
        help="verbose output",
    )
    p.add_argument(
        "-c",
        "--color",
        action="store_true",
        help="color output",
    )
    return p.parse_args()


def _init_cachedir(location: Path) -> None:
    location.mkdir(exist_ok=True, parents=True)
    (location / "CACHEDIR.TAG").write_text(CACHEDIR_TAG, encoding="utf-8")
    (location / ".gitignore").write_text("*\n", encoding="utf-8")


def _run(*cmd: str | Path, check: bool = True, **kwargs: t.Any) -> str:
    return subprocess.run(
        cmd, check=check, text=True, stdout=subprocess.PIPE, **kwargs
    ).stdout.strip()


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
        _run(
            env_dir / BIN / "python",
            "-m",
            "pip",
            "install",
            docsig,
            "--upgrade",
            "pip",
        )


def _get_diff(a: str, b: str, color: bool) -> str:
    diff = list(difflib.ndiff(a.splitlines(), b.splitlines()))
    if color:
        tokens = {"-": "\033[91m", "+": "\033[92m", "?": "\033[94m"}
        for count, line in enumerate(diff):
            try:
                diff[count] = f"{tokens[line[0]]}{line}\033[0m"
            except KeyError:
                pass

    return "\n".join(diff)


def _runner(env_dir: Path, package: Path) -> str:
    return _run(
        env_dir / BIN / "python",
        "-m",
        "docsig",
        "-cpoDPmNI",
        package,
        check=False,
    )


def _diff_expected(this: git.Repo, rev: str) -> bool:
    changed = False
    for commit in this.git.rev_list(
        f"{rev}..HEAD", ancestry_path=True
    ).splitlines():
        msg = this.git.log(commit, format="%B", max_count=1).splitlines()[0]
        # fix may result in a diff, but the prior diff goes against the
        # expected behaviour
        if BREAKING_TOKEN in msg or msg.startswith("fix:"):
            print(DIFF_EXPECTED.format(msg=msg))
            changed = True

    return changed


def _main() -> int:
    returncode = 0
    this = git.Repo(Path.cwd())
    last_tag = this.git.describe(abbrev=0)
    if _diff_expected(this, last_tag):
        print(CHANGES_MSG.format(tag=last_tag))
        return returncode

    os.environ["PRE_COMMIT_ALLOW_NO_CONFIG"] = "1"
    args = _parse_args()
    location = args.location.resolve()
    _init_cachedir(location)
    env_dir = location / last_tag
    if not env_dir.is_dir():
        print(CREATE_MSG.format(path=env_dir))
        _init_env(env_dir, last_tag)

    packages = [location / i for i in args.packages]
    for package in packages:
        if not package.is_dir():
            print(CREATE_MSG.format(path=package))
            _fetch(package)

        print(package)
        a = _runner(env_dir, package)
        b = _runner(Path(sys.executable).parent.parent, package)
        if a == b:
            print(SUCCESS_MSG.format(tag=last_tag))
        else:
            returncode = 1
            if args.verbose:
                print(_get_diff(a, b, args.color))

    return returncode


if __name__ == "__main__":
    sys.exit(_main())
