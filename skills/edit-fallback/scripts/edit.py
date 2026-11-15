"""Fallback edit for when edit_file says "old_string not found" or "occurs N times".

usage: python3 /tmp/h/edit.py FILE [--near LINE] [--dry-run] <<'EOF'
<<<<<<< SEARCH
lines as you think they are now
=======
lines as they should be
>>>>>>> REPLACE
EOF

Tries SEARCH as given, then without a last line of tool-call debris, then with JSON escapes undone (a literal \\n or
\\"): first exactly, then ignoring spaces, then (only for a SEARCH of 8 lines or fewer) the closest block of lines
(similarity >= 0.8 and clearly better than any other place; --near only breaks a near-tie). A close match changes only
the lines SEARCH and REPLACE differ in and keeps the file's own copy of the rest; where that is a guess (SEARCH and the
file differ where REPLACE makes its change, or their indentation disagrees) it changes nothing. It says when the change
is already made, lists the lines when SEARCH occurs more than once, and otherwise prints the closest lines. Output
starts with NOTHING WRITTEN when the file is unchanged. Exit 0 either way, 2 for a usage error. Python 3.8+, standard
library only.
"""
import difflib
import os
import re
import select
import sys

MIN_SCORE = 0.8
MIN_GAP = 0.05
# Length checks: a close (not exact) match is tried only for a short SEARCH. A long SEARCH that is not in the file
# is usually remembered or invented code, not a copy error, and scoring it is slow. Exact matches have no limit.
MAX_FUZZY_LINES = 8
DEBRIS = re.compile(r"""^\s*(?:"{1,2}|'{1,2}),?\s*$""")  # a stray quote and comma from a broken tool call


class Conflict(Exception):
    """Where REPLACE's change goes, or how to indent it, would be a guess."""


def norm(line):
    return " ".join(line.split())


def bare(line):
    """The line without a carriage return of its own (a CRLF file's line ending)."""
    return line[:-1] if line.endswith("\r") else line


def indent_of(line):
    return len(line) - len(line.lstrip(" \t"))


def split_lines(text):
    """Lines split on newline only (a form feed, a lone carriage return or a Unicode separator stays inside its line),
    and whether the text ends with a newline."""
    if not text:
        return [], False
    parts = text.split("\n")
    trailing = parts[-1] == ""
    return (parts[:-1] if trailing else parts), trailing


def core(lines, debris=False):
    """Lines without leading and trailing blank lines (and, with debris, without a last line of tool-call debris)."""
    lines = [bare(x) for x in lines]
    if debris:
        while lines and (not lines[-1].strip() or DEBRIS.match(lines[-1])):
            lines.pop()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def parse_blocks(text):
    """SEARCH/REPLACE blocks from text; also accepts OLD/NEW and bare <<<<<<< / ======= / >>>>>>> markers."""
    blocks, search, replace, mode = [], [], [], None
    for line in text.split("\n"):
        line = bare(line)
        s = line.strip()
        if re.match(r"^<{5,}( ?(SEARCH|OLD|ORIGINAL))?\s*$", s):
            search, replace, mode = [], [], "s"
        elif mode == "s" and re.match(r"^={5,}\s*$", s):
            mode = "r"
        elif mode == "r" and re.match(r"^>{5,}( ?(REPLACE|NEW|UPDATED))?\s*$", s):
            blocks.append(("\n".join(search), "\n".join(replace)))
            mode = None
        elif mode == "s":
            search.append(line)
        elif mode == "r":
            replace.append(line)
    return blocks


def unescape(text):
    """The text with one level of JSON-style escaping undone (a literal \\n, \\t, \\" or doubled backslash), or None
    when there is nothing to undo. Only tried after the text as given."""
    if "\\" not in text:
        return None
    table = {"n": "\n", "t": "\t", "r": "", '"': '"', "'": "'", "\\": "\\"}
    out = re.sub(r"\\([nrt\"'\\])", lambda m: table[m.group(1)], text)
    return out if out != text else None


