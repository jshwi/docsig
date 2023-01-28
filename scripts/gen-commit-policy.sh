#=======================================================================
#
#          File:  gen-commit-policy.sh
#
#         Usage:  bash gen-commit-policy.sh
#
#   Description:  Generate a COMMIT_POLICY.md file from .conform.yaml.
#
#       Options:  NA
#  Requirements:  git>=2.39.0
#                 poetry>=1.3.1
#          Bugs:  None known
#         Notes:  Generate an easy to read policy file viewable with
#                 Github's flavoured markdown.
#                 Conform will enforce these rules with a pre-commit
#                 hook.
#                 Any changes made to the policy via the .conform.yaml
#                 should automatically update the COMMIT_POLICY.md file
#                 with a pre-commit hook that runs this script.
#        AUTHOR:  Stephen Whitlock (jshwi), stephen@jshwisolutions.com
#  ORGANIZATION:  Jshwi Solutions
#       Created:  28/01/2023 16:23:03
#      Revision:  0.1.0
#=======================================================================
set -o nounset

GITHUB=".github"
MD="${GITHUB}/COMMIT_POLICY.md"

cat > "${MD}" <<EOF
<!--
This file is auto-generated and any changes made to it will be overwritten
-->
EOF

poetry run python >> "${MD}" - <<EOF
import re
from pathlib import Path

import yaml

print("# Commit Policy\n")
for p in yaml.safe_load(Path(".conform.yaml").read_text())["policies"]:
    if p["type"] == "commit":
        for k1, v1 in p["spec"].items():
            print(f"## {k1.capitalize()}\n")
            if not isinstance(v1, dict):
                print(f"{v1}\n")
            else:
                for k2, v2 in v1.items():
                    if isinstance(v2, (bool, int, str)):
                        m = [i for i in re.split("([A-Z][^A-Z]*)", k2) if i]
                        if m:
                            k2 = " ".join(m).capitalize()
                        v2 = f"{k2}: {v2}"
                    else:
                        if isinstance(v2, list):
                            v2 = "### {}\n\n- {}".format(
                                k2.capitalize(), "\n- ".join(v2)
                            )
                    print(f"{v2}\n")
EOF
git add "${MD}"
