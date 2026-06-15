"""
_gitignore
==========

Pytest plugin to ignore paths matched by gitignore during collection.

Derived from pytest-gitignore.

pytest-gitignore: https://github.com/tgs/pytest-gitignore

The original code is a United States Government Work and is in the
public domain.

---

Public Domain notice
====================

National Center for Biotechnology Information.

This software is a "United States Government Work" under the terms of the
United States Copyright Act. It was written as part of the authors'
official duties as United States Government employees and thus cannot
be copyrighted. This software is freely available to the public for
use. The National Library of Medicine and the U.S. Government have not
placed any restriction on its use or reproduction.

Although all reasonable efforts have been taken to ensure the accuracy
and reliability of the software and data, the NLM and the U.S.
Government do not and cannot warrant the performance or results that
may be obtained by using this software or data. The NLM and the U.S.
Government disclaim all warranties, express or implied, including
warranties of performance, merchantability or fitness for any
particular purpose.

Please cite NCBI in any work or product based on this material.
"""

import subprocess
import typing as t
from pathlib import Path

import pytest


def _git_ignores_path(collection_path: Path) -> bool:
    if collection_path.name == ".git":
        return True
    with subprocess.Popen(
        ["git", "check-ignore", str(collection_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as child:
        child.communicate()
        # 0: ignored, 1: not ignored, 128: git error (e.g. symlink loop)
        return child.wait() == 0


# noinspection PyUnusedLocal
@pytest.hookimpl(hookwrapper=True)
def pytest_ignore_collect(
    collection_path: Path,
    config: pytest.Config,  # pylint: disable=unused-argument
) -> t.Generator[None, t.Any, None]:
    """Ignore collection paths that git ignores.

    :param collection_path: Path that pytest is considering for
        collection.
    :param config: Pytest config object.
    :yield: Any.
    """
    outcome = yield
    if not outcome.get_result() and _git_ignores_path(collection_path):
        outcome.force_result(True)
