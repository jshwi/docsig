"""
tests.exclude_test
==================
"""

# pylint: disable=protected-access,line-too-long

import pickle
from pathlib import Path

import pytest

import docsig
import docsig.plugin

from . import (
    TREE,
    FixtureFlake8,
    FixtureMakeTree,
    InitFileFixtureType,
    MockMainType,
    long,
)


def test_fix_optional_return_statements_with_overload_func_sig502(
    main: MockMainType,
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
) -> None:
    """Test ignore typechecker.

    :param main: Mock ``main`` function.
    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    """
    template = '''
from typing import Optional, overload


@overload
def get_something(number: int) -> str:
    """For getting a string from an integer."""


@overload
def get_something(number: None) -> None:
    """For getting a string from an integer."""


def get_something(number: Optional[int]) -> Optional[str]:
    """
    For getting a string from an integer.

    Parameters
    ----------
    number : int
        The number to convert to a string.

    Returns
    -------
    str
        The string representation of the number.
    """
    if number is None:
        return None
    return str(number)
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert "SIG502" not in std.out


def test_no_fail_on_unicode_decode_error_384(
    main: MockMainType, tmp_path: Path
) -> None:
    """Ensure unicode decode error is handled without error.

    :param main: Patch package entry point.
    :param tmp_path: Create and return temporary directory.
    """
    pkl = tmp_path / "test.pkl"
    serialize = [1, 2, 3]
    with open(pkl, "wb") as fout:
        pickle.dump(serialize, fout)

    assert main(pkl, test_flake8=False) == 0


def test_exclude_dirs_392(
    monkeypatch: pytest.MonkeyPatch,
    main: MockMainType,
    make_tree: FixtureMakeTree,
) -> None:
    """Test dir regexes are correctly excluded.

    :param monkeypatch: Mock patch environment and attributes.
    :param main: Patch package entry point.
    :param make_tree: Create directory tree from dict mapping.
    """
    pyproject_toml = Path.cwd() / "pyproject.toml"
    pyproject_toml.write_text(
        r"""
[tool.docsig]
exclude = '''.*src[\\/]design[\\/].*'''
""",
        encoding="utf-8",
    )
    path_obj = docsig._core._Paths  # define to avoid recursion
    paths_list = []

    def _paths(*args, **kwargs) -> docsig._core._Paths:
        paths = path_obj(*args, **kwargs)
        paths_list.append(paths)
        return paths

    monkeypatch.setattr("docsig._core._Paths", _paths)
    make_tree(
        Path.cwd(),
        {
            "src": {"design": {"file1.py": []}},
            "ssrc": {"design": {"file2.py": []}},
            "parent": {"src": {"design": {"file3.py": []}}},
        },
    )
    main(".", test_flake8=False)
    assert not any(
        i in paths_list[0]
        for i in [
            Path("src") / "design" / "file1.py",
            Path("ssrc") / "design" / "file2.py",
            Path("parent") / "src" / "design" / "file3.py",
        ]
    )


def test_exclude_defaults_396(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    make_tree: FixtureMakeTree,
) -> None:
    """Test bash script is ignored when under __pycache__ directory.

    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    :param make_tree: Create directory tree from dict mapping.
    """
    make_tree(Path.cwd(), TREE)
    Path(".gitignore").unlink()
    main(".", long.verbose, test_flake8=False)
    std = capsys.readouterr()
    expected = [
        f"{Path('.pyaud_cache/7.5.1/CACHEDIR.TAG')}: in gitignore, skipping",
        f"{Path('.pyaud_cache/7.5.1/files.json')}: in gitignore, skipping",
        f"{Path('.pyaud_cache/7.5.1/.gitignore')}: in gitignore, skipping",
        f"{Path('.pytest_cache/CACHEDIR.TAG')}: in gitignore, skipping",
        f"{Path('.pytest_cache/README.md')}: in gitignore, skipping",
        f"{Path('.pytest_cache/.gitignore')}: in gitignore, skipping",
        f"{Path('.pytest_cache/v')}: in gitignore, skipping",
        f"{Path('.mypy_cache/CACHEDIR.TAG')}: in gitignore, skipping",
        f"{Path('.mypy_cache/3.12')}: in gitignore, skipping",
        f"{Path('.mypy_cache/.gitignore')}: in gitignore, skipping",
        f"{Path('.mypy_cache/3.8')}: in gitignore, skipping",
        f"{Path('.idea/workspace.xml')}: in gitignore, skipping",
        f"{Path('.idea/dictionaries')}: in gitignore, skipping",
        f"{Path('dist/docsig-0.49.1.tar.gz')}: in exclude list, skipping",
        f"{Path('dist/docsig-0.49.2-py3-none-any.whl')}: in exclude list, skipping",
        f"{Path('dist/docsig-0.49.2.tar.gz')}: in exclude list, skipping",
        f"{Path('dist/docsig-0.49.0-py3-none-any.whl')}: in exclude list, skipping",
        f"{Path('dist/docsig-0.49.0.tar.gz')}: in exclude list, skipping",
        f"{Path('dist/docsig-0.49.1-py3-none-any.whl')}: in exclude list, skipping",
        f"{Path('node_modules/.cache/prettier/.prettier-caches/7f51ae3462154079bc96a79583b977616b1ad315.json')}: in exclude list, skipping",
        f"{Path('.git/HEAD')}: in exclude list, skipping",
        f"{Path('.idea/docsig.iml')}: in exclude list, skipping",
        f"{Path('.idea/jsonSchemas.xml')}: in exclude list, skipping",
        f"{Path('.idea/inspectionProfiles/profiles_settings.xml')}: in exclude list, skipping",
        f"{Path('.idea/inspectionProfiles/Project_Default.xml')}: in exclude list, skipping",
        f"{Path('.idea/codeStyles/Project.xml')}: in exclude list, skipping",
        f"{Path('.idea/codeStyles/codeStyleConfig.xml')}: in exclude list, skipping",
        f"{Path('.idea/material_theme_project_new.xml')}: in exclude list, skipping",
        f"{Path('.idea/vcs.xml')}: in exclude list, skipping",
        f"{Path('.idea/.gitignore')}: in exclude list, skipping",
        f"{Path('.idea/modules.xml')}: in exclude list, skipping",
        f"{Path('.idea/watcherTasks.xml')}: in exclude list, skipping",
        f"{Path('.idea/misc.xml')}: in exclude list, skipping",
        f"{Path('.idea/scopes/whitelist_py.xml')}: in exclude list, skipping",
        f"{Path('.idea/scopes/bump2version.xml')}: in exclude list, skipping",
        f"{Path('.idea/scopes/docs__themes_graphite_static.xml')}: in exclude list, skipping",
        f"{Path('.idea/scopes/docs_conf.xml')}: in exclude list, skipping",
        f"{Path('.idea/scopes/_prettierignore.xml')}: in exclude list, skipping",
        f"{Path('.idea/scopes/docs_index.xml')}: in exclude list, skipping",
        f"{Path('.idea/scopes/_pylintrc.xml')}: in exclude list, skipping",
        f"{Path('.bumpversion.cfg')}: Parsing Python code failed",
        f"{Path('.conform.yaml')}: Parsing Python code failed",
        f"{Path('.coverage')}: Parsing Python code failed",
        f"{Path('.editorconfig')}: Parsing Python code failed",
        f"{Path('.github/COMMIT_POLICY.md')}: Parsing Python code failed",
        f"{Path('.github/dependabot.yml')}: Parsing Python code failed",
        f"{Path('.github/workflows/build.yaml')}: Parsing Python code failed",
        f"{Path('.github/workflows/codeql-analysis.yml')}: Parsing Python code failed",
        f"{Path('.pre-commit-config.yaml')}: Parsing Python code failed",
        f"{Path('.pre-commit-hooks.yaml')}: Parsing Python code failed",
        f"{Path('.prettierignore')}: Parsing Python code failed",
        f"{Path('.pylintrc')}: Parsing Python code failed",
        f"{Path('.readthedocs.yml')}: Parsing Python code failed",
        f"{Path('CHANGELOG.md')}: Parsing Python code failed",
        f"{Path('CODE_OF_CONDUCT.md')}: Parsing Python code failed",
        f"{Path('CONTRIBUTING.md')}: Parsing Python code failed",
        f"{Path('LICENSE')}: Parsing Python code failed",
        f"{Path('Makefile')}: Parsing Python code failed",
        f"{Path('README.rst')}: Parsing Python code failed",
        f"{Path('coverage.xml')}: Parsing Python code failed",
        f"{Path('docs/conf.py')}: Parsing Python code successful",
        f"{Path('docs/docsig.rst')}: Parsing Python code failed",
        f"{Path('docs/examples/classes.rst')}: Parsing Python code failed",
        f"{Path('docs/examples/message-control.rst')}: Parsing Python code failed",
        f"{Path('docs/index.rst')}: Parsing Python code failed",
        f"{Path('docs/requirements.txt')}: Parsing Python code failed",
        f"{Path('docs/static/docsig.svg')}: Parsing Python code failed",
        f"{Path('docsig/__init__.py')}: Parsing Python code successful",
        f"{Path('docsig/__main__.py')}: Parsing Python code successful",
        f"{Path('docsig/__pycache__/__init__.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/__init__.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/__main__.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/__main__.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_config.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_config.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_core.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_core.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_decorators.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_decorators.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_directives.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_directives.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_display.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_display.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_git.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_hooks.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_hooks.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_main.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_main.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_message.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_message.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_module.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_module.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_report.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_report.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_stub.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_stub.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_utils.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_utils.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_version.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/_version.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/messages.cpython-311.pyc')}: in exclude list, skipping",
        f"{Path('docsig/__pycache__/messages.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('docsig/_config.py')}: Parsing Python code successful",
        f"{Path('docsig/_core.py')}: Parsing Python code successful",
        f"{Path('docsig/_decorators.py')}: Parsing Python code successful",
        f"{Path('docsig/_directives.py')}: Parsing Python code successful",
        f"{Path('docsig/_display.py')}: Parsing Python code successful",
        f"{Path('docsig/_hooks.py')}: Parsing Python code successful",
        f"{Path('docsig/_main.py')}: Parsing Python code successful",
        f"{Path('docsig/_message.py')}: Parsing Python code successful",
        f"{Path('docsig/_module.py')}: Parsing Python code successful",
        f"{Path('docsig/_report.py')}: Parsing Python code successful",
        f"{Path('docsig/_stub.py')}: Parsing Python code successful",
        f"{Path('docsig/_utils.py')}: Parsing Python code successful",
        f"{Path('docsig/_version.py')}: Parsing Python code successful",
        f"{Path('docsig/messages.py')}: Parsing Python code successful",
        f"{Path('docsig/py.typed')}: Parsing Python code failed",
        f"{Path('package-lock.json')}: Parsing Python code failed",
        f"{Path('package.json')}: Parsing Python code failed",
        f"{Path('poetry.lock')}: Parsing Python code failed",
        f"{Path('pyproject.toml')}: Parsing Python code successful",
        f"{Path('tests/TESTS.md')}: Parsing Python code failed",
        f"{Path('tests/__init__.py')}: Parsing Python code successful",
        f"{Path('tests/__pycache__/__init__.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('tests/__pycache__/_test.cpython-38-pytest-8.1.1.pyc')}: in exclude list, skipping",
        f"{Path('tests/__pycache__/_test.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('tests/__pycache__/conftest.cpython-38-pytest-8.1.1.pyc')}: in exclude list, skipping",
        f"{Path('tests/__pycache__/disable_test.cpython-38-pytest-8.1.1.pyc')}: in exclude list, skipping",
        f"{Path('tests/__pycache__/misc_test.cpython-38-pytest-8.1.1.pyc')}: in exclude list, skipping",
        f"{Path('tests/_test.py')}: Parsing Python code successful",
        f"{Path('tests/conftest.py')}: Parsing Python code successful",
        f"{Path('tests/disable_test.py')}: Parsing Python code successful",
        f"{Path('tests/git_test.py')}: Parsing Python code successful",
        f"{Path('tests/misc_test.py')}: Parsing Python code successful",
        f"{Path('whitelist.py')}: Parsing Python code successful",
    ]
    assert all(i in std.out for i in expected)


def test_sig401_false_positive_427(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test false positive when using a code-block RST indent.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''\
def method(*, arg1 = "") -> str:
    """
    Description text

    .. code-block:: python
       print()

    :param arg1: text
    :return: text
    :raises TypeError: Incorrect argument(s)
    """
    return ""
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert "SIG401" not in std.out


@pytest.mark.parametrize(
    "template",
    [
        '''\
