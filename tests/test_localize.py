"""The offline localization study's pure functions (#112), without the competition's graphs or embeddings."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("localize", ROOT / "analysis" / "localize.py")
localize = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(localize)


def test_module_of_drops_the_src_root_and_init():
    assert localize.module_of("src/requests/models.py") == "requests.models"
    assert localize.module_of("rich/__init__.py") == "rich"
    assert localize.module_of("docs_src/events/tutorial002_py310.py") == "events.tutorial002_py310"


def test_gold_of_takes_the_changed_files_and_functions_and_leaves_tests_out():
    patch = ("--- a/rich/console.py\n+++ b/rich/console.py\n@@ -10,3 +10,4 @@ def print_json(\n"
             "--- a/tests/test_console.py\n+++ b/tests/test_console.py\n@@ -1 +1 @@ def test_x(\n")
    mods, funcs = localize.gold_of(patch)
    assert mods == {"rich.console"}
    assert "print_json" in funcs


def test_identifiers_keeps_code_like_strings_and_drops_plain_words():
    ids = localize.identifiers("Calling `Console.print_json` fails in rich.pretty when indent_guides is set; "
                               "the output looks wrong.")
    assert "Console.print_json" in ids and "rich.pretty" in ids and "indent_guides" in ids
    assert "output" not in ids and "wrong" not in ids


def test_rrf_rewards_agreement():
    s = localize.rrf(["a", "b", "c"], ["b", "a", "d"])
    assert max(s, key=s.get) in ("a", "b") and s["a"] == s["b"] > s["c"]
