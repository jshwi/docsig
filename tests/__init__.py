"""
tests
=====

Test package for ``docsig``.
"""

# pylint: disable=too-many-lines
import typing as t
from pathlib import Path

from templatest import BaseTemplate as _BaseTemplate
from templatest import templates as _templates

from docsig.messages import TEMPLATE as T
from docsig.messages import E

MockMainType = t.Callable[..., t.Union[str, int]]
FixtureFlake8 = t.Callable[..., int]
FixtureMakeTree = t.Callable[[Path, t.Dict[t.Any, t.Any]], None]
FixturePatchArgv = t.Callable[..., None]


class InitFileFixtureType(
    t.Protocol,
):  # pylint: disable=too-few-public-methods
    """Type for ``fixture_init_file``."""

    def __call__(self, content: str, path: Path = ..., /) -> Path:
        """Type for ``fixture_init_file``."""


MULTI = "m"
NAME = "name"
TEMPLATE = "template"
EXPECTED = "expected"
E10 = "e-1-0"
FAIL = "f"
PASS = "p"
TOML = "pyproject.toml"
TOOL = "tool"
LIST = "list"
CHECK_ARGS = (
    "--check-class",
    "--check-protected",
    "--check-overridden",
    "--check-dunders",
    "--check-property-returns",
    "--check-protected-class-methods",
    "--check-nested",
)
FAIL_CHECK_ARGS = tuple(f"f-{i[8:]}" for i in CHECK_ARGS)
ENABLE = "enable"
UNKNOWN = "unknown"
PATH = Path("module") / "file.py"
WILL_ERROR = """
#!/bin/bash
echo "Hello World!"
"""
TREE = {
    "file1.txt": [],
    "file2.txt": [],
    "file3.txt": [],
    "file4.txt": [],
    "file5.txt": [],
    "file10.txt": [],
    "file[1].txt": [],
    ".pyaud_cache": {
        "7.5.1": {
            "CACHEDIR.TAG": [WILL_ERROR],
            "files.json": [WILL_ERROR],
            ".gitignore": ["# Created by pyaud automatically.", "*"],
        },
    },
    "CODE_OF_CONDUCT.md": [WILL_ERROR],
    ".pylintrc": [WILL_ERROR],
    "LICENSE": [WILL_ERROR],
    ".pytest_cache": {
        "CACHEDIR.TAG": [WILL_ERROR],
        "README.md": [WILL_ERROR],
        ".gitignore": ["# Created by pytest automatically.", "*"],
        "v": {
            "cache": {
                "nodeids": [WILL_ERROR],
                "lastfailed": [WILL_ERROR],
                "stepwise": "",
            },
            "randomly_seed": [WILL_ERROR],
        },
    },
    "CHANGELOG.md": [WILL_ERROR],
    "dist": {
        "docsig-0.49.1.tar.gz": [WILL_ERROR],
        "docsig-0.49.2-py3-none-any.whl": [WILL_ERROR],
        "docsig-0.49.2.tar.gz": [WILL_ERROR],
        "docsig-0.49.0-py3-none-any.whl": [WILL_ERROR],
        "docsig-0.49.0.tar.gz": [WILL_ERROR],
        "docsig-0.49.1-py3-none-any.whl": [WILL_ERROR],
    },
    ".pre-commit-config.yaml": [WILL_ERROR],
    ".coverage": [WILL_ERROR],
    "Makefile": [WILL_ERROR],
    "whitelist.py": [],
    ".pre-commit-hooks.yaml": [WILL_ERROR],
    "pyproject.toml": [],
    ".bumpversion.cfg": [WILL_ERROR],
    "node_modules": {
        ".cache": {
            "prettier": {
                ".prettier-caches": {
                    "7f51ae3462154079bc96a79583b977616b1ad315.json": [
                        WILL_ERROR,
                    ],
                },
            },
        },
    },
    "tests": {
        "misc_test.py": [],
        "conftest.py": [],
        "disable_test.py": [],
        "__init__.py": [],
        "__pycache__": {
            "_test.cpython-38-pytest-8.1.1.pyc": [WILL_ERROR],
            "__init__.cpython-38.pyc": [WILL_ERROR],
            "disable_test.cpython-38-pytest-8.1.1.pyc": [WILL_ERROR],
            "misc_test.cpython-38-pytest-8.1.1.pyc": [WILL_ERROR],
            "_test.cpython-38.pyc": [WILL_ERROR],
            "conftest.cpython-38-pytest-8.1.1.pyc": [WILL_ERROR],
        },
        "TESTS.md": [WILL_ERROR],
        "git_test.py": [],
        "_test.py": [],
    },
    ".conform.yaml": [WILL_ERROR],
    "docs": {
        "index.rst": [WILL_ERROR],
        "requirements.txt": [WILL_ERROR],
        "docsig.rst": [WILL_ERROR],
        "conf.py": [],
        "static": {"docsig.svg": [WILL_ERROR]},
        "examples": {
            "classes.rst": [WILL_ERROR],
            "message-control.rst": [WILL_ERROR],
        },
    },
    ".readthedocs.yml": [WILL_ERROR],
    ".prettierignore": [WILL_ERROR],
    ".editorconfig": [WILL_ERROR],
    "docsig": {
        "_stub.py": [],
        "_report.py": [],
        "_main.py": [],
        "_version.py": [],
        "_module.py": [],
        "__init__.py": [],
        "_display.py": [],
        "_hooks.py": [],
        "__pycache__": {
            "_core.cpython-311.pyc": [WILL_ERROR],
            "__init__.cpython-38.pyc": [WILL_ERROR],
            "_core.cpython-38.pyc": [WILL_ERROR],
            "_main.cpython-311.pyc": [WILL_ERROR],
            "_decorators.cpython-38.pyc": [WILL_ERROR],
            "_message.cpython-311.pyc": [WILL_ERROR],
            "_config.cpython-311.pyc": [WILL_ERROR],
            "_config.cpython-38.pyc": [WILL_ERROR],
            "messages.cpython-311.pyc": [WILL_ERROR],
            "_display.cpython-311.pyc": [WILL_ERROR],
            "_display.cpython-38.pyc": [WILL_ERROR],
            "_stub.cpython-311.pyc": [WILL_ERROR],
            "_decorators.cpython-311.pyc": [WILL_ERROR],
            "_hooks.cpython-38.pyc": [WILL_ERROR],
            "_utils.cpython-38.pyc": [WILL_ERROR],
            "_report.cpython-311.pyc": [WILL_ERROR],
            "_directives.cpython-38.pyc": [WILL_ERROR],
            "_hooks.cpython-311.pyc": [WILL_ERROR],
            "__main__.cpython-38.pyc": [WILL_ERROR],
            "_version.cpython-311.pyc": [WILL_ERROR],
            "_utils.cpython-311.pyc": [WILL_ERROR],
            "_module.cpython-311.pyc": [WILL_ERROR],
            "_stub.cpython-38.pyc": [WILL_ERROR],
            "messages.cpython-38.pyc": [WILL_ERROR],
            "_message.cpython-38.pyc": [WILL_ERROR],
            "_report.cpython-38.pyc": [WILL_ERROR],
            "_version.cpython-38.pyc": [WILL_ERROR],
            "_directives.cpython-311.pyc": [WILL_ERROR],
            "_git.cpython-38.pyc": [WILL_ERROR],
            "_module.cpython-38.pyc": [WILL_ERROR],
            "_main.cpython-38.pyc": [WILL_ERROR],
            "__init__.cpython-311.pyc": [WILL_ERROR],
            "__main__.cpython-311.pyc": [WILL_ERROR],
        },
        "_message.py": [],
        "_core.py": [],
        "_decorators.py": [],
        "messages.py": [],
        "py.typed": [WILL_ERROR],
        "_config.py": [],
        "__main__.py": [],
        "_utils.py": [],
        "_directives.py": [],
    },
    ".mypy_cache": {
        "CACHEDIR.TAG": [WILL_ERROR],
        "3.12": {
            "builtins.meta.json": [WILL_ERROR],
            "genericpath.meta.json": [WILL_ERROR],
            "enum.meta.json": [WILL_ERROR],
            "abc.meta.json": [WILL_ERROR],
            "subprocess.meta.json": [WILL_ERROR],
            "dataclasses.data.json": [WILL_ERROR],
            "typing.data.json": [WILL_ERROR],
            "resource.data.json": [WILL_ERROR],
            "_codecs.meta.json": [WILL_ERROR],
            "posixpath.data.json": [WILL_ERROR],
            "contextlib.meta.json": [WILL_ERROR],
            "_codecs.data.json": [WILL_ERROR],
            "posixpath.meta.json": [WILL_ERROR],
            "contextlib.data.json": [WILL_ERROR],
            "resource.meta.json": [WILL_ERROR],
            "typing.meta.json": [WILL_ERROR],
            "_typeshed": {
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "abc.data.json": [WILL_ERROR],
            "subprocess.data.json": [WILL_ERROR],
            "zipfile": {
                "_path.data.json": [WILL_ERROR],
                "_path.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "dataclasses.meta.json": [WILL_ERROR],
            "genericpath.data.json": [WILL_ERROR],
            "enum.data.json": [WILL_ERROR],
            "builtins.data.json": [WILL_ERROR],
            "@plugins_snapshot.json": [WILL_ERROR],
            "sre_compile.meta.json": [WILL_ERROR],
            "io.data.json": [WILL_ERROR],
            "codecs.data.json": [WILL_ERROR],
            "pathlib.data.json": [WILL_ERROR],
            "typing_extensions.meta.json": [WILL_ERROR],
            "conf.meta.json": [WILL_ERROR],
            "_ast.meta.json": [WILL_ERROR],
            "sre_parse.meta.json": [WILL_ERROR],
            "sys": {
                "__init__.meta.json": [WILL_ERROR],
                "_monitoring.data.json": [WILL_ERROR],
                "_monitoring.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "_collections_abc.meta.json": [WILL_ERROR],
            "sre_constants.meta.json": [WILL_ERROR],
            "types.data.json": [WILL_ERROR],
            "re.meta.json": [WILL_ERROR],
            "os": {
                "path.data.json": [WILL_ERROR],
                "path.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "re.data.json": [WILL_ERROR],
            "types.meta.json": [WILL_ERROR],
            "importlib": {
                "abc.meta.json": [WILL_ERROR],
                "machinery.data.json": [WILL_ERROR],
                "_abc.data.json": [WILL_ERROR],
                "_abc.meta.json": [WILL_ERROR],
                "resources": {
                    "abc.meta.json": [WILL_ERROR],
                    "abc.data.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
                "abc.data.json": [WILL_ERROR],
                "machinery.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "readers.meta.json": [WILL_ERROR],
                "readers.data.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "metadata": {
                    "__init__.meta.json": [WILL_ERROR],
                    "_meta.meta.json": [WILL_ERROR],
                    "_meta.data.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
            },
            "sre_constants.data.json": [WILL_ERROR],
            "collections": {
                "abc.meta.json": [WILL_ERROR],
                "abc.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "_ast.data.json": [WILL_ERROR],
            "_collections_abc.data.json": [WILL_ERROR],
            "sre_parse.data.json": [WILL_ERROR],
            "email": {
                "header.meta.json": [WILL_ERROR],
                "charset.meta.json": [WILL_ERROR],
                "_policybase.meta.json": [WILL_ERROR],
                "message.data.json": [WILL_ERROR],
                "message.meta.json": [WILL_ERROR],
                "charset.data.json": [WILL_ERROR],
                "_policybase.data.json": [WILL_ERROR],
                "header.data.json": [WILL_ERROR],
                "errors.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "policy.data.json": [WILL_ERROR],
                "contentmanager.data.json": [WILL_ERROR],
                "contentmanager.meta.json": [WILL_ERROR],
                "policy.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "errors.meta.json": [WILL_ERROR],
            },
            "conf.data.json": [WILL_ERROR],
            "sre_compile.data.json": [WILL_ERROR],
            "io.meta.json": [WILL_ERROR],
            "codecs.meta.json": [WILL_ERROR],
            "typing_extensions.data.json": [WILL_ERROR],
            "pathlib.meta.json": [WILL_ERROR],
        },
        ".gitignore": ["# Automatically created by mypy", "*"],
        "3.8": {
            "atexit.meta.json": [WILL_ERROR],
            "datetime.data.json": [WILL_ERROR],
            "socket.meta.json": [WILL_ERROR],
            "ssl.data.json": [WILL_ERROR],
            "configparser.data.json": [WILL_ERROR],
            "packaging": {
                "tags.data.json": [WILL_ERROR],
                "_manylinux.data.json": [WILL_ERROR],
                "_elffile.data.json": [WILL_ERROR],
                "_structures.meta.json": [WILL_ERROR],
                "markers.data.json": [WILL_ERROR],
                "version.data.json": [WILL_ERROR],
                "_structures.data.json": [WILL_ERROR],
                "markers.meta.json": [WILL_ERROR],
                "version.meta.json": [WILL_ERROR],
                "_elffile.meta.json": [WILL_ERROR],
                "_manylinux.meta.json": [WILL_ERROR],
                "tags.meta.json": [WILL_ERROR],
                "_parser.meta.json": [WILL_ERROR],
                "specifiers.data.json": [WILL_ERROR],
                "utils.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "_tokenizer.data.json": [WILL_ERROR],
                "requirements.meta.json": [WILL_ERROR],
                "_musllinux.meta.json": [WILL_ERROR],
                "_musllinux.data.json": [WILL_ERROR],
                "requirements.data.json": [WILL_ERROR],
                "utils.data.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "_tokenizer.meta.json": [WILL_ERROR],
                "_parser.data.json": [WILL_ERROR],
                "specifiers.meta.json": [WILL_ERROR],
            },
            "platform.meta.json": [WILL_ERROR],
            "difflib.meta.json": [WILL_ERROR],
            "builtins.meta.json": [WILL_ERROR],
            "zlib.meta.json": [WILL_ERROR],
            "ctypes": {
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "contextvars.data.json": [WILL_ERROR],
            "time.data.json": [WILL_ERROR],
            "token.meta.json": [WILL_ERROR],
            "decimal.data.json": [WILL_ERROR],
            "markupsafe": {
                "_speedups.data.json": [WILL_ERROR],
                "_speedups.meta.json": [WILL_ERROR],
                "_native.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "_native.data.json": [WILL_ERROR],
            },
            "unittest": {
                "suite.data.json": [WILL_ERROR],
                "async_case.data.json": [WILL_ERROR],
                "loader.meta.json": [WILL_ERROR],
                "main.data.json": [WILL_ERROR],
                "case.data.json": [WILL_ERROR],
                "case.meta.json": [WILL_ERROR],
                "main.meta.json": [WILL_ERROR],
                "loader.data.json": [WILL_ERROR],
                "async_case.meta.json": [WILL_ERROR],
                "suite.meta.json": [WILL_ERROR],
                "result.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "runner.data.json": [WILL_ERROR],
                "signals.meta.json": [WILL_ERROR],
                "signals.data.json": [WILL_ERROR],
                "runner.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "result.meta.json": [WILL_ERROR],
            },
            "opcode.meta.json": [WILL_ERROR],
            "genericpath.meta.json": [WILL_ERROR],
            "_weakrefset.data.json": [WILL_ERROR],
            "shlex.meta.json": [WILL_ERROR],
            "hashlib.meta.json": [WILL_ERROR],
            "tarfile.data.json": [WILL_ERROR],
            "fractions.data.json": [WILL_ERROR],
            "textwrap.data.json": [WILL_ERROR],
            "enum.meta.json": [WILL_ERROR],
            "_ctypes.meta.json": [WILL_ERROR],
            "abc.meta.json": [WILL_ERROR],
            "traceback.meta.json": [WILL_ERROR],
            "random.data.json": [WILL_ERROR],
            "subprocess.meta.json": [WILL_ERROR],
            "itertools.meta.json": [WILL_ERROR],
            "dataclasses.data.json": [WILL_ERROR],
            "typing.data.json": [WILL_ERROR],
            "_heapq.data.json": [WILL_ERROR],
            "gc.data.json": [WILL_ERROR],
            "_decimal.data.json": [WILL_ERROR],
            "base64.meta.json": [WILL_ERROR],
            "pdb.data.json": [WILL_ERROR],
            "queue.meta.json": [WILL_ERROR],
            "_bisect.meta.json": [WILL_ERROR],
            "_locale.meta.json": [WILL_ERROR],
            "dis.meta.json": [WILL_ERROR],
            "object_colors": {
                "_version.data.json": [WILL_ERROR],
                "_version.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "pytest": {
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "_codecs.meta.json": [WILL_ERROR],
            "glob.meta.json": [WILL_ERROR],
            "posixpath.data.json": [WILL_ERROR],
            "gettext.meta.json": [WILL_ERROR],
            "errno.meta.json": [WILL_ERROR],
            "argparse.data.json": [WILL_ERROR],
            "contextlib.meta.json": [WILL_ERROR],
            "shutil.meta.json": [WILL_ERROR],
            "zipimport.data.json": [WILL_ERROR],
            "termios.data.json": [WILL_ERROR],
            "_codecs.data.json": [WILL_ERROR],
            "jinja2": {
                "compiler.meta.json": [WILL_ERROR],
                "visitor.data.json": [WILL_ERROR],
                "bccache.data.json": [WILL_ERROR],
                "optimizer.meta.json": [WILL_ERROR],
                "loaders.data.json": [WILL_ERROR],
                "async_utils.meta.json": [WILL_ERROR],
                "filters.data.json": [WILL_ERROR],
                "runtime.data.json": [WILL_ERROR],
                "sandbox.meta.json": [WILL_ERROR],
                "parser.data.json": [WILL_ERROR],
                "nodes.meta.json": [WILL_ERROR],
                "tests.meta.json": [WILL_ERROR],
                "tests.data.json": [WILL_ERROR],
                "parser.meta.json": [WILL_ERROR],
                "nodes.data.json": [WILL_ERROR],
                "filters.meta.json": [WILL_ERROR],
                "async_utils.data.json": [WILL_ERROR],
                "runtime.meta.json": [WILL_ERROR],
                "sandbox.data.json": [WILL_ERROR],
                "bccache.meta.json": [WILL_ERROR],
                "optimizer.data.json": [WILL_ERROR],
                "loaders.meta.json": [WILL_ERROR],
                "compiler.data.json": [WILL_ERROR],
                "visitor.meta.json": [WILL_ERROR],
                "defaults.meta.json": [WILL_ERROR],
                "utils.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "exceptions.meta.json": [WILL_ERROR],
                "lexer.meta.json": [WILL_ERROR],
                "idtracking.meta.json": [WILL_ERROR],
                "environment.data.json": [WILL_ERROR],
                "ext.meta.json": [WILL_ERROR],
                "_identifier.meta.json": [WILL_ERROR],
                "debug.data.json": [WILL_ERROR],
                "_identifier.data.json": [WILL_ERROR],
                "debug.meta.json": [WILL_ERROR],
                "environment.meta.json": [WILL_ERROR],
                "ext.data.json": [WILL_ERROR],
                "exceptions.data.json": [WILL_ERROR],
                "lexer.data.json": [WILL_ERROR],
                "idtracking.data.json": [WILL_ERROR],
                "utils.data.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "defaults.data.json": [WILL_ERROR],
            },
            "glob.data.json": [WILL_ERROR],
            "gettext.data.json": [WILL_ERROR],
            "posixpath.meta.json": [WILL_ERROR],
            "contextlib.data.json": [WILL_ERROR],
            "shutil.data.json": [WILL_ERROR],
            "argparse.meta.json": [WILL_ERROR],
            "errno.data.json": [WILL_ERROR],
            "termios.meta.json": [WILL_ERROR],
            "zipimport.meta.json": [WILL_ERROR],
            "_bisect.data.json": [WILL_ERROR],
            "_locale.data.json": [WILL_ERROR],
            "dis.data.json": [WILL_ERROR],
            "multiprocessing": {
                "queues.meta.json": [WILL_ERROR],
                "process.meta.json": [WILL_ERROR],
                "reduction.data.json": [WILL_ERROR],
                "shared_memory.meta.json": [WILL_ERROR],
                "pool.meta.json": [WILL_ERROR],
                "managers.meta.json": [WILL_ERROR],
                "context.data.json": [WILL_ERROR],
                "popen_spawn_posix.data.json": [WILL_ERROR],
                "popen_fork.data.json": [WILL_ERROR],
                "popen_fork.meta.json": [WILL_ERROR],
                "popen_spawn_posix.meta.json": [WILL_ERROR],
                "context.meta.json": [WILL_ERROR],
                "managers.data.json": [WILL_ERROR],
                "pool.data.json": [WILL_ERROR],
                "queues.data.json": [WILL_ERROR],
                "process.data.json": [WILL_ERROR],
                "reduction.meta.json": [WILL_ERROR],
                "shared_memory.data.json": [WILL_ERROR],
                "connection.data.json": [WILL_ERROR],
                "spawn.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "util.meta.json": [WILL_ERROR],
                "popen_spawn_win32.data.json": [WILL_ERROR],
                "synchronize.data.json": [WILL_ERROR],
                "sharedctypes.meta.json": [WILL_ERROR],
                "popen_forkserver.meta.json": [WILL_ERROR],
                "popen_forkserver.data.json": [WILL_ERROR],
                "popen_spawn_win32.meta.json": [WILL_ERROR],
                "sharedctypes.data.json": [WILL_ERROR],
                "synchronize.meta.json": [WILL_ERROR],
                "util.data.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "spawn.meta.json": [WILL_ERROR],
                "connection.meta.json": [WILL_ERROR],
            },
            "templatest": {
                "_version.data.json": [WILL_ERROR],
                "_collections.data.json": [WILL_ERROR],
                "_abc.data.json": [WILL_ERROR],
                "_abc.meta.json": [WILL_ERROR],
                "_collections.meta.json": [WILL_ERROR],
                "_version.meta.json": [WILL_ERROR],
                "_objects.meta.json": [WILL_ERROR],
                "templates.meta.json": [WILL_ERROR],
                "utils.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "exceptions.meta.json": [WILL_ERROR],
                "exceptions.data.json": [WILL_ERROR],
                "utils.data.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "templates.data.json": [WILL_ERROR],
                "_objects.data.json": [WILL_ERROR],
            },
            "typing.meta.json": [WILL_ERROR],
            "_heapq.meta.json": [WILL_ERROR],
            "_decimal.meta.json": [WILL_ERROR],
            "gc.meta.json": [WILL_ERROR],
            "_typeshed": {
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "pathspec": {
                "pathspec.data.json": [WILL_ERROR],
                "pattern.data.json": [WILL_ERROR],
                "gitignore.data.json": [WILL_ERROR],
                "patterns": {
                    "__init__.meta.json": [WILL_ERROR],
                    "gitwildmatch.meta.json": [WILL_ERROR],
                    "gitwildmatch.data.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
                "gitignore.meta.json": [WILL_ERROR],
                "pattern.meta.json": [WILL_ERROR],
                "pathspec.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "util.meta.json": [WILL_ERROR],
                "_meta.meta.json": [WILL_ERROR],
                "_meta.data.json": [WILL_ERROR],
                "util.data.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "pdb.meta.json": [WILL_ERROR],
            "queue.data.json": [WILL_ERROR],
            "base64.data.json": [WILL_ERROR],
            "urllib": {
                "parse.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "parse.meta.json": [WILL_ERROR],
            },
            "abc.data.json": [WILL_ERROR],
            "itertools.data.json": [WILL_ERROR],
            "subprocess.data.json": [WILL_ERROR],
            "traceback.data.json": [WILL_ERROR],
            "random.meta.json": [WILL_ERROR],
            "dataclasses.meta.json": [WILL_ERROR],
            "tests": {
                "disable_test.meta.json": [WILL_ERROR],
                "disable_test.data.json": [WILL_ERROR],
                "_test.data.json": [WILL_ERROR],
                "conftest.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "misc_test.meta.json": [WILL_ERROR],
                "misc_test.data.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "conftest.data.json": [WILL_ERROR],
                "_test.meta.json": [WILL_ERROR],
            },
            "opcode.data.json": [WILL_ERROR],
            "genericpath.data.json": [WILL_ERROR],
            "decimal.meta.json": [WILL_ERROR],
            "hashlib.data.json": [WILL_ERROR],
            "shlex.data.json": [WILL_ERROR],
            "tarfile.meta.json": [WILL_ERROR],
            "_weakrefset.meta.json": [WILL_ERROR],
            "enum.data.json": [WILL_ERROR],
            "importlib_metadata": {
                "_itertools.data.json": [WILL_ERROR],
                "_adapters.data.json": [WILL_ERROR],
                "_collections.data.json": [WILL_ERROR],
                "compat": {
                    "py39.data.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                    "py39.meta.json": [WILL_ERROR],
                },
                "_text.meta.json": [WILL_ERROR],
                "_text.data.json": [WILL_ERROR],
                "_adapters.meta.json": [WILL_ERROR],
                "_collections.meta.json": [WILL_ERROR],
                "_itertools.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "_meta.meta.json": [WILL_ERROR],
                "_compat.data.json": [WILL_ERROR],
                "_functools.meta.json": [WILL_ERROR],
                "_functools.data.json": [WILL_ERROR],
                "_meta.data.json": [WILL_ERROR],
                "_compat.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "textwrap.meta.json": [WILL_ERROR],
            "fractions.meta.json": [WILL_ERROR],
            "_ctypes.data.json": [WILL_ERROR],
            "click": {
                "core.meta.json": [WILL_ERROR],
                "decorators.meta.json": [WILL_ERROR],
                "formatting.data.json": [WILL_ERROR],
                "parser.data.json": [WILL_ERROR],
                "globals.data.json": [WILL_ERROR],
                "globals.meta.json": [WILL_ERROR],
                "parser.meta.json": [WILL_ERROR],
                "formatting.meta.json": [WILL_ERROR],
                "decorators.data.json": [WILL_ERROR],
                "core.data.json": [WILL_ERROR],
                "termui.meta.json": [WILL_ERROR],
                "utils.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "exceptions.meta.json": [WILL_ERROR],
                "_termui_impl.data.json": [WILL_ERROR],
                "shell_completion.data.json": [WILL_ERROR],
                "_compat.data.json": [WILL_ERROR],
                "types.data.json": [WILL_ERROR],
                "_compat.meta.json": [WILL_ERROR],
                "types.meta.json": [WILL_ERROR],
                "shell_completion.meta.json": [WILL_ERROR],
                "exceptions.data.json": [WILL_ERROR],
                "_termui_impl.meta.json": [WILL_ERROR],
                "utils.data.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "termui.data.json": [WILL_ERROR],
            },
            "zlib.data.json": [WILL_ERROR],
            "builtins.data.json": [WILL_ERROR],
            "contextvars.meta.json": [WILL_ERROR],
            "time.meta.json": [WILL_ERROR],
            "@plugins_snapshot.json": [WILL_ERROR],
            "token.data.json": [WILL_ERROR],
            "html": {
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "platform.data.json": [WILL_ERROR],
            "difflib.data.json": [WILL_ERROR],
            "datetime.meta.json": [WILL_ERROR],
            "atexit.data.json": [WILL_ERROR],
            "socket.data.json": [WILL_ERROR],
            "ssl.meta.json": [WILL_ERROR],
            "exceptiongroup": {
                "_version.data.json": [WILL_ERROR],
                "_formatting.data.json": [WILL_ERROR],
                "_catch.meta.json": [WILL_ERROR],
                "_suppress.data.json": [WILL_ERROR],
                "_suppress.meta.json": [WILL_ERROR],
                "_catch.data.json": [WILL_ERROR],
                "_version.meta.json": [WILL_ERROR],
                "_formatting.meta.json": [WILL_ERROR],
                "_exceptions.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "_exceptions.data.json": [WILL_ERROR],
            },
            "configparser.meta.json": [WILL_ERROR],
            "pprint.meta.json": [WILL_ERROR],
            "sre_compile.meta.json": [WILL_ERROR],
            "selectors.meta.json": [WILL_ERROR],
            "tty.data.json": [WILL_ERROR],
            "io.data.json": [WILL_ERROR],
            "codecs.data.json": [WILL_ERROR],
            "warnings.meta.json": [WILL_ERROR],
            "pathlib.data.json": [WILL_ERROR],
            "typing_extensions.meta.json": [WILL_ERROR],
            "_warnings.meta.json": [WILL_ERROR],
            "tokenize.data.json": [WILL_ERROR],
            "ast.data.json": [WILL_ERROR],
            "babel": {
                "core.meta.json": [WILL_ERROR],
                "plural.meta.json": [WILL_ERROR],
                "messages": {
                    "catalog.meta.json": [WILL_ERROR],
                    "pofile.data.json": [WILL_ERROR],
                    "pofile.meta.json": [WILL_ERROR],
                    "catalog.data.json": [WILL_ERROR],
                    "mofile.meta.json": [WILL_ERROR],
                    "plurals.meta.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "checkers.data.json": [WILL_ERROR],
                    "checkers.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                    "plurals.data.json": [WILL_ERROR],
                    "mofile.data.json": [WILL_ERROR],
                },
                "plural.data.json": [WILL_ERROR],
                "localtime": {
                    "_fallback.meta.json": [WILL_ERROR],
                    "_fallback.data.json": [WILL_ERROR],
                    "_helpers.meta.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "_unix.data.json": [WILL_ERROR],
                    "_unix.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                    "_helpers.data.json": [WILL_ERROR],
                },
                "core.data.json": [WILL_ERROR],
                "localedata.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "dates.meta.json": [WILL_ERROR],
                "util.meta.json": [WILL_ERROR],
                "util.data.json": [WILL_ERROR],
                "dates.data.json": [WILL_ERROR],
                "localedata.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "threading.data.json": [WILL_ERROR],
            "bisect.data.json": [WILL_ERROR],
            "copy.data.json": [WILL_ERROR],
            "functools.data.json": [WILL_ERROR],
            "tomli": {
                "_types.data.json": [WILL_ERROR],
                "_types.meta.json": [WILL_ERROR],
                "_parser.meta.json": [WILL_ERROR],
                "_re.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "_re.meta.json": [WILL_ERROR],
                "_parser.data.json": [WILL_ERROR],
            },
            "locale.data.json": [WILL_ERROR],
            "unicodedata.data.json": [WILL_ERROR],
            "_ast.meta.json": [WILL_ERROR],
            "weakref.data.json": [WILL_ERROR],
            "reprlib.meta.json": [WILL_ERROR],
            "sre_parse.meta.json": [WILL_ERROR],
            "sys": {
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "msvcrt.meta.json": [WILL_ERROR],
            "keyword.data.json": [WILL_ERROR],
            "_collections_abc.meta.json": [WILL_ERROR],
            "json": {
                "decoder.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "encoder.data.json": [WILL_ERROR],
                "encoder.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "decoder.meta.json": [WILL_ERROR],
            },
            "bz2.meta.json": [WILL_ERROR],
            "docsig": {
                "_hooks.data.json": [WILL_ERROR],
                "_version.data.json": [WILL_ERROR],
                "_stub.meta.json": [WILL_ERROR],
                "_display.data.json": [WILL_ERROR],
                "_core.meta.json": [WILL_ERROR],
                "__main__.data.json": [WILL_ERROR],
                "_config.meta.json": [WILL_ERROR],
                "_utils.meta.json": [WILL_ERROR],
                "_message.data.json": [WILL_ERROR],
                "messages.meta.json": [WILL_ERROR],
                "_decorators.meta.json": [WILL_ERROR],
                "_main.data.json": [WILL_ERROR],
                "_main.meta.json": [WILL_ERROR],
                "_decorators.data.json": [WILL_ERROR],
                "messages.data.json": [WILL_ERROR],
                "_utils.data.json": [WILL_ERROR],
                "_message.meta.json": [WILL_ERROR],
                "__main__.meta.json": [WILL_ERROR],
                "_config.data.json": [WILL_ERROR],
                "_core.data.json": [WILL_ERROR],
                "_stub.data.json": [WILL_ERROR],
                "_display.meta.json": [WILL_ERROR],
                "_version.meta.json": [WILL_ERROR],
                "_hooks.meta.json": [WILL_ERROR],
                "_directives.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "_module.data.json": [WILL_ERROR],
                "_report.data.json": [WILL_ERROR],
                "_report.meta.json": [WILL_ERROR],
                "_module.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "_directives.meta.json": [WILL_ERROR],
            },
            "math.meta.json": [WILL_ERROR],
            "heapq.data.json": [WILL_ERROR],
            "doctest.data.json": [WILL_ERROR],
            "__future__.meta.json": [WILL_ERROR],
            "string.data.json": [WILL_ERROR],
            "tempfile.meta.json": [WILL_ERROR],
            "gzip.meta.json": [WILL_ERROR],
            "uuid.data.json": [WILL_ERROR],
            "_random.meta.json": [WILL_ERROR],
            "http": {
                "__init__.meta.json": [WILL_ERROR],
                "client.data.json": [WILL_ERROR],
                "client.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "signal.meta.json": [WILL_ERROR],
            "sphinx": {
                "directives": {
                    "__init__.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
                "theming.meta.json": [WILL_ERROR],
                "parsers.data.json": [WILL_ERROR],
                "events.meta.json": [WILL_ERROR],
                "addnodes.data.json": [WILL_ERROR],
                "extension.meta.json": [WILL_ERROR],
                "jinja2glue.data.json": [WILL_ERROR],
                "domains": {
                    "cpp.data.json": [WILL_ERROR],
                    "python.data.json": [WILL_ERROR],
                    "index.meta.json": [WILL_ERROR],
                    "changeset.meta.json": [WILL_ERROR],
                    "changeset.data.json": [WILL_ERROR],
                    "index.data.json": [WILL_ERROR],
                    "python.meta.json": [WILL_ERROR],
                    "cpp.meta.json": [WILL_ERROR],
                    "std.data.json": [WILL_ERROR],
                    "javascript.meta.json": [WILL_ERROR],
                    "c.data.json": [WILL_ERROR],
                    "math.meta.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "rst.data.json": [WILL_ERROR],
                    "citation.data.json": [WILL_ERROR],
                    "citation.meta.json": [WILL_ERROR],
                    "rst.meta.json": [WILL_ERROR],
                    "c.meta.json": [WILL_ERROR],
                    "math.data.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                    "std.meta.json": [WILL_ERROR],
                    "javascript.data.json": [WILL_ERROR],
                },
                "locale": {
                    "__init__.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
                "highlighting.meta.json": [WILL_ERROR],
                "project.meta.json": [WILL_ERROR],
                "versioning.data.json": [WILL_ERROR],
                "writers": {
                    "html5.meta.json": [WILL_ERROR],
                    "latex.meta.json": [WILL_ERROR],
                    "html5.data.json": [WILL_ERROR],
                    "latex.data.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "html.data.json": [WILL_ERROR],
                    "html.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
                "util": {
                    "tags.data.json": [WILL_ERROR],
                    "logging.data.json": [WILL_ERROR],
                    "i18n.data.json": [WILL_ERROR],
                    "http_date.meta.json": [WILL_ERROR],
                    "docutils.meta.json": [WILL_ERROR],
                    "typing.data.json": [WILL_ERROR],
                    "nodes.meta.json": [WILL_ERROR],
                    "display.data.json": [WILL_ERROR],
                    "display.meta.json": [WILL_ERROR],
                    "nodes.data.json": [WILL_ERROR],
                    "typing.meta.json": [WILL_ERROR],
                    "http_date.data.json": [WILL_ERROR],
                    "docutils.data.json": [WILL_ERROR],
                    "i18n.meta.json": [WILL_ERROR],
                    "tags.meta.json": [WILL_ERROR],
                    "logging.meta.json": [WILL_ERROR],
                    "inventory.meta.json": [WILL_ERROR],
                    "docfields.data.json": [WILL_ERROR],
                    "console.data.json": [WILL_ERROR],
                    "cfamily.meta.json": [WILL_ERROR],
                    "parallel.data.json": [WILL_ERROR],
                    "template.meta.json": [WILL_ERROR],
                    "matching.meta.json": [WILL_ERROR],
                    "math.meta.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "exceptions.meta.json": [WILL_ERROR],
                    "images.meta.json": [WILL_ERROR],
                    "texescape.meta.json": [WILL_ERROR],
                    "rst.data.json": [WILL_ERROR],
                    "fileutil.meta.json": [WILL_ERROR],
                    "docstrings.meta.json": [WILL_ERROR],
                    "osutil.meta.json": [WILL_ERROR],
                    "build_phase.meta.json": [WILL_ERROR],
                    "inspect.data.json": [WILL_ERROR],
                    "build_phase.data.json": [WILL_ERROR],
                    "inspect.meta.json": [WILL_ERROR],
                    "osutil.data.json": [WILL_ERROR],
                    "exceptions.data.json": [WILL_ERROR],
                    "texescape.data.json": [WILL_ERROR],
                    "images.data.json": [WILL_ERROR],
                    "fileutil.data.json": [WILL_ERROR],
                    "rst.meta.json": [WILL_ERROR],
                    "docstrings.data.json": [WILL_ERROR],
                    "template.data.json": [WILL_ERROR],
                    "math.data.json": [WILL_ERROR],
                    "matching.data.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                    "cfamily.data.json": [WILL_ERROR],
                    "parallel.meta.json": [WILL_ERROR],
                    "console.meta.json": [WILL_ERROR],
                    "inventory.data.json": [WILL_ERROR],
                    "docfields.meta.json": [WILL_ERROR],
                },
                "builders": {
                    "gettext.meta.json": [WILL_ERROR],
                    "gettext.data.json": [WILL_ERROR],
                    "latex": {
                        "theming.meta.json": [WILL_ERROR],
                        "nodes.meta.json": [WILL_ERROR],
                        "nodes.data.json": [WILL_ERROR],
                        "theming.data.json": [WILL_ERROR],
                        "constants.data.json": [WILL_ERROR],
                        "__init__.meta.json": [WILL_ERROR],
                        "util.meta.json": [WILL_ERROR],
                        "util.data.json": [WILL_ERROR],
                        "__init__.data.json": [WILL_ERROR],
                        "constants.meta.json": [WILL_ERROR],
                    },
                    "html": {
                        "__init__.meta.json": [WILL_ERROR],
                        "__init__.data.json": [WILL_ERROR],
                    },
                    "__init__.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
                "versioning.meta.json": [WILL_ERROR],
                "highlighting.data.json": [WILL_ERROR],
                "ext": {
                    "autodoc": {
                        "importer.meta.json": [WILL_ERROR],
                        "directive.meta.json": [WILL_ERROR],
                        "mock.meta.json": [WILL_ERROR],
                        "mock.data.json": [WILL_ERROR],
                        "importer.data.json": [WILL_ERROR],
                        "directive.data.json": [WILL_ERROR],
                        "__init__.meta.json": [WILL_ERROR],
                        "__init__.data.json": [WILL_ERROR],
                    },
                    "duration.data.json": [WILL_ERROR],
                    "duration.meta.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "todo.data.json": [WILL_ERROR],
                    "napoleon": {
                        "docstring.meta.json": [WILL_ERROR],
                        "docstring.data.json": [WILL_ERROR],
                        "__init__.meta.json": [WILL_ERROR],
                        "__init__.data.json": [WILL_ERROR],
                    },
                    "todo.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
                "project.data.json": [WILL_ERROR],
                "pycode": {
                    "parser.data.json": [WILL_ERROR],
                    "parser.meta.json": [WILL_ERROR],
                    "ast.data.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                    "ast.meta.json": [WILL_ERROR],
                },
                "addnodes.meta.json": [WILL_ERROR],
                "jinja2glue.meta.json": [WILL_ERROR],
                "extension.data.json": [WILL_ERROR],
                "events.data.json": [WILL_ERROR],
                "parsers.meta.json": [WILL_ERROR],
                "theming.data.json": [WILL_ERROR],
                "search": {
                    "en.meta.json": [WILL_ERROR],
                    "en.data.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
                "io.data.json": [WILL_ERROR],
                "testing": {
                    "path.data.json": [WILL_ERROR],
                    "path.meta.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
                "errors.data.json": [WILL_ERROR],
                "transforms": {
                    "i18n.data.json": [WILL_ERROR],
                    "references.meta.json": [WILL_ERROR],
                    "references.data.json": [WILL_ERROR],
                    "i18n.meta.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "post_transforms": {
                        "__init__.meta.json": [WILL_ERROR],
                        "__init__.data.json": [WILL_ERROR],
                    },
                    "__init__.data.json": [WILL_ERROR],
                },
                "registry.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "pygments_styles.data.json": [WILL_ERROR],
                "config.data.json": [WILL_ERROR],
                "application.data.json": [WILL_ERROR],
                "deprecation.data.json": [WILL_ERROR],
                "roles.data.json": [WILL_ERROR],
                "environment": {
                    "collectors": {
                        "__init__.meta.json": [WILL_ERROR],
                        "__init__.data.json": [WILL_ERROR],
                    },
                    "adapters": {
                        "toctree.meta.json": [WILL_ERROR],
                        "toctree.data.json": [WILL_ERROR],
                        "__init__.meta.json": [WILL_ERROR],
                        "indexentries.data.json": [WILL_ERROR],
                        "asset.meta.json": [WILL_ERROR],
                        "asset.data.json": [WILL_ERROR],
                        "indexentries.meta.json": [WILL_ERROR],
                        "__init__.data.json": [WILL_ERROR],
                    },
                    "__init__.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
                "deprecation.meta.json": [WILL_ERROR],
                "roles.meta.json": [WILL_ERROR],
                "application.meta.json": [WILL_ERROR],
                "config.meta.json": [WILL_ERROR],
                "pygments_styles.meta.json": [WILL_ERROR],
                "registry.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "errors.meta.json": [WILL_ERROR],
                "io.meta.json": [WILL_ERROR],
            },
            "filecmp.data.json": [WILL_ERROR],
            "_weakref.data.json": [WILL_ERROR],
            "struct.meta.json": [WILL_ERROR],
            "sre_constants.meta.json": [WILL_ERROR],
            "_csv.data.json": [WILL_ERROR],
            "marshal.meta.json": [WILL_ERROR],
            "concurrent": {
                "futures": {
                    "_base.data.json": [WILL_ERROR],
                    "process.meta.json": [WILL_ERROR],
                    "thread.meta.json": [WILL_ERROR],
                    "thread.data.json": [WILL_ERROR],
                    "_base.meta.json": [WILL_ERROR],
                    "process.data.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "_stat.meta.json": [WILL_ERROR],
            "array.meta.json": [WILL_ERROR],
            "cmd.data.json": [WILL_ERROR],
            "_thread.data.json": [WILL_ERROR],
            "fnmatch.meta.json": [WILL_ERROR],
            "pickle.meta.json": [WILL_ERROR],
            "inspect.data.json": [WILL_ERROR],
            "_compression.meta.json": [WILL_ERROR],
            "_operator.data.json": [WILL_ERROR],
            "sysconfig.meta.json": [WILL_ERROR],
            "operator.data.json": [WILL_ERROR],
            "types.data.json": [WILL_ERROR],
            "pluggy": {
                "_hooks.data.json": [WILL_ERROR],
                "_version.data.json": [WILL_ERROR],
                "_manager.data.json": [WILL_ERROR],
                "_tracing.data.json": [WILL_ERROR],
                "_result.meta.json": [WILL_ERROR],
                "_result.data.json": [WILL_ERROR],
                "_manager.meta.json": [WILL_ERROR],
                "_tracing.meta.json": [WILL_ERROR],
                "_version.meta.json": [WILL_ERROR],
                "_hooks.meta.json": [WILL_ERROR],
                "_warnings.meta.json": [WILL_ERROR],
                "_callers.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "_callers.data.json": [WILL_ERROR],
                "_warnings.data.json": [WILL_ERROR],
            },
            "zipfile.data.json": [WILL_ERROR],
            "arcon": {
                "_version.data.json": [WILL_ERROR],
                "_version.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "bdb.data.json": [WILL_ERROR],
            "_socket.data.json": [WILL_ERROR],
            "stat.meta.json": [WILL_ERROR],
            "copyreg.data.json": [WILL_ERROR],
            "numbers.data.json": [WILL_ERROR],
            "re.meta.json": [WILL_ERROR],
            "csv.meta.json": [WILL_ERROR],
            "_socket.meta.json": [WILL_ERROR],
            "bdb.meta.json": [WILL_ERROR],
            "os": {
                "path.data.json": [WILL_ERROR],
                "path.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "copyreg.meta.json": [WILL_ERROR],
            "stat.data.json": [WILL_ERROR],
            "numbers.meta.json": [WILL_ERROR],
            "re.data.json": [WILL_ERROR],
            "csv.data.json": [WILL_ERROR],
            "_compression.data.json": [WILL_ERROR],
            "inspect.meta.json": [WILL_ERROR],
            "pickle.data.json": [WILL_ERROR],
            "operator.meta.json": [WILL_ERROR],
            "_operator.meta.json": [WILL_ERROR],
            "sysconfig.data.json": [WILL_ERROR],
            "zipfile.meta.json": [WILL_ERROR],
            "types.meta.json": [WILL_ERROR],
            "marshal.data.json": [WILL_ERROR],
            "_stat.data.json": [WILL_ERROR],
            "importlib": {
                "abc.meta.json": [WILL_ERROR],
                "machinery.data.json": [WILL_ERROR],
                "abc.data.json": [WILL_ERROR],
                "machinery.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "util.meta.json": [WILL_ERROR],
                "util.data.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "metadata": {
                    "__init__.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
            },
            "_thread.meta.json": [WILL_ERROR],
            "fnmatch.data.json": [WILL_ERROR],
            "cmd.meta.json": [WILL_ERROR],
            "array.data.json": [WILL_ERROR],
            "signal.data.json": [WILL_ERROR],
            "filecmp.meta.json": [WILL_ERROR],
            "_weakref.meta.json": [WILL_ERROR],
            "sre_constants.data.json": [WILL_ERROR],
            "struct.data.json": [WILL_ERROR],
            "collections": {
                "abc.meta.json": [WILL_ERROR],
                "abc.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "_csv.meta.json": [WILL_ERROR],
            "iniconfig": {
                "_parse.data.json": [WILL_ERROR],
                "_parse.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "exceptions.meta.json": [WILL_ERROR],
                "exceptions.data.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "math.data.json": [WILL_ERROR],
            "__future__.data.json": [WILL_ERROR],
            "doctest.meta.json": [WILL_ERROR],
            "heapq.meta.json": [WILL_ERROR],
            "_random.data.json": [WILL_ERROR],
            "uuid.meta.json": [WILL_ERROR],
            "tempfile.data.json": [WILL_ERROR],
            "string.meta.json": [WILL_ERROR],
            "gzip.data.json": [WILL_ERROR],
            "reprlib.data.json": [WILL_ERROR],
            "weakref.meta.json": [WILL_ERROR],
            "asyncio": {
                "queues.meta.json": [WILL_ERROR],
                "events.meta.json": [WILL_ERROR],
                "transports.data.json": [WILL_ERROR],
                "subprocess.meta.json": [WILL_ERROR],
                "tasks.data.json": [WILL_ERROR],
                "protocols.meta.json": [WILL_ERROR],
                "selector_events.meta.json": [WILL_ERROR],
                "selector_events.data.json": [WILL_ERROR],
                "subprocess.data.json": [WILL_ERROR],
                "tasks.meta.json": [WILL_ERROR],
                "protocols.data.json": [WILL_ERROR],
                "events.data.json": [WILL_ERROR],
                "transports.meta.json": [WILL_ERROR],
                "queues.data.json": [WILL_ERROR],
                "futures.data.json": [WILL_ERROR],
                "streams.meta.json": [WILL_ERROR],
                "runners.data.json": [WILL_ERROR],
                "unix_events.meta.json": [WILL_ERROR],
                "locks.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "coroutines.meta.json": [WILL_ERROR],
                "exceptions.meta.json": [WILL_ERROR],
                "base_events.data.json": [WILL_ERROR],
                "base_events.meta.json": [WILL_ERROR],
                "coroutines.data.json": [WILL_ERROR],
                "exceptions.data.json": [WILL_ERROR],
                "unix_events.data.json": [WILL_ERROR],
                "locks.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "streams.data.json": [WILL_ERROR],
                "runners.meta.json": [WILL_ERROR],
                "futures.meta.json": [WILL_ERROR],
            },
            "unicodedata.meta.json": [WILL_ERROR],
            "_ast.data.json": [WILL_ERROR],
            "keyword.meta.json": [WILL_ERROR],
            "_collections_abc.data.json": [WILL_ERROR],
            "logging": {
                "handlers.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "handlers.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
            },
            "sre_parse.data.json": [WILL_ERROR],
            "msvcrt.data.json": [WILL_ERROR],
            "bz2.data.json": [WILL_ERROR],
            "email": {
                "header.meta.json": [WILL_ERROR],
                "charset.meta.json": [WILL_ERROR],
                "message.data.json": [WILL_ERROR],
                "message.meta.json": [WILL_ERROR],
                "charset.data.json": [WILL_ERROR],
                "header.data.json": [WILL_ERROR],
                "errors.data.json": [WILL_ERROR],
                "utils.meta.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "policy.data.json": [WILL_ERROR],
                "contentmanager.data.json": [WILL_ERROR],
                "contentmanager.meta.json": [WILL_ERROR],
                "policy.meta.json": [WILL_ERROR],
                "utils.data.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "errors.meta.json": [WILL_ERROR],
            },
            "ast.meta.json": [WILL_ERROR],
            "tokenize.meta.json": [WILL_ERROR],
            "threading.meta.json": [WILL_ERROR],
            "bisect.meta.json": [WILL_ERROR],
            "copy.meta.json": [WILL_ERROR],
            "locale.meta.json": [WILL_ERROR],
            "functools.meta.json": [WILL_ERROR],
            "_pytest": {
                "_version.data.json": [WILL_ERROR],
                "scope.meta.json": [WILL_ERROR],
                "compat.meta.json": [WILL_ERROR],
                "logging.data.json": [WILL_ERROR],
                "python.data.json": [WILL_ERROR],
                "capture.data.json": [WILL_ERROR],
                "python_api.meta.json": [WILL_ERROR],
                "_argcomplete.data.json": [WILL_ERROR],
                "outcomes.data.json": [WILL_ERROR],
                "terminal.data.json": [WILL_ERROR],
                "timing.data.json": [WILL_ERROR],
                "main.data.json": [WILL_ERROR],
                "hookspec.meta.json": [WILL_ERROR],
                "deprecated.data.json": [WILL_ERROR],
                "recwarn.data.json": [WILL_ERROR],
                "nodes.meta.json": [WILL_ERROR],
                "tmpdir.data.json": [WILL_ERROR],
                "monkeypatch.data.json": [WILL_ERROR],
                "config": {
                    "compat.meta.json": [WILL_ERROR],
                    "argparsing.meta.json": [WILL_ERROR],
                    "argparsing.data.json": [WILL_ERROR],
                    "compat.data.json": [WILL_ERROR],
                    "findpaths.meta.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "exceptions.meta.json": [WILL_ERROR],
                    "exceptions.data.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                    "findpaths.data.json": [WILL_ERROR],
                },
                "helpconfig.data.json": [WILL_ERROR],
                "monkeypatch.meta.json": [WILL_ERROR],
                "helpconfig.meta.json": [WILL_ERROR],
                "recwarn.meta.json": [WILL_ERROR],
                "nodes.data.json": [WILL_ERROR],
                "tmpdir.meta.json": [WILL_ERROR],
                "main.meta.json": [WILL_ERROR],
                "deprecated.meta.json": [WILL_ERROR],
                "hookspec.data.json": [WILL_ERROR],
                "terminal.meta.json": [WILL_ERROR],
                "timing.meta.json": [WILL_ERROR],
                "python_api.data.json": [WILL_ERROR],
                "_argcomplete.meta.json": [WILL_ERROR],
                "outcomes.meta.json": [WILL_ERROR],
                "mark": {
                    "structures.meta.json": [WILL_ERROR],
                    "structures.data.json": [WILL_ERROR],
                    "expression.meta.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "expression.data.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                },
                "logging.meta.json": [WILL_ERROR],
                "python.meta.json": [WILL_ERROR],
                "capture.meta.json": [WILL_ERROR],
                "scope.data.json": [WILL_ERROR],
                "compat.data.json": [WILL_ERROR],
                "_code": {
                    "code.meta.json": [WILL_ERROR],
                    "code.data.json": [WILL_ERROR],
                    "source.meta.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                    "source.data.json": [WILL_ERROR],
                },
                "assertion": {
                    "rewrite.meta.json": [WILL_ERROR],
                    "rewrite.data.json": [WILL_ERROR],
                    "truncate.data.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "util.meta.json": [WILL_ERROR],
                    "util.data.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                    "truncate.meta.json": [WILL_ERROR],
                },
                "_version.meta.json": [WILL_ERROR],
                "warnings.meta.json": [WILL_ERROR],
                "pathlib.data.json": [WILL_ERROR],
                "freeze_support.data.json": [WILL_ERROR],
                "pytester_assertions.meta.json": [WILL_ERROR],
                "legacypath.data.json": [WILL_ERROR],
                "cacheprovider.data.json": [WILL_ERROR],
                "_io": {
                    "terminalwriter.meta.json": [WILL_ERROR],
                    "saferepr.meta.json": [WILL_ERROR],
                    "saferepr.data.json": [WILL_ERROR],
                    "terminalwriter.data.json": [WILL_ERROR],
                    "pprint.meta.json": [WILL_ERROR],
                    "wcwidth.meta.json": [WILL_ERROR],
                    "__init__.meta.json": [WILL_ERROR],
                    "wcwidth.data.json": [WILL_ERROR],
                    "__init__.data.json": [WILL_ERROR],
                    "pprint.data.json": [WILL_ERROR],
                },
                "reports.meta.json": [WILL_ERROR],
                "stash.meta.json": [WILL_ERROR],
                "doctest.data.json": [WILL_ERROR],
                "__init__.meta.json": [WILL_ERROR],
                "runner.data.json": [WILL_ERROR],
                "warning_types.data.json": [WILL_ERROR],
                "debugging.meta.json": [WILL_ERROR],
                "fixtures.data.json": [WILL_ERROR],
                "pytester.data.json": [WILL_ERROR],
                "fixtures.meta.json": [WILL_ERROR],
                "pytester.meta.json": [WILL_ERROR],
                "runner.meta.json": [WILL_ERROR],
                "warning_types.meta.json": [WILL_ERROR],
                "debugging.data.json": [WILL_ERROR],
                "cacheprovider.meta.json": [WILL_ERROR],
                "reports.data.json": [WILL_ERROR],
                "stash.data.json": [WILL_ERROR],
                "doctest.meta.json": [WILL_ERROR],
                "__init__.data.json": [WILL_ERROR],
                "pytester_assertions.data.json": [WILL_ERROR],
                "legacypath.meta.json": [WILL_ERROR],
                "freeze_support.meta.json": [WILL_ERROR],
                "pathlib.meta.json": [WILL_ERROR],
                "warnings.data.json": [WILL_ERROR],
            },
            "selectors.data.json": [WILL_ERROR],
            "pprint.data.json": [WILL_ERROR],
            "sre_compile.data.json": [WILL_ERROR],
            "io.meta.json": [WILL_ERROR],
            "tty.meta.json": [WILL_ERROR],
            "codecs.meta.json": [WILL_ERROR],
            "typing_extensions.data.json": [WILL_ERROR],
            "_warnings.data.json": [WILL_ERROR],
            "pathlib.meta.json": [WILL_ERROR],
            "warnings.data.json": [WILL_ERROR],
        },
    },
    ".gitignore": [
        "*build/",
        "*coverage*",
        "*venv",
        ".DS_Store",
        ".env",
        "__pycache__/",
        "dist/",
        "node_modules/",
    ],
    "package-lock.json": [WILL_ERROR],
    "package.json": [WILL_ERROR],
    "CONTRIBUTING.md": [WILL_ERROR],
    ".github": {
        "COMMIT_POLICY.md": [WILL_ERROR],
        "workflows": {
            "codeql-analysis.yml": [WILL_ERROR],
            "build.yaml": [WILL_ERROR],
        },
        "dependabot.yml": [WILL_ERROR],
    },
    "coverage.xml": [WILL_ERROR],
    "poetry.lock": [WILL_ERROR],
    "README.rst": [WILL_ERROR],
    ".git": {
        "HEAD": [WILL_ERROR],
    },
    ".idea": {
        "docsig.iml": [WILL_ERROR],
        "jsonSchemas.xml": [WILL_ERROR],
        "inspectionProfiles": {
            "profiles_settings.xml": [WILL_ERROR],
            "Project_Default.xml": [WILL_ERROR],
        },
        "codeStyles": {
            "Project.xml": [WILL_ERROR],
            "codeStyleConfig.xml": [WILL_ERROR],
        },
        "material_theme_project_new.xml": [WILL_ERROR],
        "vcs.xml": [WILL_ERROR],
        ".gitignore": [
            "/dataSources.local.xml",
            "/dataSources/",
            "/dictionaries",
            "/httpRequests/",
            "/shelf/",
            "/sonarlint/",
            "/tasks.xml",
            "/usage.statistics.xml",
            "/workspace.xml",
        ],
        "workspace.xml": [WILL_ERROR],
        "modules.xml": [WILL_ERROR],
        "watcherTasks.xml": [WILL_ERROR],
        "dictionaries": {
            "swhitlock.xml": [WILL_ERROR],
            "default_user.xml": [WILL_ERROR],
        },
        "misc.xml": [WILL_ERROR],
        "scopes": {
            "whitelist_py.xml": [WILL_ERROR],
            "bump2version.xml": [WILL_ERROR],
            "docs__themes_graphite_static.xml": [WILL_ERROR],
            "docs_conf.xml": [WILL_ERROR],
            "_prettierignore.xml": [WILL_ERROR],
            "docs_index.xml": [WILL_ERROR],
            "_pylintrc.xml": [WILL_ERROR],
        },
    },
}


@_templates.register
class _PParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FParamDocsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FParamSigS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FNoDocNoRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    pass
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _PNoParamsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function() -> None:
    """No params."""
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PUnderscoreParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, _) -> None:
    """Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FOutOfOrderS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PRetTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    :return: Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FRetTypeSigS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG501NoRetNoTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FNoRetDocsNoTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FRetDocsAttrTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> t.Optional[str]:
    """Proper docstring.

    :param param1: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FRetDocsNameTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> Optional[str]:
    """Proper docstring.

    :param param1: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG402OutOfOrderSingleErrorS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _FIncorrectDocS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> None:
    """Proper docstring.

    :param param1: Fails.
    :param: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG202ParamDocsSingleErrorS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG203ParamSigSingleErrorS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FSIG502RetTypeDocsSingleErrorS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FSIG503RetTypeSigSingleErrorS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FDupesSumS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[201].fstring(T)


@_templates.register
class _FIncorrectDocSumS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    :param param1: Fails.
    :param param1: Fails.
    :param param2: Fails.
    :param: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[303].fstring(T)


@_templates.register
class _PWArgsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    :param args: Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWArgsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    :param kwargs: Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Proper docstring.

    :param param1: Pass.
    :param param2: Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _MFailS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """

def function_2(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

def function_3(param1, param2, param3) -> None:
    """Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:10 in function_2
    {E[202].fstring(T)}
{PATH}:18 in function_3
    {E[203].fstring(T)}
"""


@_templates.register
class _FMethodWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Proper docstring.

        :param param1: Pass.
        :param param2: Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PClassSelfS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1) -> None:
        """Proper docstring.

        :param param1: Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FPropertyReturnsClassS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    @property
    def method(self) -> int:
        """Proper docstring."""
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PWKwargsKeyS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Proper docstring.

    :param param1: Passes
    :key kwarg1: Pass
    :keyword kwarg2: Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FKwargsOutOfOrderS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Proper docstring.

    :keyword kwarg1: Fail
    :keyword kwarg3: Fail
    :param param1: Fail
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PDualColonWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(attachments, sync, **kwargs) -> None:
    """Proper docstring.

    Note: Keyword args (dict) to pass to ``attachments``:

        See ``flask_mail.Message.attach``.

        * filename:     filename of attachment
        * content_type: file mimetype
        * data:         the raw file data

    :param attachments: Iterable of kwargs to construct attachment.
    :param sync: Don't thread if True: Defaults to False.
    :param kwargs: Keyword args to pass to ``Message``:
        See ``flask_mail.Message``.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _POnlyParamsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    """Proper docstring.

    :param reduce: :func:`~lsfiles.utils._Tree.reduce`
    :return: Tuple of `Path` objects or str repr.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PReturnAnyWArgsWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    """Proper docstring.

    :param args: Manipulate string(s).
    :key format: Return a string instead of a tuple if strings are
        passed as tuple.
    :return: Colored string or None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FMsgPoorIndentS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_post(
        id: int, version: t.Optional[int] = None, checkauthor: bool = True
) -> Post:
    """Get post by post's ID or abort with ``404: Not Found.``

    Standard behaviour would be to return None, so do not bypass
     silently.

     :param id: The post's ID.
     :param version: If provided populate session object with
        version.
     :param checkauthor: Rule whether to check for author ID.
     :return: Post's connection object.
    """
'''

    @property
    def expected(self) -> str:
        return E[401].fstring(T)


@_templates.register
class _FSIG302NoSpaceS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> None:
    """Proper docstring.

    :param param1:Passes.
    """
'''

    @property
    def expected(self) -> str:
        return E[302].fstring(T)


@_templates.register
class _PBinOpS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_index(index: int, seq: _t.Sequence[_T]) -> _T | None:
    """Fet index without throwing an error if index does not exist.

    :param index: Index to get.
    :param seq: Sequence object that can be indexed.
    :return: Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FBinOpReprS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_index(index: int) -> _T | None:
    """Get index without throwing an error if index does not exist.

    :return: Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PDoubleUnderscoreParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, __) -> None:
    """Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PUnderscoreArgsKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*_, **__) -> None:
    """Proper docstring."""
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FPropertyReturnsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Proper docstring."""
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PPropertyReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Proper docstring.

        :return: Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FHintMissingReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_post() -> Post:
    """Proper docstring.

     return: Post's connection object.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].hint or ""


@_templates.register
class _FOverriddenS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
import typing as _t

T = _t.TypeVar("T")

class MutableSet(_t.MutableSet[T]):
    """Set object to inherit from."""

    def __init__(self) -> None:
        self._set: _t.Set[T] = set()

    def add(self, value: T) -> None:
        self._set.add(value)

    def discard(self, value: T) -> None:
        self._set.discard(value)

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[T]:
        return self._set.__iter__()
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FNoDocRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function() -> int:
    pass
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _PInconsistentSpaceS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@pytest.fixture(name="main")
def fixture_main(monkeypatch) -> t.Callable[..., None]:
    """Function for passing mock ``main`` commandline arguments
    to package's main function.

    :param monkeypatch: ``pytest`` fixture for mocking attributes.
    :return:            Function for using this fixture.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FSIG501WRetQuestionS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring.

    :return: Does it?
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG501WORetQuestionS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring."""
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG404NES(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(arg, param2) -> None:
    """Docstring.

    :param param1: Not equal.
    :param para2: Not equal.
    """
'''

    @property
    def expected(self) -> str:
        return E[404].fstring(T)


@_templates.register
class _FMethodHeaderWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Proper docstring.

        :param param1: Pass.
        :param param2: Pass.
        """
'''

    @property
    def expected(self) -> str:
        return f"{PATH}:4 in Klass"


@_templates.register
class _PKWOnlyArgsWArgsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def docsig(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    """...

    :param path: Path(s) to check.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :return: Boolean value for whether there were any failures or not.
    """
'''

    @property
    def expected(self) -> str:
        return """"""


@_templates.register
class _FClassS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FPropertyReturnsTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    @property
    def method(self):
        """Proper docstring."""
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _PInitNoRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    :param param1: Fails.
    :param param2: Fails.
    """

    def __init__(self, param1, param2):
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PInitBadRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    :param param1: Fails.
    :param param2: Fails.
    """

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassRetNoneS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :return: Fails
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FSIG504S(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :return: Fails
    """

    def __init__(param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FProtectFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def _function(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FFuncPropS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(self) -> int:
    """Docstring.

    :param self: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PFuncPropReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(*_, **__) -> int:
    """Docstring.

    :return: Returncode.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def method(self):
    """Docstring.

    :param self: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FProtectNInitS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def __init__(param1, param2) -> None:
    pass
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _PStaticSelfS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @staticmethod
    def method(self, param1) -> None:
        """Proper docstring.

        :param self: Pass.
        :param param1: Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PClassNoSelfS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:

    # against convention but not up to this package to decide
    def method(no_self) -> None:
        """Docstring."""
        return None
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Proper docstring.

        :param param1: Pass.
        :param param2: Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FDundersS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class MutableSet:
    """Set object to inherit from."""

    def __init__(self) -> None:
        self._set: _t.Set[T] = set()

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[T]:
        return self._set.__iter__()
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FDundersParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def __dunder__(self, param1, param2) -> None:
        """...

        :param param1: Fails.
        :param param2: Fails.
        :param param3: Fails.
        """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG403S(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param) -> None:
    """Docstring.

    :param pram: Misspelled.
    """
'''

    @property
    def expected(self) -> str:
        return E[403].fstring(T)


@_templates.register
class _PParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
        param3 : int
            Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FParamDocsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FParamSigN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Not proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FNoDocNoRetN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function(param1, param2, param3) -> None:
    pass
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _PNoParamsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function() -> None:
    """No params."""
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PUnderscoreParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, _) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FOutOfOrderN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    Parameters
    ----------
        param2 : int
            Fails.
        param3 : int
            Fails.
        param1 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PRetTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
        param3 : int
            Passes.

    Returns
    -------
        int
            Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.

    Returns
    -------
        int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FRetTypeSigN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG501NoRetNoTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
        param3 : int
            Passes.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FNoRetDocsNoTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.

    Returns
    -------
        int
            :return: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FRetDocsAttrTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> t.Optional[str]:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FRetDocsNameTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> Optional[str]:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG402OutOfOrderSingleErrorN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Parameters
    ----------
        param2 : int
            Fails.
        param3 : int
            Fails.
        param1 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _FSIG202ParamDocsSingleErrorN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG203ParamSigSingleErrorN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Not proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FSIG502RetTypeDocsSingleErrorN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.

    Returns
    -------
    int
        :return: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FSIG503RetTypeSigSingleErrorN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FDupesSumN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[201].fstring(T)


@_templates.register
class _PWArgsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
        *args : int
            Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWArgsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
        **kwargs : int
            Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Pass.
        param2 : int
            Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _MFailN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Proper docstring.

    Parameters
    ----------
        param2 : int
            Fails.
        param3 : int
            Fails.
        param1 : int
            Fails.
    """

def function_2(param1, param2) -> None:
    """...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """

def function_3(param1, param2, param3) -> None:
    """Not proper docstring.

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:15 in function_2
    {E[202].fstring(T)}
{PATH}:28 in function_3
    {E[203].fstring(T)}
"""


@_templates.register
class _FMethodWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Proper docstring.

        Parameters
        ----------
            param1 : int
                Pass.
            param2 : int
                Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PClassSelfN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def method(self, param1) -> None:
        """Proper docstring.

        Parameters
        ----------
            param1 : int
                Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FPropertyReturnsClassN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def method(self) -> int:
        """Proper docstring."""
        return self._method
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PWKwargsKeyN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes
        **kwargs : int
            Passes
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FKwargsOutOfSectN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Proper docstring.

    **kwargs : int
        Passes

    Parameters
    ----------
        param1 : int Fail
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FKwargsOutOfOrderN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Proper docstring.

    Parameters
    ----------
        **kwargs : int
            Passes
        param1 : int
            Fail
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PDualColonWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(attachments, sync, **kwargs) -> None:
    """Proper docstring.

    Note: Keyword args (dict) to pass to ``attachments``:

        See ``flask_mail.Message.attach``.

        * filename:     filename of attachment
        * content_type: file mimetype
        * data:         the raw file data

    Parameters
    ----------
        attachments : int
            Iterable of kwargs to construct attachment.
        sync : int
            Don't thread if True: Defaults to False.
        **kwargs : int
            Keyword args to pass to ``Message``:
            See ``flask_mail.Message``.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _POnlyParamsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    """Proper docstring.

    Parameters
    ----------
        reduce : int
            :func:`~lsfiles.utils._Tree.reduce`

    Returns
    -------
        int
            Tuple of `Path` objects or str repr.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PReturnAnyWArgsWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    """Proper docstring.

    Parameters
    ----------
        *args : int
            Manipulate string(s).
        **kwargs : int
            Return a string instead of a tuple if strings are passed as tuple.

    Returns
    -------
        int
            Colored string or None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PBinOpN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_index(index: int, seq: _t.Sequence[_T]) -> _T | None:
    """Fet index without throwing an error if index does not exist.

    Parameters
    ----------
        index : int
            Index to get.
        seq : int
            Sequence object that can be indexed.

    Returns
    -------
        int
            Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FBinOpReprN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_index(index: int) -> _T | None:
    """Get index without throwing an error if index does not exist.

    Returns
    -------
        int
            Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PDoubleUnderscoreParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, __) -> None:
    """Proper docstring.

    Parameters
    ----------
        param1 : int
            Passes.
        param2 : int
            Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PUnderscoreArgsKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*_, **__) -> None:
    """Proper docstring."""
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FPropertyReturnsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Proper docstring."""
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PPropertyReturnN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Proper docstring.

        Returns
        -------
            int
                Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PPropertyReturnCachedN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @cached_property
    def function(*_, **__) -> int:
        """Proper docstring.

        Returns
        -------
            int
                Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PPropertyReturnFunctoolsCachedN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @functools.cached_property
    def function(*_, **__) -> int:
        """Proper docstring.

        Returns
        -------
            int
                Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FOverriddenN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
import typing as _t

T = _t.TypeVar("T")

class MutableSet(_t.MutableSet[T]):
    """Set object to inherit from."""

    def __init__(self) -> None:
        self._set: _t.Set[T] = set()

    def add(self, value: T) -> None:
        self._set.add(value)

    def discard(self, value: T) -> None:
        self._set.discard(value)

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[T]:
        return self._set.__iter__()
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FNoDocRetN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def function() -> int:
    pass
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FSIG501WRetQuestionN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring.

    Returns
    -------
        int
            Does it?
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG501WORetQuestionN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring."""
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG404NEN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(arg, param2) -> None:
    """Docstring.

    Parameters
    ----------
        param1 : int
            Not equal.
        para2 : int
            Not equal.
    """
'''

    @property
    def expected(self) -> str:
        return E[404].fstring(T)


@_templates.register
class _FMethodHeaderWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Proper docstring.

        Parameters
        ----------
            param1 : int
                Pass.
            param2 : int
                Pass.
        """
'''

    @property
    def expected(self) -> str:
        return f"{PATH}:4 in Klass"


@_templates.register
class _PKWOnlyArgsWArgsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def docsig(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    """...

    Parameters
    ----------
        path : int
            Path(s) to check.
        targets : int
            List of errors to target.
        disable : int
            List of errors to disable.

    Returns
    -------
        int
            Boolean value for whether there were any failures or not.
    """
'''

    @property
    def expected(self) -> str:
        return """"""


@_templates.register
class _FClassN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FPropertyReturnsTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    @property
    def method(self):
        """Proper docstring."""
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _PInitNoRetN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
    """

    def __init__(self, param1, param2):
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PInitBadRetN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Parameters
    ----------
    param1 : int
        Fails.
    param2 : int
        Fails.
    """

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassRetNoneN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.

    Returns
    -------
        int
            Fails
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FSIG504N(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.

    Returns
    -------
        int
            Fails
    """

    def __init__(param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FProtectFuncN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def _function(param1, param2) -> None:
    """...

    Parameters
    ----------
        param1 : int
            Fails.
        param2 : int
            Fails.
        param3 : int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FFuncPropN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(self) -> int:
    """Docstring.

    Parameters
    ----------
        self : Klass
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PFuncPropReturnN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(*_, **__) -> int:
    """Docstring.

    Returns
    -------
        int
            Returncode.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def method(self):
    """Docstring.

    Parameters
    ----------
        self : Klass
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FProtectNInitN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
def __init__(param1, param2) -> None:
    pass
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _PStaticSelfN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @staticmethod
    def method(self, param1) -> None:
        """Proper docstring.

        Parameters
        ----------
            self : Klass
                Pass.
            param1 : int
                Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PClassNoSelfN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:

    # against convention but not up to this package to decide
    def method(no_self) -> None:
        """Docstring."""
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Proper docstring.

        Parameters
        ----------
            param1 : int
                Pass.
            param2 : int
                Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FDundersN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class MutableSet:
    """Set object to inherit from."""

    def __init__(self) -> None:
        self._set: _t.Set[T] = set()

    def __contains__(self, x: object) -> bool:
        return self._set.__contains__(x)

    def __len__(self) -> int:
        return self._set.__len__()

    def __iter__(self) -> _t.Iterator[T]:
        return self._set.__iter__()
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FDundersParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def __dunder__(self, param1, param2) -> None:
        """...

        Parameters
        ----------
            param1 : int
                Fails.
            param2 : int
                Fails.
            param3 : int
                Fails.
        """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG403N(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param) -> None:
    """Docstring.

    Parameters
    ----------
        pram : int
            Misspelled.
    """
'''

    @property
    def expected(self) -> str:
        return E[403].fstring(T)


@_templates.register
class _PSphinxWNumpy(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function() -> str:
    """Proper docstring.

    :return: Returns is an indicator this could be a numpy docstring.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PNoIdentN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param) -> None:
    """Docstring.

    Parameters
    ----------
    param : int
        Description.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PColonSpaceN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param) -> None:
    """Docstring.

    Parameters
    ----------
    param: int
        Description.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PIssue36ParamN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def modify(numericString: Union[str, int]) -> str:
    """Do stuff.

    Parameters
    ----------
    numericString: Union[str, int]
        Numeric string that should be converted.

    Returns
    -------
    str
        Reformatted string
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PIssue36ReturnN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def check_stuff(str_lin: str) -> bool:
    """Check if "A" or "B".

    The function checks whether the string is "A" or "B".

    Parameters
    ----------
    str_lin: str
        Special string produced by function_of_y

    Returns
    -------
    bool
        Returns True, else false
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    param3: int
        Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FParamDocsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FParamSigNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Not proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PUnderscoreParamNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, _) -> None:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FOutOfOrderNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    Parameters
    ----------
    param2: int
        Fails.
    param3: int
        Fails.
    param1: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PRetTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    param3: int
        Passes.

    Returns
    -------
    int
        Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.

    Returns
    -------
        int
            Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FRetTypeSigNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG501NoRetNoTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    param3: int
        Passes.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FNoRetDocsNoTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.

    Returns
    -------
    int
        :return: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FRetDocsAttrTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> t.Optional[str]:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FRetDocsNameTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> Optional[str]:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG402OutOfOrderSingleErrorNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Parameters
    ----------
    param2: int
        Fails.
    param3: int
        Fails.
    param1: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _FSIG202ParamDocsSingleErrorNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG203ParamSigSingleErrorNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Not proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FSIG502RetTypeDocsSingleErrorNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.

    Returns
    -------
    int
        :return: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FSIG503RetTypeSigSingleErrorNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FDupesSumNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[201].fstring(T)


@_templates.register
class _PWArgsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Pass.
    param2: int
        Pass.
    *args: int
        Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWArgsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Pass.
    param2: int
        Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Pass.
    param2: int
        Pass.
    **kwargs: int
        Pass
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Pass.
    param2: int
        Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _MFailNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Proper docstring.

    Parameters
    ----------
    param2: int
        Fails.
    param3: int
        Fails.
    param1: int
        Fails.
    """

def function_2(param1, param2) -> None:
    """...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """

def function_3(param1, param2, param3) -> None:
    """Not proper docstring.

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:15 in function_2
    {E[202].fstring(T)}
{PATH}:28 in function_3
    {E[203].fstring(T)}
"""


@_templates.register
class _FMethodWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Proper docstring.

        Parameters
        ----------
        param1: int
            Pass.
        param2: int
            Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PClassSelfNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1) -> None:
        """Proper docstring.

        Parameters
        ----------
        param1: int
            Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PWKwargsKeyNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Passes
    **kwargs: int
        Passes
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsOutOfSectNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Proper docstring.

    **kwargs: int
        Passes

    Parameters
    ----------
    param1: int
        Fail
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FKwargsOutOfOrderNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Proper docstring.

    Parameters
    ----------
    **kwargs : int
        Passes
    param1 : int
        Fail
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PDualColonWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(attachments, sync, **kwargs) -> None:
    """Proper docstring.

    Note: Keyword args (dict) to pass to ``attachments``:

        See ``flask_mail.Message.attach``.

        * filename:     filename of attachment
        * content_type: file mimetype
        * data:         the raw file data

    Parameters
    ----------
    attachments: int
        Iterable of kwargs to construct attachment.
    sync: int
        Don't thread if True: Defaults to False.
    **kwargs: int
        Keyword args to pass to ``Message``:
        See ``flask_mail.Message``.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _POnlyParamsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(reduce: bool = False) -> tuple[str, ...]:
    """Proper docstring.

    Parameters
    ----------
    reduce: int
        :func:`~lsfiles.utils._Tree.reduce`

    Returns
    -------
    int
        Tuple of `Path` objects or str repr.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PReturnAnyWArgsWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    """Proper docstring.

    Parameters
    ----------
    *args: int
        Manipulate string(s).
    **kwargs: int
        Return a string instead of a tuple if strings are passed as tuple.

    Returns
    -------
    int
        Colored string or None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PBinOpNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_index(index: int, seq: _t.Sequence[_T]) -> _T | None:
    """Fet index without throwing an error if index does not exist.

    Parameters
    ----------
    index: int
        Index to get.
    seq: int
        Sequence object that can be indexed.

    Returns
    -------
    int
        Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FBinOpReprNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_index(index: int) -> _T | None:
    """Get index without throwing an error if index does not exist.

    Returns
    -------
    int
        Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PDoubleUnderscoreParamNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, __) -> None:
    """Proper docstring.

    Parameters
    ----------
    param1: int
        Passes.
    param2: int
        Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PPropertyReturnNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Proper docstring.

        Returns
        -------
        int
            Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FSIG501WRetQuestionNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring.

    Returns
    -------
    int
        Does it?
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG404NENI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(arg, param2) -> None:
    """Docstring.

    Parameters
    ----------
    param1: int
        Not equal.
    para2: int
        Not equal.
    """
'''

    @property
    def expected(self) -> str:
        return E[404].fstring(T)


@_templates.register
class _PKWOnlyArgsWArgsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def docsig(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    """...

    Parameters
    ----------
    path: int
        Path(s) to check.
    targets: int
        List of errors to target.
    disable: int
        List of errors to disable.

    Returns
    -------
    int
        Boolean value for whether there were any failures or not.
    """
'''

    @property
    def expected(self) -> str:
        return """"""


@_templates.register
class _FClassNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _PInitNoRetNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    """

    def __init__(self, param1, param2):
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PInitBadRetNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    """

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassRetNoneNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.

    Returns
    -------
    int
        Fails
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FSIG504NI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.

    Returns
    -------
    int
        Fails
    """

    def __init__(param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FProtectFuncNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def _function(param1, param2) -> None:
    """...

    Parameters
    ----------
    param1: int
        Fails.
    param2: int
        Fails.
    param3: int
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FFuncPropNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(self) -> int:
    """Docstring.

    Parameters
    ----------
    self: Klass
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PFuncPropReturnNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(*_, **__) -> int:
    """Docstring.

    Returns
    -------
    int
        Returncode.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def method(self):
    """Docstring.

    Parameters
    ----------
    self: Klass
        Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _PStaticSelfNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @staticmethod
    def method(self, param1) -> None:
        """Proper docstring.

        Parameters
        ----------
        self: Klass
            Pass.
        param1: int
            Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsWKwargsNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Proper docstring.

        Parameters
        ----------
        param1: int
            Pass.
        param2: int
            Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FDundersParamNI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def __dunder__(self, param1, param2) -> None:
        """...

        Parameters
        ----------
        param1: int
            Fails.
        param2: int
            Fails.
        param3: int
            Fails.
        """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG403NI(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param) -> None:
    """Docstring.

    Parameters
    ----------
    pram: int
        Misspelled.
    """
'''

    @property
    def expected(self) -> str:
        return E[403].fstring(T)


@_templates.register
class _PRetTypeSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    :param param1: Passes.
    :param param2: Passes.
    :param param3: Passes.
    :returns: Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :returns: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FNoRetDocsNoTypeSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :returns: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG502RetTypeDocsSingleErrorSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :returns: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _POnlyParamsSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    """Proper docstring.

    :param reduce: :func:`~lsfiles.utils._Tree.reduce`
    :returns: Tuple of `Path` objects or str repr.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PReturnAnyWArgsWKwargsSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    """Proper docstring.

    :param args: Manipulate string(s).
    :key format: Return a string instead of a tuple if strings are
        passed as tuple.
    :returns: Colored string or None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FMsgPoorIndentSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_post(
        id: int, version: t.Optional[int] = None, checkauthor: bool = True
) -> Post:
    """Get post by post's ID or abort with ``404: Not Found.``

    Standard behaviour would be to return None, so do not bypass
     silently.

     :param id: The post's ID.
     :param version: If provided populate session object with
        version.
     :param checkauthor: Rule whether to check for author ID.
     :returns: Post's connection object.
    """
'''

    @property
    def expected(self) -> str:
        return E[401].fstring(T)


@_templates.register
class _PBinOpSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_index(index: int, seq: _t.Sequence[_T]) -> _T | None:
    """Fet index without throwing an error if index does not exist.

    :param index: Index to get.
    :param seq: Sequence object that can be indexed.
    :returns: Item from index else None.
    """
    try:
        return seq[index]
    except IndexError:
        return None
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FBinOpReprSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_index(index: int) -> _T | None:
    """Get index without throwing an error if index does not exist.

    :returns: Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PPropertyReturnSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Proper docstring.

        :returns: Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FHintMissingReturnSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_post() -> Post:
    """Proper docstring.

     return: Post's connection object.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].hint or ""


@_templates.register
class _PInconsistentSpaceSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@pytest.fixture(name="main")
def fixture_main(monkeypatch) -> t.Callable[..., None]:
    """Function for passing mock ``main`` commandline arguments
    to package's main function.

    :param monkeypatch: ``pytest`` fixture for mocking attributes.
    :returns:            Function for using this fixture.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FSIG501WRetQuestionSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring.

    :returns: Does it?
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _PKWOnlyArgsWArgsSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def docsig(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    """...

    :param path: Path(s) to check.
    :param targets: List of errors to target.
    :param disable: List of errors to disable.
    :returns: Boolean value for whether there were any failures or not.
    """
'''

    @property
    def expected(self) -> str:
        return """"""


@_templates.register
class _FClassRetNoneSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :returns: Fails
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FSIG504SRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :returns: Fails
    """

    def __init__(param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _PFuncPropReturnSRs(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(*_, **__) -> int:
    """Docstring.

    :returns: Returncode.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Args:
        param1 (int): Passes.
        param2 (int): Passes.
        param3 (int): Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FParamDocsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """...

    Args:
        param1 (int): Passes.
        param2 (int): Passes.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FParamSigG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Not proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FOutOfOrderG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    Args:
        param2 (int): Fails.
        param3 (int): Fails.
        param1 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PRetTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
        param3 (int): Pass.

    Returns:
        bool: Pass.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FRetTypeDocsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.

    Returns:
        bool: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FRetTypeSigG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG501NoRetNoTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FNoRetDocsNoTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3):
    """Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.

    Returns:
        bool: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FRetDocsAttrTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> t.Optional[str]:
    """Proper docstring.

    Args:
        param1 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FRetDocsNameTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1) -> Optional[str]:
    """Proper docstring.

    Args:
        param1 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FSIG402OutOfOrderSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Args:
        param2 (int): Fails.
        param3 (int): Fails.
        param1 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _FSIG202ParamDocsSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:
    """...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG203ParamSigSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Not proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FSIG502RetTypeDocsSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.

    Returns:
        bool: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[502].fstring(T)


@_templates.register
class _FSIG503RetTypeSigSingleErrorG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> int:
    """Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _FDupesSumG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, param3) -> None:
    """Proper docstring.

    Args:
        param1 (int): Fails.
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[201].fstring(T)


@_templates.register
class _PWArgsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        *args (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWArgsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, *args) -> None:
    """Proper docstring.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Proper docstring.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
        **kwargs (int): Pass.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, **kwargs) -> None:
    """Proper docstring.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _MFailG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Proper docstring.

    Args:
        param2 (int): Fails.
        param3 (int): Fails.
        param1 (int): Fails.
    """

def function_2(param1, param2) -> None:
    """...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """

def function_3(param1, param2, param3) -> None:
    """Not proper docstring.

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:11 in function_2
    {E[202].fstring(T)}
{PATH}:20 in function_3
    {E[203].fstring(T)}
"""


@_templates.register
class _FMethodWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Proper docstring.

    Args:
        param1 (int): Pass.
        param2 (int): Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PClassSelfG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class Klass:
    def method(self, param1) -> None:
        """Proper docstring.

        Args:
            param1 (int): Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PWKwargsKeyG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Proper docstring.

    Args:
        param1 (int): Pass.
        **kwargs (int): Pass.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FWKwargsOutOfSectG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Proper docstring.

    **kwargs (int): Fails

    Args:
        param1 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FKwargsOutOfOrderG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Proper docstring.

    Args:
        **kwargs (int): Fails.
        param1 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[402].fstring(T)


@_templates.register
class _PDualColonWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(attachments, sync, **kwargs) -> None:
    """Proper docstring.

    Note: Keyword args (dict) to pass to ``attachments``:

        See ``flask_mail.Message.attach``.

        * filename:     filename of attachment
        * content_type: file mimetype
        * data:         the raw file data

    Args:
        attachments (int): Iterable of kwargs to construct attachment.
        sync (int): Don't thread if True: Defaults to False.
        **kwargs (int): Keyword args to pass to ``Message``: See
            ``flask_mail.Message``.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _POnlyParamsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(reduce: bool = False) -> _t.Tuple[str, ...]:
    """Proper docstring.

    Args:
        reduce (int): :func:`~lsfiles.utils._Tree.reduce`

    Returns:
        int: Tuple of `Path` objects or str repr.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PReturnAnyWArgsWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(*args: _t.Any, **kwargs: bool) -> _t.Any:
    """Proper docstring.

    Args:
        *args (int): Manipulate string(s).
        **kwargs (int): Return a string instead of a tuple if strings
            are passed as tuple.

    Returns:
        int: Colored string or None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PBinOpG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_index(index: int, seq: _t.Sequence[_T]) -> _T | None:
    """Fet index without throwing an error if index does not exist.

    Args:
        index (int): Index to get.
        seq (int): Sequence object that can be indexed.

    Returns:
        int: Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FBinOpReprG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def get_index(index: int) -> _T | None:
    """Get index without throwing an error if index does not exist.

    Returns:
        int: Item from index else None.
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _PDoubleUnderscoreParamG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2, __) -> None:
    """Proper docstring.

    Args:
        param1 (int): Passes.
        param2 (int): Passes.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PPropertyReturnG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @property
    def function(*_, **__) -> int:
        """Proper docstring.

        Returns:
            int: Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FSIG501WRetQuestionG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function():
    """Docstring.

    Returns:
        int: Does it?
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _FSIG404NEG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(arg, param2) -> None:
    """Docstring.

    Args:
        param1 (int): Not equal.
        para2 (int): Not equal.
    """
'''

    @property
    def expected(self) -> str:
        return E[404].fstring(T)


@_templates.register
class _PKWOnlyArgsWArgsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def docsig(
    *path: _Path,
    targets: _t.List[str] | None = None,
    disable: _t.List[str] | None = None,
) -> bool:
    """...

    Args:
        path (int): Path(s) to check.
        targets (int): List of errors to target.
        disable (int): List of errors to disable.

    Returns:
        int: Boolean value for whether there were any failures or not.
    """
'''

    @property
    def expected(self) -> str:
        return """"""


@_templates.register
class _FClassG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _PInitNoRetG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    """

    def __init__(self, param1, param2):
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PInitBadRetG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
    """

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FClassRetNoneG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.

    Returns:
        int: Fails
    """

    def __init__(self, param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FSIG504G(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.

    Returns:
        int: Fails
    """

    def __init__(param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].fstring(T)


@_templates.register
class _FProtectFuncG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def _function(param1, param2) -> None:
    """...

    Args:
        param1 (int): Fails.
        param2 (int): Fails.
        param3 (int): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FFuncPropG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(self) -> int:
    """Docstring.

    Args:
        self (Klass): Fails.
    """
'''

    @property
    def expected(self) -> str:
        return E[503].fstring(T)


@_templates.register
class _PFuncPropReturnG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def function(*_, **__) -> int:
    """Docstring.

    Returns:
        int: Returncode.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncPropNoRetTypeG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@property
def method(self):
    """Docstring.

    Returns:
        int: Returncode.
    """
'''

    @property
    def expected(self) -> str:
        return E[501].fstring(T)


@_templates.register
class _PStaticSelfG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    @staticmethod
    def method(self, param1) -> None:
        """Proper docstring.

        Args:
            self (Klass): Pass.
            param1 (int): Pass.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FProtectClsWKwargsG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''

class _Klass:
    def method(self, param1, param2, **kwargs) -> None:
        """Proper docstring.

        Args:
            param1 (int): Pass.
            param2 (int): Pass.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FDundersParamG(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def __dunder__(self, param1, param2) -> None:
        """...

        Args:
            param1 (int): Fail.
            param2 (int): Fail.
            param3 (int): Fail.
        """
'''

    @property
    def expected(self) -> str:
        return E[202].fstring(T)


@_templates.register
class _FSIG403G(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param) -> None:
    """Docstring.

    Args:
        pram (int): Misspelled.
    """
'''

    @property
    def expected(self) -> str:
        return E[403].fstring(T)


@_templates.register
class _PEscapedKwargWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(attachments, sync, **kwargs) -> None:
    """Proper docstring.

    Note: Keyword args (dict) to pass to ``attachments``:

        See ``flask_mail.Message.attach``.

        * filename:     filename of attachment
        * content_type: file mimetype
        * data:         the raw file data

    :param attachments: Iterable of kwargs to construct attachment.
    :param sync: Don't thread if True: Defaults to False.
    :param **kwargs: Keyword args to pass to ``Message``:
        See ``flask_mail.Message``.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FNoKwargsIncludedWKwargsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, **kwargs) -> None:
    """Proper docstring.

    :param param1: Fail
    """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FNoDocClassS(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
class Klass:

    def __init__(param1, param2, param3) -> None:
        pass
"""

    @property
    def expected(self) -> str:
        return E[102].fstring(T)


@_templates.register
class _FIssue36OffIndentN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def check_stuff(str_lin: str, a: str) -> bool:
    """Check if "A" or "B".

    The function checks whether the string is "A" or "B".

    Parameters
    ----------
    str_lin: str
        special string produced by function_of_y ["a"]
            a second wrong indent line
    a: str
        string stuff

    Returns
    -------
    bool
        Returns True, else false
    """
'''

    @property
    def expected(self) -> str:
        return E[302].fstring(T)


@_templates.register
class _FOverriddenAncestorsMultipleS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
import typing as _t

T = _t.TypeVar("T")
KT = _t.TypeVar("KT")
VT = _t.TypeVar("VT")

class _MutableSequence(_t.MutableSequence[T]):
    """List-object to inherit from."""

    def __init__(self) -> None:
        self._list: list[T] = []

    def insert(self, index: int, value: T) -> None:
        self._list.insert(index, value)

    @_t.overload
    def __getitem__(self, i: int) -> T:
        ...

    @_t.overload
    def __getitem__(self, s: slice) -> _t.MutableSequence[T]:
        ...

    def __getitem__(self, i):
        return self._list.__getitem__(i)

    @_t.overload
    def __setitem__(self, i: int, o: T) -> None:
        ...

    @_t.overload
    def __setitem__(self, s: slice, o: _t.Iterable[T]) -> None:
        ...

    def __setitem__(self, i, o):
        return self._list.__setitem__(i, o)

    @_t.overload
    def __delitem__(self, i: int) -> None:
        ...

    @_t.overload
    def __delitem__(self, i: slice) -> None:
        ...

    def __delitem__(self, i):
        return self._list.__delitem__(i)

    def __len__(self):
        return self._list.__len__()

# without this, the test will fail (not ideal)
# TODO: remove this to test for why
class Param(_t.NamedTuple):
    """A tuple of param types and their names."""

    kind: str = "param"
    name: str | None = None
    description: str | None = None
    indent: int = 0

class Params(_MutableSequence[Param]):
    """Represents collection of parameters."""

    def insert(self, index: int, value: Param) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _PStringAnnotation(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def example(some_input: int) -> "int":
    """
    Do something.

    Args:
        some_input: Random integer

    Returns:
        Unchanged input
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FNoParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def example(some_input: int) -> int:
    """Return input."""
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FMethodReturnHintS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :return: Fails
    """

    def __init__(param1, param2) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return E[504].hint or ""


@_templates.register
class _PIssue114PosOnlyArgsWArgsWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def starmap(
    fun: Callable[..., Any],
    iterable: Sequence[Sequence[Any]],
    /,
    *args: Any,
    timeout: float = 0,
    show_progress: bool | None = None,
    **kwargs: Any,
) -> list[Job]:
    """Submits many jobs to the queue.

    One for each sequence in the iterable.
    Waits for all to finish, then returns the results.

    Args:
        fun: ...
        iterable: ...
        *args: Static arguments passed to the function.
        timeout: ...
        show_progress: ...
        **kwargs: Static keyword-arguments passed to the function.

    Returns:
        ...
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PIssue114PosOnlyArgsSelfWArgsWKwargsN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def starmap(
        self,
        fun: Callable[..., Any],
        iterable: Sequence[Sequence[Any]],
        /,
        *args: Any,
        timeout: float = 0,
        show_progress: bool | None = None,
        **kwargs: Any,
    ) -> list[Job]:
        """Submits many jobs to the queue.

        One for each sequence in the iterable.
        Waits for all to finish, then returns the results.

        Args:
            fun: ...
            iterable: ...
            *args: Static arguments passed to the function.
            timeout: ...
            show_progress: ...
            **kwargs: Static keyword-arguments passed to the function.

        Returns:
            ...
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MPassOverloadS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@overload
def process(response: None) -> None:
    ...

@overload
def process(response: int) -> tuple[int, str]:
    ...

@overload
def process(response: bytes) -> str:
    ...

def process(response):
    """process a response.

    :param response: The response to process
    :return: Something depending on what the response is
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailOverloadMissingReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@overload
def process(response: None) -> None:
    ...

@overload
def process(response: int) -> tuple[int, str]:
    ...

@overload
def process(response: bytes) -> str:
    ...

def process(response):
    """process a response.

    :param response: The response to process
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:14 in process
    {E[503].fstring(T)}
"""


@_templates.register
class _MFailOverloadMissingParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@overload
def process(response: None) -> None:
    ...

@overload
def process(response: int) -> tuple[int, str]:
    ...

@overload
def process(response: bytes) -> str:
    ...

def process(response):
    """process a response.

    :return: something depending on what the response is
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:14 in process
    {E[203].fstring(T)}
"""


@_templates.register
class _MPassOverloadNoReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@overload
def process(response: None) -> None:
    ...

@overload
def process(response: int) -> None:
    ...

@overload
def process(response: bytes) -> None:
    ...

def process(response):
    """process a response.

    :param response: The response to process
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MPassMultiOverloadsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@overload
def process(response: None) -> None:
    ...

@overload
def process(response: int) -> tuple[int, str]:
    ...

@overload
def process(response: bytes) -> str:
    ...

def process(response):
    """process a response.

    :param response: The response to process
    :return: something depending on what the response is
    """

@overload
def another_process(response: int) -> tuple[int, str]:
    ...

@overload
def another_process(response: bool) -> None:
    ...

@overload
def another_process(response: str) -> int:
    ...

def another_process(response):
    """process another response.

    :param response: The response to process
    :return: something depending on what the response is
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailOverloadNoReturnDocumentedS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
@overload
def process(response: None) -> None:
    ...

@overload
def process(response: int) -> None:
    ...

@overload
def process(response: bytes) -> None:
    ...

def process(response):
    """process a response.

    :param response: The response to process
    :return: NoneType
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:14 in process
    {E[502].fstring(T)}
"""


@_templates.register
class _MPassOverloadMethodS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class SomeClass:
    @overload
    def process(self, response: None) -> None:
        ...

    @overload
    def process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def process(self, response: bytes) -> str:
        ...

    def process(self, response):
        """process a response.

        :param response: The response to process
        :return: something depending on what the response is
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailOverloadMethodMissingReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class SomeClass:
    @overload
    def process(self, response: None) -> None:
        ...

    @overload
    def process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def process(self, response: bytes) -> str:
        ...

    def process(self, response):
        """process a response.

        :param response: The response to process
        """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:15 in SomeClass.process
    {E[503].fstring(T)}
"""


@_templates.register
class _MFailOverloadMethodMissingParamS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class SomeClass:
    @overload
    def process(self, response: None) -> None:
        ...

    @overload
    def process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def process(self, response: bytes) -> str:
        ...

    def process(self, response):
        """process a response.

        :return: something depending on what the response is
        """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:15 in SomeClass.process
    {E[203].fstring(T)}
"""


@_templates.register
class _MFailOverloadMethodNoReturnS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class SomeClass:
    @overload
    def process(self, response: None) -> None:
        ...

    @overload
    def process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def process(self, response: bytes) -> None:
        ...

    def process(self, response):
        """process a response.

        :param response: The response to process
        """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:15 in SomeClass.process
    {E[503].fstring(T)}
"""


@_templates.register
class _MPassMultiOverloadMethodsS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class SomeClass:
    @overload
    def process(self, response: None) -> None:
        ...

    @overload
    def process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def process(self, response: bytes) -> str:
        ...

    def process(self, response):
        """process a response.

        :param response: The response to process
        :return: something depending on what the response is
        """

    @overload
    def another_process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def another_process(self, response: bool) -> None:
        ...

    @overload
    def another_process(self, response: str) -> int:
        ...

    def another_process(self, response):
        """process another response.

        :param response: The response to process
        :return: something depending on what the response is
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MPassOverloadMethodNoReturnDocumentedS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class SomeClass:
    @overload
    def process(self, response: None) -> None:
        ...

    @overload
    def process(self, response: int) -> tuple[int, str]:
        ...

    @overload
    def process(self, response: bytes) -> None:
        ...

    def process(self, response):
        """process a response.

        :param response: The response to process
        :return: Optional
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamDocsCommentModuleS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disable
def function(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamDocsCommentFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:  # docsig: disable
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailCommentDisableFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:  # docsig: disable
    """Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """

def function_2(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

def function_3(param1, param2, param3) -> None:
    """Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:10 in function_2
    {E[202].fstring(T)}
{PATH}:18 in function_3
    {E[203].fstring(T)}
"""


@_templates.register
class _MPassCommentDisableModuleFirstS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disable
def function_1(param1, param2, param3) -> None:
    """Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """

def function_2(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

def function_3(param1, param2, param3) -> None:
    """Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailCommentDisableModuleSecondS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """

# docsig: disable
def function_2(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

def function_3(param1, param2, param3) -> None:
    """Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
"""


@_templates.register
class _MFailCommentDisableModuleThirdS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """

def function_2(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

# docsig: disable
def function_3(param1, param2, param3) -> None:
    """Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:10 in function_2
    {E[202].fstring(T)}
"""


@_templates.register
class _MFailCommentDisableModuleEnableS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """

# docsig: disable
def function_2(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
# docsig: enable

def function_3(param1, param2, param3) -> None:
    """Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:20 in function_3
    {E[203].fstring(T)}
"""


@_templates.register
class _MFailCommentDisableMixedS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_1(param1, param2, param3) -> None:
    """Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """

# docsig: disable
def function_2(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
# docsig: enable

def function_3(param1, param2, param3) -> None:
    """Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    """

def function_4(param1, param2, param3) -> None:  # docsig: disable
    """Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """

# docsig: disable
def function_5(param1, param2) -> None:
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
# docsig: enable

def function_6(param1, param2, param3) -> None:
    """Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_1
    {E[402].fstring(T)}
{PATH}:20 in function_3
    {E[203].fstring(T)}
{PATH}:45 in function_6
    {E[203].fstring(T)}
"""


@_templates.register
class _PParamDocsCommentNoSpaceAfterCommentS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:  #docsig:disable
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PParamDocsCommentNoSpaceAfterColonS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function(param1, param2) -> None:  # docsig:disable
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _MFailCommentDisableEnableOneFuncS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disable
def function_1(param1, param2, param3) -> None:
    """Proper docstring.

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """

def function_2(param1, param2) -> None:  # docsig: enable
    """...

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

def function_3(param1, param2, param3) -> None:
    """Not proper docstring.

    :param param1: Fails.
    :param param2: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:11 in function_2
    {E[202].fstring(T)}
"""


@_templates.register
class _MPassBadInlineDirective(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disable
def function_1(param1, param2, param3) -> None:  # docsig: ena
    """

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """

def function_2(param1, param2) -> None:  # docsig: ena
    """

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in function_1
    {E[2].fstring(T).format(directive="ena")}
{PATH}:11 in function_2
    {E[2].fstring(T).format(directive="ena")}
"""


@_templates.register
class _MPassBadModuleDirective(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disa
def function_1(param1, param2) -> None:
    """

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

def function_2(param1, param2, param3) -> None:
    """

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in function_1
    {E[1].fstring(T).format(directive="disa")}
    {E[202].fstring(T)}
{PATH}:11 in function_2
    {E[1].fstring(T).format(directive="disa")}
    {E[402].fstring(T)}
"""


@_templates.register
class _MPylintDirective(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: unknown
def function_1(param1, param2, param3) -> None:  # pylint: disable
    """

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """

# pylint: disable=unknown,unknown-the-third
def function_2(param1, param2) -> None:
    """

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

def function_3(  # docsig: enable=unknown,unknown-the-third
    param1, param2, param3
) -> None:
    """

    :param param1: Fails.
    :param param2: Fails.
    """

def function_4(param1, param2, param3) -> None:
    """

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    """

def function_5(param1, param2, param3) -> int:
    """

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

def f6(param, param2, param3) -> None:
    """

    :param param: Fails.
    :param param: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

def f7(param, param2, param3) -> None:
    """

    :param param: Fails.
    :param param: Fails.
    :param param2: Fails.
    :param: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in function_1
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[402].fstring(T)}
{PATH}:12 in function_2
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[202].fstring(T)}
{PATH}:20 in function_3
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[4].fstring(T).format(directive=ENABLE, option=UNKNOWN)}
    {E[4].fstring(T).format(directive=ENABLE, option="unknown-the-third")}
    {E[203].fstring(T)}
{PATH}:29 in function_4
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[502].fstring(T)}
{PATH}:38 in function_5
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[503].fstring(T)}
{PATH}:46 in f6
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[201].fstring(T)}
{PATH}:55 in f7
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[201].fstring(T)}
    {E[303].fstring(T)}
"""


@_templates.register
class _MInvalidDirectiveOptions(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: unknown
def function_1(param1, param2, param3) -> None:  # pylint: disable
    """SIG402

    :param param2: Fails.
    :param param3: Fails.
    :param param1: Fails.
    """

# pylint: disable=unknown,unknown-the-third
def function_2(param1, param2) -> None:
    """

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

def function_3(  # docsig: enable=unknown,unknown-the-third
    param1, param2, param3
) -> None:
    """

    :param param1: Fails.
    :param param2: Fails.
    """

def function_4(param1, param2, param3) -> None:
    """

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    :return: Fails.
    """

def function_5(param1, param2, param3) -> int:
    """

    :param param1: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

def f6(param, param2, param3) -> None:
    """

    :param param: Fails.
    :param param: Fails.
    :param param2: Fails.
    :param param3: Fails.
    """

def f7(param, param2, param3) -> None:
    """

    :param param: Fails.
    :param param: Fails.
    :param param2: Fails.
    :param: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in function_1
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[402].fstring(T)}
{PATH}:12 in function_2
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[202].fstring(T)}
{PATH}:20 in function_3
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[4].fstring(T).format(directive=ENABLE, option=UNKNOWN)}
    {E[4].fstring(T).format(directive=ENABLE, option="unknown-the-third")}
    {E[203].fstring(T)}
{PATH}:29 in function_4
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[502].fstring(T)}
{PATH}:38 in function_5
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[503].fstring(T)}
{PATH}:46 in f6
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[201].fstring(T)}
{PATH}:55 in f7
    {E[1].fstring(T).format(directive=UNKNOWN)}
    {E[201].fstring(T)}
    {E[303].fstring(T)}
"""


@_templates.register
class _MInvalidSingleDirectiveOptions(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
def function_3(  # docsig: enable=unknown
    param1, param2, param3
) -> None:
    """

    :param param1: Fails.
    :param param2: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:2 in function_3
    {E[4].fstring(T).format(directive=ENABLE, option=UNKNOWN)}
    {E[203].fstring(T)}
"""


@_templates.register
class _FWClassConstructorFS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """..."""

    def __init__(self, param1, param2) -> None:
        """...

        :param param1: Fails.
        :param param2: Fails.
        :param param3: Fails.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FWClassConstructorInitNoRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """..."""

    def __init__(self, param1, param2):
        """...

        :param param1: Fails.
        :param param2: Fails.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FWClassConstructorInitBadRetS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """..."""

    # bad typing, but leave that up to mypy
    def __init__(self, param1, param2) -> int:
        """...

        :param param1: Fails.
        :param param2: Fails.
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FWClassConstructorRetNoneFS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """..."""

    def __init__(self, param1, param2) -> None:
        """...

        :param param1: Fails.
        :param param2: Fails.
        :return: Fails
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _FWClassConstructorSIG504FS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    """..."""

    def __init__(param1, param2) -> None:
        """...

        :param param1: Fails.
        :param param2: Fails.
        :return: Fails
        """
'''

    @property
    def expected(self) -> str:
        return E[203].fstring(T)


@_templates.register
class _MInvalidSingleModuleDirectiveOptions(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: enable=unknown
def function_3(param1, param2, param3) -> None:
    """

    :param param1: Fails.
    :param param2: Fails.
    """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in function_3
    {E[3].fstring(T).format(directive=ENABLE, option=UNKNOWN)}
    {E[203].fstring(T)}
"""


@_templates.register
class _MFailProtectedMethods(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class _Messages(_t.Dict[int, Message]):
    def __init__(self) -> None:
        self._this_should_not_need_a_docstring

    def fromcode(self, ref: str) -> Message:
        """

        :param ref: Codes or symbolic reference.
        """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:3 in _Messages.__init__
    {E[102].fstring(T)}
{PATH}:6 in _Messages.fromcode
    {E[503].fstring(T)}
"""


@_templates.register
class _MFDisableClassInlineCommentS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class _MessageSequence(_t.List[str]):  # docsig: disable
    def __init__(
        self,
        targets: list[_Message],
        disable: list[_Message],
    ) -> None:
        pass

    def add(self, value: _Message, hint: bool = False, **kwargs) -> None:
        """Add an error to the container.

        :param value: Value to add.
        :param hint: Whether to print a hint or not.
        :param kwargs: Variable(s) if format string.
        """

class Report(_MessageSequence):
    def order(self, sig: _Param, doc: _Param) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:19 in Report.order
    {E[101].fstring(T)}
"""


@_templates.register
class _MFDisableClassModuleCommentDisableEnableS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disable
class _MessageSequence(_t.List[str]):
    def __init__(
        self,
        targets: list[_Message],
        disable: list[_Message],
    ) -> None:
        pass

    def add(self, value: _Message, hint: bool = False, **kwargs) -> None:
        """Add an error to the container.

        :param value: Value to add.
        :param hint: Whether to print a hint or not.
        :param kwargs: Variable(s) if format string.
        """

# docsig: enable

class Report(_MessageSequence):
    def order(self, sig: _Param, doc: _Param) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:22 in Report.order
    {E[101].fstring(T)}
"""


@_templates.register
class _MFDisableClassModuleCommentDisableS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
# docsig: disable
class _MessageSequence(_t.List[str]):
    def __init__(
        self,
        targets: list[_Message],
        disable: list[_Message],
    ) -> None:
        pass

    def add(self, value: _Message, hint: bool = False, **kwargs) -> None:
        """Add an error to the container.

        :param value: Value to add.
        :param hint: Whether to print a hint or not.
        :param kwargs: Variable(s) if format string.
        """

class Report(_MessageSequence):
    def order(self, sig: _Param, doc: _Param) -> None:
        pass
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FFuncInIfStatementN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
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

if True:
    my_function(42)
    def my_external_function(argument: int = 42) -> int:
        pass
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FKlassInIfStatementN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
if True:
    class Klass:
        """Class is OK."""
        def my_external_function(self, argument: int = 42) -> int:
            pass
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FFuncInIfInIfStatementN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
if True:
    if True:
        def my_external_function(argument: int = 42) -> int:
            pass
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FKlassNotMethodOkN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
class Klass:
    def __init__(self, this) -> None:
        self.this = this
    def my_external_function(self, argument: int = 42) -> int:
        """This is a method.

        :param argument: An int.
        :return: An int.
        """
'''

    @property
    def expected(self) -> str:
        return E[102].fstring(T)


@_templates.register
class _FFuncInForLoopN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
container = []

for argument in container:
    def my_external_function(argument: int = 42) -> int:
        pass
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FFuncInForLoopIfN(_BaseTemplate):
    @property
    def template(self) -> str:
        return """
for argument in container:
    if argument > 0:
        def my_external_function(argument: int = 42) -> int:
            pass
"""

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


@_templates.register
class _FNestedFuncN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
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
    def my_external_function(argument: int = 42) -> int:
        pass
'''

    @property
    def expected(self) -> str:
        return E[101].fstring(T)


# starts with `M` for multi instead of `F` so we don't run
# `test_single_flag` with this as it needs `-N/--check-nested` and
# `-c/--check-class` to fail
@_templates.register
class _MNestedKlassNotMethodOkN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
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
    class Klass:
        def __init__(self, this) -> None:
            pass
        def my_external_function(self, argument: int = 42) -> int:
            """This is a method.

            :param argument: An int.
            :return: An int.
            """
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:17 in Klass.__init__
    {E[102].fstring(T)}
"""


@_templates.register
class _MNestedKlassNotMethodNotN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
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
    class Klass:
        def __init__(self, this) -> None:
            pass
        def my_external_function(self, argument: int = 42) -> int:
            pass
'''

    @property
    def expected(self) -> str:
        return f"""\
{PATH}:17 in Klass.__init__
    {E[102].fstring(T)}
{PATH}:19 in Klass.my_external_function
    {E[101].fstring(T)}
"""


@_templates.register
class _MPassOverloadNoReturnAliasS(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
from typing import overload as _overload

@_overload
def process(response: None) -> None:
    ...

@_overload
def process(response: int) -> None:
    ...

@_overload
def process(response: bytes) -> None:
    ...

@_overload
def process(response):
    """process a response.

    :param response: The response to process
    """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _PPropertyReturnFunctoolsCachedAliasN(_BaseTemplate):
    @property
    def template(self) -> str:
        return '''
from functools import cached_property as _cached_property

class Klass:
    @_cached_property
    def function(*_, **__) -> int:
        """Proper docstring.

        Returns
        -------
            int
                Returncode.
        """
'''

    @property
    def expected(self) -> str:
        return ""


@_templates.register
class _FIncorrectDocDotS(_BaseTemplate):
    @property
    def template(self) -> str:
        return r'''
def display(
    define: tuple[tuple[str, str], ...],
    data: list[_t.Any],
    sort_by_field: int | None = None,
    summary_line: _t.Iterable[_t.Any] | None = None,
    print_field_total: int | None = None,
) -> None:
    """Display data as a table.

    :param define: Define the headers and the format of the fields
        belonging to the headers.
    :param data: Data to display.
    :param sort_by_field. Sort the table by the index of the field to
        sort by.
    :param summary_line: Add a row to the end of the table that will not
        be sorted if `sort_by_field` is provided.
    :param print_field_total: Print the total number in the same format
        of the index of the field provided.
    """
'''

    @property
    def expected(self) -> str:
        return E[304].fstring(T).format(token=".")


@_templates.register
class _FPropertyReturnMissingDescS(_BaseTemplate):
    @property
    def template(self) -> str:
        return r'''
def normalize(ticker: str) -> str:
    """Normalize ticket names.

    :param ticker: Ticker to normalize.
    :return:
    """
'''

    @property
    def expected(self) -> str:
        return E[506].fstring(T)
