"""Generate version of changelog suitable for documentation."""

import functools
import os
import re
import shutil
import subprocess
import typing as t
from pathlib import Path

import yaml
from sphinx.application import Sphinx

DOCS_DIR = Path(__file__).parent.parent.absolute()
USAGE = DOCS_DIR / "usage"
CONFIGURATION = USAGE / "configuration"
GENERATED = DOCS_DIR / "_generated"
MESSAGES_DIR = USAGE / "messages"
GITIGNORE = GENERATED / ".gitignore"
REPO = DOCS_DIR.parent
README = REPO / "README.rst"
TEST_RST = """
tests
=====

.. automodule:: tests._test
    :members:
    :undoc-members:
    :show-inheritance:
"""


def _normalize_strange_characters(s: str) -> str:
    mapping = {
        "‘": "'",
        "’": "'",
        "–": "-",
        "“": '"',
        "”": '"',
    }
    for k, v in mapping.items():
        s = s.replace(k, v)

    return s


def code_block(lang: str) -> re.Pattern:
    """Extract content from a code block.

    :param lang: Code block language.
    :return: Regex matching the code block.
    """
    return re.compile(rf"(\.\. code-block:: {lang}\s*\n(?:\s{{4}}.+\n)+)")


def extension(func: t.Callable[..., None]) -> t.Callable[..., None]:
    """Consume unused sphinx option.

    :param func: Extension function.
    :return: Decorated function.
    """

    @functools.wraps(func)
    def wrapper(_: Sphinx) -> None:
        return func()

    return wrapper


def get_docsig_help() -> t.Optional[str]:
    """Extract help from readme.

    :return: Help text, or None (won't be None - typechecker stuff).
    """
    content = README.read_text(encoding="utf-8")
    items = code_block("console").findall(content)
    for item in items:
        if "usage: docsig" in item:
            return item

    return None


@extension
def make_generated_dir() -> None:
    """Make dir for generated files and make sure it is ignored."""
    if GENERATED.is_dir():
        shutil.rmtree(GENERATED)

    MESSAGES_DIR.mkdir(exist_ok=True, parents=True)
    CONFIGURATION.mkdir(exist_ok=True, parents=True)
    GENERATED.mkdir(exist_ok=True, parents=True)
    GITIGNORE.write_text("*", encoding="utf-8")


@extension
def generate_changelog() -> None:
    """Generate changelog documentation."""
    content = "# Changelog\n\n{}".format(
        (
            (REPO / "CHANGELOG.md")
            .read_text(encoding="utf-8")
            .split("<!-- release notes start -->")
        )[1],
    )
    (GENERATED / "changelog.md").write_text(content, encoding="utf-8")


@extension
def generate_contributing() -> None:
    """Generate contributing documentation."""
    content = (
        (REPO / "CONTRIBUTING.md")
        .read_text(encoding="utf-8")
        .replace("# Contributing to docsig", "# Contributing")
    )
    (GENERATED / "contributing.md").write_text(content, encoding="utf-8")


@extension
def generate_docsig_help() -> None:
    """Generate docsig help documentation."""
    content = get_docsig_help()
    if content is not None:
        (GENERATED / "docsig-help.rst").write_text(content, encoding="utf-8")


@extension
def generate_pyproject_toml_example() -> None:
    """Generate pyproject.toml example."""
    content = README.read_text(encoding="utf-8")
    (GENERATED / "pyproject-toml-example.rst").write_text(
        code_block("toml").findall(content)[0],
        encoding="utf-8",
    )


@extension
def generate_tests() -> None:
    """Generate documentation for tests."""
    os.environ["PYTHONPATH"] = str(REPO)
    content = []
    source = DOCS_DIR / "_build"
    build = source / "markdown"
    (source / "index.rst").write_text(TEST_RST)
    subprocess.run(
        [
            "sphinx-build",
            "-b",
            "markdown",
            "-C",
            "-D",
            "extensions=sphinx.ext.autodoc",
            source,
            build,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    lines = (build / "index.md").read_text(encoding="utf-8").splitlines()
    skip_lines = False
    for line in lines:
        match = re.match(r"(.*)tests\._test\.test_(.*)\((.*)", line)
        if match:
            skip_lines = False
            content.append(
                "{}{}\n".format(
                    match.group(1),
                    match.group(2).capitalize().replace("_", " "),
                ),
            )
        elif line.startswith("* **"):
            skip_lines = True
        elif not skip_lines:
            content.append(line)

    (GENERATED / "tests.md").write_text(
        _normalize_strange_characters(
            "{}\n".format(
                "\n".join(content)
                .strip()
                .replace("\n###", "##")
                .replace("# tests", "# Tests"),
            ),
        ),
    )


@extension
def generate_pre_commit_example() -> None:
    """Generate pre-commit example."""
    content = README.read_text(encoding="utf-8")
    (GENERATED / "pre-commit-example.rst").write_text(
        code_block("yaml").findall(content)[0],
        encoding="utf-8",
    )


@extension
def generate_pre_commit_flake8_example() -> None:
    """Generate pre-commit flake8 example."""
    content = README.read_text(encoding="utf-8")
    (GENERATED / "pre-commit-flake8-example.rst").write_text(
        code_block("yaml").findall(content)[1],
        encoding="utf-8",
    )


@extension
def generate_commit_policy() -> None:
    """Generate commit-policy page."""
    file = REPO / ".conform.yaml"
    build = GENERATED / "commit-policy.md"
    content = ["# Commit Policy\n"]
    policy = yaml.safe_load(file.read_text(encoding="utf-8"))["policies"][0]
    for header, obj in policy["spec"].items():
        content.append(f"## {header.capitalize()}\n")
        if not isinstance(obj, dict):
            content.append(f"{obj}\n")
        else:
            for key, value in obj.items():
                if isinstance(value, list):
                    value = "### {}\n\n- {}".format(
                        key.capitalize(),
                        "\n- ".join(value),
                    )
                else:
                    pattern = re.compile(r"([A-Z][^A-Z]*)")
                    match = [i for i in pattern.split(key) if i]
                    if match:
                        key = " ".join(match).capitalize()

                    value = f"{key}: {value}"

                content.append(f"{value}\n")

    build.write_text("\n".join(content), encoding="utf-8")


@extension
def generate_flake8_help() -> None:
    """Generate flake8 documentation."""
    build = GENERATED / "flake8.rst"
    readme = README.read_text(encoding="utf-8")
    pattern = re.compile(r"Flake8\n\*{6}(.*?)end flake8", re.DOTALL)
    match = pattern.search(readme)
    if match:
        build.write_text(match.group(1).strip()[:-2].strip(), encoding="utf-8")


def setup(app: Sphinx) -> None:
    """Set up the Sphinx extension.

    :param app: The Sphinx application to register the extension with.
    """
    app.connect("builder-inited", make_generated_dir)
    app.connect("builder-inited", generate_contributing)
    app.connect("builder-inited", generate_changelog)
    app.connect("builder-inited", generate_docsig_help)
    app.connect("builder-inited", generate_pyproject_toml_example)
    app.connect("builder-inited", generate_tests)
    app.connect("builder-inited", generate_pre_commit_example)
    app.connect("builder-inited", generate_pre_commit_flake8_example)
    app.connect("builder-inited", generate_commit_policy)
    app.connect("builder-inited", generate_flake8_help)
