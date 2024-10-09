"""
docsig._files
=============
"""

from __future__ import annotations as _

import logging as _logging
import os as _os
import re as _re
import typing as _t
from pathlib import Path as _Path

from pathspec import PathSpec as _PathSpec
from pathspec.patterns import GitWildMatchPattern as _GitWildMatchPattern
from wcmatch.pathlib import Path as _WcPath

FILE_INFO = "%s: %s"


class _Gitignore(_PathSpec):
    def _get_repo_relative_to(self, path: _Path) -> _Path | None:
        if (path / ".git" / "HEAD").is_file():
            return path

        if str(path) == _os.path.abspath(_os.sep):
            return None

        return self._get_repo_relative_to(path.parent)

    def __init__(self) -> None:
        patterns = []
        repo = self._get_repo_relative_to(_Path.cwd())
        # only consider gitignore patterns valid if inside a git repo
        # there might be stray gitignore files lying about
        if repo is not None:
            # add patterns from all gitignore files
            # adjust patterns to account for their relative paths
            for file in repo.rglob(".gitignore"):
                for pattern in file.read_text(encoding="utf-8").splitlines():
                    if pattern.startswith("#"):
                        continue

                    # if pattern starts with "/" then os.path.join will
                    # consider it in the filesystem root, and it will
                    # only ever return /pattern
                    if pattern.startswith("/"):
                        pattern = pattern[1:]

                    # use os.path.dirname, so it joins without a leading
                    # "./", like it does with pathlib parent
                    # use os.path.join so trailing slash is preserved
                    # replace sep with "/" as, even on windows,
                    # gitignore patterns only ever use "/"
                    patterns.append(
                        _os.path.join(
                            _os.path.dirname(file.relative_to(repo)),
                            pattern.strip(),
                        ).replace(_os.sep, "/")
                    )

        super().__init__(map(_GitWildMatchPattern, patterns))


def _glob(path: _Path, pattern: str) -> bool:
    # pylint: disable=no-member
    return _WcPath(str(path)).globmatch(pattern)  # type: ignore


class Paths(_t.List[_Path]):
    """Collect a list of valid paths.

    :param paths: Path(s) to parse ``Module``(s) from.
    :param patterns: List pf regular expression of files and dirs to
        exclude from checks.
    :param excludes: Files or dirs to exclude from checks.
    :param include_ignored: Check files even if they match a gitignore
        pattern.
    """

    def __init__(
        self,
        *paths: _Path | str,
        patterns: list[str],
        excludes: list[str] | None = None,
        include_ignored: bool = False,
    ) -> None:
        super().__init__()
        self._patterns = patterns
        self._excludes = excludes or []
        self._include_ignored = include_ignored
        self._gitignore = _Gitignore()
        self._logger = _logging.getLogger(__package__)
        for path in paths:
            self._populate(_Path(path))

        for path in list(self):
            if str(path) != "." and (
                any(_re.match(i, str(path)) for i in self._patterns)
                or any(_glob(path, i) for i in self._excludes)
            ):
                self._logger.debug(
                    FILE_INFO, path, "in exclude list, skipping"
                )
                self.remove(path)

        self.sort()

    def _populate(self, root: _Path) -> None:
        if not root.exists():
            raise FileNotFoundError(root)

        if not self._include_ignored and self._gitignore.match_file(root):
            self._logger.debug(FILE_INFO, root, "in gitignore, skipping")
            return

        if root.is_file():
            self.append(root)

        if root.is_dir():
            for path in root.iterdir():
                self._populate(path)