def func(param, param2, param3, param4) -> int:
    """Desc.

     :param param1: About param1.
    :param param2:A.
    :param param3:
    """
''',
        '''\
def func(param, param2, param3, param4) -> int:
    """Desc.

     :param param1: About param1.
     :param param2:A.
    :param param3:
    """
''',
        '''\
def func(param, param2, param3, param4) -> int:
    """Desc.

     :param param1: About param1.
     :param param2:A.
     :param param3:
    """
''',
    ],
    ids=["one", "two", "all"],
)
def test_indent_427(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
    template: str,
) -> None:
    """Test indent properly records, for params only.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    :param template: Python code.
    """
    init_file(template)
    main(".", test_flake8=False)
    std = capsys.readouterr()
    assert "SIG401" in std.out


def test_class_and_class_constructor_452(
    capsys: pytest.CaptureFixture,
    flake8: FixtureFlake8,
    init_file: InitFileFixtureType,
) -> None:
    """Test command lines errors when passed incompatible options.

    :param capsys: Capture sys out.
    :param flake8: Patch package entry point.
    :param init_file: Initialize a test file.
    """
    template = '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    """
'''
    init_file(template)
    flake8(".", "--sig-check-class", "--sig-check-class-constructor")
    std = capsys.readouterr()
    assert docsig.messages.E[5].description in std.out
