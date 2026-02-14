"""
tests
=====

Test package for ``docsig``.
"""

import typing as t
from pathlib import Path

from . import _templates  # noqa

FixtureMain = t.Callable[..., t.Union[str, int]]
FixtureFlake8 = t.Callable[..., int]
FixturePatchArgv = t.Callable[..., None]
FixtureInitPyprojectTomlFile = t.Callable[[dict[str, t.Any]], Path]


class FixtureInitFile(
    t.Protocol,
):  # pylint: disable=too-few-public-methods
    """Type for ``fixture_init_file``."""

    def __call__(self, content: str, path: Path = ..., /) -> Path:
        """Type for ``fixture_init_file``."""


class FixtureMakeTree(t.Protocol):  # pylint: disable=too-few-public-methods
    """Type for ``fixture_mock_tree``."""

    def __call__(self, obj: t.Dict[t.Any, t.Any], path: Path = ..., /) -> None:
        """Type for ``fixture_make_tree``."""


CHECK_ARGS = (
    "--check-class",
    "--check-protected",
    "--check-overridden",
    "--check-dunders",
    "--check-property-returns",
    "--check-protected-class-methods",
    "--check-nested",
)
FAIL_CHECK_ARGS = tuple(f"f-{i[8:]}" for i in CHECK_ARGS)
WILL_ERROR = 'echo "Hello World!"'
TREE = {
    "file1.txt": [],
    "file2.txt": [],
    "file3.txt": [],
    "file4.txt": [],
    "file5.txt": [],
    "file10.txt": [],
    "file[1].txt": [],
    ".pyaud_cache": {
        "7.5.1": {
            "CACHEDIR.TAG": [WILL_ERROR],
            "files.json": [WILL_ERROR],
            ".gitignore": ["# Created by pyaud automatically.", "*"],
        },
    },
    "CODE_OF_CONDUCT.md": [WILL_ERROR],
    ".pylintrc": [WILL_ERROR],
    "LICENSE": [WILL_ERROR],
    ".pytest_cache": {
        "CACHEDIR.TAG": [WILL_ERROR],
        "README.md": [WILL_ERROR],
        ".gitignore": ["# Created by pytest automatically.", "*"],
        "v": {
            "cache": {
                "nodeids": [WILL_ERROR],
                "lastfailed": [WILL_ERROR],
                "stepwise": "",
            },
            "randomly_seed": [WILL_ERROR],
        },
    },
    "CHANGELOG.md": [WILL_ERROR],
    "dist": {
        "docsig-0.49.1.tar.gz": [WILL_ERROR],
        "docsig-0.49.2-py3-none-any.whl": [WILL_ERROR],
        "docsig-0.49.2.tar.gz": [WILL_ERROR],
        "docsig-0.49.0-py3-none-any.whl": [WILL_ERROR],
        "docsig-0.49.0.tar.gz": [WILL_ERROR],
        "docsig-0.49.1-py3-none-any.whl": [WILL_ERROR],
    },
    ".pre-commit-config.yaml": [WILL_ERROR],
    ".coverage": [WILL_ERROR],
    "Makefile": [WILL_ERROR],
    "whitelist.py": [],
    ".pre-commit-hooks.yaml": [WILL_ERROR],
    "pyproject.toml": [],
    ".bumpversion.cfg": [WILL_ERROR],
    "node_modules": {
        ".cache": {
            "prettier": {
                ".prettier-caches": {
                    "7f51ae3462154079bc96a79583b977616b1ad315.json": [
                        WILL_ERROR,
                    ],
                },
            },
        },
    },
    "tests": {
        "misc_test.py": [],
        "conftest.py": [],
        "disable_test.py": [],
        "__init__.py": [],
        "__pycache__": {
            "_test.cpython-38-pytest-8.1.1.pyc": [WILL_ERROR],
            "__init__.cpython-38.pyc": [WILL_ERROR],
            "disable_test.cpython-38-pytest-8.1.1.pyc": [WILL_ERROR],
            "misc_test.cpython-38-pytest-8.1.1.pyc": [WILL_ERROR],
            "_test.cpython-38.pyc": [WILL_ERROR],
            "conftest.cpython-38-pytest-8.1.1.pyc": [WILL_ERROR],
        },
        "TESTS.md": [WILL_ERROR],
        "git_test.py": [],
        "_test.py": [],
    },
    ".conform.yaml": [WILL_ERROR],
    "docs": {
        "index.rst": [WILL_ERROR],
        "requirements.txt": [WILL_ERROR],
        "docsig.rst": [WILL_ERROR],
        "conf.py": [],
        "static": {"docsig.svg": [WILL_ERROR]},
        "examples": {
            "classes.rst": [WILL_ERROR],
            "message-control.rst": [WILL_ERROR],
        },
    },
    ".readthedocs.yml": [WILL_ERROR],
    ".prettierignore": [WILL_ERROR],
    ".editorconfig": [WILL_ERROR],
    "docsig": {
        "_stub.py": [],
        "_report.py": [],
        "_main.py": [],
        "_version.py": [],
        "_module.py": [],
        "__init__.py": [],
        "_display.py": [],
        "_hooks.py": [],
        "__pycache__": {
            "_core.cpython-311.pyc": [WILL_ERROR],
            "__init__.cpython-38.pyc": [WILL_ERROR],
            "_core.cpython-38.pyc": [WILL_ERROR],
            "_main.cpython-311.pyc": [WILL_ERROR],
            "_decorators.cpython-38.pyc": [WILL_ERROR],
            "_message.cpython-311.pyc": [WILL_ERROR],
            "_config.cpython-311.pyc": [WILL_ERROR],
            "_config.cpython-38.pyc": [WILL_ERROR],
            "messages.cpython-311.pyc": [WILL_ERROR],
            "_display.cpython-311.pyc": [WILL_ERROR],
            "_display.cpython-38.pyc": [WILL_ERROR],
            "_stub.cpython-311.pyc": [WILL_ERROR],
            "_decorators.cpython-311.pyc": [WILL_ERROR],
            "_hooks.cpython-38.pyc": [WILL_ERROR],
            "_utils.cpython-38.pyc": [WILL_ERROR],
            "_report.cpython-311.pyc": [WILL_ERROR],
            "_directives.cpython-38.pyc": [WILL_ERROR],
            "_hooks.cpython-311.pyc": [WILL_ERROR],
            "__main__.cpython-38.pyc": [WILL_ERROR],
            "_version.cpython-311.pyc": [WILL_ERROR],
            "_utils.cpython-311.pyc": [WILL_ERROR],
            "_module.cpython-311.pyc": [WILL_ERROR],
            "_stub.cpython-38.pyc": [WILL_ERROR],
            "messages.cpython-38.pyc": [WILL_ERROR],
            "_message.cpython-38.pyc": [WILL_ERROR],
            "_report.cpython-38.pyc": [WILL_ERROR],
            "_version.cpython-38.pyc": [WILL_ERROR],
            "_directives.cpython-311.pyc": [WILL_ERROR],
            "_git.cpython-38.pyc": [WILL_ERROR],
            "_module.cpython-38.pyc": [WILL_ERROR],
            "_main.cpython-38.pyc": [WILL_ERROR],
            "__init__.cpython-311.pyc": [WILL_ERROR],
            "__main__.cpython-311.pyc": [WILL_ERROR],
        },
        "_message.py": [],
        "_core.py": [],
        "_decorators.py": [],
        "messages.py": [],
        "py.typed": [WILL_ERROR],
        "_config.py": [],
        "__main__.py": [],
        "_utils.py": [],
        "_directives.py": [],
    },
    ".mypy_cache": {
        "CACHEDIR.TAG": [WILL_ERROR],
        "3.12": {},
        ".gitignore": ["# Automatically created by mypy", "*"],
        "3.8": {},
    },
    ".gitignore": [
        "*build/",
        "*coverage*",
        "*venv",
        ".DS_Store",
        ".env",
        "__pycache__/",
        "dist/",
        "node_modules/",
    ],
    "package-lock.json": [WILL_ERROR],
    "package.json": [WILL_ERROR],
    "CONTRIBUTING.md": [WILL_ERROR],
    ".github": {
        "COMMIT_POLICY.md": [WILL_ERROR],
        "workflows": {
            "codeql-analysis.yml": [WILL_ERROR],
            "build.yaml": [WILL_ERROR],
        },
        "dependabot.yml": [WILL_ERROR],
    },
    "coverage.xml": [WILL_ERROR],
    "poetry.lock": [WILL_ERROR],
    "README.rst": [WILL_ERROR],
    ".git": {"HEAD": [WILL_ERROR]},
    ".idea": {
        "docsig.iml": [WILL_ERROR],
        "jsonSchemas.xml": [WILL_ERROR],
        "inspectionProfiles": {
            "profiles_settings.xml": [WILL_ERROR],
            "Project_Default.xml": [WILL_ERROR],
        },
        "codeStyles": {
            "Project.xml": [WILL_ERROR],
            "codeStyleConfig.xml": [WILL_ERROR],
        },
        "material_theme_project_new.xml": [WILL_ERROR],
        "vcs.xml": [WILL_ERROR],
        ".gitignore": [
            "/dataSources.local.xml",
            "/dataSources/",
            "/dictionaries",
            "/httpRequests/",
            "/shelf/",
            "/sonarlint/",
            "/tasks.xml",
            "/usage.statistics.xml",
            "/workspace.xml",
        ],
        "workspace.xml": [WILL_ERROR],
        "modules.xml": [WILL_ERROR],
        "watcherTasks.xml": [WILL_ERROR],
        "dictionaries": {
            "swhitlock.xml": [WILL_ERROR],
            "default_user.xml": [WILL_ERROR],
        },
        "misc.xml": [WILL_ERROR],
        "scopes": {
            "whitelist_py.xml": [WILL_ERROR],
            "bump2version.xml": [WILL_ERROR],
            "docs__themes_graphite_static.xml": [WILL_ERROR],
            "docs_conf.xml": [WILL_ERROR],
            "_prettierignore.xml": [WILL_ERROR],
            "docs_index.xml": [WILL_ERROR],
            "_pylintrc.xml": [WILL_ERROR],
        },
    },
}
