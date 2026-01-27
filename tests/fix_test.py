"""
tests.fix_test
==============
"""

# pylint: disable=protected-access,line-too-long,too-many-lines
import io
import pickle
from pathlib import Path

import pytest

# noinspection PyProtectedMember
from docsig._config import _ArgumentParser, _split_comma

# noinspection PyProtectedMember
from docsig._files import Files
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
    """Allow optional return as something when overloaded.

    Fix return statement documented for None.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''
from typing import Optional, overload

@overload
def function(a: int) -> str:
    """Docstring summary."""

@overload
def function(a: None) -> None:
    """Docstring summary."""

def function(a: Optional[int]) -> Optional[str]:
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
    """Ensure the unicode-decode error is handled without crashing.

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
    path_obj = Files  # define to avoid recursion
    paths_list = []

    def _paths(*args, **kwargs) -> Files:
        paths = path_obj(*args, **kwargs)
        paths_list.append(paths)
        return paths

    monkeypatch.setattr("docsig._core._Files", _paths)
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
        f"{Path('.bumpversion.cfg')}: parsing python code failed",
        f"{Path('.conform.yaml')}: parsing python code failed",
        f"{Path('.coverage')}: parsing python code failed",
        f"{Path('.editorconfig')}: parsing python code failed",
        f"{Path('.github/COMMIT_POLICY.md')}: parsing python code failed",
        f"{Path('.github/dependabot.yml')}: parsing python code failed",
        f"{Path('.github/workflows/build.yaml')}: parsing python code failed",
        f"{Path('.github/workflows/codeql-analysis.yml')}: parsing python code failed",
        f"{Path('.pre-commit-config.yaml')}: parsing python code failed",
        f"{Path('.pre-commit-hooks.yaml')}: parsing python code failed",
        f"{Path('.prettierignore')}: parsing python code failed",
        f"{Path('.pylintrc')}: parsing python code failed",
        f"{Path('.readthedocs.yml')}: parsing python code failed",
        f"{Path('CHANGELOG.md')}: parsing python code failed",
        f"{Path('CODE_OF_CONDUCT.md')}: parsing python code failed",
        f"{Path('CONTRIBUTING.md')}: parsing python code failed",
        f"{Path('LICENSE')}: parsing python code failed",
        f"{Path('Makefile')}: parsing python code failed",
        f"{Path('README.rst')}: parsing python code failed",
        f"{Path('coverage.xml')}: parsing python code failed",
        f"{Path('docs/conf.py')}: parsing python code successful",
        f"{Path('docs/docsig.rst')}: parsing python code failed",
        f"{Path('docs/examples/classes.rst')}: parsing python code failed",
        f"{Path('docs/examples/message-control.rst')}: parsing python code failed",
        f"{Path('docs/index.rst')}: parsing python code failed",
        f"{Path('docs/requirements.txt')}: parsing python code failed",
        f"{Path('docs/static/docsig.svg')}: parsing python code failed",
        f"{Path('docsig/__init__.py')}: parsing python code successful",
        f"{Path('docsig/__main__.py')}: parsing python code successful",
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
        f"{Path('docsig/_config.py')}: parsing python code successful",
        f"{Path('docsig/_core.py')}: parsing python code successful",
        f"{Path('docsig/_decorators.py')}: parsing python code successful",
        f"{Path('docsig/_directives.py')}: parsing python code successful",
        f"{Path('docsig/_display.py')}: parsing python code successful",
        f"{Path('docsig/_hooks.py')}: parsing python code successful",
        f"{Path('docsig/_main.py')}: parsing python code successful",
        f"{Path('docsig/_message.py')}: parsing python code successful",
        f"{Path('docsig/_module.py')}: parsing python code successful",
        f"{Path('docsig/_report.py')}: parsing python code successful",
        f"{Path('docsig/_stub.py')}: parsing python code successful",
        f"{Path('docsig/_utils.py')}: parsing python code successful",
        f"{Path('docsig/_version.py')}: parsing python code successful",
        f"{Path('docsig/messages.py')}: parsing python code successful",
        f"{Path('docsig/py.typed')}: parsing python code failed",
        f"{Path('package-lock.json')}: parsing python code failed",
        f"{Path('package.json')}: parsing python code failed",
        f"{Path('poetry.lock')}: parsing python code failed",
        f"{Path('pyproject.toml')}: parsing python code successful",
        f"{Path('tests/TESTS.md')}: parsing python code failed",
        f"{Path('tests/__init__.py')}: parsing python code successful",
        f"{Path('tests/__pycache__/__init__.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('tests/__pycache__/_test.cpython-38-pytest-8.1.1.pyc')}: in exclude list, skipping",
        f"{Path('tests/__pycache__/_test.cpython-38.pyc')}: in exclude list, skipping",
        f"{Path('tests/__pycache__/conftest.cpython-38-pytest-8.1.1.pyc')}: in exclude list, skipping",
        f"{Path('tests/__pycache__/disable_test.cpython-38-pytest-8.1.1.pyc')}: in exclude list, skipping",
        f"{Path('tests/__pycache__/misc_test.cpython-38-pytest-8.1.1.pyc')}: in exclude list, skipping",
        f"{Path('tests/_test.py')}: parsing python code successful",
        f"{Path('tests/conftest.py')}: parsing python code successful",
        f"{Path('tests/disable_test.py')}: parsing python code successful",
        f"{Path('tests/git_test.py')}: parsing python code successful",
        f"{Path('tests/misc_test.py')}: parsing python code successful",
        f"{Path('whitelist.py')}: parsing python code successful",
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
def function(*, arg1 = "") -> str:
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

    Flake8 doesn't have mutually exclusive options like argparse does..

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

    Also, check this does fail with ``check_property_returns``.

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
    main(".", "--check-property-returns", test_flake8=False)
    std = capsys.readouterr()
    assert E[503].ref in std.out


