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
class Class:
    def __init__(self, a, b) -> None:
        """Docstring summary.

        :param b: Description of b.
        :param a: Description of a.
        """
''',
            "klass.py",
        ),
        (
            '''
class Class:
    """Docstring summary.

    :param b: Description of b.
    :param a: Description of a.
    """

    def __init__(self, a, b) -> None:
        pass
''',
            "klass.py",
        ),
        (
            '''
class Class:
    def __get__(self, a, b) -> None:
        """Docstring summary.

        :param b: Description of b.
        :param a: Description of a.
        """
''',
            "klass.py",
        ),
        (
            '''
def function(a: int = 42) -> int:
    """
    Function that prints a message and returns the argument + 1

    Parameters
    ----------
    argument : int, optional
        Description of argument.

    Returns
    -------
    int
        Return description.
    """
    def nested_function(a: int = 42) -> int:
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
        pass
''',
            "parent_and_child.py",
        ),
        (
            '''
class Class:
    @property
    def method(self) -> int:
        """Docstring summary."""
''',
            "klass_with_property.py",
        ),
        (
            '''
class _Class:
    @property
    def method(self, a) -> int:
        """Docstring summary."""
''',
            "klass_with_documented_property.py",
        ),
        (
            '''
class Parent:
    def _method(self, a) -> None:
        """Docstring summary."""
''',
            "parent_with_protected.py",
        ),
        (
            '''
def function(a, b, *args) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param args: Description of args.
    """
''',
            "function_with_args.py",
        ),
        (
            '''
def function(a, b, **kwargs) -> None:
    """Docstring summary.

    :param a: Description of a.
    :param b: Description of b.
    :param kwargs: Description of kwargs.
    """
''',
            "function_with_kwargs.py",
        ),
        (
            '''
def function(a, b, *args) -> None:
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
