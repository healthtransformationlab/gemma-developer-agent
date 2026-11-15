"""Find the code an issue is about: the repository's Python files ranked by the names you give.

usage: python3 /tmp/h/find.py NAME [NAME ...]

NAME is a function, class, module or variable name from the issue (`Table.add_row`, `rich.table`, `get_openapi`), or
a short quoted error message. Tests, docs and examples are left out (they are listed last, only if nothing else
matches). Files are ranked by how many of the names they contain, whether they define them (def/class/assignment),
and whether a dotted name is their module path; each comes with its matching lines and their numbers, for read_file.
Python 3.8+, standard library only; reads /workspace (or the current directory).
"""
import os
import re
import sys

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".tox", ".venv", "venv", "build", "dist", ".eggs", "site-packages"}
LOW_DIRS = {"tests", "test", "testing", "docs", "docs_src", "doc", "examples", "example", "benchmarks", "scripts"}
MAX_FILES = 8
MAX_LINES = 3
MAX_FILE_BYTES = 2000000


def is_low(rel):
    parts = rel.split("/")
    name = parts[-1]
    return (any(p in LOW_DIRS for p in parts[:-1]) or name.startswith("test_") or name.endswith("_test.py")
            or name == "conftest.py")


def terms(names):
    """Each NAME as (shown, needle, kind): the whole dotted name, its last part and last two parts."""
    out = []
    for raw in names:
        raw = raw.strip().strip("`'\"")
        if not raw:
            continue
        if " " in raw or not re.match(r"^[A-Za-z_][\w.]*$", raw):
            out.append((raw, raw, "text"))
            continue
        parts = [p for p in raw.split(".") if p]
        out.append((raw, parts[-1], "name"))
        if len(parts) >= 2:
            out.append((raw, ".".join(parts[-2:]), "dotted"))
    return out


def module_path_bonus(rel, names):
    """True when a dotted NAME names this file's module (rich.table, rich.table.Table) or NAME is the file's name."""
    mod = rel[:-3].replace("/", ".")
    if mod.endswith(".__init__"):
        mod = mod[: -len(".__init__")]
    for prefix in ("src.", "lib."):
        if mod.startswith(prefix):
            mod = mod[len(prefix):]
    last = mod.split(".")[-1]
    for n in names:
        n = n.strip("`'\"")
        if not n or " " in n:
            continue
        parts = n.split(".")
        if len(parts) == 1:
            if n == last:
                return True
        elif mod == n or n.startswith(mod + ".") or last in parts[:-1]:
            return True
    return False


def scan(root, names):
    found = []
    tlist = terms(names)
    pats = []
    for shown, needle, kind in tlist:
        if kind == "text":
            pats.append((shown, re.compile(re.escape(needle)), None))
        else:
            word = re.escape(needle)
            pats.append((shown, re.compile(r"(?<![\w.])" + word + r"(?!\w)" if kind == "dotted" else
                                           r"(?<!\w)" + word + r"(?!\w)"),
                         re.compile(r"^\s*(?:async\s+)?(?:def|class)\s+" + re.escape(needle.split(".")[-1]) + r"\b|^"
                                    + re.escape(needle.split(".")[-1]) + r"\s*[:=]")))
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(filenames):
            if not fn.endswith(".py"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            try:
                if os.path.getsize(full) > MAX_FILE_BYTES:
                    continue
                with open(full, encoding="utf-8", errors="replace") as f:
                    lines = f.read().splitlines()
            except OSError:
                continue
            matched, defined, hits, shown_lines = set(), set(), 0, []
            for no, line in enumerate(lines, 1):
                for shown, pat, defpat in pats:
                    if pat.search(line):
                        matched.add(shown)
                        hits += 1
                        is_def = bool(defpat and defpat.search(line))
                        if is_def:
                            defined.add(shown)
                        shown_lines.append((0 if is_def else 1, no, line.strip()))
                        break
            bonus = module_path_bonus(rel, names)
            if not matched and not bonus:
                continue
            if not matched:  # the file is the named module but never says its own name
                matched.add(rel)
                shown_lines.append((1, 1, lines[0].strip() if lines else ""))
            score = 3 * len(matched) + 4 * len(defined) + 3 * bonus + min(hits, 20) / 10.0
            found.append((is_low(rel), -score, rel, sorted(shown_lines)[:MAX_LINES], len(matched), len(defined)))
    found.sort(key=lambda r: (r[0], r[1], len(r[2]), r[2]))
    return found


def root_dir():
    """The repository: the current folder when it is a git checkout (the subprocess sandbox runs commands in the
    workspace but has no real /workspace), else /workspace, else the current folder."""
    if os.path.isdir(".git"):
        return os.getcwd()
    return "/workspace" if os.path.isdir("/workspace") else os.getcwd()


def main(argv=None):
    names = list(sys.argv[1:] if argv is None else argv)
    if not names:
        print(__doc__)
        return 2
    found = scan(root_dir(), names)
    if not found:
        print("No Python file contains %s. Try a shorter or different name from the issue." % ", ".join(names))
        return 1
    main_files = [r for r in found if not r[0]]
    shown = (main_files or found)[:MAX_FILES]
    for low, neg, rel, lines, nm, nd in shown:
        print("%s  (names %d, defines %d)" % (rel, nm, nd))
        for _, no, text in lines:
            print("  %d: %s" % (no, text[:160]))
    rest = len(main_files) - len(shown) if main_files else 0
    if rest > 0:
        print("... %d more files" % rest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
