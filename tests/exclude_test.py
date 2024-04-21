"""
tests.exclude_test
==================
"""

from __future__ import annotations

from pathlib import Path

from . import InitFileFixtureType, MockMainType, long


def test_exclude_defaults(
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test bash script is ignored when under __pycache__ directory.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = """\
#!/usr/bin/env bash
echo "${1//[ ]/\\\\ }"
"""
    init_file(template, Path("__pycache__") / "file.py")
    assert main(".") == 0


def test_exclude_argument(
    init_file: InitFileFixtureType,
    main: MockMainType,
) -> None:
    """Test bash script is ignored when exclude argument passed.

    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    template = """
#!/usr/bin/env bash
new-ssl() {
  domain="${1}"
  config="${2:-"${domain}.conf"}"
  openssl \
    req \
    -new \
    -newkey \
    rsa:2048 \
    -nodes \
    -sha256 \
    -out "${domain}.csr" \
    -keyout "${domain}.key" \
    -config "${config}"
}

new-ssl "${@}"
"""
    init_file(template)
    assert main(".", long.exclude, "file.py") == 0
