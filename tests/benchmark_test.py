"""
tests.benchmark_test
====================
"""

import pytest

from docsig import docsig

from . import MockMainType


@pytest.mark.parametrize(
    "template,path",
    [
        (
            '''
class Klass:
    def __init__(self, param1, param2) -> None:
        """Info about class.

        :param param2: Info about param2.
        :param param1: Info about param1.
        """
''',
            "klass.py",
        ),
        (
            '''
class Klass:
    """Info about class.

    :param param2: Info about param2.
    :param param1: Info about param1.
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
        """Info about class.

        :param param2: Info about param2.
        :param param1: Info about param1.
        """
''',
            "klass.py",
        ),
        (
            '''
def my_function(argument: int = 42) -> int:
    """
    Function that prints a message and returns the argument + 1

    Parameters
    ----------
    argument : int, optional
        The input argument, by default 42

    Returns
    -------
    int
        The input argument + 1
    """
    print("Hello from a function")
    print(argument)

    def my_external_function(argument: int = 42) -> int:
        print("Hello from an external function")
        print(argument)
        return argument + 42

    return argument + 1
''',
            "my_function.py",
        ),
        (
            '''
class Parent:
    def method(self) -> None:
        """This is documented."""
        self._set: _t.Set[T] = set()

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
    def prop(self) -> str:
        """This is documented."""
''',
            "klass_with_property.py",
        ),
        (
            '''
class _Klass:
    @property
    def prop(self, param1) -> str:
        """This is documented."""
''',
            "klass_with_documented_property.py",
        ),
        (
            '''
class Parent:
    def _protected(self, param1) -> None:
        """This is documented."""
        self._set: _t.Set[T] = set()
''',
            "parent_with_protected.py",
        ),
        (
            '''
def function(param1, param2, *args) -> None:
    """Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    :param args: Pass
    """
''',
            "function_with_args.py",
        ),
        (
            '''
def function(param1, param2, **kwargs) -> None:
    """Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    :param kwargs: Pass
    """
''',
            "function_with_kwargs.py",
        ),
        (
            '''
def function(param1, param2, *args) -> None:
    """Proper docstring."""
''',
            "function_with_undocumented_params.py",
        ),
        (
            '''
def function() -> None:
    """Proper docstring.

    :return: Returncode.
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
def test_bench(bench: MockMainType, template: str, path: str) -> None:
    """A small benchmark test.

    :param bench: Benchmark fixture that is active when the environment
        allows it to be.
    :param template: String data.
    :param path: An associated mock file path.
    """
    bench(docsig, path, string=template)