def find_lines(file_lines, search_lines, exact):
    """Start indexes where search_lines occur (exactly, or with whitespace normalised)."""
    n = len(search_lines)
    if n == 0:
        return []
    if exact:
        fb = [bare(x) for x in file_lines]
        return [i for i in range(len(fb) - n + 1) if fb[i:i + n] == search_lines]
    fn = [norm(x) for x in file_lines]
    sn = [norm(x) for x in search_lines]
    return [i for i in range(len(fn) - n + 1) if fn[i:i + n] == sn]


def closest(file_lines, search_lines, top=3):
    """(score, start, end) of the closest windows of n-1..n+1 lines, best first, non-overlapping. A long SEARCH gets a
    line-level score only (for showing, never for applying); one over 40 lines gets none."""
    if len(search_lines) > 40:
        return []
    target = "\n".join(norm(x) for x in search_lines)
    fn = [norm(x) for x in file_lines]
    sn = [norm(x) for x in search_lines]
    n = len(search_lines)
    # Only score windows near a line that matches a SEARCH line: exactly (whitespace aside) for a distinctive line,
    # or, for the longest SEARCH line, closely (similarity >= 0.7). Keeps a 5,000-line file to well under a second.
    where = {}
    for p, x in enumerate(fn):
        if len(x) >= 6:
            where.setdefault(x, []).append(p)
    starts = set()
    for k, x in enumerate(sn):
        if len(where.get(x, ())) <= 50:  # a line that occurs everywhere (return None) anchors nothing
            for p in where.get(x, ()):
                starts.update(range(p - k - 1, p - k + 2))
    longest = max(range(n), key=lambda k: len(sn[k]))
    for p, x in enumerate(fn):
        sm = difflib.SequenceMatcher(None, sn[longest], x, autojunk=False)
        if sm.real_quick_ratio() >= 0.7 and sm.quick_ratio() >= 0.7 and sm.ratio() >= 0.7:
            starts.update(range(p - longest - 1, p - longest + 2))
    rough = []
    for size in sorted({max(1, n - 1), n, n + 1}):
        for i in sorted(s for s in starts if 0 <= s <= len(file_lines) - size):
            rough.append((difflib.SequenceMatcher(None, sn, fn[i:i + size], autojunk=False).ratio(), i, i + size))
    rough.sort(key=lambda c: (-c[0], c[1]))
    cands = []
    for score, i, j in rough[:12]:
        if n > MAX_FUZZY_LINES:
            cands.append((score, i, j))
            continue
        r = difflib.SequenceMatcher(None, target, "\n".join(fn[i:j]), autojunk=False).ratio()
        if r >= MIN_SCORE - 0.3:
            cands.append((r, i, j))
    cands.sort(key=lambda c: (-c[0], c[1]))
    picked = []
    for c in cands:
        if all(c[2] <= p[1] or c[1] >= p[2] for p in picked):
            picked.append(c)
        if len(picked) == top:
            break
    return picked


def choose(cands, near):
    """The one clear candidate: the best at MIN_SCORE or more with no other within MIN_GAP of it; --near picks among
    such near-ties only."""
    if not cands or cands[0][0] < MIN_SCORE:
        return None
    ties = [c for c in cands if c[0] >= MIN_SCORE and cands[0][0] - c[0] < MIN_GAP]
    if len(ties) == 1:
        return ties[0]
    if near:
        best = min(ties, key=lambda c: abs(c[1] + 1 - near))
        if abs(best[1] + 1 - near) <= 30:
            return best
    return None


