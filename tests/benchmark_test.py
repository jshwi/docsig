"""
tests.benchmark_test
====================
"""

import pytest

from docsig import docsig

from . import FixtureMain


@pytest.mark.parametrize(
    "template,path",
    [
        (
            '''
class Klass:
    def __init__(self, param1, param2) -> None:
        """Docstring summary.

        :param param2: Description of param2.
        :param param1: Description of param1.
        """
''',
            "klass.py",
        ),
        (
            '''
class Klass:
    """Docstring summary.

    :param param2: Description of param2.
    :param param1: Description of param1.
    """

    def __init__(self, param1, param2) -> None:
        pass
''',
            "klass.py",
        ),
        (
            '''
class Klass:
    def __get__(self, param1, param2) -> None:
        """Docstring summary.

        :param param2: Description of param2.
        :param param1: Description of param1.
        """
''',
            "klass.py",
        ),
        (
            '''
def function(argument: int = 42) -> int:
    """
    Function that prints a message and returns the argument + 1

    Parameters
    ----------
    argument : int, optional
        The input argument, by default 42

    Returns
    -------
    int
        Return description.
    """
    def nested_function(argument: int = 42) -> int:
        pass
''',
            "my_function.py",
        ),
        (
            '''
class Parent:
    def method(self) -> None:
        """Docstring summary."""

class Child(Parent):
    def method(self) -> None:
        self._set: _t.Set[T] = set()
''',
            "parent_and_child.py",
        ),
        (
            '''
class Klass:
    @property
    def method(self) -> str:
        """Docstring summary."""
''',
            "klass_with_property.py",
        ),
        (
            '''
class _Klass:
    @property
    def method(self, param1) -> str:
        """Docstring summary."""
''',
            "klass_with_documented_property.py",
        ),
        (
            '''
class Parent:
    def _method(self, param1) -> None:
        """Docstring summary."""
''',
            "parent_with_protected.py",
        ),
        (
            '''
def function(param1, param2, *args) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param args: Pass
    """
''',
            "function_with_args.py",
        ),
        (
            '''
def function(param1, param2, **kwargs) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param kwargs: Pass
    """
''',
            "function_with_kwargs.py",
        ),
        (
            '''
def function(param1, param2, *args) -> None:
    """Docstring summary."""
''',
            "function_with_undocumented_params.py",
        ),
        (
            '''
def function() -> None:
    """Docstring summary.

    :return: Return description.
    """,
''',
            "function_with_documented_return.py",
        ),
    ],
    ids=[
        "c_init",
        "c_class",
        "c_dunder",
        "c_nested",
        "c_override",
        "c_prop_ret",
        "c_prot_meth",
        "c_protected",
        "i_args",
        "i_kwargs",
        "i_no_params",
        "i_types",
    ],
)
@pytest.mark.benchmark
def test_bench(bench: FixtureMain, template: str, path: str) -> None:
    """A small benchmark test.

    :param bench: Benchmark fixture that is active when the environment
        allows it to be.
    :param template: String data.
    :param path: An associated mock file path.
    """
    bench(docsig, path, string=template)
