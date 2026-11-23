"""Find the code an issue is about: the repository's Python files ranked by the names you give.

usage: python3 /tmp/h/find.py NAME [NAME ...]
       python3 /tmp/h/find.py --tests FILE_YOU_CHANGED NAME [NAME ...]
       python3 /tmp/h/find.py --show NAME [NAME ...]      (also prints the top functions' code)
       python3 /tmp/h/find.py --read FILE:START-END [FILE:START-END ...]   (several ranges in one call)

NAME is a function, class, module or variable name from the issue (`Table.add_row`, `rich.table`, `get_openapi`), or
a short quoted error message. Tests, docs and examples are left out (they are listed last, only if nothing else
matches). Files are ranked by how many of the names they contain, whether they define them (def/class/assignment),
and whether a dotted name is their module path; each comes with its matching lines and their numbers, for read_file.
The output opens with "Functions to read first:": up to three functions or classes, by path and line, that the
names point to (named by a NAME counts three times what using it does; tests, docs and examples left out).
With --tests, after an edit, it prints only the test files to run for the file you changed (`Tests to run:
python3 -m pytest ... -x -q`): up to three, that file's own test_<stem>.py first, then by how many of the names they
mention.
Python 3.8+, standard library only; reads /workspace (or the current directory).
"""
import ast
import math
import os
import re
import sys

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".tox", ".venv", "venv", "build", "dist", ".eggs", "site-packages"}
LOW_DIRS = {"tests", "test", "testing", "docs", "docs_src", "doc", "examples", "example"}  # scripts/ is code
MAX_CHARS = 4000  # run_command shows 5,000
MAX_FILES = 8
MAX_LINES = 3
MAX_FILE_BYTES = 2000000
TEST_DIRS = {"tests", "test", "testing"}
NOT_TEST_DIRS = {"docs", "docs_src", "doc", "examples", "example"}
MAX_TESTS = 3
MAX_FUNCS = 3
SHOW_FUNC_LINES = 40  # --show: lines of each function's code (#206)
SHOW_TOTAL_CHARS = 4900  # --show / --read: the whole output, under run_command's 5,000
SHOW_RANK_CHARS = 1800  # --show: the ranking part, so the code has room


def is_low(rel):
    parts = rel.split("/")
    name = parts[-1]
    return (any(p in LOW_DIRS for p in parts[:-1]) or name.startswith("test_") or name.endswith("_test.py")
            or name == "conftest.py")


def is_test(rel):
    """A test module (not conftest.py, and not under docs or examples)."""
    parts = rel.split("/")
    name = parts[-1]
    if name == "conftest.py" or any(p in NOT_TEST_DIRS for p in parts[:-1]):
        return False
    return any(p in TEST_DIRS for p in parts[:-1]) or name.startswith("test_") or name.endswith("_test.py")


def is_tooling(rel):
    """Top-level scripts/ and benchmarks/: code (pipeline repositories keep theirs there), ranked a little lower,
    since in library repositories they are release and docs tooling."""
    return rel.split("/")[0] in ("scripts", "benchmarks")


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
                on_line, line_def = False, False
                for shown, pat, defpat in pats:  # every name on the line counts
                    if pat.search(line):
                        matched.add(shown)
                        hits += 1
                        on_line = True
                        if defpat and defpat.search(line):
                            defined.add(shown)
                            line_def = True
                if on_line:
                    shown_lines.append((0 if line_def else 1, no, line.strip()))
            bonus = module_path_bonus(rel, names)
            if not matched and not bonus:
                continue
            if not matched:  # the file is the named module but never says its own name
                matched.add(rel)
                shown_lines.append((1, 1, lines[0].strip() if lines else ""))
            score = 3 * len(matched) + 4 * len(defined) + 3 * bonus + min(hits, 20) / 10.0 - 2 * is_tooling(rel)
            found.append((is_low(rel), -score, rel, sorted(shown_lines)[:MAX_LINES], len(matched), len(defined), hits))
    found.sort(key=lambda r: (r[0], r[1], len(r[2]), r[2]))
    return found


def _defs(text):
    """Each function and class in a file: (name, first line, last line, kind)."""
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return []
    out = []
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.append((n.name, n.lineno, getattr(n, "end_lineno", None) or n.lineno,
                        "class" if isinstance(n, ast.ClassDef) else "def"))
    return out


