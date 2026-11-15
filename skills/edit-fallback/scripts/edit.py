"""Fallback edit for when edit_file says "old_string not found" or "occurs N times".

usage: python3 /tmp/h/edit.py FILE [--near LINE] [--dry-run] <<'EOF'
<<<<<<< SEARCH
lines as you think they are now
=======
lines as they should be
>>>>>>> REPLACE
EOF

Tries, in order: exact text; the text with JSON escapes undone (a literal \\n or \\"); whitespace-insensitive lines;
then the closest block of lines (similarity >= 0.8, clearly better than any other place). A close match changes only
the lines that differ between SEARCH and REPLACE, keeping the file's own copy of the others. If REPLACE is already in
the file it says so and changes nothing. If no place is clear it changes nothing and prints the closest lines with
their numbers. Several matches: give --near with a line number from read_file. Python 3.8+, standard library only.
"""
import difflib
import os
import re
import sys

MIN_SCORE = 0.8
MIN_GAP = 0.05
# Length checks: a close (not exact) match is tried only for a short SEARCH. A long SEARCH that is not in the file
# is usually remembered or invented code, not a copy error, and scoring it is slow. Exact matches have no limit.
MAX_FUZZY_LINES = 8


def norm(line):
    return " ".join(line.split())


def indent_of(line):
    return len(line) - len(line.lstrip(" \t"))


DEBRIS = re.compile(r"""^\s*(?:"{1,2}|'{1,2}),?\s*$""")  # a stray quote and comma from a broken tool call