def _shift(window, search_lines, pairs):
    """(shift, first_differs): the indentation shift from SEARCH to the file, from the line pairs that match ignoring
    spaces. Allowed to differ only on SEARCH's first line (copied from mid-line). Tabs against spaces: Conflict."""
    lead_w = [bare(w)[:indent_of(bare(w))] for w in window if w.strip()]
    lead_s = [s[:indent_of(s)] for s in search_lines if s.strip()]
    if any("\t" in x for x in lead_w) != any("\t" in x for x in lead_s) and any(lead_w + lead_s):
        raise Conflict("tabs and spaces")
    shifts = [(k, indent_of(bare(window[j])) - indent_of(search_lines[k])) for k, j in pairs
              if search_lines[k].strip()]
    if not shifts:
        return 0, False
    rest = {d for k, d in shifts if k != 0}
    if len({d for _, d in shifts}) == 1:
        return shifts[0][1], False
    if len(rest) == 1 and shifts[0][0] == 0:
        return rest.pop(), True
    raise Conflict("indentation")


def _reindent(line, shift, cr):
    if not line.strip():
        return "\r" if cr else ""
    if shift > 0:
        line = " " * shift + line
    elif shift < 0:
        if indent_of(line) < -shift:
            raise Conflict("indentation")
        line = line[-shift:]
    return line + ("\r" if cr else "")


def merge(window, search_lines, replace_lines, cr=False):
    """A three-way merge with SEARCH as the base: the agent's changes come from REPLACE (re-indented to the file), every
    other line from the file. Conflict when where the change goes is a guess."""
    n = len(search_lines)
    status = [None] * n                   # "one": a file line stands for it; (i1, i2): part of an unequal block
    w_of = [[] for _ in range(n)]
    w_before = [[] for _ in range(n + 1)]  # file lines SEARCH left out, before SEARCH line k
    pairs = []
    sw = difflib.SequenceMatcher(None, [norm(x) for x in search_lines], [norm(x) for x in window], autojunk=False)
    for tag, i1, i2, j1, j2 in sw.get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                status[i1 + k] = "one"
                w_of[i1 + k] = [window[j1 + k]]
                if tag == "equal":
                    pairs.append((i1 + k, j1 + k))
        elif tag == "replace":
            for k in range(i1, i2):
                status[k] = (i1, i2)
            w_of[i1] = window[j1:j2]
        elif tag == "insert":
            w_before[i1].extend(window[j1:j2])
        else:  # delete: SEARCH lines the file does not have
            for k in range(i1, i2):
                status[k] = "missing"
    shift, first_differs = _shift(window, search_lines, pairs)
    keep = [False] * n
    r_at = [[] for _ in range(n + 1)]     # REPLACE lines that go before SEARCH line k (or at the end)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, search_lines, replace_lines,
                                                       autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i1, i2):
                keep[k] = True
        elif tag in ("replace", "insert"):
            r_at[i1].extend(replace_lines[j1:j2])
    for k in range(n):
        if status[k] == "missing" and not keep[k]:
            raise Conflict("REPLACE changes a SEARCH line the file does not have")
        if status[k] == "missing" and (r_at[k] or r_at[k + 1]):
            raise Conflict("REPLACE adds lines next to a SEARCH line the file does not have")
    for i1, i2 in {s for s in status if isinstance(s, tuple)}:
        changed = [k for k in range(i1, i2) if not keep[k]]
        if (changed and len(changed) != i2 - i1) or any(r_at[k] for k in range(i1 + 1, i2)):
            raise Conflict("REPLACE changes part of a block the file has in a different form")
    if first_differs and n and not keep[0]:
        raise Conflict("SEARCH's first line is indented unlike the file and REPLACE changes it")
    out = []
    for k in range(n + 1):
        new_lines = [_reindent(x, shift, cr) for x in r_at[k]]
        if w_before[k] and new_lines:
            if [norm(x) for x in w_before[k]] != [norm(x) for x in new_lines]:
                raise Conflict("the file has lines SEARCH left out exactly where REPLACE adds lines")
            new_lines = []                # the same lines: the change is already there
        out.extend(w_before[k])
        out.extend(new_lines)
        if k < n and keep[k] and (status[k] == "one" or (isinstance(status[k], tuple) and status[k][0] == k)):
            out.extend(w_of[k])
    return out


