"""The numbers in docs/fallback-scripts-study.md, from the CSVs the study wrote (#122): the competition's development
set (find_ranks.csv, fallback_synth.csv, fallback_replay.csv), then this organisation's own repositories as the
generality check (find_ranks_own.csv, fallback_synth_own.csv). Pairs are compared with the exact McNemar test
(two-sided binomial on the discordant pairs).

usage: fallback_summary.py [analysis dir]   (default: this script's folder)
"""
import csv
import sys
from collections import Counter
from math import comb
from pathlib import Path

DAMAGES = ["exact", "escaped", "copy_s", "indent", "drop_line", "junk_tail", "not_in_file", "already_done"]


def mcnemar(b, c):
    """Exact two-sided p for b pairs only the first method got and c only the second."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def hit(row, col, k):
    return row[col] != "" and int(row[col]) <= k


def repos_of(rows):
    return list(dict.fromkeys(x["repo_name"] for x in rows))


def find_table(rows):
    out = ["| Repository | Tasks | Top 1: grep / find.py | Top 3 | Top 8 |", "|---|---|---|---|---|"]
    for repo in repos_of(rows) + ["all"]:
        r = [x for x in rows if repo == "all" or x["repo_name"] == repo]
        cells = [f"{sum(hit(x, 'grep_file_rank_num', k) for x in r)} / "
                 f"{sum(hit(x, 'find_file_rank_num', k) for x in r)}" for k in (1, 3, 8)]
        out.append(f"| {repo} | {len(r)} | " + " | ".join(cells) + " |")
    for k in (1, 8):
        b = sum(hit(x, "grep_file_rank_num", k) and not hit(x, "find_file_rank_num", k) for x in rows)
        c = sum(hit(x, "find_file_rank_num", k) and not hit(x, "grep_file_rank_num", k) for x in rows)
        out.append(f"\nTop {k}: only grep {b}, only find.py {c}, p = {mcnemar(b, c):.2g}")
    out.append(f"Slowest find.py search: {max(float(x['find_seconds']) for x in rows):.2f} s")
    return "\n".join(out)


def synth_table(rows):
    def cwr(r, col):
        c = Counter(x[col] for x in r)
        return f"{c['correct']} / {c['wrong']} / {c['refused']}"
    out = ["| Damage | Edits | edit_file: correct / wrong / refused | edit.py |", "|---|---|---|---|"]
    for d in DAMAGES + ["all"]:
        r = [x for x in rows if d == "all" or x["damage_code"] == d]
        out.append(f"| {d} | {len(r)} | {cwr(r, 'edit_file_outcome_code')} | {cwr(r, 'edit_py_outcome_code')} |")
    out += ["", "| Repository | Edits | edit_file | edit.py |", "|---|---|---|---|"]
    for repo in repos_of(rows):
        r = [x for x in rows if x["repo_name"] == repo]
        out.append(f"| {repo} | {len(r)} | {cwr(r, 'edit_file_outcome_code')} | {cwr(r, 'edit_py_outcome_code')} |")
    for what in ("correct", "wrong"):
        b = sum(x["edit_file_outcome_code"] == what and x["edit_py_outcome_code"] != what for x in rows)
        c = sum(x["edit_py_outcome_code"] == what and x["edit_file_outcome_code"] != what for x in rows)
        out.append(f"\n{what}: only edit_file {b}, only edit.py {c}, p = {mcnemar(b, c):.2g}")
    out += ["", "| SEARCH lines | Damaged edits | edit.py correct / wrong / refused |", "|---|---|---|"]
    for lo, hi in [(1, 3), (4, 6), (7, 8), (9, 12), (13, 20), (21, 10 ** 6)]:
        r = [x for x in rows if lo <= int(x["search_line_count"]) <= hi and x["damage_code"] != "exact"]
        out.append(f"| {lo}-{hi if hi < 10 ** 6 else ''} | {len(r)} | {cwr(r, 'edit_py_outcome_code')} |")
    secs = sorted(float(x["edit_py_seconds"]) for x in rows)
    out.append(f"\nedit.py seconds: slowest {secs[-1]:.2f}, 99th percentile {secs[int(len(secs) * 0.99)]:.3f}")
    return "\n".join(out)


def replay_table(rows):
    out = ["| Failure | Failed edits | edit.py, no hint | edit.py, --near the last read |", "|---|---|---|---|"]
    for f in ("not_found", "multiple"):
        r = [x for x in rows if x["replay_failure_code"] == f]
        a = ", ".join(f"{k} {v}" for k, v in Counter(x["edit_py_outcome_code"] for x in r).most_common())
        b = ", ".join(f"{k} {v}" for k, v in Counter(x["edit_py_near_outcome_code"] or "no read"
                                                       for x in r).most_common())
        out.append(f"| {f} | {len(r)} | {a} | {b} |")
    labelled = [x for x in rows if x["later_fix_start_num"]]
    out.append(f"\nFailed edits the agent later fixed itself: {len(labelled)} of {len(rows)}")
    return "\n".join(out)


def main(folder):
    folder = Path(folder)
    print("## The competition's development set\n")
    print(find_table(list(csv.DictReader(open(folder / "find_ranks.csv")))))
    print()
    print(synth_table(list(csv.DictReader(open(folder / "fallback_synth.csv")))))
    print()
    print(replay_table(list(csv.DictReader(open(folder / "fallback_replay.csv")))))
    print("\n## This organisation's repositories (the generality check)\n")
    print(find_table(list(csv.DictReader(open(folder / "find_ranks_own.csv")))))
    print()
    print(synth_table(list(csv.DictReader(open(folder / "fallback_synth_own.csv")))))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent)