def core(lines, debris=False):
    """Lines without leading and trailing blank lines (and, for SEARCH, without a last line of tool-call debris)."""
    lines = list(lines)
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
    for line in text.splitlines():
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
    when there is nothing to undo. Only used when the escaped form is not in the file."""
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
        return [i for i in range(len(file_lines) - n + 1) if file_lines[i:i + n] == search_lines]
    fn = [norm(x) for x in file_lines]
    sn = [norm(x) for x in search_lines]
    return [i for i in range(len(file_lines) - n + 1) if fn[i:i + n] == sn]


def closest(file_lines, search_lines, top=3):
    """(score, start, end) of the closest windows of n-1..n+1 lines, best first, non-overlapping."""
    target = "\n".join(norm(x) for x in search_lines)
    fn = [norm(x) for x in file_lines]
    sn = [norm(x) for x in search_lines]
    n = len(search_lines)
    cands = []
    floor = MIN_SCORE - 0.3
    # Only score windows near a line that matches a SEARCH line: exactly (whitespace aside) for a distinctive line,
    # or, for the longest SEARCH line, closely (similarity >= 0.7). Keeps a 5,000-line file to well under a second.
    where = {}
    for p, x in enumerate(fn):
        if len(x) >= 6:
            where.setdefault(x, []).append(p)
    starts = set()
    for k, x in enumerate(sn):
        for p in where.get(x, ()):
            starts.update(range(p - k - 1, p - k + 2))
    longest = max(range(n), key=lambda k: len(sn[k]))
    for p, x in enumerate(fn):
        sm = difflib.SequenceMatcher(None, sn[longest], x, autojunk=False)
        if sm.real_quick_ratio() >= 0.7 and sm.quick_ratio() >= 0.7 and sm.ratio() >= 0.7:
            starts.update(range(p - longest - 1, p - longest + 2))
    # cheap pass: line-level similarity of every candidate window; then character-level only for the best dozen
    rough = []
    for size in sorted({max(1, n - 1), n, n + 1}):
        for i in sorted(s for s in starts if 0 <= s <= len(file_lines) - size):
            rough.append((difflib.SequenceMatcher(None, sn, fn[i:i + size], autojunk=False).ratio(), i, i + size))
    rough.sort(key=lambda c: (-c[0], c[1]))
    for _, i, j in rough[:12]:
        if n > MAX_FUZZY_LINES:  # long: line-level score only (for showing the closest lines, never for applying)
            cands.append((_, i, j))
            continue
        r = difflib.SequenceMatcher(None, target, "\n".join(fn[i:j]), autojunk=False).ratio()
        if r >= floor:
            cands.append((r, i, j))
    cands.sort(key=lambda c: (-c[0], c[1]))
    picked = []
    for c in cands:
        if all(c[2] <= p[1] or c[1] >= p[2] for p in picked):
            picked.append(c)
        if len(picked) == top:
            break
    return picked


def reindent(lines, shift):
    out = []
    for x in lines:
        if not x.strip():
            out.append("")
        elif shift > 0:
            out.append(" " * shift + x)
        elif shift < 0:
            out.append(x[min(-shift, indent_of(x)):])
        else:
            out.append(x)
    return out


def merge(window, search_lines, replace_lines):
    """Apply the SEARCH->REPLACE change to window (the file's lines): lines SEARCH and REPLACE share are taken from
    the file, so a copy error in SEARCH is not written back; changed lines come from REPLACE, re-indented to the
    file."""
    first_s = next((x for x in search_lines if x.strip()), "")
    first_w = next((x for x in window if x.strip()), "")
    shift = indent_of(first_w) - indent_of(first_s)
    replace_lines = reindent(replace_lines, shift)
    search_ind = reindent(search_lines, shift)
    n = len(search_ind)
    # A three-way merge with SEARCH as the base: the file's side (window) and the agent's side (REPLACE) each differ
    # from it; take the agent's changes, and everything else as the file has it.
    # File side: the window line(s) standing for each SEARCH line, and window lines SEARCH left out.
    w_of = [[] for _ in range(n)]          # window lines for SEARCH line k (empty: not in the file)
    w_before = [[] for _ in range(n + 1)]  # window lines SEARCH does not have, before SEARCH line k
    sm_sw = difflib.SequenceMatcher(None, [norm(x) for x in search_ind], [norm(x) for x in window], autojunk=False)
    for tag, i1, i2, j1, j2 in sm_sw.get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):  # same lines, or copy-error variants
            for k in range(i2 - i1):
                w_of[i1 + k] = [window[j1 + k]]
        elif tag == "replace":
            w_of[i1] = window[j1:j2]  # unequal block: the file's lines stand for the whole SEARCH block
        elif tag == "insert":
            w_before[i1].extend(window[j1:j2])
        # delete: SEARCH lines the file does not have; nothing from the file
    # Agent side: which SEARCH lines REPLACE keeps, and what it puts in place of the rest.
    keep = [False] * n
    r_at = [[] for _ in range(n + 1)]      # REPLACE lines that go before SEARCH line k (or at the end)
    sm_sr = difflib.SequenceMatcher(None, search_ind, replace_lines, autojunk=False)  # both the agent's: exact
    for tag, i1, i2, j1, j2 in sm_sr.get_opcodes():
        if tag == "equal":
            for k in range(i1, i2):
                keep[k] = True
        elif tag in ("replace", "insert"):
            r_at[i1].extend(replace_lines[j1:j2])
        # delete: those SEARCH lines go
    out = []
    for k in range(n + 1):
        if w_before[k] and r_at[k]:
            raise Conflict(w_before[k][0])  # the file has lines SEARCH left out exactly where REPLACE adds lines
        if k < n and not keep[k] and len(w_of[k]) > 1:
            raise Conflict(w_of[k][0])      # REPLACE changes a block the file has in a different form
        out.extend(w_before[k])
        out.extend(r_at[k])
        if k < n and keep[k]:
            out.extend(w_of[k])
    return out


class Conflict(Exception):
    """SEARCH and the file differ where REPLACE makes its change, so where the change goes is a guess."""


def already_there(file_lines, r_lines, s_lines, i, j):
    """A message when REPLACE, which adds lines SEARCH does not have, is already in the file around lines i..j (so
    applying it again would add them twice); else None."""
    if not r_lines or len(r_lines) <= len(s_lines):
        return None
    for h in find_lines(file_lines, r_lines, False):
        if h <= j and h + len(r_lines) >= i:
            return "REPLACE is already in the file at line %d: this change is done; move on." % (h + 1)
    return None


def apply(content, search, replace, near=None):
    """(new_content, message) or (None, message)."""
    eol = "\r\n" if "\r\n" in content else "\n"
    trailing = content.endswith(("\n", "\r\n"))
    file_lines = content.splitlines()
    attempts = [(search, replace, "")]
    un_s = unescape(search)
    if un_s is not None:
        attempts.append((un_s, unescape(replace) or replace, " after undoing escapes"))
    for s_text, r_text, how in attempts:
        s_lines, r_lines = core(s_text.splitlines(), debris=True), r_text.splitlines()
        if not s_lines:
            return None, "SEARCH is empty: copy one to three lines from read_file into it."
        for exact in (True, False):
            hits = find_lines(file_lines, s_lines, exact)
            if len(hits) > 1 and near:
                hits = sorted(hits, key=lambda i: abs(i + 1 - near))[:1]
            if len(hits) == 1:
                i = hits[0]
                done = already_there(file_lines, core(r_lines), s_lines, i, i + len(s_lines))
                if done:
                    return None, done
                window = file_lines[i:i + len(s_lines)]
                try:
                    new = merge(window, s_lines, core(r_lines) if r_lines else [])
                except Conflict:
                    return None, "SEARCH and the file differ where REPLACE makes its change; nothing changed."
                if new == window:
                    return None, "REPLACE is the same as lines %d-%d: nothing to change." % (i + 1, i + len(s_lines))
                return finish(file_lines, i, i + len(s_lines), new, eol, trailing,
                              "matched lines %d-%d%s%s" % (i + 1, i + len(s_lines),
                                                           "" if exact else " ignoring spaces", how))
            if len(hits) > 1:
                where = ", ".join(str(i + 1) for i in hits[:10])
                return None, ("SEARCH occurs at lines %s. Run again with --near LINE (the line you mean, from "
                              "read_file)." % where)
    # already applied?
    for _, r_text, _ in attempts:
        r_lines = core(r_text.splitlines())
        if r_lines and r_text.strip() != search.strip() and len(find_lines(file_lines, r_lines, False)) >= 1:
            i = find_lines(file_lines, r_lines, False)[0]
            return None, "REPLACE is already in the file at line %d: this change is done; move on." % (i + 1)
    # closest block
    s_text, r_text, how = attempts[-1]
    s_lines, r_lines = core(s_text.splitlines(), debris=True), core(r_text.splitlines())
    cands = closest(file_lines, s_lines)
    long_search = len(s_lines) > MAX_FUZZY_LINES
    by_near = False
    if cands and near and not long_search:
        cands.sort(key=lambda c: (-(c[0] >= MIN_SCORE), abs(c[1] + 1 - near)))
        by_near = cands[0][0] >= MIN_SCORE and abs(cands[0][1] + 1 - near) <= 30
    clear = len(cands) == 1 or (len(cands) > 1 and cands[0][0] - cands[1][0] >= MIN_GAP) or by_near
    if cands and not long_search and cands[0][0] >= MIN_SCORE and clear:
        score, i, j = cands[0]
        try:
            new = merge(file_lines[i:j], s_lines, r_lines)
        except Conflict:
            return None, "\n".join(
                ["The closest place, lines %d-%d (similarity %.2f), has lines SEARCH leaves out where REPLACE makes "
                 "its change; nothing changed. The file there:" % (i + 1, j, score)]
                + ["%5d  %s" % (k + 1, file_lines[k]) for k in range(i, j)]
                + ["Copy SEARCH from these lines (without the numbers) and run again."])
        if new == file_lines[i:j]:
            return None, "REPLACE already matches lines %d-%d: this change is done; move on." % (i + 1, j)
        return finish(file_lines, i, j, new, eol, trailing,
                      "closest match lines %d-%d (similarity %.2f)%s" % (i + 1, j, score, how))
    if long_search:
        msg = ["SEARCH has %d lines and is not in the file; a close match is tried only for %d lines or fewer. "
               "Nothing changed." % (len(s_lines), MAX_FUZZY_LINES)]
    else:
        msg = ["SEARCH is not in the file and no place is clearly closest; nothing changed."]
    for score, i, j in cands:
        msg.append("--- lines %d-%d (similarity %.2f):" % (i + 1, j, score))
        msg.extend("%5d  %s" % (k + 1, file_lines[k]) for k in range(i, j))
    msg.append("Copy SEARCH from the lines above (without the numbers) and run again.")
    return None, "\n".join(msg)


def finish(file_lines, i, j, new, eol, trailing, how):
    lines = file_lines[:i] + new + file_lines[j:]
    content = eol.join(lines) + (eol if trailing else "")
    diff = difflib.unified_diff(file_lines[i:j], new, "before", "after", lineterm="", n=1)
    return content, how + "\n" + "\n".join(list(diff)[2:])


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
    text = (stdin if stdin is not None else sys.stdin).read()
    blocks = parse_blocks(text)
    if not blocks:
        print("No SEARCH/REPLACE block on stdin. Write:\n"
              "<<<<<<< SEARCH\nold lines\n=======\nnew lines\n>>>>>>> REPLACE")
        return 2
    with open(path, encoding="utf-8", newline="") as f:
        content = f.read()
    code = 0
    for search, replace in blocks:
        new, msg = apply(content, search, replace, near)
        print(msg)
        if new is None:
            code = 1
            continue
        content = new
    if not dry and code == 0:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        print("written: %s" % argv[0])
    elif code:
        print("nothing written")
    return code


if __name__ == "__main__":
    sys.exit(main())
