"""
tests.misc_test
===============
"""
# pylint: disable=protected-access
import pytest
from templatest import templates

import docsig.messages

from . import InitFileFixtureType, MockMainType, long, short
from ._utils import DummyFunc, errors, hints


@pytest.mark.parametrize("arg", (short.v, long.version))
def test_print_version(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    main: MockMainType,
    arg: str,
) -> None:
    """Test printing of version on commandline.

    :param monkeypatch: Mock patch environment and attributes.
    :param capsys: Capture sys out.
    :param main: Patch package entry point.
    :param arg: Version argument.
    """
    monkeypatch.setattr("docsig._config.__version__", "1.0.0")
    with pytest.raises(SystemExit):
        main(arg)

    std = capsys.readouterr()
    assert std.out.strip() == "1.0.0"


def test_mutable_sequence() -> None:
    """Get coverage on ``MutableSequence``."""
    report = docsig._report.Report(DummyFunc(), [], [], False)  # type: ignore
    report.append(errors[0])
    assert getattr(docsig.messages, errors[0]) in report
    assert len(report) == 1
    report[0] = errors[1]
    report.pop()
    assert errors[1] not in report


def test_message_sequence() -> None:
    """Test disabling of error messages.

    Assert that all following hints are disabled, until a new error
    message that has not been disabled is appended to the sequence.
    """
    # noinspection PyUnresolvedReferences
    msg_seq = docsig._report._MessageSequence(disable=[errors[0]])
    msg_seq.append(errors[0])
    msg_seq.append(hints[0])
    msg_seq.append(hints[1])
    assert getattr(docsig.messages, errors[0]) not in msg_seq
    assert getattr(docsig.messages, hints[1]) not in msg_seq
    assert getattr(docsig.messages, hints[1]) not in msg_seq
    msg_seq.append(errors[1])
    msg_seq.append(hints[0])
    msg_seq.append(hints[1])
    assert getattr(docsig.messages, errors[1]) in msg_seq
    assert getattr(docsig.messages, hints[0]) in msg_seq
    assert getattr(docsig.messages, hints[1]) in msg_seq


@pytest.mark.parametrize("message", errors)
def test_target_report(message: str) -> None:
    """Test report only adds the target error provided.

    The test should fail as it matches with the selected target.

    Assert that the error appears in the report to confirm it has
    triggered.

    :param message: Error message code.
    """
    # noinspection PyUnresolvedReferences
    report = docsig._report.Report(
        DummyFunc(),  # type: ignore
        targets=[message],
        disable=[],
        check_property_returns=False,
    )
    report.extend(errors)
    assert getattr(docsig.messages, message) in report
    assert len(report) == 1


def test_lineno(
    capsys: pytest.CaptureFixture,
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test printing of three function errors with line number.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(
        templates.registered.getbyname("m-fail-s").template  # type: ignore
    )
    main()
    std = capsys.readouterr()
    assert "module/file.py:2" in std.out
    assert "module/file.py:11" in std.out
    assert "module/file.py:19" in std.out


def test_param_ne() -> None:
    """Get coverage on `Param.__eq__`."""
    # noinspection PyUnresolvedReferences
    assert docsig._function.Param() != object
