#=======================================================================
#
#          File:  gen-test-docs.sh
#
#         Usage:  bash gen-test-docs.sh
#
#   Description:  Generate a TESTS.md file.
#
#       Options:  NA
#  Requirements:  git>=2.39.0
#                 poetry>=1.3.1
#          Bugs:  None known
#         Notes:  Generate TESTS.md with a temporary toc file.
#                 Keep this temporary as this is not part of the
#                 package's documentation build. Format the md file for
#                 human readable documentation, built with
#                 sphinx-markdown-builder.
#        AUTHOR:  Stephen Whitlock (jshwi), stephen@jshwisolutions.com
#  ORGANIZATION:  Jshwi Solutions
#       Created:  27/01/2023 17:39:53
#      Revision:  0.1.0
#=======================================================================
set -o nounset

DOCS="docs"
TESTS="tests"
RST="${DOCS}/tests.rst"
BUILD="${DOCS}/_build"
MD="${TESTS}/TESTS.md"


cat > "${RST}" <<EOF
tests
=====

.. automodule:: tests._test
   :members:
   :undoc-members:
   :show-inheritance:
EOF
poetry run sphinx-build -M markdown "${DOCS}" "${BUILD}" >/dev/null 2>&1
rm -f "${RST}"
cat > "${MD}" <<EOF
<!--
This file is auto-generated and any changes made to it will be overwritten
-->
EOF

poetry run python >> ${MD} <<EOF
import re
from pathlib import Path

_SKIP_LINES = False
p = Path("docs/_build/markdown/tests.md")
for i in p.read_text(encoding="utf-8").splitlines():
    m = re.match(r"(.*)tests\._test\.test_(.*)\((.*)", i)
    if m:
        _SKIP_LINES = False
        print(f"{m.group(1)}{m.group(2).capitalize().replace('_', ' ')}\n")
    elif i.startswith("* **"):
        _SKIP_LINES = True
    elif not _SKIP_LINES:
        print(i)
EOF
git add "${MD}"