def test_properties_not_recognized_when_on_top_of_other_decorators_509(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Fix properties not recognized when stacked.

    Also, check this does fail with ``check_property_returns``.

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
    main(".", "--check-property-returns", test_flake8=False)
    std = capsys.readouterr()
    assert E[503].ref in std.out


def test_no_erroneous_301_in_duplicate(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Make sure SIG301 does not appear for duplicate parameters.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = r'''
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
        super().__init__()
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
    @remove_last_args(['normalize'])
    def method(self, force_iso: bool = False) -> str:
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
    """SIG402 should not be showing for very similar names.

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
def function(
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


def test_fix_token_error_763(
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Skip parsing directives instead of crashing.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = r'''
"""The problem is the trailing line continuation at the end of the line,
which produces a TokenError."""
# +2: [syntax-error]
""\
'''
    init_file(template)
    assert main(".") == 0


def test_prevent_parsing_file_for_directives_if_ast_parse_failed_770(
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Prevent parsing file for directives if AST parse failed.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = r"""
CONDITION=true
EXECUTABLE=C

while [ $# -gt 0 ]; do
  case "$1" in
    --executable=*)
      EXECUTABLE="${1#*=}"
      ;;
    --no-build*)
      CONDITION=false
      ;;
    *)
      echo "invalid argument '${1}'"
      exit 1
      ;;
  esac
  shift
done
"""
    init_file(template, Path("script.sh"))
    assert main(".") == 0


def test_fix_docsig_crashes_on_recursion_error_777(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test fix docsig crashes on recursion error.

    Test case borrowed from a portion of
    sympy/sympy/polys/numberfields/resolvent_lookup.py where this was
    discovered.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = """\
lambda s1, s2, s3, s4, s5, s6: (
    -9375 * s1**7 * s5 * s6**4
    + 3125 * s1**6 * s2 * s4 * s6**4
    + 7500 * s1**6 * s2 * s5**2 * s6**3
    + 3125 * s1**6 * s3**2 * s6**4
    - 1250 * s1**6 * s3 * s4 * s5 * s6**3
    - 2000 * s1**6 * s3 * s5**3 * s6**2
    + 3250 * s1**6 * s4**2 * s5**2 * s6**2
    - 1600 * s1**6 * s4 * s5**4 * s6
    + 256 * s1**6 * s5**6
    + 40625 * s1**6 * s6**5
    - 3125 * s1**5 * s2**2 * s3 * s6**4
    - 3500 * s1**5 * s2**2 * s4 * s5 * s6**3
    - 1450 * s1**5 * s2**2 * s5**3 * s6**2
    - 1750 * s1**5 * s2 * s3**2 * s5 * s6**3
    + 625 * s1**5 * s2 * s3 * s4**2 * s6**3
    - 850 * s1**5 * s2 * s3 * s4 * s5**2 * s6**2
    + 1760 * s1**5 * s2 * s3 * s5**4 * s6
    - 2050 * s1**5 * s2 * s4**3 * s5 * s6**2
    + 780 * s1**5 * s2 * s4**2 * s5**3 * s6
    - 192 * s1**5 * s2 * s4 * s5**5
    + 35000 * s1**5 * s2 * s5 * s6**4
    + 1200 * s1**5 * s3**3 * s5**2 * s6**2
    - 725 * s1**5 * s3**2 * s4**2 * s5 * s6**2
    - 160 * s1**5 * s3**2 * s4 * s5**3 * s6
    - 192 * s1**5 * s3**2 * s5**5
    - 125 * s1**5 * s3 * s4**4 * s6**2
    + 590 * s1**5 * s3 * s4**3 * s5**2 * s6
    - 16 * s1**5 * s3 * s4**2 * s5**4
    - 20625 * s1**5 * s3 * s4 * s6**4
    + 17250 * s1**5 * s3 * s5**2 * s6**3
    - 124 * s1**5 * s4**5 * s5 * s6
    + 17 * s1**5 * s4**4 * s5**3
    - 20250 * s1**5 * s4**2 * s5 * s6**3
    + 1900 * s1**5 * s4 * s5**3 * s6**2
    + 1344 * s1**5 * s5**5 * s6
    + 625 * s1**4 * s2**4 * s6**4
    + 2300 * s1**4 * s2**3 * s3 * s5 * s6**3
    + 250 * s1**4 * s2**3 * s4**2 * s6**3
    + 1470 * s1**4 * s2**3 * s4 * s5**2 * s6**2
    - 276 * s1**4 * s2**3 * s5**4 * s6
    - 125 * s1**4 * s2**2 * s3**2 * s4 * s6**3
    - 610 * s1**4 * s2**2 * s3**2 * s5**2 * s6**2
    + 1995 * s1**4 * s2**2 * s3 * s4**2 * s5 * s6**2
    - 1174 * s1**4 * s2**2 * s3 * s4 * s5**3 * s6
    - 16 * s1**4 * s2**2 * s3 * s5**5
    + 375 * s1**4 * s2**2 * s4**4 * s6**2
    - 172 * s1**4 * s2**2 * s4**3 * s5**2 * s6
    + 82 * s1**4 * s2**2 * s4**2 * s5**4
    - 7750 * s1**4 * s2**2 * s4 * s6**4
    - 46650 * s1**4 * s2**2 * s5**2 * s6**3
    + 15 * s1**4 * s2 * s3**3 * s4 * s5 * s6**2
    - 384 * s1**4 * s2 * s3**3 * s5**3 * s6
    + 525 * s1**4 * s2 * s3**2 * s4**3 * s6**2
    - 528 * s1**4 * s2 * s3**2 * s4**2 * s5**2 * s6
    + 384 * s1**4 * s2 * s3**2 * s4 * s5**4
    - 10125 * s1**4 * s2 * s3**2 * s6**4
    - 29 * s1**4 * s2 * s3 * s4**4 * s5 * s6
    - 118 * s1**4 * s2 * s3 * s4**3 * s5**3
    + 36700 * s1**4 * s2 * s3 * s4 * s5 * s6**3
    + 2410 * s1**4 * s2 * s3 * s5**3 * s6**2
    + 38 * s1**4 * s2 * s4**6 * s6
    + 5 * s1**4 * s2 * s4**5 * s5**2
    + 5550 * s1**4 * s2 * s4**3 * s6**3
    - 10040 * s1**4 * s2 * s4**2 * s5**2 * s6**2
    + 5800 * s1**4 * s2 * s4 * s5**4 * s6
    - 1600 * s1**4 * s2 * s5**6
    - 292500 * s1**4 * s2 * s6**5
    - 99 * s1**4 * s3**5 * s5 * s6**2
    - 150 * s1**4 * s3**4 * s4**2 * s6**2
    + 196 * s1**4 * s3**4 * s4 * s5**2 * s6
    + 48 * s1**4 * s3**4 * s5**4
    + 12 * s1**4 * s3**3 * s4**3 * s5 * s6
    - 128 * s1**4 * s3**3 * s4**2 * s5**3
    - 6525 * s1**4 * s3**3 * s5 * s6**3
    - 12 * s1**4 * s3**2 * s4**5 * s6
    + 65 * s1**4 * s3**2 * s4**4 * s5**2
    + 225 * s1**4 * s3**2 * s4**2 * s6**3
    + 80 * s1**4 * s3**2 * s4 * s5**2 * s6**2
    - 13 * s1**4 * s3 * s4**6 * s5
    + 5145 * s1**4 * s3 * s4**3 * s5 * s6**2
    - 6746 * s1**4 * s3 * s4**2 * s5**3 * s6
    + 1760 * s1**4 * s3 * s4 * s5**5
    - 103500 * s1**4 * s3 * s5 * s6**4
    + s1**4 * s4**8
    + 954 * s1**4 * s4**5 * s6**2
    + 449 * s1**4 * s4**4 * s5**2 * s6
    - 276 * s1**4 * s4**3 * s5**4
    + 70125 * s1**4 * s4**2 * s6**4
    + 58900 * s1**4 * s4 * s5**2 * s6**3
    - 23310 * s1**4 * s5**4 * s6**2
    - 468 * s1**3 * s2**5 * s5 * s6**3
    - 200 * s1**3 * s2**4 * s3 * s4 * s6**3
    - 294 * s1**3 * s2**4 * s3 * s5**2 * s6**2
    - 676 * s1**3 * s2**4 * s4**2 * s5 * s6**2
    + 180 * s1**3 * s2**4 * s4 * s5**3 * s6
    + 17 * s1**3 * s2**4 * s5**5
    + 50 * s1**3 * s2**3 * s3**3 * s6**3
    - 397 * s1**3 * s2**3 * s3**2 * s4 * s5 * s6**2
    + 514 * s1**3 * s2**3 * s3**2 * s5**3 * s6
    - 700 * s1**3 * s2**3 * s3 * s4**3 * s6**2
    + 447 * s1**3 * s2**3 * s3 * s4**2 * s5**2 * s6
    - 118 * s1**3 * s2**3 * s3 * s4 * s5**4
    + 11700 * s1**3 * s2**3 * s3 * s6**4
    - 12 * s1**3 * s2**3 * s4**4 * s5 * s6
    + 6 * s1**3 * s2**3 * s4**3 * s5**3
    + 10360 * s1**3 * s2**3 * s4 * s5 * s6**3
    + 11404 * s1**3 * s2**3 * s5**3 * s6**2
    + 141 * s1**3 * s2**2 * s3**4 * s5 * s6**2
    - 185 * s1**3 * s2**2 * s3**3 * s4**2 * s6**2
    + 168 * s1**3 * s2**2 * s3**3 * s4 * s5**2 * s6
    - 128 * s1**3 * s2**2 * s3**3 * s5**4
    + 93 * s1**3 * s2**2 * s3**2 * s4**3 * s5 * s6
    + 19 * s1**3 * s2**2 * s3**2 * s4**2 * s5**3
    + 5895 * s1**3 * s2**2 * s3**2 * s5 * s6**3
    - 36 * s1**3 * s2**2 * s3 * s4**5 * s6
    + 5 * s1**3 * s2**2 * s3 * s4**4 * s5**2
    - 12020 * s1**3 * s2**2 * s3 * s4**2 * s6**3
    - 5698 * s1**3 * s2**2 * s3 * s4 * s5**2 * s6**2
    - 6746 * s1**3 * s2**2 * s3 * s5**4 * s6
    + 5064 * s1**3 * s2**2 * s4**3 * s5 * s6**2
    - 762 * s1**3 * s2**2 * s4**2 * s5**3 * s6
    + 780 * s1**3 * s2**2 * s4 * s5**5
    + 93900 * s1**3 * s2**2 * s5 * s6**4
    + 198 * s1**3 * s2 * s3**5 * s4 * s6**2
    - 78 * s1**3 * s2 * s3**5 * s5**2 * s6
    - 95 * s1**3 * s2 * s3**4 * s4**2 * s5 * s6
    + 44 * s1**3 * s2 * s3**4 * s4 * s5**3
    + 25 * s1**3 * s2 * s3**3 * s4**4 * s6
    - 15 * s1**3 * s2 * s3**3 * s4**3 * s5**2
    + 1935 * s1**3 * s2 * s3**3 * s4 * s6**3
    - 2808 * s1**3 * s2 * s3**3 * s5**2 * s6**2
    + s1**3 * s2 * s3**2 * s4**5 * s5
    - 4844 * s1**3 * s2 * s3**2 * s4**2 * s5 * s6**2
    + 8996 * s1**3 * s2 * s3**2 * s4 * s5**3 * s6
    - 160 * s1**3 * s2 * s3**2 * s5**5
    - 3616 * s1**3 * s2 * s3 * s4**4 * s6**2
    + 500 * s1**3 * s2 * s3 * s4**3 * s5**2 * s6
    - 1174 * s1**3 * s2 * s3 * s4**2 * s5**4
    + 72900 * s1**3 * s2 * s3 * s4 * s6**4
    - 55665 * s1**3 * s2 * s3 * s5**2 * s6**3
    + 128 * s1**3 * s2 * s4**5 * s5 * s6
    + 180 * s1**3 * s2 * s4**4 * s5**3
    + 16240 * s1**3 * s2 * s4**2 * s5 * s6**3
    - 9330 * s1**3 * s2 * s4 * s5**3 * s6**2
    + 1900 * s1**3 * s2 * s5**5 * s6
    - 27 * s1**3 * s3**7 * s6**2
    + 18 * s1**3 * s3**6 * s4 * s5 * s6
    - 4 * s1**3 * s3**6 * s5**3
    - 4 * s1**3 * s3**5 * s4**3 * s6
    + s1**3 * s3**5 * s4**2 * s5**2
    + 54 * s1**3 * s3**5 * s6**3
    + 1143 * s1**3 * s3**4 * s4 * s5 * s6**2
    - 820 * s1**3 * s3**4 * s5**3 * s6
    + 923 * s1**3 * s3**3 * s4**3 * s6**2
    + 57 * s1**3 * s3**3 * s4**2 * s5**2 * s6
    - 384 * s1**3 * s3**3 * s4 * s5**4
    + 29700 * s1**3 * s3**3 * s6**4
    - 547 * s1**3 * s3**2 * s4**4 * s5 * s6
    + 514 * s1**3 * s3**2 * s4**3 * s5**3
    - 10305 * s1**3 * s3**2 * s4 * s5 * s6**3
    - 7405 * s1**3 * s3**2 * s5**3 * s6**2
    + 108 * s1**3 * s3 * s4**6 * s6
    - 148 * s1**3 * s3 * s4**5 * s5**2
    - 11360 * s1**3 * s3 * s4**3 * s6**3
    + 22209 * s1**3 * s3 * s4**2 * s5**2 * s6**2
    + 2410 * s1**3 * s3 * s4 * s5**4 * s6
    - 2000 * s1**3 * s3 * s5**6
    + 432000 * s1**3 * s3 * s6**5
    + 12 * s1**3 * s4**7 * s5
    - 22624 * s1**3 * s4**4 * s5 * s6**2
    + 11404 * s1**3 * s4**3 * s5**3 * s6
    - 1450 * s1**3 * s4**2 * s5**5
    - 242100 * s1**3 * s4 * s5 * s6**4
    + 58430 * s1**3 * s5**3 * s6**3
    + 56 * s1**2 * s2**6 * s4 * s6**3
    + 86 * s1**2 * s2**6 * s5**2 * s6**2
    - 14 * s1**2 * s2**5 * s3**2 * s6**3
    + 304 * s1**2 * s2**5 * s3 * s4 * s5 * s6**2
    - 148 * s1**2 * s2**5 * s3 * s5**3 * s6
    + 152 * s1**2 * s2**5 * s4**3 * s6**2
    - 54 * s1**2 * s2**5 * s4**2 * s5**2 * s6
    + 5 * s1**2 * s2**5 * s4 * s5**4
    - 2472 * s1**2 * s2**5 * s6**4
    - 76 * s1**2 * s2**4 * s3**3 * s5 * s6**2
    + 370 * s1**2 * s2**4 * s3**2 * s4**2 * s6**2
    - 287 * s1**2 * s2**4 * s3**2 * s4 * s5**2 * s6
    + 65 * s1**2 * s2**4 * s3**2 * s5**4
    - 28 * s1**2 * s2**4 * s3 * s4**3 * s5 * s6
    + 5 * s1**2 * s2**4 * s3 * s4**2 * s5**3
    - 8092 * s1**2 * s2**4 * s3 * s5 * s6**3
    + 8 * s1**2 * s2**4 * s4**5 * s6
    - 2 * s1**2 * s2**4 * s4**4 * s5**2
    + 1096 * s1**2 * s2**4 * s4**2 * s6**3
    - 5144 * s1**2 * s2**4 * s4 * s5**2 * s6**2
    + 449 * s1**2 * s2**4 * s5**4 * s6
    - 210 * s1**2 * s2**3 * s3**4 * s4 * s6**2
    + 76 * s1**2 * s2**3 * s3**4 * s5**2 * s6
    + 43 * s1**2 * s2**3 * s3**3 * s4**2 * s5 * s6
    - 15 * s1**2 * s2**3 * s3**3 * s4 * s5**3
    - 6 * s1**2 * s2**3 * s3**2 * s4**4 * s6
    + 2 * s1**2 * s2**3 * s3**2 * s4**3 * s5**2
    + 1962 * s1**2 * s2**3 * s3**2 * s4 * s6**3
    + 3181 * s1**2 * s2**3 * s3**2 * s5**2 * s6**2
    + 1684 * s1**2 * s2**3 * s3 * s4**2 * s5 * s6**2
    + 500 * s1**2 * s2**3 * s3 * s4 * s5**3 * s6
    + 590 * s1**2 * s2**3 * s3 * s5**5
    - 168 * s1**2 * s2**3 * s4**4 * s6**2
    - 494 * s1**2 * s2**3 * s4**3 * s5**2 * s6
    - 172 * s1**2 * s2**3 * s4**2 * s5**4
    - 22080 * s1**2 * s2**3 * s4 * s6**4
    + 58894 * s1**2 * s2**3 * s5**2 * s6**3
    + 27 * s1**2 * s2**2 * s3**6 * s6**2
    - 9 * s1**2 * s2**2 * s3**5 * s4 * s5 * s6
    + s1**2 * s2**2 * s3**5 * s5**3
    + s1**2 * s2**2 * s3**4 * s4**3 * s6
    - 486 * s1**2 * s2**2 * s3**4 * s6**3
    + 1071 * s1**2 * s2**2 * s3**3 * s4 * s5 * s6**2
    + 57 * s1**2 * s2**2 * s3**3 * s5**3 * s6
    + 2262 * s1**2 * s2**2 * s3**2 * s4**3 * s6**2
    - 2742 * s1**2 * s2**2 * s3**2 * s4**2 * s5**2 * s6
    - 528 * s1**2 * s2**2 * s3**2 * s4 * s5**4
    - 29160 * s1**2 * s2**2 * s3**2 * s6**4
    + 772 * s1**2 * s2**2 * s3 * s4**4 * s5 * s6
    + 447 * s1**2 * s2**2 * s3 * s4**3 * s5**3
    - 96732 * s1**2 * s2**2 * s3 * s4 * s5 * s6**3
    + 22209 * s1**2 * s2**2 * s3 * s5**3 * s6**2
    - 160 * s1**2 * s2**2 * s4**6 * s6
    - 54 * s1**2 * s2**2 * s4**5 * s5**2
    - 7992 * s1**2 * s2**2 * s4**3 * s6**3
    + 8634 * s1**2 * s2**2 * s4**2 * s5**2 * s6**2
    - 10040 * s1**2 * s2**2 * s4 * s5**4 * s6
    + 3250 * s1**2 * s2**2 * s5**6
    + 529200 * s1**2 * s2**2 * s6**5
    - 351 * s1**2 * s2 * s3**5 * s5 * s6**2
    - 1215 * s1**2 * s2 * s3**4 * s4**2 * s6**2
    - 360 * s1**2 * s2 * s3**4 * s4 * s5**2 * s6
    + 196 * s1**2 * s2 * s3**4 * s5**4
    + 741 * s1**2 * s2 * s3**3 * s4**3 * s5 * s6
    + 168 * s1**2 * s2 * s3**3 * s4**2 * s5**3
    + 11718 * s1**2 * s2 * s3**3 * s5 * s6**3
    - 106 * s1**2 * s2 * s3**2 * s4**5 * s6
    - 287 * s1**2 * s2 * s3**2 * s4**4 * s5**2
    + 22572 * s1**2 * s2 * s3**2 * s4**2 * s6**3
    - 8892 * s1**2 * s2 * s3**2 * s4 * s5**2 * s6**2
    + 80 * s1**2 * s2 * s3**2 * s5**4 * s6
    + 88 * s1**2 * s2 * s3 * s4**6 * s5
    + 22144 * s1**2 * s2 * s3 * s4**3 * s5 * s6**2
    - 5698 * s1**2 * s2 * s3 * s4**2 * s5**3 * s6
    - 850 * s1**2 * s2 * s3 * s4 * s5**5
    + 169560 * s1**2 * s2 * s3 * s5 * s6**4
    - 8 * s1**2 * s2 * s4**8
    + 3032 * s1**2 * s2 * s4**5 * s6**2
    - 5144 * s1**2 * s2 * s4**4 * s5**2 * s6
    + 1470 * s1**2 * s2 * s4**3 * s5**4
    - 249480 * s1**2 * s2 * s4**2 * s6**4
    - 105390 * s1**2 * s2 * s4 * s5**2 * s6**3
    + 58900 * s1**2 * s2 * s5**4 * s6**2
    + 162 * s1**2 * s3**6 * s4 * s6**2
    + 216 * s1**2 * s3**6 * s5**2 * s6
    - 216 * s1**2 * s3**5 * s4**2 * s5 * s6
    - 78 * s1**2 * s3**5 * s4 * s5**3
    + 36 * s1**2 * s3**4 * s4**4 * s6
    + 76 * s1**2 * s3**4 * s4**3 * s5**2
    - 3564 * s1**2 * s3**4 * s4 * s6**3
    + 8802 * s1**2 * s3**4 * s5**2 * s6**2
    - 22 * s1**2 * s3**3 * s4**5 * s5
    - 11475 * s1**2 * s3**3 * s4**2 * s5 * s6**2
    - 2808 * s1**2 * s3**3 * s4 * s5**3 * s6
    + 1200 * s1**2 * s3**3 * s5**5
    + 2 * s1**2 * s3**2 * s4**7
    + 222 * s1**2 * s3**2 * s4**4 * s6**2
    + 3181 * s1**2 * s3**2 * s4**3 * s5**2 * s6
    - 610 * s1**2 * s3**2 * s4**2 * s5**4
    - 165240 * s1**2 * s3**2 * s4 * s6**4
    + 118260 * s1**2 * s3**2 * s5**2 * s6**3
    + 572 * s1**2 * s3 * s4**5 * s5 * s6
    - 294 * s1**2 * s3 * s4**4 * s5**3
    - 32616 * s1**2 * s3 * s4**2 * s5 * s6**3
    - 55665 * s1**2 * s3 * s4 * s5**3 * s6**2
    + 17250 * s1**2 * s3 * s5**5 * s6
    - 232 * s1**2 * s4**7 * s6
    + 86 * s1**2 * s4**6 * s5**2
    + 48408 * s1**2 * s4**4 * s6**3
    + 58894 * s1**2 * s4**3 * s5**2 * s6**2
    - 46650 * s1**2 * s4**2 * s5**4 * s6
    + 7500 * s1**2 * s4 * s5**6
    - 129600 * s1**2 * s4 * s6**5
    + 41040 * s1**2 * s5**2 * s6**4
    - 48 * s1 * s2**7 * s4 * s5 * s6**2
    + 12 * s1 * s2**7 * s5**3 * s6
    + 12 * s1 * s2**6 * s3**2 * s5 * s6**2
    - 144 * s1 * s2**6 * s3 * s4**2 * s6**2
    + 88 * s1 * s2**6 * s3 * s4 * s5**2 * s6
    - 13 * s1 * s2**6 * s3 * s5**4
    + 1680 * s1 * s2**6 * s5 * s6**3
    + 72 * s1 * s2**5 * s3**3 * s4 * s6**2
    - 22 * s1 * s2**5 * s3**3 * s5**2 * s6
    - 4 * s1 * s2**5 * s3**2 * s4**2 * s5 * s6
    + s1 * s2**5 * s3**2 * s4 * s5**3
    - 144 * s1 * s2**5 * s3 * s4 * s6**3
    + 572 * s1 * s2**5 * s3 * s5**2 * s6**2
    + 736 * s1 * s2**5 * s4**2 * s5 * s6**2
    + 128 * s1 * s2**5 * s4 * s5**3 * s6
    - 124 * s1 * s2**5 * s5**5
    - 9 * s1 * s2**4 * s3**5 * s6**2
    + s1 * s2**4 * s3**4 * s4 * s5 * s6
    + 36 * s1 * s2**4 * s3**3 * s6**3
    - 2028 * s1 * s2**4 * s3**2 * s4 * s5 * s6**2
    - 547 * s1 * s2**4 * s3**2 * s5**3 * s6
    - 480 * s1 * s2**4 * s3 * s4**3 * s6**2
    + 772 * s1 * s2**4 * s3 * s4**2 * s5**2 * s6
    - 29 * s1 * s2**4 * s3 * s4 * s5**4
    + 6336 * s1 * s2**4 * s3 * s6**4
    - 12 * s1 * s2**4 * s4**3 * s5**3
    + 4368 * s1 * s2**4 * s4 * s5 * s6**3
    - 22624 * s1 * s2**4 * s5**3 * s6**2
    + 441 * s1 * s2**3 * s3**4 * s5 * s6**2
    + 336 * s1 * s2**3 * s3**3 * s4**2 * s6**2
    + 741 * s1 * s2**3 * s3**3 * s4 * s5**2 * s6
    + 12 * s1 * s2**3 * s3**3 * s5**4
    - 868 * s1 * s2**3 * s3**2 * s4**3 * s5 * s6
    + 93 * s1 * s2**3 * s3**2 * s4**2 * s5**3
    + 11016 * s1 * s2**3 * s3**2 * s5 * s6**3
    + 176 * s1 * s2**3 * s3 * s4**5 * s6
    - 28 * s1 * s2**3 * s3 * s4**4 * s5**2
    + 14784 * s1 * s2**3 * s3 * s4**2 * s6**3
    + 22144 * s1 * s2**3 * s3 * s4 * s5**2 * s6**2
    + 5145 * s1 * s2**3 * s3 * s5**4 * s6
    - 11344 * s1 * s2**3 * s4**3 * s5 * s6**2
    + 5064 * s1 * s2**3 * s4**2 * s5**3 * s6
    - 2050 * s1 * s2**3 * s4 * s5**5
    - 346896 * s1 * s2**3 * s5 * s6**4
    - 54 * s1 * s2**2 * s3**5 * s4 * s6**2
    - 216 * s1 * s2**2 * s3**5 * s5**2 * s6
    + 324 * s1 * s2**2 * s3**4 * s4**2 * s5 * s6
    - 95 * s1 * s2**2 * s3**4 * s4 * s5**3
    - 80 * s1 * s2**2 * s3**3 * s4**4 * s6
    + 43 * s1 * s2**2 * s3**3 * s4**3 * s5**2
    - 12204 * s1 * s2**2 * s3**3 * s4 * s6**3
    - 11475 * s1 * s2**2 * s3**3 * s5**2 * s6**2
    - 4 * s1 * s2**2 * s3**2 * s4**5 * s5
    - 3888 * s1 * s2**2 * s3**2 * s4**2 * s5 * s6**2
    - 4844 * s1 * s2**2 * s3**2 * s4 * s5**3 * s6
    - 725 * s1 * s2**2 * s3**2 * s5**5
    - 1312 * s1 * s2**2 * s3 * s4**4 * s6**2
    + 1684 * s1 * s2**2 * s3 * s4**3 * s5**2 * s6
    + 1995 * s1 * s2**2 * s3 * s4**2 * s5**4
    + 139104 * s1 * s2**2 * s3 * s4 * s6**4
    - 32616 * s1 * s2**2 * s3 * s5**2 * s6**3
    + 736 * s1 * s2**2 * s4**5 * s5 * s6
    - 676 * s1 * s2**2 * s4**4 * s5**3
    + 131040 * s1 * s2**2 * s4**2 * s5 * s6**3
    + 16240 * s1 * s2**2 * s4 * s5**3 * s6**2
    - 20250 * s1 * s2**2 * s5**5 * s6
    - 27 * s1 * s2 * s3**6 * s4 * s5 * s6
    + 18 * s1 * s2 * s3**6 * s5**3
    + 9 * s1 * s2 * s3**5 * s4**3 * s6
    - 9 * s1 * s2 * s3**5 * s4**2 * s5**2
    + 1944 * s1 * s2 * s3**5 * s6**3
    + s1 * s2 * s3**4 * s4**4 * s5
    + 6156 * s1 * s2 * s3**4 * s4 * s5 * s6**2
    + 1143 * s1 * s2 * s3**4 * s5**3 * s6
    + 324 * s1 * s2 * s3**3 * s4**3 * s6**2
    + 1071 * s1 * s2 * s3**3 * s4**2 * s5**2 * s6
    + 15 * s1 * s2 * s3**3 * s4 * s5**4
    - 7776 * s1 * s2 * s3**3 * s6**4
    - 2028 * s1 * s2 * s3**2 * s4**4 * s5 * s6
    - 397 * s1 * s2 * s3**2 * s4**3 * s5**3
    + 112860 * s1 * s2 * s3**2 * s4 * s5 * s6**3
    - 10305 * s1 * s2 * s3**2 * s5**3 * s6**2
    + 336 * s1 * s2 * s3 * s4**6 * s6
    + 304 * s1 * s2 * s3 * s4**5 * s5**2
    - 68976 * s1 * s2 * s3 * s4**3 * s6**3
    - 96732 * s1 * s2 * s3 * s4**2 * s5**2 * s6**2
    + 36700 * s1 * s2 * s3 * s4 * s5**4 * s6
    - 1250 * s1 * s2 * s3 * s5**6
    - 1477440 * s1 * s2 * s3 * s6**5
    - 48 * s1 * s2 * s4**7 * s5
    + 4368 * s1 * s2 * s4**4 * s5 * s6**2
    + 10360 * s1 * s2 * s4**3 * s5**3 * s6
    - 3500 * s1 * s2 * s4**2 * s5**5
    + 935280 * s1 * s2 * s4 * s5 * s6**4
    - 242100 * s1 * s2 * s5**3 * s6**3
    - 972 * s1 * s3**6 * s5 * s6**2
    - 351 * s1 * s3**5 * s4 * s5**2 * s6
    - 99 * s1 * s3**5 * s5**4
    + 441 * s1 * s3**4 * s4**3 * s5 * s6
    + 141 * s1 * s3**4 * s4**2 * s5**3
    - 36936 * s1 * s3**4 * s5 * s6**3
    - 84 * s1 * s3**3 * s4**5 * s6
    - 76 * s1 * s3**3 * s4**4 * s5**2
    + 17496 * s1 * s3**3 * s4**2 * s6**3
    + 11718 * s1 * s3**3 * s4 * s5**2 * s6**2
    - 6525 * s1 * s3**3 * s5**4 * s6
    + 12 * s1 * s3**2 * s4**6 * s5
    + 11016 * s1 * s3**2 * s4**3 * s5 * s6**2
    + 5895 * s1 * s3**2 * s4**2 * s5**3 * s6
    - 1750 * s1 * s3**2 * s4 * s5**5
    - 252720 * s1 * s3**2 * s5 * s6**4
    - 2544 * s1 * s3 * s4**5 * s6**2
    - 8092 * s1 * s3 * s4**4 * s5**2 * s6
    + 2300 * s1 * s3 * s4**3 * s5**4
    + 536544 * s1 * s3 * s4**2 * s6**4
    + 169560 * s1 * s3 * s4 * s5**2 * s6**3
    - 103500 * s1 * s3 * s5**4 * s6**2
    + 1680 * s1 * s4**6 * s5 * s6
    - 468 * s1 * s4**5 * s5**3
    - 346896 * s1 * s4**3 * s5 * s6**3
    + 93900 * s1 * s4**2 * s5**3 * s6**2
    + 35000 * s1 * s4 * s5**5 * s6
    - 9375 * s1 * s5**7
    + 108864 * s1 * s5 * s6**5
    + 16 * s2**8 * s4**2 * s6**2
    - 8 * s2**8 * s4 * s5**2 * s6
    + s2**8 * s5**4
    - 8 * s2**7 * s3**2 * s4 * s6**2
    + 2 * s2**7 * s3**2 * s5**2 * s6
    - 96 * s2**7 * s4 * s6**3
    - 232 * s2**7 * s5**2 * s6**2
    + s2**6 * s3**4 * s6**2
    + 24 * s2**6 * s3**2 * s6**3
    + 336 * s2**6 * s3 * s4 * s5 * s6**2
    + 108 * s2**6 * s3 * s5**3 * s6
    - 32 * s2**6 * s4**3 * s6**2
    - 160 * s2**6 * s4**2 * s5**2 * s6
    + 38 * s2**6 * s4 * s5**4
    + 144 * s2**6 * s6**4
    - 84 * s2**5 * s3**3 * s5 * s6**2
    + 8 * s2**5 * s3**2 * s4**2 * s6**2
    - 106 * s2**5 * s3**2 * s4 * s5**2 * s6
    - 12 * s2**5 * s3**2 * s5**4
    + 176 * s2**5 * s3 * s4**3 * s5 * s6
    - 36 * s2**5 * s3 * s4**2 * s5**3
    - 2544 * s2**5 * s3 * s5 * s6**3
    - 32 * s2**5 * s4**5 * s6
    + 8 * s2**5 * s4**4 * s5**2
    - 3072 * s2**5 * s4**2 * s6**3
    + 3032 * s2**5 * s4 * s5**2 * s6**2
    + 954 * s2**5 * s5**4 * s6
    + 36 * s2**4 * s3**4 * s5**2 * s6
    - 80 * s2**4 * s3**3 * s4**2 * s5 * s6
    + 25 * s2**4 * s3**3 * s4 * s5**3
    + 16 * s2**4 * s3**2 * s4**4 * s6
    - 6 * s2**4 * s3**2 * s4**3 * s5**2
    + 2520 * s2**4 * s3**2 * s4 * s6**3
    + 222 * s2**4 * s3**2 * s5**2 * s6**2
    - 1312 * s2**4 * s3 * s4**2 * s5 * s6**2
    - 3616 * s2**4 * s3 * s4 * s5**3 * s6
    - 125 * s2**4 * s3 * s5**5
    + 1296 * s2**4 * s4**4 * s6**2
    - 168 * s2**4 * s4**3 * s5**2 * s6
    + 375 * s2**4 * s4**2 * s5**4
    + 19296 * s2**4 * s4 * s6**4
    + 48408 * s2**4 * s5**2 * s6**3
    + 9 * s2**3 * s3**5 * s4 * s5 * s6
    - 4 * s2**3 * s3**5 * s5**3
    - 2 * s2**3 * s3**4 * s4**3 * s6
    + s2**3 * s3**4 * s4**2 * s5**2
    - 432 * s2**3 * s3**4 * s6**3
    + 324 * s2**3 * s3**3 * s4 * s5 * s6**2
    + 923 * s2**3 * s3**3 * s5**3 * s6
    - 752 * s2**3 * s3**2 * s4**3 * s6**2
    + 2262 * s2**3 * s3**2 * s4**2 * s5**2 * s6
    + 525 * s2**3 * s3**2 * s4 * s5**4
    - 9936 * s2**3 * s3**2 * s6**4
    - 480 * s2**3 * s3 * s4**4 * s5 * s6
    - 700 * s2**3 * s3 * s4**3 * s5**3
    - 68976 * s2**3 * s3 * s4 * s5 * s6**3
    - 11360 * s2**3 * s3 * s5**3 * s6**2
    - 32 * s2**3 * s4**6 * s6
    + 152 * s2**3 * s4**5 * s5**2
    + 6912 * s2**3 * s4**3 * s6**3
    - 7992 * s2**3 * s4**2 * s5**2 * s6**2
    + 5550 * s2**3 * s4 * s5**4 * s6
    - 29376 * s2**3 * s6**5
    + 108 * s2**2 * s3**4 * s4**2 * s6**2
    - 1215 * s2**2 * s3**4 * s4 * s5**2 * s6
    - 150 * s2**2 * s3**4 * s5**4
    + 336 * s2**2 * s3**3 * s4**3 * s5 * s6
    - 185 * s2**2 * s3**3 * s4**2 * s5**3
    + 17496 * s2**2 * s3**3 * s5 * s6**3
    + 8 * s2**2 * s3**2 * s4**5 * s6
    + 370 * s2**2 * s3**2 * s4**4 * s5**2
    - 864 * s2**2 * s3**2 * s4**2 * s6**3
)
"""
    init_file(template)
    assert main(".") == 1
    std = capsys.readouterr()
    assert E[903].ref in std.out


def test_fix_google_style_multiline_return_desc_false_positive_sig506_781(
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Description of return on multiple lines generates an error.

    This code uses Google style with a multiple line Returns comment. If
    the long line is on a single line there is no error, but then
    violates other rules with line length.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = '''\
def fct() -> bool:
    """Function.

    Returns:
        bool: Very long description
            on multiple lines
    """
'''
    init_file(template)
    assert main(".") == 0


def test_fix_docsig_crashes_on_duplicate_bases_error_783(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test fix docsig crashes on duplicates found in mros.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = """\
from dataclasses import dataclass
import typing as t
from abc import ABC

A = t.TypeVar("A")
B = t.TypeVar("B", bound=t.SupportsFloat)
C = t.TypeVar("C")


class D(t.Protocol[B, A]): ...


class E(D[B, A], t.Protocol[B, A, C]): ...


class F(E[B, A, C], t.Generic[B, A, C], ABC): ...


@dataclass(frozen=True)
class G(F[B, A, C], t.Generic[B, A, C]): ...
"""
    init_file(template)
    assert main(".") == 1
    std = capsys.readouterr()
    assert E[904].ref in std.out
