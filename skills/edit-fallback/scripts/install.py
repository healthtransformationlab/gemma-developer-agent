"""Install the fallback helpers once, as the first tool call: run_skill_script with skill_name "edit-fallback" and
file_path "scripts/install.py" and no other argument (array arguments can hang the tool-call parser). It copies
find.py and edit.py to /tmp/h/ (outside /workspace, so they never enter the patch) and prints how to use them; from
then on they are plain run_command lines. Python 3.8+, standard library only.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))  # ADK's wrapper puts every script of the skill here
TARGET = "/tmp/h"
HELPERS = ("find.py", "edit.py")

USAGE = """Installed {target}/find.py and {target}/edit.py. Use them with run_command:

Find the code (instead of grep): names from the issue, tests left out, best file first, with line numbers:
  python3 {target}/find.py NAME [NAME ...]

After edit_file fails ("old_string not found" or "occurs N times"), never resend it; run instead:
  python3 {target}/edit.py path/to/file.py [--near LINE] <<'EOF'
<<<<<<< SEARCH
one to three lines as read_file showed them
=======
the same lines as they should be
>>>>>>> REPLACE
EOF
It matches exactly, then with escapes undone, then ignoring spaces, then the closest place; it says when the change
is already made, lists the lines when SEARCH occurs more than once (then add --near LINE), and changes nothing when
unsure.
"""


def main(target=None, out=None):
    target = target or os.environ.get("EDIT_FALLBACK_DIR") or TARGET
    out = out or sys.stdout
    os.makedirs(target, exist_ok=True)
    for name in HELPERS:
        shutil.copyfile(os.path.join(HERE, name), os.path.join(target, name))
    out.write(USAGE.format(target=target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
