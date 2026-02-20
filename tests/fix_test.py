"""
tests.exclude_test
==================
"""

# pylint: disable=protected-access,line-too-long,too-many-lines
import io
import pickle
from pathlib import Path

import pytest
import tomli_w

import docsig
import docsig.plugin

# noinspection PyProtectedMember
from docsig._config import _ArgumentParser, _split_comma

from . import (
    TREE,
    FixtureFlake8,
    FixtureMakeTree,
    FixturePatchArgv,
    InitFileFixtureType,
    MockMainType,
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
    main: MockMainType,
    tmp_path: Path,
) -> None:
    """Ensure the unicode-decode error is handled without error.

    :param main: Patch package entry point.
    :param tmp_path: Create and return the temporary directory.
    """
    pkl = tmp_path / "test.pkl"
    serialize = [1, 2, 3]
    with open(pkl, "wb") as fout:
        pickle.dump(serialize, fout)  # type: ignore

    assert main(pkl, test_flake8=False) == 0


def test_exclude_dirs_392(
    monkeypatch: pytest.MonkeyPatch,
    main: MockMainType,
    make_tree: FixtureMakeTree,
) -> None:
    """Test dir regexes are correctly excluded.

    :param monkeypatch: Mock patch environment and attributes.
    :param main: Patch package entry point.
    :param make_tree: Create the directory tree from dict mapping.
    """
    pyproject_toml = Path.cwd() / "pyproject.toml"
    pyproject_toml.write_text(
        tomli_w.dumps(
            {
                "tool": {
                    docsig.__name__: {"exclude": r".*src[\\/]design[\\/].*"},
                },
            },
        ),
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
    main: MockMainType,
    make_tree: FixtureMakeTree,
    patch_logger: io.StringIO,
) -> None:
    """Test bash script is ignored when under __pycache__ directory.

    :param main: Patch package entry point.
    :param make_tree: Create the directory tree from dict mapping.
    :param patch_logger: Logs as an io instance.
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
def function(param, param2, param3, param4) -> int:
    """Desc.

     :param param1: Description of param1.
    :param param2:Description of param2.
    :param param3:
    """
''',
        '''\
def function(param, param2, param3, param4) -> int:
    """Desc.

     :param param1: Description of param1.
     :param param2:Description of param2.
    :param param3:
    """
''',
        '''\
def function(param, param2, param3, param4) -> int:
    """Desc.

     :param param1: Description of param1.
     :param param2:Description of param2.
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
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """
'''
    init_file(template)
    flake8(".", "--sig-check-class", "--sig-check-class-constructor")
    std = capsys.readouterr()
    assert docsig.messages.E[5].description in std.out


def test_description_missing_and_description_syntax_error_461(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test description missing raised with other description.

    The other description would cause a syntax in description error if
    it spanned over multiple lines.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
def function(param1, param2) -> None:
    """

    :param param1:
    :param param2: This one does have a description however
        and continues on the next line.
    """
'''
    init_file(template)
    main(".", test_flake8=False)
    std = capsys.readouterr()
    assert docsig.messages.E[301].description in std.out


def test_config_not_correctly_loaded_when_running_pre_commit_on_windows_488(
    patch_argv: FixturePatchArgv,
) -> None:
    """Test that config correctly loads on windows.

    Problem: When running the pre-commit hook in Windows PowerShell,
    get_config returns {} because prog='docsig.EXE' instead of 'docsig'.

    :param patch_argv: Patch commandline arguments.
    """
    disable = [
        "SIG101",
        "SIG202",
        "SIG203",
        "SIG301",
        "SIG302",
        "SIG401",
        "SIG402",
        "SIG404",
        "SIG501",
        "SIG502",
        "SIG503",
        "SIG505",
    ]
    pyproject_toml = Path.cwd() / "pyproject.toml"
    pyproject_toml.write_text(
        tomli_w.dumps({"tool": {docsig.__name__: {"disable": disable}}}),
        encoding="utf-8",
    )
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
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Fix properties not recognized when stacked.

    Also, check this does fail with --check-property-returns.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
import typing as _t
from abc import abstractmethod as _abstractmethod
from functools import cached_property as _cached_property

from ._ticker import Tickers as _Ticker
from ._transactions import Trades as _Trades

class Trades(dict[str, _Trades]):
    """Represents a collection of trades."""

class Account(dict[str, _t.Any]):
    """Represents an account."""

    @_abstractmethod
    @_cached_property
    def trades(self) -> Trades:
        """Get all trades."""

    @_abstractmethod
    @_cached_property
    def portfolio(self) -> _Tickers:
        """Get portfolio."""
'''
    init_file(template)
    assert not main(".", test_flake8=False)
    main(".", "-P", test_flake8=False)
    std = capsys.readouterr()
    assert docsig.messages.E[503].description in std.out


def test_properties_not_recognized_when_on_top_of_other_decorators_509(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Fix properties not recognized when stacked.

    Also, check this does fail with --check-property-returns.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
import typing as _t
from abc import abstractmethod as _abstractmethod
from functools import cached_property as _cached_property

from ._ticker import Tickers as _Ticker
from ._transactions import Trades as _Trades

class Trades(dict[str, _Trades]):
    """Represents a collection of trades."""

class Account(dict[str, _t.Any]):
    """Represents an account."""

    @_cached_property
    @_abstractmethod
    def trades(self) -> Trades:
        """Get all trades."""

    @_cached_property
    @_abstractmethod
    def portfolio(self) -> _Tickers:
        """Get portfolio."""
'''
    init_file(template)
    assert not main(".", test_flake8=False)
    main(".", "-P", test_flake8=False)
    std = capsys.readouterr()
    assert docsig.messages.E[503].description in std.out


def test_no_erroneous_301_in_duplicate(
    main: MockMainType,
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
) -> None:
    """Make sure 301 does not appear for duplicate parameters.

    :param main: Mock ``main`` function.
    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    """
    template = r'''
# pylint: disable=too-many-locals,too-many-statements
@_g.cache("arb.json")
@_g.cache("diff.json")
def print_target_progress(
    diff_obj: _g.CacheObj,
    arb_obj: _g.CacheObj,
    coins: _Coins,
    executor: _ThreadPoolExecutor,
    ignore_actionable_diff_score: bool,
) -> None:
    """Print table of target values.

    :param diff_obj: Object containing diff information.
    :param arb_obj: Object containing arb information.
    :param coins: Total coins to print.
    :param executor: Thread-safe Executor object.
    :param ignore_actionable_diff_score: Ignore actionable difference
        score.
    :param executor: ThreadPoolExecutor.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert docsig.messages.E[301].description not in std.out


