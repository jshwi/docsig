"""
tests.fuzz_test
===============

Property-based fuzzing of the public API with generated Python source.

Every strategy below generates source that compiles, so docsig must
always return an exit status for it: 0 or 1 for a completed run, or 123
for the rare module astroid cannot parse even though compile accepted
it. Anything raised out of the API is a bug.

Runs are derandomized so a green push cannot turn red on a reseed; a
deeper sweep is a matter of raising DOCSIG_FUZZ_EXAMPLES.
"""

import os

from hypothesis import HealthCheck, given, settings
from hypothesmith import from_grammar, from_node

import docsig

MAX_EXAMPLES = int(os.environ.get("DOCSIG_FUZZ_EXAMPLES", "30"))
SUPPRESSED = (
    HealthCheck.too_slow,
    HealthCheck.filter_too_much,
    HealthCheck.function_scoped_fixture,
)


def _check_string(source: str) -> None:
    assert docsig.docsig(
        string=source,
        check_class=True,
        check_dunders=True,
        check_nested=True,
        check_overridden=True,
        check_protected=True,
        check_protected_class_methods=True,
        check_property_returns=True,
    ) in (0, 1, 123)


@settings(
    deadline=None,
    derandomize=True,
    max_examples=MAX_EXAMPLES,
    suppress_health_check=SUPPRESSED,
)
@given(source=from_grammar())
def test_fuzz_grammar_source_returns_exit_status(source: str) -> None:
    """Grammar-generated modules always produce an exit status.

    :param source: Generated Python module source.
    """
    _check_string(source)


@settings(
    deadline=None,
    derandomize=True,
    max_examples=MAX_EXAMPLES,
    suppress_health_check=SUPPRESSED,
)
@given(source=from_node())
def test_fuzz_node_source_returns_exit_status(source: str) -> None:
    """Syntax-tree-generated modules always produce an exit status.

    :param source: Generated Python module source.
    """
    _check_string(source)
