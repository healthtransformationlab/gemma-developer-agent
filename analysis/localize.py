"""Offline localization study on the competition's development tasks: where does each method rank the code the
reference patch changed? CPU only; reads the competition's own graphs and embeddings (the ones the shipped tools use).

usage: localize.py <tasks.jsonl> <graphs dir> <embeddings dir> [--out results.csv]
"""
# ruff: noqa: B023  the per-task helpers are called inside the loop iteration that defines them
import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

STOP = {"the", "and", "for", "with", "that", "this", "from", "into", "when", "then", "than", "have", "has", "not", "are", "was", "were", "will", "would", "should", "could", "can", "its", "it's", "use", "used", "using", "does", "doesn't", "don't", "also", "like", "just", "only", "more", "most", "some", "such", "each", "other", "which", "while", "where", "what", "why", "how", "all", "any", "but", "one", "two", "get", "set", "new", "add", "none", "true", "false", "self", "cls", "str", "int", "list", "dict", "type", "value", "values", "error", "errors", "issue", "issues", "bug", "fix", "fixes", "fixed", "support", "feature", "request", "return", "returns", "raise", "raises", "import", "python", "version", "file", "files", "test", "tests", "example", "examples", "code", "line", "lines", "output", "input", "default", "option", "options"}
IDENT = re.compile(r"`([^`]+)`|\b([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+)\b|\b([A-Za-z_][A-Za-z0-9_]{2,})\b")


def module_of(path: str) -> str:
    """A file path as the graph's dotted module name (src/ and docs_src/ roots dropped, __init__ dropped)."""
    p = path.removesuffix(".py")
    parts = [x for x in p.split("/") if x]
    if parts and parts[0] in ("src", "docs_src"):
        parts = parts[1:]
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def is_test(name: str) -> bool:
    return name.startswith("tests.") or ".tests." in name or any(c.startswith("test_") or c == "conftest"
                                                                 for c in name.split("."))


def gold_of(patch: str) -> tuple[set, set]:
    """The modules and the function/class names the reference patch changes (test files excluded)."""
    files = [f for f in re.findall(r"^\+\+\+ b/(\S+)", patch, re.MULTILINE) if f.endswith(".py")]
    mods = {module_of(f) for f in files if not is_test(module_of(f))}
    funcs = set(re.findall(r"^@@[^@]*@@\s*(?:async\s+)?(?:def|class)\s+([A-Za-z_]\w*)", patch, re.MULTILINE))
    funcs |= set(re.findall(r"^-\s*(?:async\s+)?(?:def|class)\s+([A-Za-z_]\w*)", patch, re.MULTILINE))
    return mods, funcs


def identifiers(text: str) -> list[str]:
    """The issue's identifier-like strings, as the prompt's regex step would grep for: backticked spans, dotted
    names, and words with an underscore, a capital inside, or a call."""
    out = []
    for m in IDENT.finditer(text):
        tok = m.group(1) or m.group(2) or m.group(3)
        for t in re.findall(r"[A-Za-z_][A-Za-z0-9_.]*", tok):
            t = t.strip(".")
            if not t or t.lower() in STOP or len(t) < 3:
                continue
            last = t.split(".")[-1]
            if m.group(1) or "." in t or "_" in last or re.search(r"[a-z][A-Z]", last) or \
                    re.search(re.escape(t) + r"\(", text):
                out.append(t)
    return list(dict.fromkeys(out))


def node_module(name: str, modules: set) -> str | None:
    parts = name.split(".")
    for i in range(len(parts), 0, -1):
        if ".".join(parts[:i]) in modules:
            return ".".join(parts[:i])
    return None


def file_ranking(node_scores: dict, node_mod: dict) -> list[str]:
    best = {}
    for n, s in node_scores.items():
        m = node_mod.get(n)
        if m is not None and s > best.get(m, -1e9):
            best[m] = s
    return [m for m, _ in sorted(best.items(), key=lambda kv: -kv[1])]


def rrf(*rankings: list, k: int = 60) -> dict:
    score = defaultdict(float)
    for r in rankings:
        for i, x in enumerate(r):
            score[x] += 1 / (k + i + 1)
    return dict(score)