def already_there(file_lines, r_lines, s_lines, i, j):
    """A message when REPLACE, which adds lines SEARCH does not have, already overlaps lines i..j (so applying it again
    would add them twice); else None."""
    if not r_lines or len(r_lines) <= len(s_lines):
        return None
    for h in find_lines(file_lines, r_lines, False):
        if h < j and h + len(r_lines) > i:
            return "REPLACE is already in the file at line %d: this change is done; move on." % (h + 1)
    return None


def _variants(search, replace):
    """(search lines, replace lines, how): as given, without debris, with escapes undone (and without debris)."""
    out = []
    pairs = [(search, replace, "")]
    un = unescape(search)
    if un is not None:
        pairs.append((un, unescape(replace) or replace, " after undoing escapes"))
    for s, r, how in pairs:
        given = [bare(x) for x in s.split("\n")]  # as written: a blank line at either end is part of it
        raw = core(s.split("\n"))
        r_lines = core(r.split("\n"))
        if given != raw and raw:
            out.append((given, [bare(x) for x in r.split("\n")], how))
        out.append((raw, r_lines, how))
        clean = core(s.split("\n"), debris=True)
        if clean != raw:
            out.append((clean, r_lines, how + " without tool-call debris"))
    return [v for v in out if v[0]]


def _listing(file_lines, cands):
    out = []
    for score, i, j in cands:
        out.append("--- lines %d-%d (similarity %.2f):" % (i + 1, j, score))
        out.extend("%5d  %s" % (k + 1, bare(file_lines[k])) for k in range(i, j))
    if cands:
        out.append("Copy SEARCH from the lines above (without the numbers) and run again.")
    return out


def apply(content, search, replace, near=None):
    """(new_content, message) or (None, message)."""
    file_lines, trailing = split_lines(content)
    cr = bool(file_lines) and 2 * sum(x.endswith("\r") for x in file_lines) > len(file_lines)
    variants = _variants(search, replace)
    if not variants:
        return None, "SEARCH is empty: copy one to three lines from read_file into it."
    for exact in (True, False):
        for s_lines, r_lines, how in variants:
            hits = find_lines(file_lines, s_lines, exact)
            if len(hits) > 1 and near:
                hits = sorted(hits, key=lambda i: abs(i + 1 - near))[:1]
            if len(hits) > 1:
                where = ", ".join(str(i + 1) for i in hits[:10])
                return None, ("SEARCH occurs at lines %s. Run again with --near LINE (the line you mean, from "
                              "read_file)." % where)
            if not hits:
                continue
            i, j = hits[0], hits[0] + len(s_lines)
            done = already_there(file_lines, r_lines, s_lines, i, j)
            if done:
                return None, done
            try:
                new = merge(file_lines[i:j], s_lines, r_lines, cr)
            except Conflict as e:
                return None, "SEARCH matches lines %d-%d but %s; nothing changed." % (i + 1, j, e)
            if new == file_lines[i:j]:
                return None, "REPLACE is the same as lines %d-%d: nothing to change." % (i + 1, j)
            return finish(file_lines, trailing, i, j, new, "matched lines %d-%d%s%s" % (
                i + 1, j, "" if exact else " ignoring spaces", how))
    conflict, shown, long_n = None, None, 0
    for s_lines, r_lines, how in variants:
        cands = closest(file_lines, s_lines)
        shown = shown if shown is not None else cands
        if len(s_lines) > MAX_FUZZY_LINES:
            long_n = long_n or len(s_lines)
            continue
        pick = choose(cands, near)
        if pick is None:
            continue
        score, i, j = pick
        if len(r_lines) > len(s_lines):  # REPLACE adds lines: is it already where the change would go?
            for h in find_lines(file_lines, r_lines, False):
                if h < j and h + len(r_lines) > i:
                    return None, "REPLACE is already in the file at line %d: this change is done; move on." % (h + 1)
        try:
            new = merge(file_lines[i:j], s_lines, r_lines, cr)
        except Conflict as e:
            conflict = conflict or (i, j, score, str(e))
            continue
        if new == file_lines[i:j]:
            return None, "REPLACE already matches lines %d-%d: this change is done; move on." % (i + 1, j)
        return finish(file_lines, trailing, i, j, new,
                      "closest match lines %d-%d (similarity %.2f)%s" % (i + 1, j, score, how))
    if conflict:
        i, j, score, why = conflict
        return None, "\n".join(["The closest place, lines %d-%d (similarity %.2f), is a guess: %s; nothing changed. "
                                "The file there:" % (i + 1, j, score, why)]
                               + ["%5d  %s" % (k + 1, bare(file_lines[k])) for k in range(i, j)]
                               + ["Copy SEARCH from these lines (without the numbers) and run again."])
    if long_n:
        head = ("SEARCH has %d lines and is not in the file; a close match is tried only for %d lines or fewer. "
                "Nothing changed." % (long_n, MAX_FUZZY_LINES))
    else:
        head = "SEARCH is not in the file and no place is clearly closest; nothing changed."
    return None, "\n".join([head] + _listing(file_lines, shown or []))