def rank_functions(root, names, limit=MAX_FUNCS):
    """The functions and classes the names point to (#44): a function named by a NAME scores 3 x idf, one whose body
    uses a NAME 1 x idf, idf counted over the repository's functions. Tests, docs and examples are left out (a class
    is read by its first 30 lines, so a large class does not win on its methods' bodies). Returns
    [(rel, line, kind, name, score)], best first."""
    wanted = []
    for shown, needle, kind in terms(names):
        if kind == "name" and needle not in wanted:
            wanted.append(needle)
    if not wanted:
        return []
    pats = {w: re.compile(r"(?<!\w)" + re.escape(w) + r"(?!\w)") for w in wanted}
    nodes = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(filenames):
            if not fn.endswith(".py"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if is_low(rel):
                continue
            try:
                if os.path.getsize(full) > MAX_FILE_BYTES:
                    continue
                with open(full, encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except OSError:
                continue
            lines = text.splitlines()
            for name, first, last, kind in _defs(text):
                body = "\n".join(lines[first - 1:min(last, first + 29) if kind == "class" else last])
                used = {w for w, pat in pats.items() if pat.search(body)}
                if used or name in pats:
                    nodes.append((rel, first, kind, name, used))
    if not nodes:
        return []
    total = len(nodes)
    df = {w: sum(1 for n in nodes if w in n[4] or n[3] == w) for w in wanted}
    ranked = []
    for rel, first, kind, name, used in nodes:
        score = 0.0
        for w in wanted:
            if not df[w]:
                continue
            idf = math.log((total + 1) / df[w])
            if name == w:
                score += 3 * idf
            elif w in used:
                score += idf
        if score > 0:
            ranked.append((rel, first, kind, name, round(score, 3)))
    ranked.sort(key=lambda r: (-r[4], is_tooling(r[0]), len(r[0]), r[0], r[1]))
    return ranked[:limit]


def test_files(root, found, top_rel, limit=MAX_TESTS):
    """The test files to run for top_rel, the file changed (#170): ranked by how many of the names they mention,
    its own test_<stem>.py raised by two; then by matches, then the shorter path. Those that mention no name are left
    out, except test_<stem>.py. Measured on the 129 development tasks in analysis/find_ranks.csv
    (find_tests_rank_num), with the reference fix's file as the file changed."""
    want = None
    if top_rel:
        stem = os.path.basename(top_rel)[:-3].lstrip("_")
        want = "test_%s.py" % stem if stem and stem != "init" else None
    scored = {}
    for r in found:
        rel, names_matched, hits = r[2], r[4], r[6]
        if is_test(rel) and names_matched and rel != top_rel:
            scored[rel] = (names_matched + 2 * (os.path.basename(rel) == want), hits)
    if want:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
            if want in filenames:
                rel = os.path.relpath(os.path.join(dirpath, want), root).replace(os.sep, "/")
                if is_test(rel) and rel not in scored:
                    scored[rel] = (2, 0)
    order = sorted(scored, key=lambda rel: (-scored[rel][0], -scored[rel][1], len(rel), rel))
    return order[:limit]


def root_dir():
    """The repository: the current folder when it is a git checkout (the subprocess sandbox runs commands in the
    workspace but has no real /workspace), else /workspace, else the current folder."""
    if os.path.isdir(".git"):
        return os.getcwd()
    return "/workspace" if os.path.isdir("/workspace") else os.getcwd()


# Stopwords and stems used only as generic English; never tuned on a reference patch (#106).
_BEHAVIOR_STOP = {
    "the", "and", "for", "that", "with", "this", "from", "have", "been", "were", "when", "what",
    "which", "where", "there", "their", "about", "into", "also", "than", "then", "them", "they",
    "would", "could", "should", "will", "just", "like", "some", "such", "only", "over", "after",
    "before", "between", "under", "again", "further", "once", "here", "both", "each", "few", "more",
    "most", "other", "same", "than", "too", "very", "can", "did", "does", "doing", "has", "had",
    "having", "not", "but", "out", "off", "own", "all", "any", "because", "while", "during", "issue",
    "issues", "bug", "fix", "fixes", "fixed", "error", "errors", "please", "thanks", "http", "https",
    "github", "com", "www", "pull", "request", "discussion", "discussions", "ref", "refs", "same",
    "using", "used", "use", "via", "per", "see", "add", "added", "adding", "make", "made", "need",
    "needs", "want", "wants", "try", "tried", "still", "already", "also", "even", "much", "many",
}


def _stem(word):
    """Very light suffix stem; stdlib only."""
    w = word.lower()
    # scopes→scope, caches→cache (not scop/cach)
    if len(w) > 5 and w.endswith("es") and w[-3] in "bcdfgkp":
        return w[:-1]
    for suf in ("ingly", "edly", "ing", "ers", "ies", "ied", "ed", "ly", "es", "s"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            if suf == "ies":
                return w[:-3] + "y"
            return w[: -len(suf)]
    return w


def code_identifier_count(names):
    """How many NAME args look like code identifiers (not free-text error strings)."""
    n = 0
    for raw in names:
        raw = (raw or "").strip().strip("`'\"")
        if raw and " " not in raw and re.match(r"^[A-Za-z_][\w.]*$", raw):
            n += 1
    return n


def issue_literals(issue_text):
    """Quoted / backticked spans long enough to search as literal strings."""
    text = issue_text or ""
    out = []
    for m in re.finditer(r"[\"']([^\"'\n]{6,120})[\"']|`([^`\n]{6,120})`", text):
        s = (m.group(1) or m.group(2) or "").strip()
        if s and s not in out:
            out.append(s)
    return out


def behavior_words(issue_text):
    """Stemmed content words from the issue; not code-shaped tokens, not stopwords."""
    text = issue_text or ""
    words = []
    for tok in re.findall(r"[A-Za-z][A-Za-z0-9_]{3,}", text):
        if "_" in tok or re.search(r"[a-z][A-Z]", tok) or "." in tok:
            continue
        low = tok.lower()
        if low in _BEHAVIOR_STOP or low.startswith("http"):
            continue
        stem = _stem(low)
        if stem in _BEHAVIOR_STOP or len(stem) < 4:
            continue
        if stem not in words:
            words.append(stem)
    return words[:24]


def _option_tokens(line):
    return re.findall(r"--[a-z][\w-]*|[a-z][\w-]*(?:_|=)[\w-]+", line.lower())


def behavior_scan(root, issue_text):
    """Score files by literals and stemmed behavior words against names, docs, comments and options (#106)."""
    literals = issue_literals(issue_text)
    stems = behavior_words(issue_text)
    if not literals and not stems:
        return []
    lit_pats = [(s, re.compile(re.escape(s), re.I)) for s in literals]
    stem_pats = [(s, re.compile(r"(?<![a-z0-9_])" + re.escape(s) + r"[a-z]*", re.I)) for s in stems]
    scored = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(filenames):
            if not fn.endswith(".py"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if is_low(rel):
                continue
            try:
                if os.path.getsize(full) > MAX_FILE_BYTES:
                    continue
                with open(full, encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except OSError:
                continue
            lines = text.splitlines()
            file_score = 0.0
            best_func, best_func_score, reasons = "", 0.0, []
            mod = rel[:-3].replace("/", ".").split(".")[-1]
            for stem, pat in stem_pats:
                if _stem(mod) == stem or pat.search(mod):
                    file_score += 4
                    reasons.append("module~%s" % stem)
            for lit, pat in lit_pats:
                if pat.search(text):
                    file_score += 8
                    reasons.append("literal")
                    break
            for name, first, last, kind in _defs(text):
                body = "\n".join(lines[first - 1:last])
                fscore = 0.0
                why = []
                for stem, pat in stem_pats:
                    if _stem(name) == stem or pat.search(name):
                        fscore += 6
                        why.append("name~%s" % stem)
                    elif pat.search(body):
                        # docstring / comment / option / use in body
                        hit_doc = False
                        for no in range(first, min(last, first + 40) + 1):
                            if no - 1 >= len(lines):
                                break
                            line = lines[no - 1]
                            stripped = line.strip()
                            if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''") \
                                    or '"""' in line or "'''" in line:
                                if pat.search(line):
                                    fscore += 3
                                    why.append("doc/comment~%s" % stem)
                                    hit_doc = True
                                    break
                            for opt in _option_tokens(line):
                                if pat.search(opt):
                                    fscore += 3
                                    why.append("option~%s" % stem)
                                    hit_doc = True
                                    break
                            if hit_doc:
                                break
                        if not hit_doc and pat.search(body):
                            fscore += 1.5
                            why.append("body~%s" % stem)
                for lit, pat in lit_pats:
                    if pat.search(body):
                        fscore += 5
                        why.append("literal")
                        break
                if fscore > best_func_score:
                    best_func_score, best_func = fscore, name
                    if why:
                        reasons = why[:3]
                file_score += fscore
            if file_score > 0:
                if is_tooling(rel):
                    file_score -= 2
                reason = ", ".join(dict.fromkeys(reasons))[:120] or "behavior match"
                scored[rel] = (file_score, best_func or mod, reason)
    ranked = sorted(scored.items(), key=lambda kv: (-kv[1][0], is_tooling(kv[0]), len(kv[0]), kv[0]))
    return [(rel, func, reason, score) for rel, (score, func, reason) in ranked[:MAX_FILES]]


def rank_for_issue(root, names, issue_text=""):
    """Rank files for an issue. With ≤2 code identifiers, merge identifier scan with behavior/literal fallback."""
    names = [n for n in names if n]
    if code_identifier_count(names) > 2:
        found = scan(root, names)
        main_files = [r for r in found if not r[0]] or found
        funcs = {(r[0], r[3]): r for r in rank_functions(root, names, limit=40)}
        out = []
        for low, neg, rel, lines, nm, nd, hits in main_files[:MAX_FILES]:
            best = next((funcs[k] for k in funcs if k[0] == rel), None)
            func = best[3] if best else (lines[0][2].split()[-1] if lines else "")
            reason = "identifier match (%d names)" % nm
            out.append((rel, func, reason, -neg))
        return out
    id_rows = []
    if names:
        found = scan(root, names)
        main_files = [r for r in found if not r[0]] or found
        for low, neg, rel, lines, nm, nd, hits in main_files[:MAX_FILES]:
            id_rows.append((rel, -neg + 2 * nd, "identifier"))
    beh = behavior_scan(root, issue_text)
    combined = {}
    for rel, score, why in [(r[0], r[1], r[2]) for r in id_rows]:
        combined[rel] = [score, "", why]
    for rel, func, reason, score in beh:
        if rel in combined:
            combined[rel][0] += score
            combined[rel][1] = func or combined[rel][1]
            combined[rel][2] = reason
        else:
            combined[rel] = [score, func, reason]
    # attach best function from identifier defs when behavior gave none
    if names:
        for rel, first, kind, name, sc in rank_functions(root, names, limit=40):
            if rel in combined and not combined[rel][1]:
                combined[rel][1] = name
    ranked = sorted(combined.items(), key=lambda kv: (-kv[1][0], is_tooling(kv[0]), len(kv[0]), kv[0]))
    return [(rel, func or "", reason or "match", score) for rel, (score, func, reason) in ranked[:MAX_FILES]]


def function_source(root, rel, name_or_line):
    """(first, last, lines) of the function or class in REL named NAME, or starting at (or containing) LINE; None if
    there is none (#206)."""
    try:
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError:
        return None
    lines = text.splitlines()
    defs = _defs(text)
    if isinstance(name_or_line, int):
        exact = [d for d in defs if d[1] == name_or_line]
        inside = sorted((d for d in defs if d[1] <= name_or_line <= d[2]), key=lambda d: d[2] - d[1])
        pick = (exact or inside or [None])[0]
    else:
        named = [d for d in defs if d[0] == name_or_line]
        pick = (sorted(named, key=lambda d: d[3] == "class") or [None])[0]
    if pick is None:
        return None
    return pick[1], pick[2], lines


def render_code(root, targets, budget):
    """The code section of --show: each (rel, name_or_line) target's source, line-numbered, at most SHOW_FUNC_LINES
    lines each and BUDGET characters in all (#206)."""
    out, used, seen = ["Code of the functions to read first:"], 0, set()
    used = len(out[0]) + 1
    for rel, key in targets:
        src = function_source(root, rel, key)
        if not src or (rel, src[0]) in seen:
            continue
        first, last, lines = src
        seen.add((rel, first))
        end = min(last, first + SHOW_FUNC_LINES - 1)
        block = ["== %s:%d-%d" % (rel, first, last)]
        block += ["%4d: %s" % (no, lines[no - 1][:200]) for no in range(first, end + 1) if no - 1 < len(lines)]
        if last > end:
            block.append("... (%d more lines: --read %s:%d-%d)" % (last - end, rel, end + 1, last))
        for line in block:
            if used + len(line) + 1 > budget:
                out.append("... (cut)")
                return "\n".join(out)
            out.append(line)
            used += len(line) + 1
    return "\n".join(out) if len(out) > 1 else ""


def read_ranges(root, specs):
    """--read FILE:START-END ...: several ranges in one call, line-numbered, SHOW_TOTAL_CHARS in all (#206)."""
    out, used = [], 0
    for spec in specs:
        m = re.match(r"^(.+):(\d+)-(\d+)$", spec)
        if not m:
            msg = "%s: use FILE:START-END" % spec
            out.append(msg)
            used += len(msg) + 1
            continue
        rel = m.group(1).replace("/workspace/", "").lstrip("./")
        a, b = int(m.group(2)), int(m.group(3))
        try:
            with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
        except OSError:
            msg = "%s: no such file" % rel
            out.append(msg)
            used += len(msg) + 1
            continue
        block = ["== %s:%d-%d" % (rel, a, b)] + ["%4d: %s" % (no, lines[no - 1][:200])
                                                 for no in range(max(1, a), min(b, len(lines)) + 1)]
        for line in block:
            if used + len(line) + 1 > SHOW_TOTAL_CHARS - 12:
                out.append("... (cut)")
                return "\n".join(out)
            out.append(line)
            used += len(line) + 1
    return "\n".join(out)


def main(argv=None):
    names = list(sys.argv[1:] if argv is None else argv)
    show = "--show" in names
    names = [n for n in names if n != "--show"]
    if not names:
        print(__doc__)
        return 2
    root = root_dir()
    if names[0] == "--read":
        if len(names) < 2:
            print(__doc__)
            return 2
        print(read_ranges(root, names[1:]))
        return 0
    if names[0] == "--tests":
        if len(names) < 2:
            print(__doc__)
            return 2
        changed = names[1].replace("/workspace/", "").lstrip("./")
        tests = test_files(root, scan(root, names[2:]) if names[2:] else [], changed)
        if not tests:
            print("No test file found for %s: run the test file that imports its module." % changed)
            return 1
        print("Tests to run: python3 -m pytest %s -x -q" % " ".join(tests))
        return 0
    issue_text = ""
    if names and names[0] == "--issue":
        # Optional: find.py --issue ISSUE.txt NAME...  (behavior fallback when ≤2 identifiers)
        if len(names) < 2:
            print(__doc__)
            return 2
        try:
            with open(names[1], encoding="utf-8", errors="replace") as f:
                issue_text = f.read()
        except OSError:
            issue_text = names[1]
        names = names[2:]
        ranked = rank_for_issue(root, names, issue_text)
        if not ranked:
            label = ", ".join(names) if names else "the issue"
            print("No Python file contains %s. Try a shorter or different name from the issue." % label)
            return 1
        out = []
        for rel, func, reason, score in ranked:
            if func:
                out.append("%s  (%s)  # %s" % (rel, func, reason))
            else:
                out.append("%s  # %s" % (rel, reason))
        text_out = "\n".join(out)
        cap = SHOW_RANK_CHARS if show else MAX_CHARS
        if len(text_out) > cap:
            text_out = text_out[:cap - 20].rsplit("\n", 1)[0] + "\n... (cut)"
        if show:
            code = render_code(root, [(rel, func) for rel, func, _, _ in ranked if func][:MAX_FUNCS],
                               SHOW_TOTAL_CHARS - len(text_out) - 1)
            text_out = text_out + ("\n" + code if code else "")
        print(text_out)
        return 0
    found = scan(root, names)
    if not found:
        print("No Python file contains %s. Try a shorter or different name from the issue." % ", ".join(names))
        return 1
    main_files = [r for r in found if not r[0]]
    low_count = len(found) - len(main_files)
    shown = (main_files or found)[:MAX_FILES]
    out = []
    funcs = rank_functions(root, names)
    if funcs:
        out.append("Functions to read first:")
        out.extend("  %s:%d  %s %s" % (rel, line, kind, name) for rel, line, kind, name, _ in funcs)
    for low, neg, rel, lines, nm, nd, hits in shown:
        out.append("%s  (names %d, defines %d)" % (rel, nm, nd))
        out.extend("  %d: %s" % (no, text[:160]) for _, no, text in lines)
    rest = (len(main_files) if main_files else len(found)) - len(shown)
    if rest > 0:
        out.append("... %d more files" % rest)
    if main_files and low_count:
        out.append("... %d more in tests, docs or examples" % low_count)
    text = "\n".join(out)
    cap = SHOW_RANK_CHARS if show else MAX_CHARS
    if len(text) > cap:
        text = text[:cap - 20].rsplit("\n", 1)[0] + "\n... (cut)"
    if show:
        targets = [(rel, line) for rel, line, _, _, _ in funcs]
        if not targets:
            targets = [(r[2], r[3][0][1]) for r in shown[:MAX_FUNCS] if r[3]]
        code = render_code(root, targets, SHOW_TOTAL_CHARS - len(text) - 1)
        text = text + ("\n" + code if code else "")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
