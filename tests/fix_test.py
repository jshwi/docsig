"""
tests.exclude_test
==================
"""

# pylint: disable=protected-access,line-too-long,too-many-lines
import io
import pickle
from pathlib import Path

import pytest

# noinspection PyProtectedMember
from docsig._config import _ArgumentParser, _split_comma

# noinspection PyProtectedMember
from docsig._files import Paths
from docsig.messages import E

from . import (
    TREE,
    FixtureFlake8,
    FixtureInitFile,
    FixtureInitPyprojectTomlFile,
    FixtureMain,
    FixtureMakeTree,
    FixturePatchArgv,
)


def test_fix_optional_return_statements_with_overload_func_sig502(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test ignore typechecker.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
from typing import Optional, overload

@overload
def function(a: int) -> int:
    """Docstring summary."""

@overload
def function(a: None) -> None:
    """Docstring summary."""

def function(a: Optional[int]) -> int:
    """Docstring summary.

    Parameters
    ----------
    a : int
        Description of a.

    Returns
    -------
    str
        Return description.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[502].ref not in std.out


def test_no_fail_on_unicode_decode_error_384(
    tmp_path: Path,
    main: FixtureMain,
) -> None:
    """Ensure the unicode-decode error is handled without error.

    :param tmp_path: Create and return the temporary directory.
    :param main: Patch package entry point.
    """
    pkl = tmp_path / "test.pkl"
    serialize = [1, 2, 3]
    with open(pkl, "wb") as fout:
        pickle.dump(serialize, fout)  # type: ignore

    assert main(pkl, test_flake8=False) == 0


def test_exclude_dirs_392(
    monkeypatch: pytest.MonkeyPatch,
    init_pyproject_toml: FixtureInitPyprojectTomlFile,
    make_tree: FixtureMakeTree,
    main: FixtureMain,
) -> None:
    """Test dir regexes are correctly excluded.

    :param monkeypatch: Mock patch environment and attributes.
    :param init_pyproject_toml: Initialize a test pyproject.toml file.
    :param make_tree: Create the directory tree from dict mapping.
    :param main: Patch package entry point.
    """
    init_pyproject_toml({"exclude": r".*src[\\/]design[\\/].*"})
    path_obj = Paths  # define to avoid recursion
    paths_list = []

    def _paths(*args, **kwargs) -> Paths:
        paths = path_obj(*args, **kwargs)
        paths_list.append(paths)
        return paths

    monkeypatch.setattr("docsig._core._Paths", _paths)
    make_tree(
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
    make_tree: FixtureMakeTree,
    patch_logger: io.StringIO,
    main: FixtureMain,
) -> None:
    """Test bash script is ignored when under __pycache__ directory.

    :param make_tree: Create the directory tree from dict mapping.
    :param patch_logger: Logs as an io instance.
    :param main: Patch package entry point.
    """
    make_tree(TREE)
    Path(".gitignore").unlink()
    main(".", "--verbose", test_flake8=False)
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
    assert all(i in patch_logger.getvalue() for i in expected)


def test_sig401_false_positive_427(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test false positive when using a code-block RST indent.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''\
def function(*, arg1 = "") -> int:
    """
    Description text

    .. code-block:: python
       print()

    :param arg1: Description of arg1.
    :returns: Return description.
    :raises TypeError: Incorrect argument(s)
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[401].ref not in std.out


@pytest.mark.parametrize(
    "template",
    [
        '''\
def function(d, b, c, d) -> int:
    """Docstring summary.

     :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """
''',
        '''\
def function(d, b, c, d) -> int:
    """Docstring summary.

     :param a: Description of a.
     :param b: Description of b.
    :param c: Description of c.
    """
''',
        '''\
def function(d, b, c, d) -> int:
    """Docstring summary.

     :param a: Description of a.
     :param b: Description of b.
     :param c: Description of c.
    """
''',
    ],
    ids=["one", "two", "all"],
)
def test_indent_427(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    template: str,
) -> None:
    """Test indent properly records, for params only.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param template: Python code.
    """
    init_file(template)
    main(".", test_flake8=False)
    std = capsys.readouterr()
    assert E[401].ref in std.out


def test_class_and_class_constructor_452(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    flake8: FixtureFlake8,
) -> None:
    """Test command lines errors when passed incompatible options.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param flake8: Patch package entry point.
    """
    template = '''
def function(a, b, c) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param c: Description of c.
    """
'''
    init_file(template)
    flake8(".", "--sig-check-class", "--sig-check-class-constructor")
    std = capsys.readouterr()
    assert E[5].ref in std.out


def test_description_missing_and_description_syntax_error_461(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test description missing raised with other description.

    The other description would cause a syntax in description error if
    it spanned over multiple lines.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
def function(a, b) -> None:
    """Docstring summary.

    :param a:
    :param b: Description of b.
        and continues on the next line.
    """
'''
    init_file(template)
    main(".", test_flake8=False)
    std = capsys.readouterr()
    assert E[301].ref in std.out


def test_config_not_correctly_loaded_when_running_pre_commit_on_windows_488(
    init_pyproject_toml: FixtureInitPyprojectTomlFile,
    patch_argv: FixturePatchArgv,
) -> None:
    """Test that config correctly loads on windows.

    Problem: When running the pre-commit hook in Windows PowerShell,
    get_config returns {} because prog='docsig.EXE' instead of 'docsig'.

    :param init_pyproject_toml: Initialize a test pyproject.toml file.
    :param patch_argv: Patch commandline arguments.
    """
    disable = [
        E[101].ref,
        E[202].ref,
        E[203].ref,
        E[301].ref,
        E[302].ref,
        E[401].ref,
        E[402].ref,
        E[404].ref,
        E[501].ref,
        E[502].ref,
        E[503].ref,
        E[505].ref,
    ]
    init_pyproject_toml({"disable": disable})
    patch_argv("docsig.EXE")
    parser = _ArgumentParser()
    parser.add_argument(
        "-d",
        "--disable",
        action="store",
        type=_split_comma,
        default=[],
    )
    namespace = parser.parse_args()
    assert all(i in namespace.disable for i in disable)


def test_properties_not_recognized_when_underneath_other_decorators_509(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Fix properties not recognized when stacked.

    Also, check this does fail with --check-property-returns.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
import typing as _t
from abc import abstractmethod as _abstractmethod
from functools import cached_property as _cached_property

from ._ticker import Tickers as _Ticker
from ._transactions import Trades as _Trades

class Trades(dict[str, _Trades]):
    """Docstring summary."""

class Account(dict[str, _t.Any]):
    """Docstring summary."""

    @_abstractmethod
    @_cached_property
    def method_1(self) -> Trades:
        """Docstring summary."""

    @_abstractmethod
    @_cached_property
    def method_2(self) -> _Tickers:
        """Docstring summary."""
'''
    init_file(template)
    assert not main(".", test_flake8=False)
    main(".", "-P", test_flake8=False)
    std = capsys.readouterr()
    assert E[503].ref in std.out


def test_properties_not_recognized_when_on_top_of_other_decorators_509(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Fix properties not recognized when stacked.

    Also, check this does fail with --check-property-returns.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
import typing as _t
from abc import abstractmethod as _abstractmethod
from functools import cached_property as _cached_property

from ._ticker import Tickers as _Ticker
from ._transactions import Trades as _Trades

class Trades(dict[str, _Trades]):
    """Docstring summary."""

class Account(dict[str, _t.Any]):
    """Docstring summary."""

    @_cached_property
    @_abstractmethod
    def method_1(self) -> Trades:
        """Docstring summary."""

    @_cached_property
    @_abstractmethod
    def method_2(self) -> _Tickers:
        """Docstring summary."""
'''
    init_file(template)
    assert not main(".", test_flake8=False)
    main(".", "-P", test_flake8=False)
    std = capsys.readouterr()
    assert E[503].ref in std.out


def test_no_erroneous_301_in_duplicate(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Make sure 301 does not appear for duplicate parameters.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = r'''
# pylint: disable=too-many-locals,too-many-statements
@_g.cache("arb.json")
@_g.cache("diff.json")
def function(
    diff_obj: _g.CacheObj,
    arb_obj: _g.CacheObj,
    coins: _Coins,
    executor: _ThreadPoolExecutor,
    ignore_actionable_diff_score: bool,
) -> None:
    """Docstring summary.

    :param diff_obj: Description of diff_obj.
    :param arb_obj: Description of arb_obj.
    :param coins: Description of coins.
    :param executor: Description of executor.
    :param ignore_actionable_diff_score: Description of ignore_actionable_diff_score.
        score.
    :param executor: Description of executor.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[301].ref not in std.out


def test_handle_empty_symlinks(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
    main: FixtureMain,
) -> None:
    """Ensure the program doesn't crash when it checks broken symlinks.

    :param tmp_path: Create and return the temporary directory.
    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    """
    (tmp_path / "broken_symlink.py").symlink_to("does-not-exist")
    main(".")
    std = capsys.readouterr()
    assert E[301].ref not in std.out


def test_no_erroneous_402_when_order_cannot_be_confirmed(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Fix params out-of-order popping up with a single document.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
class Transactions(_Transactions):
    """Docstring summary.

    :param symbol: Description of symbol.
    """

    def __init__(self, client: Client, symbol: str, attr: str):
        pass
'''
    init_file(template)
    main(".", "--check-class")
    std = capsys.readouterr()
    assert E[402].ref not in std.out


def test_fix_allow_or_operator_in_type_545(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test type declaration in name with pipe is allowed.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
def function(a, **kwargs) -> None:
    """Docstring summary.

    :param str | None a: Use string or None for this purpose.
    :keyword str | None bar: Use string or None for this purpose.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[201].ref not in std.out
    assert E[203].ref not in std.out
    assert E[301].ref not in std.out
    assert E[304].ref.format(token="|") not in std.out


def test_close_with_bitwise_operator_545(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test pipe still treated as a bad closing token.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
def function(**kwargs) -> None:
    """Docstring summary.

    :keyword bar| Use string or None for this purpose.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[304].ref.format(token="|") in std.out


def test_recognise_yield_550(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Recognize yield in docstrings.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
def function(n: int) -> _t.Generator[int, None, None]:
    """Docstring summary.

    Counts from 0 up to n - 1.

    Args:
        n (int): The upper limit (exclusive).

    Yields:
        int: The next number in the sequence.
    """
    for i in range(n):
        yield i
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert not std.out


def test_sig401_false_positives_562(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test indents are ignored within double dot directives.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
class Classy:
    @remove_last_args(['normalize'])  # since 8.2.0
    def method(self, force_iso: bool = False) -> int:
        """Docstring summary.

        .. seealso:: :meth:`fromTimestr` for differences between output
           with and without *force_iso* parameter.

        .. versionchanged:: 8.0
           *normalize* parameter was added.
        .. versionchanged:: 8.2
           *normalize* parameter was removed due to :phab:`T340495` and
           :phab:`T57755`

        :param force_iso: Description of force_iso.
        :return: Return description.
        """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert not std.out


def test_fix_incorrect_sig402_when_it_should_only_be_sig203(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test no additional out-of-order or not-equal-to-arg.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
class ChildTransactions(Transactions):
    """Docstring summary.

    :param symbol: Description of symbol.
    :param attr: Description of attr.
    :param timestamp: Description of timestamp.
    """

    def __init__(
        self,
        transaction_obj,
        symbol: str,
        attr: str,
        timestamp: int,
    ) -> None:
        super().__init__()
'''
    init_file(template)
    main(".", "--check-class")
    std = capsys.readouterr()
    assert E[402].ref not in std.out
    assert E[404].ref not in std.out


def test_fix_incorrect_sig402_when_it_should_also_be_sig203(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test out-of-order still valid when param missing.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
class ChildTransactions(Transactions):
    """Docstring summary.

    :param symbol: Description of symbol.
    :param attr: Description of attr.
    :param timestamp: Description of timestamp.
    """

    def __init__(
        self,
        transaction_obj,
        attr: str,
        symbol: str,
        timestamp: int,
    ) -> None:
        super().__init__()
'''
    init_file(template)
    main(".", "--check-class")
    std = capsys.readouterr()
    assert E[402].ref in std.out


def test_fix_no_402_for_very_similar_names_683(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """402 should not be showing for very similar names.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
def function(a, b, c, d) -> None:
    """Docstring summary.

    :param b: Description of b.
    :param c: Description of c.
    :param d: Description of d.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[402].ref not in std.out


def test_fix_incorrect_sig402_when_it_should_only_be_sig203_701(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test no additional out-of-order or not-equal-to-arg.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
@_decorators.parse_msgs
@_decorators.validate_args
def function(  # pylint: disable=too-many-locals,too-many-arguments
    *path: str | _Path,
    string: str | None = None,
    list_checks: bool = False,
    check_class: bool = False,
    check_class_constructor: bool = False,
    check_dunders: bool = False,
    check_protected_class_methods: bool = False,
    check_nested: bool = False,
    check_overridden: bool = False,
    check_protected: bool = False,
    check_property_returns: bool = False,
    include_ignored: bool = False,
    ignore_no_params: bool = False,
    ignore_args: bool = False,
    ignore_kwargs: bool = False,
    ignore_typechecker: bool = False,
    no_ansi: bool = False,
    verbose: bool = False,
    target: _Messages | None = None,
    disable: _Messages | None = None,
    exclude: str | None = None,
    excludes: list[str] | None = None,
) -> int:
    """Docstring summary.

    Populate a sequence of module objects before iterating over their
    top-level functions and classes.

    If any of the functions within the module - and methods within its
    classes - fail, print the resulting function string representation
    and report.

    :param path: Description of path.
    :param string: Description of string.
    :param list_checks: Description of list_checks.
    :param check_class: Description of check_class.
    :param check_class_constructor: Description of check_class_constructor.
        that this is mutually incompatible with check_class.
    :param check_dunders: Description of check_dunders.
    :param check_protected_class_methods: Description of check_protected_class_methods.
        to protected classes.
    :param check_nested: Description of check_nested.
    :param check_overridden: Description of check_overridden.
    :param check_protected: Description of check_protected.
    :param check_property_returns: Description of check_property_returns.
    :param include_ignored: Description of include_ignored.
        pattern.
    :param ignore_no_params: Description of ignore_no_params.
        documented
    :param ignore_args: Description of ignore_args.
    :param ignore_kwargs: Description of ignore_kwargs.
    :param ignore_typechecker: Description of ignore_typechecker.
    :param enforce_capitalization: Description of enforce_capitalization.
        capitalized.
    :param no_ansi: Description of no_ansi.
    :param verbose: Description of verbose.
    :param target: Description of target.
    :param disable: Description of disable.
    :param exclude: Description of exclude.
        checks.
    :param excludes: Description of excludes.
    :return: Return description.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[402].ref not in std.out


def test_incorrect_sig301_with_both_sig202_and_sig402_707(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test no incorrect SIG301 with both SIG202 and SIG402.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
def function(a, b) -> None:
    """Docstring summary.

    :param b: Description of b.
    :param a: Description of a.
    :param c: Description of c.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert E[301].ref not in std.out
