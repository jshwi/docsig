"""Generate version of changelog suitable for documentation."""

import json
import os
import re
import subprocess
import typing as t

import yaml
from sphinx.application import Sphinx

from docsig.plugin import ValidatePyproject


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


def get_docsig_help(app: Sphinx) -> t.Optional[str]:
    """Extract help from readme.

    :param app: The Sphinx application to register the extension with.
    :return: Help text, or None (won't be None - typechecker stuff).
    """
    items = code_block("console").findall(app.config.readme)
    for item in items:
        if "usage: docsig" in item:
            return item

    return None


def make_generated(app: Sphinx) -> None:
    """Make dir for generated files and make sure it is ignored.

    :param app: The Sphinx application to register the extension with.
    """
    app.config.generated.mkdir(exist_ok=True, parents=True)
    (app.config.generated / ".gitignore").write_text("*", encoding="utf-8")


def generate_changelog(app: Sphinx) -> None:
    """Generate changelog documentation.

    :param app: The Sphinx application to register the extension with.
    """
    content = "# Changelog\n\n{}".format(
        (
            (app.config.repo / "CHANGELOG.md")
            .read_text(encoding="utf-8")
            .split("<!-- release notes start -->")
        )[1],
    )
    (app.config.generated / "changelog.md").write_text(
        content,
        encoding="utf-8",
    )


def generate_contributing(app: Sphinx) -> None:
    """Generate contributing documentation.

    :param app: The Sphinx application to register the extension with.
    """
    content = (
        (app.config.repo / "CONTRIBUTING.md")
        .read_text(encoding="utf-8")
        .replace("# Contributing to docsig", "# Contributing")
    )
    (app.config.generated / "contributing.md").write_text(
        content,
        encoding="utf-8",
    )


def generate_docsig_help(app: Sphinx) -> None:
    """Generate docsig help documentation.

    :param app: The Sphinx application to register the extension with.
    """
    content = get_docsig_help(app)
    if content is not None:
        (app.config.generated / "docsig-help.rst").write_text(
            content,
            encoding="utf-8",
        )


def generate_pyproject_toml_example(app: Sphinx) -> None:
    """Generate pyproject.toml example.

    :param app: The Sphinx application to register the extension with.
    """
    (app.config.generated / "pyproject-toml-example.rst").write_text(
        code_block("toml").findall(app.config.readme)[0],
        encoding="utf-8",
    )


def generate_pyproject_toml_schema_info(app: Sphinx) -> None:
    """Generate pyproject.toml schema info.

    :param app: The Sphinx application to register the extension with.
    """
    pattern = re.compile(
        r"\.\. schema-info start\s*(.*?)\s*\.\. schema-info end",
        re.DOTALL,
    )
    match = pattern.search(app.config.readme)
    (app.config.generated / "pyproject-schema-info.rst").write_text(
        match.group(1).strip() if match else "",
        encoding="utf-8",
    )


def generate_tests(app: Sphinx) -> None:
    """Generate documentation for tests.

    :param app: The Sphinx application to register the extension with.
    """
    os.environ["PYTHONPATH"] = str(app.config.repo)
    content = []
    source = app.srcdir / "_build"
    build = source / "markdown"
    test_rst = """
tests
=====

.. automodule:: tests.base_test
    :members:
    :undoc-members:
    :show-inheritance:
"""
    (source / "index.rst").write_text(test_rst)
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
        match = re.match(r"(.*)tests\.base_test\.test_(.*)\((.*)", line)
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

    (app.config.generated / "tests.md").write_text(
        _normalize_strange_characters(
            "{}\n".format(
                "\n".join(content)
                .strip()
                .replace("\n###", "##")
                .replace("# tests", "# Tests"),
            ),
        ),
    )


def generate_pre_commit_example(app: Sphinx) -> None:
    """Generate pre-commit example.

    :param app: The Sphinx application to register the extension with.
    """
    (app.config.generated / "pre-commit-example.rst").write_text(
        code_block("yaml").findall(app.config.readme)[0],
        encoding="utf-8",
    )


def generate_pre_commit_flake8_example(app: Sphinx) -> None:
    """Generate pre-commit flake8 example.

    :param app: The Sphinx application to register the extension with.
    """
    (app.config.generated / "pre-commit-flake8-example.rst").write_text(
        code_block("yaml").findall(app.config.readme)[1],
        encoding="utf-8",
    )


def generate_commit_policy(app: Sphinx) -> None:
    """Generate commit-policy page.

    :param app: The Sphinx application to register the extension with.
    """
    file = app.config.repo / ".conform.yaml"
    build = app.config.generated / "commit-policy.md"
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


def generate_flake8_help(app: Sphinx) -> None:
    """Generate flake8 documentation.

    :param app: The Sphinx application to register the extension with.
    """
    build = app.config.generated / "flake8.rst"
    pattern = re.compile(r"Flake8\n\*{6}(.*?)end flake8", re.DOTALL)
    match = pattern.search(app.config.readme)
    if match:
        build.write_text(match.group(1).strip()[:-2].strip(), encoding="utf-8")


def generate_schema(app: Sphinx) -> None:
    """Generate docsig schema.

    :param app: The Sphinx application to register the extension with.
    """
    (app.config.generated / "schema.json").write_text(
        json.dumps(ValidatePyproject(), indent=2),
    )


def setup(app: Sphinx) -> None:
    """Set up the Sphinx extension.

    :param app: The Sphinx application to register the extension with.
    """
    app.add_config_value("generated", app.srcdir / "_generated", "html")
    app.add_config_value("repo", app.srcdir.parent, "html")
    app.add_config_value(
        "readme",
        (app.config.repo / "README.rst").read_text(encoding="utf-8"),
        "html",
    )
    app.connect("builder-inited", make_generated)
    app.connect("builder-inited", generate_contributing)
    app.connect("builder-inited", generate_changelog)
    app.connect("builder-inited", generate_docsig_help)
    app.connect("builder-inited", generate_pyproject_toml_example)
    app.connect("builder-inited", generate_tests)
    app.connect("builder-inited", generate_pre_commit_example)
    app.connect("builder-inited", generate_pre_commit_flake8_example)
    app.connect("builder-inited", generate_commit_policy)
    app.connect("builder-inited", generate_flake8_help)
    app.connect("builder-inited", generate_schema)