def study(tasks, gdir: Path, edir: Path):
    import numpy as np  # only the study needs it; the tested helpers do not
    rows = []
    for t in tasks:
        key = f"{t['repo'].split('/')[1]}_{t['base_commit']}"
        g = json.loads((gdir / f"{key}.json").read_text())
        emb = np.load(edir / f"{key}.npz")
        names = [n["name"] for n in g["nodes"]]
        text = {n["name"]: n.get("text") or "" for n in g["nodes"]}
        # modules are every dotted prefix that owns a node; the longest one owning a node is its file
        modules = set()
        for n in names:
            parts = n.split(".")
            for i in range(1, len(parts)):
                modules.add(".".join(parts[:i]))
        gold_mods, gold_funcs = gold_of(t["patch"])
        gold_mods_present = {m for m in gold_mods if m in modules}
        node_mod = {}
        for n in names:
            parts = n.split(".")
            # the file is the longest prefix that is a module of a gold file, or else the parent of the symbol
            m = node_module(n, gold_mods_present) or ".".join(parts[:-1])
            node_mod[n] = m
        ids = identifiers(t["problem_statement"])
        # document frequency over node texts, for idf weights
        df = Counter()
        lowered = {n: (n.lower() + "\n" + text[n].lower()) for n in names}
        for i in ids:
            il = i.split(".")[-1].lower()
            df[i] = sum(1 for n in names if il in lowered[n])
        N = len(names)

        def regex_scores(keep_tests: bool) -> dict:
            s = {}
            for n in names:
                if not keep_tests and is_test(n):
                    continue
                last = n.split(".")[-1].lower()
                sc = 0.0
                for i in ids:
                    il = i.split(".")[-1].lower()
                    idf = math.log(1 + N / (1 + df[i]))
                    if last == il or n.lower().endswith("." + i.lower()):
                        sc += 3 * idf
                    elif il in lowered[n]:
                        sc += idf
                if sc > 0:
                    s[n] = sc
            return s

        rx_all = regex_scores(keep_tests=True)
        rx = regex_scores(keep_tests=False)
        seeds = [n for n, _ in sorted(rx.items(), key=lambda kv: -kv[1])[:3]]
        # embedding expansion: cosine to the seeds, as search_similar_code does from a symbol
        vecs = {n: emb[n] for n in names if n in emb.files and not is_test(n)}
        em = {}
        if seeds and vecs:
            M = np.stack(list(vecs.values()))
            M = M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
            S = [emb[s] / (np.linalg.norm(emb[s]) + 1e-9) for s in seeds if s in emb.files]
            if S:
                sims = (M @ np.stack(S).T).max(axis=1)
                em = dict(zip(vecs.keys(), sims.tolist()))
        # graph expansion: the seeds and their one-hop callers and callees, as get_code_neighbors does
        nb = defaultdict(set)
        for e in g["edges"]:
            nb[e["source"]].add(e["target"])
            nb[e["target"]].add(e["source"])
        gr = {}
        for r, s in enumerate(seeds):
            gr[s] = gr.get(s, 0) + 3 - r
            for x in sorted(nb[s]):
                if not is_test(x):
                    gr[x] = gr.get(x, 0) + 1
        r_rx = file_ranking(rx, node_mod)
        r_rx_all = file_ranking(rx_all, node_mod)
        r_em = file_ranking(em, node_mod)
        r_gr = file_ranking(gr, node_mod)
        r_hy = file_ranking(rrf([n for n, _ in sorted(rx.items(), key=lambda kv: -kv[1])],
                                [n for n, _ in sorted(em.items(), key=lambda kv: -kv[1])][:200]), node_mod)
        r_hyg = file_ranking(rrf([n for n, _ in sorted(rx.items(), key=lambda kv: -kv[1])],
                                 [n for n, _ in sorted(gr.items(), key=lambda kv: -kv[1])]), node_mod)

        def rank(r):
            hits = [i for i, m in enumerate(r) if m in gold_mods_present]
            return hits[0] + 1 if hits else None

        def frank(scores):
            order = [n for n, _ in sorted(scores.items(), key=lambda kv: -kv[1])]
            hits = [i for i, n in enumerate(order) if n.split(".")[-1] in gold_funcs and node_mod[n] in gold_mods_present]
            return hits[0] + 1 if hits else None

        rows.append({"instance_id": t["instance_id"], "repo": t["repo"], "identifier_count": len(ids),
                     "gold_file_count": len(gold_mods), "gold_file_present_count": len(gold_mods_present),
                     "regex_with_tests_file_rank": rank(r_rx_all), "regex_file_rank": rank(r_rx),
                     "embedding_file_rank": rank(r_em), "graph_file_rank": rank(r_gr),
                     "hybrid_embedding_file_rank": rank(r_hy), "hybrid_graph_file_rank": rank(r_hyg),
                     "regex_with_tests_function_rank": frank(rx_all), "regex_function_rank": frank(rx)})
    return rows


def summary(rows):
    usable = [r for r in rows if r["gold_file_present_count"]]
    out = {"tasks": len(rows), "usable": len(usable)}
    for col in [c for c in rows[0] if c.endswith("_rank")]:
        for k in (1, 5, 10):
            out[f"{col}@{k}"] = sum(1 for r in usable if r[col] is not None and r[col] <= k)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("tasks"); ap.add_argument("graphs", type=Path); ap.add_argument("embeddings", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    with open(a.tasks) as f:
        tasks = [json.loads(line) for line in f]
    rows = study(tasks, a.graphs, a.embeddings)
    if a.out:
        with open(a.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    s = summary(rows)
    print(f"tasks {s['tasks']}, with a changed file present in the graph {s['usable']}")
    for col in [c for c in rows[0] if c.endswith("_rank")]:
        print(f"{col:34s} @1 {s[col+'@1']:3d}  @5 {s[col+'@5']:3d}  @10 {s[col+'@10']:3d}")
