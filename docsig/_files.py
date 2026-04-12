"""
docsig._files
=============

Path collection and filtering for files to check.
"""

import logging as _logging
import os as _os
import re as _re
from pathlib import Path as _Path

from pathspec import PathSpec as _PathSpec
from pathspec.patterns import GitWildMatchPattern as _GitWildMatchPattern
from wcmatch.pathlib import Path as _WcPath

from ._config import Filters as _Filters

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

                    # if the pattern starts with "/" then os.path.join
                    # will consider it in the filesystem root, and it
                    # will only ever return /pattern
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
                        ).replace(_os.sep, "/"),
                    )

        super().__init__(map(_GitWildMatchPattern, patterns))


def _glob(path: _Path, pattern: str) -> bool:
    # pylint: disable-next=no-member
    return _WcPath(str(path)).globmatch(pattern)  # type: ignore


class Files(list[_Path]):
    """Collect paths to check (gitignore and exclude applied).

    :param paths: Path(s) to collect (files or directories).
    :param filters: Filters object.
    """

    def __init__(
        self,
        paths: tuple[str | _Path, ...],
        filters: _Filters,
    ) -> None:
        super().__init__()
        self._include_ignored = filters.include_ignored
        self._gitignore = _Gitignore()
        logger = _logging.getLogger(__package__)
        for path in paths:
            self._populate(_Path(path))

        for path in list(self):
            if str(path) != "." and (
                any(_re.match(i, str(path)) for i in filters.exclude)
                or any(_glob(path, i) for i in filters.excludes)
            ):
                logger.debug(FILE_INFO, path, "in exclude list, skipping")
                self.remove(path)

        self.sort()

    def _populate(self, root: _Path) -> None:
        logger = _logging.getLogger(__package__)
        if not root.exists():
            if root.is_symlink():
                logger.debug(FILE_INFO, root, "broken link, skipping")
                return

            raise FileNotFoundError(root)

        if not self._include_ignored and self._gitignore.match_file(root):
            logger.debug(FILE_INFO, root, "in gitignore, skipping")
            return

        if root.is_file():
            self.append(root)

        if root.is_dir():
            for path in root.iterdir():
                self._populate(path)
