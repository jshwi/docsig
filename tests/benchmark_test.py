"""
tests.benchmark_test
====================
"""

import pytest

from docsig import docsig

from . import MockMainType


@pytest.mark.parametrize(
    "template",
    [
        '''
class Klass:
    def __init__(self, param1, param2) -> None:
        """Info about class.

        :param param2: Info about param2.
        :param param1: Info about param1.
        """
''',
        '''
class Klass:
    """Info about class.

    :param param2: Info about param2.
    :param param1: Info about param1.
    """

    def __init__(self, param1, param2) -> None:
        pass
''',
        '''
class Klass:
    def __get__(self, param1, param2) -> None:
        """Info about class.

        :param param2: Info about param2.
        :param param1: Info about param1.
        """
''',
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
        '''
class Parent:
    def method(self) -> None:
        """This is documented."""
        self._set: _t.Set[T] = set()

class Child(Parent):
    def method(self) -> None:
        self._set: _t.Set[T] = set()
''',
        '''
class Klass:
    @property
    def prop(self) -> str:
        """This is documented."""
''',
        '''
class _Klass:
    @property
    def prop(self, param1) -> str:
        """This is documented."""
''',
        '''
class Parent:
    def _protected(self, param1) -> None:
        """This is documented."""
        self._set: _t.Set[T] = set()
''',
        '''
def function(param1, param2, *args) -> None:
    """Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    :param args: Pass
    """
''',
        '''
def function(param1, param2, **kwargs) -> None:
    """Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    :param kwargs: Pass
    """
''',
        '''
def function(param1, param2, *args) -> None:
    """Proper docstring."""
''',
        '''
def function() -> None:
    """Proper docstring.

    :return: Returncode.
    """
''',
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
def test_bench(bench: MockMainType, template: str) -> None:
    """A small benchmark test.

    :param bench: Benchmark fixture that is active when environment
        allows it to be.
    :param template: String data.
    """
    bench(docsig, string=template)
