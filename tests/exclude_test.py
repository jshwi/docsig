"""
tests.exclude_test
==================
"""

# pylint: disable=too-many-lines,line-too-long,protected-access
# pylint: disable=too-many-arguments

from __future__ import annotations

import io
from pathlib import Path

import pytest

import docsig

from . import TREE, FixtureMakeTree, InitFileFixtureType, MockMainType, long


def test_exclude_defaults(
    main: MockMainType,
    make_tree: FixtureMakeTree,
    patch_logger: io.StringIO,
) -> None:
    """Test bash script is ignored when under __pycache__ directory.

    :param main: Patch package entry point.
    :param make_tree: Create directory tree from dict mapping.
    :param patch_logger: Logs as an io instance.
    """
    make_tree(Path.cwd(), TREE)
    main(".", long.verbose, long.include_ignored, test_flake8=False)
    expected = [
        f"{Path('.pyaud_cache/7.5.1/CACHEDIR.TAG')}: Parsing Python code failed",
        f"{Path('.pyaud_cache/7.5.1/files.json')}: Parsing Python code failed",
        f"{Path('.pyaud_cache/7.5.1/.gitignore')}: Parsing Python code failed",
        f"{Path('CODE_OF_CONDUCT.md')}: Parsing Python code failed",
        f"{Path('.pylintrc')}: Parsing Python code failed",
        f"{Path('LICENSE')}: Parsing Python code failed",
        f"{Path('CHANGELOG.md')}: Parsing Python code failed",
        f"{Path('.pre-commit-config.yaml')}: Parsing Python code failed",
        f"{Path('.coverage')}: Parsing Python code failed",
        f"{Path('Makefile')}: Parsing Python code failed",
        f"{Path('whitelist.py')}: Parsing Python code successful",
        f"{Path('.pre-commit-hooks.yaml')}: Parsing Python code failed",
        f"{Path('pyproject.toml')}: Parsing Python code successful",
        f"{Path('.bumpversion.cfg')}: Parsing Python code failed",
        f"{Path('tests/misc_test.py')}: Parsing Python code successful",
        f"{Path('tests/conftest.py')}: Parsing Python code successful",
        f"{Path('tests/disable_test.py')}: Parsing Python code successful",
        f"{Path('tests/__init__.py')}: Parsing Python code successful",
        f"{Path('tests/TESTS.md')}: Parsing Python code failed",
        f"{Path('tests/git_test.py')}: Parsing Python code successful",
        f"{Path('tests/_test.py')}: Parsing Python code successful",
        f"{Path('.conform.yaml')}: Parsing Python code failed",
        f"{Path('docs/index.rst')}: Parsing Python code failed",
        f"{Path('docs/requirements.txt')}: Parsing Python code failed",
        f"{Path('docs/docsig.rst')}: Parsing Python code failed",
        f"{Path('docs/conf.py')}: Parsing Python code successful",
        f"{Path('docs/static/docsig.svg')}: Parsing Python code failed",
        f"{Path('docs/examples/classes.rst')}: Parsing Python code failed",
        f"{Path('docs/examples/message-control.rst')}: Parsing Python code failed",
        f"{Path('.readthedocs.yml')}: Parsing Python code failed",
        f"{Path('.prettierignore')}: Parsing Python code failed",
        f"{Path('.editorconfig')}: Parsing Python code failed",
        f"{Path('docsig/_stub.py')}: Parsing Python code successful",
        f"{Path('docsig/_report.py')}: Parsing Python code successful",
        f"{Path('docsig/_main.py')}: Parsing Python code successful",
        f"{Path('docsig/_version.py')}: Parsing Python code successful",
        f"{Path('docsig/_module.py')}: Parsing Python code successful",
        f"{Path('docsig/__init__.py')}: Parsing Python code successful",
        f"{Path('docsig/_display.py')}: Parsing Python code successful",
        f"{Path('docsig/_hooks.py')}: Parsing Python code successful",
        f"{Path('docsig/_message.py')}: Parsing Python code successful",
        f"{Path('docsig/_core.py')}: Parsing Python code successful",
        f"{Path('docsig/_decorators.py')}: Parsing Python code successful",
        f"{Path('docsig/messages.py')}: Parsing Python code successful",
        f"{Path('docsig/py.typed')}: Parsing Python code failed",
        f"{Path('docsig/_config.py')}: Parsing Python code successful",
        f"{Path('docsig/__main__.py')}: Parsing Python code successful",
        f"{Path('docsig/_utils.py')}: Parsing Python code successful",
        f"{Path('docsig/_directives.py')}: Parsing Python code successful",
        f"{Path('.gitignore')}: Parsing Python code failed",
        f"{Path('package-lock.json')}: Parsing Python code failed",
        f"{Path('package.json')}: Parsing Python code failed",
        f"{Path('CONTRIBUTING.md')}: Parsing Python code failed",
        f"{Path('.github/COMMIT_POLICY.md')}: Parsing Python code failed",
        f"{Path('.github/workflows/codeql-analysis.yml')}: Parsing Python code failed",
        f"{Path('.github/workflows/build.yaml')}: Parsing Python code failed",
        f"{Path('.github/dependabot.yml')}: Parsing Python code failed",
        f"{Path('coverage.xml')}: Parsing Python code failed",
        f"{Path('poetry.lock')}: Parsing Python code failed",
        f"{Path('README.rst')}: Parsing Python code failed",
    ]
    assert all(i in patch_logger.getvalue() for i in expected)