def test_handle_empty_symlinks(
    main: MockMainType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """Ensure the program doesn't crash when it checks broken symlinks.

    :param main: Mock ``main`` function.
    :param tmp_path: Create and return the temporary directory.
    :param capsys: Capture sys out.
    """
    (tmp_path / "broken_symlink.py").symlink_to("does-not-exist")
    main(".")
    std = capsys.readouterr()
    assert docsig.messages.E[301].description not in std.out


def test_no_erroneous_402_when_order_cannot_be_confirmed(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Fix params out-of-order popping up with a single document.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
class Transactions(_Transactions):
    """Represents a transaction.

    :param symbol: Symbol.
    """

    def __init__(self, client: Client, symbol: str, attr: str):
        super().__init__()
        data = getattr(client, attr)(symbol=symbol)
        for i in data:
            try:
                epoch_seconds = i["insertTime"] / 1000
            except KeyError:
                dt_object = _datetime.strptime(
                    i["applyTime"], "%Y-%m-%d %H:%M:%S"
                )
                epoch_seconds = int(dt_object.timestamp())
            self.append(
                _Transaction(
                    _datetime.fromtimestamp(epoch_seconds).replace(
                        tzinfo=_timezone.utc
                    ),
                    float(i["amount"]),
                )
            )
'''
    init_file(template)
    main(".", "--check-class")
    std = capsys.readouterr()
    assert docsig.messages.E[402].description not in std.out


def test_fix_allow_or_operator_in_type_545(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test type declaration in name with pipe is allowed.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
def foo(a, **kwargs) -> None:
    """Test for docsig.

    :param str | None a: Use string or None for this purpose.
    :keyword str | None bar: Use string or None for this purpose.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert docsig.messages.E[201].description not in std.out
    assert docsig.messages.E[203].description not in std.out
    assert docsig.messages.E[301].description not in std.out
    assert docsig.messages.E[304].description.format(token="|") not in std.out


def test_close_with_bitwise_operator_545(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test pipe still treated as a bad closing token.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
def foo(**kwargs) -> None:
    """Test for docsig.

    :keyword bar| Use string or None for this purpose.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert docsig.messages.E[304].description.format(token="|") in std.out


def test_recognise_yield_550(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Recognize yield in docstrings.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
def count_up_to(n: int) -> _t.Generator[int, None, None]:
    """
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
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test indents are ignored within double dot directives.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
class Classy:
    @remove_last_args(['normalize'])  # since 8.2.0
    def toTimestr(self, force_iso: bool = False) -> str:
        """Convert the data to a UTC date/time string.

        .. seealso:: :meth:`fromTimestr` for differences between output
           with and without *force_iso* parameter.

        .. versionchanged:: 8.0
           *normalize* parameter was added.
        .. versionchanged:: 8.2
           *normalize* parameter was removed due to :phab:`T340495` and
           :phab:`T57755`

        :param force_iso: Whether the output should be forced to ISO 8601
        :return: Timestamp in a format resembling ISO 8601
        """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert not std.out


def test_fix_incorrect_sig402_when_it_should_only_be_sig203(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test no additional out-of-order or not-equal-to-arg.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
class ChildTransactions(Transactions):
    """Represents a collection of transactions.

    :param symbol: Currency symbol.
    :param attr: Transaction attribute.
    :param timestamp: Session timestamp.
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
    assert docsig.messages.E[402].description not in std.out
    assert docsig.messages.E[404].description not in std.out


def test_fix_incorrect_sig402_when_it_should_also_be_sig203(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test out-of-order still valid when param missing.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
class ChildTransactions(Transactions):
    """Represents a collection of transactions.

    :param symbol: Currency symbol.
    :param attr: Transaction attribute.
    :param timestamp: Session timestamp.
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
    assert docsig.messages.E[402].description in std.out


def test_fix_no_402_for_very_similar_names_683(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """402 should not be showing for very similar names.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
def function(param1, param2, param3, param4) -> None:
    """Function summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param4: Description of param4.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert docsig.messages.E[402].description not in std.out


def test_fix_incorrect_sig402_when_it_should_only_be_sig203_701(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test no additional out-of-order or not-equal-to-arg.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
@_decorators.parse_msgs
@_decorators.validate_args
def docsig(  # pylint: disable=too-many-locals,too-many-arguments
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
    """Package's core functionality.

    Populate a sequence of module objects before iterating over their
    top-level functions and classes.

    If any of the functions within the module - and methods within its
    classes - fail, print the resulting function string representation
    and report.

    :param path: Path(s) to check.
    :param string: String to check.
    :param list_checks: Display a list of all checks and their messages.
    :param check_class: Check class docstrings.
    :param check_class_constructor: Check ``__init__`` methods. Note
        that this is mutually incompatible with check_class.
    :param check_dunders: Check dunder methods
    :param check_protected_class_methods: Check public methods belonging
        to protected classes.
    :param check_nested: Check nested functions and classes.
    :param check_overridden: Check overridden methods
    :param check_protected: Check protected functions and classes.
    :param check_property_returns: Run return checks on properties.
    :param include_ignored: Check files even if they match a gitignore
        pattern.
    :param ignore_no_params: Ignore docstrings where parameters are not
        documented
    :param ignore_args: Ignore args prefixed with an asterisk.
    :param ignore_kwargs: Ignore kwargs prefixed with two asterisks.
    :param ignore_typechecker: Ignore checking return values.
    :param enforce_capitalization: Ensure param descriptions are
        capitalized.
    :param no_ansi: Disable ANSI output.
    :param verbose: Increase output verbosity.
    :param target: List of errors to target.
    :param disable: List of errors to disable.
    :param exclude: Regular expression of files and dirs to exclude from
        checks.
    :param excludes: Files or dirs to exclude from checks.
    :return: Exit status for whether a test failed or not.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert docsig.messages.E[402].description not in std.out


def test_incorrect_sig301_with_both_sig202_and_sig402_707(
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    init_file: InitFileFixtureType,
) -> None:
    """Test no incorrect SIG301 with both SIG202 and SIG402.

    :param capsys: Capture sys out.
    :param main: Mock ``main`` function.
    :param init_file: Initialize a test file.
    """
    template = '''
def function(a, b) -> None:
    """Function summary.

    :param b: Description of b.
    :param a: Description of a.
    :param c: Description of c.
    """
'''
    init_file(template)
    main(".")
    std = capsys.readouterr()
    assert docsig.messages.E[301].description not in std.out
