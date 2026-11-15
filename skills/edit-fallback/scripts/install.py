"""Install the fallback helpers once, as the first tool call: run_skill_script with skill_name "edit-fallback" and
file_path "scripts/install.py" and no other argument (array arguments can hang the tool-call parser). It copies
find.py and edit.py to /tmp/h/ (outside /workspace, so they never enter the patch) and prints how to use them; from
then on they are plain run_command lines. If it cannot write, it says so, and the agent goes on with grep and
edit_file. Python 3.8+, standard library only.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))  # ADK's wrapper puts every script of the skill here
TARGET = "/tmp/h"  # the path the agent types in run_command
HELPERS = ("find.py", "edit.py")

USAGE = """Installed /tmp/h/find.py and /tmp/h/edit.py. Use them with run_command:

Find the code (instead of grep): names from the issue, tests left out, best file first, with line numbers:
  python3 /tmp/h/find.py NAME [NAME ...]

After edit_file fails ("old_string not found" or "occurs N times"), never resend it; run instead:
  python3 /tmp/h/edit.py path/to/file.py [--near LINE] <<'EOF'
<<<<<<< SEARCH
one to three lines as read_file showed them
=======
the same lines as they should be
>>>>>>> REPLACE
EOF
It matches exactly, then with escapes undone, then ignoring spaces, then the closest place; it says when the change
is already made, lists the lines when SEARCH occurs more than once (then add --near LINE), and when unsure it prints
NOTHING WRITTEN and the closest lines to copy from.
"""

FAILED = """Could not install the helpers ({error}). Do without them: localize with grep (tests left out), and after a
failed edit_file re-read the lines and retry once with a shorter anchor.
"""


def folders():
    """Where to install. A Docker sandbox runs commands as typed, so /tmp/h. The subprocess sandbox rewrites /tmp in a
    command to its own folder, which it also sets as TMPDIR, while Python code writing to /tmp/h reaches the real
    /tmp; so also $TMPDIR/h."""
    out = [TARGET]
    tmp = os.environ.get("TMPDIR")
    if tmp and os.path.abspath(os.path.join(tmp, "h")) != os.path.abspath(TARGET):
        out.append(os.path.join(tmp, "h"))
    return out


def main(target=None, out=None):
    out = out or sys.stdout
    override = target or os.environ.get("EDIT_FALLBACK_DIR")
    written, error = [], None
    for folder in ([override] if override else folders()):
        try:
            os.makedirs(folder, exist_ok=True)
            for name in HELPERS:
                shutil.copyfile(os.path.join(HERE, name), os.path.join(folder, name))
            written.append(folder)
        except OSError as e:
            error = "%s: %s" % (type(e).__name__, e)
    if not written:
        out.write(FAILED.format(error=error))
        return 1
    out.write(USAGE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