def test_exclude_argument(
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test bash script is ignored when exclude argument passed.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = """
#!/usr/bin/env bash
new-ssl() {
  domain="${1}"
  config="${2:-"${domain}.conf"}"
  openssl \
    req \
    -new \
    -newkey \
    rsa:2048 \
    -nodes \
    -sha256 \
    -out "${domain}.csr" \
    -keyout "${domain}.key" \
    -config "${config}"
}

new-ssl "${@}"
"""
    init_file(template)
    assert (
        main(".", long.exclude, r"module[\\/]file.py", test_flake8=False) == 0
    )


def test_gitignore(
    monkeypatch: pytest.MonkeyPatch,
    main: MockMainType,
    make_tree: FixtureMakeTree,
    patch_logger: io.StringIO,
) -> None:
    """Test files properly ignored from reading gitignore files.

    :param monkeypatch: Mock patch environment and attributes.
    :param main: Patch package entry point.
    :param make_tree: Create directory tree from dict mapping.
    :param patch_logger: Logs as an io instance.
    """
    make_tree(Path.cwd(), TREE)
    # remove default excludes to better test nested gitignore files
    monkeypatch.setattr("docsig._core._DEFAULT_EXCLUDES", "^$")
    main(".", long.verbose, test_flake8=False)
    expected = [
        f"{Path('.pyaud_cache/7.5.1/CACHEDIR.TAG')}: in gitignore, skipping",
        f"{Path('.pyaud_cache/7.5.1/files.json')}: in gitignore, skipping",
        f"{Path('.pyaud_cache/7.5.1/.gitignore')}: in gitignore, skipping",
        f"{Path('CODE_OF_CONDUCT.md')}: Parsing Python code failed",
        f"{Path('.pylintrc')}: Parsing Python code failed",
        f"{Path('LICENSE')}: Parsing Python code failed",
        f"{Path('.pytest_cache/CACHEDIR.TAG')}: in gitignore, skipping",
        f"{Path('.pytest_cache/README.md')}: in gitignore, skipping",
        f"{Path('.pytest_cache/.gitignore')}: in gitignore, skipping",
        f"{Path('.pytest_cache/v')}: in gitignore, skipping",
        f"{Path('CHANGELOG.md')}: Parsing Python code failed",
        f"{Path('dist/docsig-0.49.1.tar.gz')}: in gitignore, skipping",
        f"{Path('dist/docsig-0.49.2-py3-none-any.whl')}: in gitignore, skipping",
        f"{Path('dist/docsig-0.49.2.tar.gz')}: in gitignore, skipping",
        f"{Path('dist/docsig-0.49.0-py3-none-any.whl')}: in gitignore, skipping",
        f"{Path('dist/docsig-0.49.0.tar.gz')}: in gitignore, skipping",
        f"{Path('dist/docsig-0.49.1-py3-none-any.whl')}: in gitignore, skipping",
        f"{Path('.pre-commit-config.yaml')}: Parsing Python code failed",
        f"{Path('.coverage')}: in gitignore, skipping",
        f"{Path('Makefile')}: Parsing Python code failed",
        f"{Path('whitelist.py')}: Parsing Python code successful",
        f"{Path('.pre-commit-hooks.yaml')}: Parsing Python code failed",
        f"{Path('pyproject.toml')}: Parsing Python code successful",
        f"{Path('.bumpversion.cfg')}: Parsing Python code failed",
        f"{Path('node_modules/.cache')}: in gitignore, skipping",
        f"{Path('tests/misc_test.py')}: Parsing Python code successful",
        f"{Path('tests/conftest.py')}: Parsing Python code successful",
        f"{Path('tests/disable_test.py')}: Parsing Python code successful",
        f"{Path('tests/__init__.py')}: Parsing Python code successful",
        f"{Path('tests/__pycache__/_test.cpython-38-pytest-8.1.1.pyc')}: in gitignore, skipping",
        f"{Path('tests/__pycache__/__init__.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('tests/__pycache__/disable_test.cpython-38-pytest-8.1.1.pyc')}: in gitignore, skipping",
        f"{Path('tests/__pycache__/misc_test.cpython-38-pytest-8.1.1.pyc')}: in gitignore, skipping",
        f"{Path('tests/__pycache__/_test.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('tests/__pycache__/conftest.cpython-38-pytest-8.1.1.pyc')}: in gitignore, skipping",
        f"{Path('tests/TESTS.md')}: Parsing Python code failed",
        f"{Path('tests/git_test.py')}: Parsing Python code successful",
        f"{Path('tests/_test.py')}: Parsing Python code successful",
        f"{Path('.conform.yaml')}: Parsing Python code failed",
        f"{Path('docs/index.rst')}: Parsing Python code failed",
        f"{Path('docs/requirements.txt')}: Parsing Python code failed",
        f"{Path('docs/docsig.rst')}: Parsing Python code failed",
        f"{Path('docs/conf.py')}: Parsing Python code successful",
        f"{Path('docs/static/docsig.svg')}: Parsing Python code failed",
        f"{Path('docs/examples/classes.rst')}: Parsing Python code failed",
        f"{Path('docs/examples/message-control.rst')}: Parsing Python code failed",
        f"{Path('.readthedocs.yml')}: Parsing Python code failed",
        f"{Path('.prettierignore')}: Parsing Python code failed",
        f"{Path('.editorconfig')}: Parsing Python code failed",
        f"{Path('docsig/_stub.py')}: Parsing Python code successful",
        f"{Path('docsig/_report.py')}: Parsing Python code successful",
        f"{Path('docsig/_main.py')}: Parsing Python code successful",
        f"{Path('docsig/_version.py')}: Parsing Python code successful",
        f"{Path('docsig/_module.py')}: Parsing Python code successful",
        f"{Path('docsig/__init__.py')}: Parsing Python code successful",
        f"{Path('docsig/_display.py')}: Parsing Python code successful",
        f"{Path('docsig/_hooks.py')}: Parsing Python code successful",
        f"{Path('docsig/__pycache__/_core.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/__init__.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_core.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_main.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_decorators.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_message.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_config.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_config.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/messages.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_display.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_display.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_stub.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_decorators.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_hooks.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_utils.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_report.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_directives.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_hooks.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/__main__.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_version.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_utils.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_module.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_stub.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/messages.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_message.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_report.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_version.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_directives.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_git.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_module.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/_main.cpython-38.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/__init__.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/__pycache__/__main__.cpython-311.pyc')}: in gitignore, skipping",
        f"{Path('docsig/_message.py')}: Parsing Python code successful",
        f"{Path('docsig/_core.py')}: Parsing Python code successful",
        f"{Path('docsig/_decorators.py')}: Parsing Python code successful",
        f"{Path('docsig/messages.py')}: Parsing Python code successful",
        f"{Path('docsig/py.typed')}: Parsing Python code failed",
        f"{Path('docsig/_config.py')}: Parsing Python code successful",
        f"{Path('docsig/__main__.py')}: Parsing Python code successful",
        f"{Path('docsig/_utils.py')}: Parsing Python code successful",
        f"{Path('docsig/_directives.py')}: Parsing Python code successful",
        f"{Path('.mypy_cache/CACHEDIR.TAG')}: in gitignore, skipping",
        f"{Path('.mypy_cache/3.12')}: in gitignore, skipping",
        f"{Path('.mypy_cache/.gitignore')}: in gitignore, skipping",
        f"{Path('.mypy_cache/3.8')}: in gitignore, skipping",
        f"{Path('.gitignore')}: Parsing Python code failed",
        f"{Path('package-lock.json')}: Parsing Python code failed",
        f"{Path('package.json')}: Parsing Python code failed",
        f"{Path('CONTRIBUTING.md')}: Parsing Python code failed",
        f"{Path('.github/COMMIT_POLICY.md')}: Parsing Python code failed",
        f"{Path('.github/workflows/codeql-analysis.yml')}: Parsing Python code failed",
        f"{Path('.github/workflows/build.yaml')}: Parsing Python code failed",
        f"{Path('.github/dependabot.yml')}: Parsing Python code failed",
        f"{Path('coverage.xml')}: in gitignore, skipping",
        f"{Path('poetry.lock')}: Parsing Python code failed",
        f"{Path('README.rst')}: Parsing Python code failed",
        f"{Path('.git/HEAD')}: Parsing Python code failed",
        f"{Path('.idea/docsig.iml')}: Parsing Python code failed",
        f"{Path('.idea/jsonSchemas.xml')}: Parsing Python code failed",
        f"{Path('.idea/inspectionProfiles/profiles_settings.xml')}: Parsing Python code failed",
        f"{Path('.idea/inspectionProfiles/Project_Default.xml')}: Parsing Python code failed",
        f"{Path('.idea/codeStyles/Project.xml')}: Parsing Python code failed",
        f"{Path('.idea/codeStyles/codeStyleConfig.xml')}: Parsing Python code failed",
        f"{Path('.idea/material_theme_project_new.xml')}: Parsing Python code failed",
        f"{Path('.idea/vcs.xml')}: Parsing Python code failed",
        f"{Path('.idea/.gitignore')}: Parsing Python code failed",
        f"{Path('.idea/workspace.xml')}: in gitignore, skipping",
        f"{Path('.idea/modules.xml')}: Parsing Python code failed",
        f"{Path('.idea/watcherTasks.xml')}: Parsing Python code failed",
        f"{Path('.idea/dictionaries')}: in gitignore, skipping",
        f"{Path('.idea/misc.xml')}: Parsing Python code failed",
        f"{Path('.idea/scopes/whitelist_py.xml')}: Parsing Python code failed",
        f"{Path('.idea/scopes/bump2version.xml')}: Parsing Python code failed",
        f"{Path('.idea/scopes/docs__themes_graphite_static.xml')}: Parsing Python code failed",
        f"{Path('.idea/scopes/docs_conf.xml')}: Parsing Python code failed",
        f"{Path('.idea/scopes/_prettierignore.xml')}: Parsing Python code failed",
        f"{Path('.idea/scopes/docs_index.xml')}: Parsing Python code failed",
        f"{Path('.idea/scopes/_pylintrc.xml')}: Parsing Python code failed",
    ]
    assert all(i in patch_logger.getvalue() for i in expected)


def test_exclude_defaults_and_gitignore(
    main: MockMainType,
    make_tree: FixtureMakeTree,
    patch_logger: io.StringIO,
) -> None:
    """Test files excluded and ignored.

    :param main: Patch package entry point.
    :param make_tree: Create directory tree from dict mapping.
    :param patch_logger: Logs as an io instance.
    """
    make_tree(Path.cwd(), TREE)
    main(".", long.verbose, test_flake8=False)
    expected = [
        f"{Path('.pyaud_cache/7.5.1/CACHEDIR.TAG')}: in gitignore, skipping",
        f"{Path('.pyaud_cache/7.5.1/files.json')}: in gitignore, skipping",
        f"{Path('.pyaud_cache/7.5.1/.gitignore')}: in gitignore, skipping",
        f"{Path('CODE_OF_CONDUCT.md')}: Parsing Python code failed",
        f"{Path('.pylintrc')}: Parsing Python code failed",
        f"{Path('LICENSE')}: Parsing Python code failed",
        f"{Path('CHANGELOG.md')}: Parsing Python code failed",
        f"{Path('.pre-commit-config.yaml')}: Parsing Python code failed",
        f"{Path('.coverage')}: in gitignore, skipping",
        f"{Path('Makefile')}: Parsing Python code failed",
        f"{Path('whitelist.py')}: Parsing Python code successful",
        f"{Path('.pre-commit-hooks.yaml')}: Parsing Python code failed",
        f"{Path('pyproject.toml')}: Parsing Python code successful",
        f"{Path('.bumpversion.cfg')}: Parsing Python code failed",
        f"{Path('tests/misc_test.py')}: Parsing Python code successful",
        f"{Path('tests/conftest.py')}: Parsing Python code successful",
        f"{Path('tests/disable_test.py')}: Parsing Python code successful",
        f"{Path('tests/__init__.py')}: Parsing Python code successful",
        f"{Path('tests/TESTS.md')}: Parsing Python code failed",
        f"{Path('tests/git_test.py')}: Parsing Python code successful",
        f"{Path('tests/_test.py')}: Parsing Python code successful",
        f"{Path('.conform.yaml')}: Parsing Python code failed",
        f"{Path('docs/index.rst')}: Parsing Python code failed",
        f"{Path('docs/requirements.txt')}: Parsing Python code failed",
        f"{Path('docs/docsig.rst')}: Parsing Python code failed",
        f"{Path('docs/conf.py')}: Parsing Python code successful",
        f"{Path('docs/static/docsig.svg')}: Parsing Python code failed",
        f"{Path('docs/examples/classes.rst')}: Parsing Python code failed",
        f"{Path('docs/examples/message-control.rst')}: Parsing Python code failed",
        f"{Path('.readthedocs.yml')}: Parsing Python code failed",
        f"{Path('.prettierignore')}: Parsing Python code failed",
        f"{Path('.editorconfig')}: Parsing Python code failed",
        f"{Path('docsig/_stub.py')}: Parsing Python code successful",
        f"{Path('docsig/_report.py')}: Parsing Python code successful",
        f"{Path('docsig/_main.py')}: Parsing Python code successful",
        f"{Path('docsig/_version.py')}: Parsing Python code successful",
        f"{Path('docsig/_module.py')}: Parsing Python code successful",
        f"{Path('docsig/__init__.py')}: Parsing Python code successful",
        f"{Path('docsig/_display.py')}: Parsing Python code successful",
        f"{Path('docsig/_hooks.py')}: Parsing Python code successful",
        f"{Path('docsig/_message.py')}: Parsing Python code successful",
        f"{Path('docsig/_core.py')}: Parsing Python code successful",
        f"{Path('docsig/_decorators.py')}: Parsing Python code successful",
        f"{Path('docsig/messages.py')}: Parsing Python code successful",
        f"{Path('docsig/py.typed')}: Parsing Python code failed",
        f"{Path('docsig/_config.py')}: Parsing Python code successful",
        f"{Path('docsig/__main__.py')}: Parsing Python code successful",
        f"{Path('docsig/_utils.py')}: Parsing Python code successful",
        f"{Path('docsig/_directives.py')}: Parsing Python code successful",
        f"{Path('.gitignore')}: Parsing Python code failed",
        f"{Path('package-lock.json')}: Parsing Python code failed",
        f"{Path('package.json')}: Parsing Python code failed",
        f"{Path('CONTRIBUTING.md')}: Parsing Python code failed",
        f"{Path('.github/COMMIT_POLICY.md')}: Parsing Python code failed",
        f"{Path('.github/workflows/codeql-analysis.yml')}: Parsing Python code failed",
        f"{Path('.github/workflows/build.yaml')}: Parsing Python code failed",
        f"{Path('.github/dependabot.yml')}: Parsing Python code failed",
        f"{Path('coverage.xml')}: in gitignore, skipping",
        f"{Path('poetry.lock')}: Parsing Python code failed",
        f"{Path('README.rst')}: Parsing Python code failed",
    ]
    assert all(i in patch_logger.getvalue() for i in expected)


def test_gitignore_patterns(
    monkeypatch: pytest.MonkeyPatch,
    main: MockMainType,
    make_tree: FixtureMakeTree,
) -> None:
    """Test patterns rendered correctly.

    :param monkeypatch: Mock patch environment and attributes.
    :param main: Patch package entry point.
    :param make_tree: Create directory tree from dict mapping.
    """
    make_tree(Path.cwd(), TREE)
    # remove default excludes to better test nested gitignore files
    gitignore = docsig._files._Gitignore()  # type: ignore
    monkeypatch.setattr("docsig._files._Gitignore", lambda: gitignore)
    main(".", long.verbose, test_flake8=False)
    patterns = [
        "*build/",
        "*coverage*",
        "*venv",
        ".DS_Store",
        ".env",
        "__pycache__/",
        "dist/",
        "node_modules/",
        ".pyaud_cache/7.5.1/",
        ".pyaud_cache/7.5.1/*",
        ".pytest_cache/*",
        ".mypy_cache/*",
        ".idea/dataSources.local.xml",
        ".idea/dataSources/",
        ".idea/dictionaries",
        ".idea/httpRequests/",
        ".idea/shelf/",
        ".idea/sonarlint/",
        ".idea/tasks.xml",
        ".idea/usage.statistics.xml",
        ".idea/workspace.xml",
    ]
    assert all(
        i.pattern in patterns for i in gitignore.patterns  # type: ignore
    )


@pytest.mark.parametrize(
    "args,expected",
    [
        (
            ["docs/*"],
            [
                Path("docs/index.rst"),
                Path("docs/requirements.txt"),
                Path("docs/docsig.rst"),
                Path("docs/conf.py"),
            ],
        ),
        (
            [".pyaud_cache/7.5.1/CACHEDIR.TAG"],
            [
                Path(".pyaud_cache/7.5.1/CACHEDIR.TAG"),
            ],
        ),
        (
            ["docs/examples/*"],
            [
                Path("docs/examples/classes.rst"),
                Path("docs/examples/message-control.rst"),
            ],
        ),
        (
            [
                "CODE_OF_CONDUCT.md",
                ".pylintrc",
                "LICENSE",
                "CHANGELOG.md",
                ".pre-commit-config.yaml",
                ".coverage",
                "Makefile",
                "whitelist.py",
                ".pre-commit-hooks.yaml",
                "pyproject.toml",
                ".bumpversion.cfg",
                ".conform.yaml",
                ".readthedocs.yml",
                ".prettierignore",
                ".editorconfig",
                "package-lock.json",
                "package.json",
                "CONTRIBUTING.md",
                "coverage.xml",
                "poetry.lock",
                "README.rst",
            ],
            [
                Path("CODE_OF_CONDUCT.md"),
                Path(".pylintrc"),
                Path("LICENSE"),
                Path("CHANGELOG.md"),
                Path(".pre-commit-config.yaml"),
                Path(".coverage"),
                Path("Makefile"),
                Path("whitelist.py"),
                Path(".pre-commit-hooks.yaml"),
                Path("pyproject.toml"),
                Path(".bumpversion.cfg"),
                Path(".conform.yaml"),
                Path(".readthedocs.yml"),
                Path(".prettierignore"),
                Path(".editorconfig"),
                Path("package-lock.json"),
                Path("package.json"),
                Path("CONTRIBUTING.md"),
                Path("coverage.xml"),
                Path("poetry.lock"),
                Path("README.rst"),
            ],
        ),
        (
            ["*.md"],
            [
                Path("CODE_OF_CONDUCT.md"),
                Path("CHANGELOG.md"),
                Path("CONTRIBUTING.md"),
            ],
        ),
        (
            ["**/*.md"],
            [
                Path("tests/TESTS.md"),
            ],
        ),
        (
            ["docs/**/*.rst"],
            [
                Path("docs/examples/classes.rst"),
                Path("docs/examples/message-control.rst"),
            ],
        ),
        (
            ["file?.txt"],
            [
                Path("file1.txt"),
                Path("file2.txt"),
                Path("file3.txt"),
                Path("file4.txt"),
                Path("file5.txt"),
            ],
        ),
        (
            ["file[1-3].txt"],
            [
                Path("file1.txt"),
                Path("file2.txt"),
                Path("file3.txt"),
            ],
        ),
        (
            ["file[!1-3].txt"],
            [
                Path("file4.txt"),
                Path("file5.txt"),
            ],
        ),
        (
            [".pyaud_cache/7.5.1/*", "tests/*"],
            [
                Path(".pyaud_cache/7.5.1/CACHEDIR.TAG"),
                Path(".pyaud_cache/7.5.1/files.json"),
                Path("tests/misc_test.py"),
                Path("tests/conftest.py"),
                Path("tests/disable_test.py"),
                Path("tests/__init__.py"),
                Path("tests/TESTS.md"),
                Path("tests/git_test.py"),
                Path("tests/_test.py"),
            ],
        ),
        (
            [
                "tests/*",
                ".pyaud_cache/7.5.1/CACHEDIR.TAG",
            ],
            [
                Path(".pyaud_cache/7.5.1/CACHEDIR.TAG"),
                Path("tests/misc_test.py"),
                Path("tests/conftest.py"),
                Path("tests/disable_test.py"),
                Path("tests/__init__.py"),
                Path("tests/TESTS.md"),
                Path("tests/git_test.py"),
                Path("tests/_test.py"),
            ],
        ),
        (
            ["tests/*", ".pyaud_cache/7.5.1/CACHEDIR.TAG", "docs/examples/*"],
            [
                Path(".pyaud_cache/7.5.1/CACHEDIR.TAG"),
                Path("tests/misc_test.py"),
                Path("tests/conftest.py"),
                Path("tests/disable_test.py"),
                Path("tests/__init__.py"),
                Path("tests/TESTS.md"),
                Path("tests/git_test.py"),
                Path("tests/_test.py"),
                Path("docs/examples/classes.rst"),
                Path("docs/examples/message-control.rst"),
            ],
        ),
        (
            [
                "tests/*",
                ".pyaud_cache/7.5.1/CACHEDIR.TAG",
                "docs/examples/*",
                "CODE_OF_CONDUCT.md",
                ".pylintrc",
                "LICENSE",
                "CHANGELOG.md",
                ".pre-commit-config.yaml",
                ".coverage",
                "Makefile",
                "whitelist.py",
                ".pre-commit-hooks.yaml",
                "pyproject.toml",
                ".bumpversion.cfg",
                ".conform.yaml",
                ".readthedocs.yml",
                ".prettierignore",
                ".editorconfig",
                "package-lock.json",
                "package.json",
                "CONTRIBUTING.md",
                "coverage.xml",
                "poetry.lock",
                "README.rst",
            ],
            [
                Path(".pyaud_cache/7.5.1/CACHEDIR.TAG"),
                Path("tests/misc_test.py"),
                Path("tests/conftest.py"),
                Path("tests/disable_test.py"),
                Path("tests/__init__.py"),
                Path("tests/TESTS.md"),
                Path("tests/git_test.py"),
                Path("tests/_test.py"),
                Path("docs/examples/classes.rst"),
                Path("docs/examples/message-control.rst"),
                Path("CODE_OF_CONDUCT.md"),
                Path(".pylintrc"),
                Path("LICENSE"),
                Path("CHANGELOG.md"),
                Path(".pre-commit-config.yaml"),
                Path(".coverage"),
                Path("Makefile"),
                Path("whitelist.py"),
                Path(".pre-commit-hooks.yaml"),
                Path("pyproject.toml"),
                Path(".bumpversion.cfg"),
                Path(".conform.yaml"),
                Path(".readthedocs.yml"),
                Path(".prettierignore"),
                Path(".editorconfig"),
                Path("package-lock.json"),
                Path("package.json"),
                Path("CONTRIBUTING.md"),
                Path("coverage.xml"),
                Path("poetry.lock"),
                Path("README.rst"),
            ],
        ),
    ],
    ids=[
        "dir",
        "path-to-file",
        "nested-dir",
        "files",
        "suffix",
        "suffix-recurse",
        "dir-suffix-recurse",
        "question-mark",
        "square-brackets",
        "exclude-square-brackets",
        "multiple-dirs",
        "dir-and-path-to-file",
        "dir-path-to-file-and-nested-dir",
        "dir-path-to-file-and-nested-dir-and-files",
    ],
)
def test_exclude_glob(  # pylint: disable=too-many-positional-arguments
    monkeypatch: pytest.MonkeyPatch,
    main: MockMainType,
    make_tree: FixtureMakeTree,
    patch_logger: io.StringIO,
    args: list[str],
    expected: list[str],
) -> None:
    """Test using path glob instead of regex.

    :param monkeypatch: Mock patch environment and attributes.
    :param main: Patch package entry point.
    :param make_tree: Create directory tree from dict mapping.
    :param patch_logger: Logs as an io instance.
    :param args: Args to pass to main.
    :param expected: List of expected output.
    """
    paths = [
        Path(".pyaud_cache/7.5.1/CACHEDIR.TAG"),
        Path(".pyaud_cache/7.5.1/files.json"),
        Path(".pyaud_cache/7.5.1/.gitignore"),
        Path("CODE_OF_CONDUCT.md"),
        Path(".pylintrc"),
        Path("LICENSE"),
        Path("CHANGELOG.md"),
        Path(".pre-commit-config.yaml"),
        Path(".coverage"),
        Path("Makefile"),
        Path("whitelist.py"),
        Path(".pre-commit-hooks.yaml"),
        Path("pyproject.toml"),
        Path(".bumpversion.cfg"),
        Path("tests/misc_test.py"),
        Path("tests/conftest.py"),
        Path("tests/disable_test.py"),
        Path("tests/__init__.py"),
        Path("tests/TESTS.md"),
        Path("tests/git_test.py"),
        Path("tests/_test.py"),
        Path(".conform.yaml"),
        Path("docs/index.rst"),
        Path("docs/requirements.txt"),
        Path("docs/docsig.rst"),
        Path("docs/conf.py"),
        Path("docs/static/docsig.svg"),
        Path("docs/examples/classes.rst"),
        Path("docs/examples/message-control.rst"),
        Path(".readthedocs.yml"),
        Path(".prettierignore"),
        Path(".editorconfig"),
        Path("docsig/_stub.py"),
        Path("docsig/_report.py"),
        Path("docsig/_main.py"),
        Path("docsig/_version.py"),
        Path("docsig/_module.py"),
        Path("docsig/__init__.py"),
        Path("docsig/_display.py"),
        Path("docsig/_hooks.py"),
        Path("docsig/_message.py"),
        Path("docsig/_core.py"),
        Path("docsig/_decorators.py"),
        Path("docsig/messages.py"),
        Path("docsig/py.typed"),
        Path("docsig/_config.py"),
        Path("docsig/__main__.py"),
        Path("docsig/_utils.py"),
        Path("docsig/_directives.py"),
        Path("package-lock.json"),
        Path("package.json"),
        Path("CONTRIBUTING.md"),
        Path(".github/COMMIT_POLICY.md"),
        Path(".github/workflows/codeql-analysis.yml"),
        Path(".github/workflows/build.yaml"),
        Path(".github/dependabot.yml"),
        Path("coverage.xml"),
        Path("poetry.lock"),
        Path("README.rst"),
        Path("file1.txt"),
        Path("file2.txt"),
        Path("file3.txt"),
        Path("file4.txt"),
        Path("file5.txt"),
        Path("file10.txt"),
        Path("file[1].txt"),
    ]
    monkeypatch.setattr("docsig._core._DEFAULT_EXCLUDES", "^$")
    make_tree(Path.cwd(), TREE)
    main(
        ".",
        long.verbose,
        long.include_ignored,
        long.excludes,
        *args,
        test_flake8=False,
    )
    assert all(
        f"{i}: in exclude list, skipping" in patch_logger.getvalue()
        for i in expected
    )
    assert not any(
        f"{i}: in exclude list, skipping" in patch_logger.getvalue()
        for i in paths
        if i not in expected
    )