def finish(file_lines, trailing, i, j, new, how):
    lines = file_lines[:i] + new + file_lines[j:]
    content = "\n".join(lines) + ("\n" if trailing else "")
    diff = difflib.unified_diff([bare(x) for x in file_lines[i:j]], [bare(x) for x in new], "before", "after",
                                lineterm="", n=1)
    return content, how + "\n" + "\n".join(list(diff)[2:])


def _read_stdin(wait=5.0):
    """stdin's text, or "" when nothing arrives within `wait` seconds (a call without a heredoc must not hang)."""
    try:
        ready, _, _ = select.select([sys.stdin], [], [], wait)
    except (ValueError, OSError, TypeError):
        ready = [sys.stdin]
    return sys.stdin.read() if ready else ""


def main(argv=None, stdin=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    near, dry = None, False
    if "--dry-run" in argv:
        argv.remove("--dry-run")
        dry = True
    if "--near" in argv:
        k = argv.index("--near")
        try:
            near = int(argv[k + 1])
        except (IndexError, ValueError):
            print("--near needs a line number")
            return 2
        del argv[k:k + 2]
    if len(argv) != 1:
        print(__doc__)
        return 2
    path = argv[0]
    if not os.path.isabs(path) and os.path.isdir("/workspace") and not os.path.exists(path):
        path = os.path.join("/workspace", path)
    if not os.path.isfile(path):
        print("No such file: %s (use the path from the repository root)." % argv[0])
        return 2
    text = stdin.read() if stdin is not None else _read_stdin()
    blocks = parse_blocks(text)
    if not blocks:
        print("No SEARCH/REPLACE block on stdin. Write:\n"
              "<<<<<<< SEARCH\nold lines\n=======\nnew lines\n>>>>>>> REPLACE")
        return 2
    with open(path, encoding="utf-8", newline="") as f:
        content = f.read()
    reports = []
    for n, (search, replace) in enumerate(blocks, 1):
        new, msg = apply(content, search, replace, near)
        if new is None:
            where = "block %d of %d: " % (n, len(blocks)) if len(blocks) > 1 else ""
            print("NOTHING WRITTEN: %s%s" % (where, msg.splitlines()[0]))
            print("\n".join(msg.splitlines()[1:]))
            return 0
        reports.append(msg)
        content = new
    print("\n".join(reports))
    if dry:
        print("dry run: nothing written")
        return 0
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("written: %s" % argv[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
