"""The edit-fallback skill's find.py (#122): the repository's Python files ranked by the issue's names, tests, docs
and examples left out, with matching line numbers. On the 129 development tasks it put the reference fix's file first
in 39, against 12 for the prompt's grep | head -40 (analysis/find_ranks.csv). Run: python -m pytest -q tests
"""

import contextlib
import importlib.util
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True   # no __pycache__ in skills/: a .pyc in the submission is refused
spec = importlib.util.spec_from_file_location("fallback_find",
                                              ROOT / "skills" / "edit-fallback" / "scripts" / "find.py")
find = importlib.util.module_from_spec(spec)
spec.loader.exec_module(find)


def _repo(tmp_path):
    files = {
        "pkg/__init__.py": "from .table import Table\n",
        "pkg/table.py": "class Table:\n    def add_row(self, *cells):\n        self.rows.append(cells)\n",
        "pkg/console.py": "from .table import Table\n\ndef render(t: Table):\n    return t.add_row\n",
        "pkg/util.py": "def helper():\n    return 'Table'\n",
        "tests/test_table.py": "from pkg.table import Table\n\ndef test_add_row():\n    Table().add_row(1)\n",
        "docs_src/example.py": "from pkg import Table\nTable().add_row('a')\n",
        "pkg/errors.py": "MESSAGE = 'row has too many cells'\n",
    }
    for rel, text in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return tmp_path


def test_the_file_that_defines_the_names_comes_first(tmp_path):
    found = find.scan(str(_repo(tmp_path)), ["Table.add_row", "Table"])
    assert found[0][2] == "pkg/table.py"


def test_tests_docs_and_examples_come_after_the_code(tmp_path):
    found = find.scan(str(_repo(tmp_path)), ["add_row"])
    order = [r[2] for r in found]
    assert order.index("tests/test_table.py") > order.index("pkg/console.py")
    assert order.index("docs_src/example.py") > order.index("pkg/console.py")


def test_a_dotted_module_name_ranks_its_file(tmp_path):
    found = find.scan(str(_repo(tmp_path)), ["pkg.console"])
    assert found and found[0][2] == "pkg/console.py"


def test_a_quoted_message_is_searched_as_text(tmp_path):
    found = find.scan(str(_repo(tmp_path)), ["too many cells"])
    assert [r[2] for r in found] == ["pkg/errors.py"]


def test_main_prints_files_with_line_numbers_and_leaves_tests_out(tmp_path, monkeypatch):
    monkeypatch.chdir(_repo(tmp_path))
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert find.main(["add_row"]) == 0
    text = out.getvalue()
    assert text.splitlines()[0].startswith("pkg/table.py")
    assert "  2: def add_row(self, *cells):" in text
    assert "tests/test_table.py" not in text


def test_main_searches_the_current_git_checkout_first(tmp_path, monkeypatch):
    """In the subprocess sandbox a command runs in the workspace, but there is no real /workspace."""
    repo = _repo(tmp_path)
    (repo / ".git").mkdir()
    monkeypatch.chdir(repo)
    assert find.root_dir() == str(repo)


def test_no_match_says_so_and_exits_1(tmp_path, monkeypatch):
    monkeypatch.chdir(_repo(tmp_path))
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert find.main(["NoSuchName"]) == 1
    assert "No Python file contains NoSuchName" in out.getvalue()


def test_no_names_prints_usage_and_exits_2():
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert find.main([]) == 2
    assert "usage" in out.getvalue()


def test_output_is_short(tmp_path, monkeypatch):
    repo = _repo(tmp_path)
    for k in range(40):
        (repo / "pkg" / f"mod{k}.py").write_text("def add_row():\n    pass\n" * 30)
    monkeypatch.chdir(repo)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        find.main(["add_row"])
    assert len(out.getvalue()) < 2500
    assert f"{find.MAX_FILES}" and out.getvalue().count("(names") == find.MAX_FILES


def test_every_name_on_a_line_is_credited(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "render.py").write_text("def render_table(width, padding):\n    return width + padding\n")
    found = find.scan(str(tmp_path), ["render_table", "width", "padding"])
    assert found[0][4] == 3


def test_code_under_scripts_counts_and_left_out_files_are_counted(tmp_path, monkeypatch):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "pkg").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "scripts" / "load_claims.py").write_text("def load_claims(path):\n    return path\n")
    (tmp_path / "pkg" / "run.py").write_text("from scripts.load_claims import load_claims\n")
    (tmp_path / "tests" / "test_load.py").write_text("from scripts.load_claims import load_claims\n")
    found = find.scan(str(tmp_path), ["load_claims"])
    assert found[0][2] == "scripts/load_claims.py"
    monkeypatch.chdir(tmp_path)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        find.main(["load_claims"])
    assert "1 more in tests, docs or examples" in out.getvalue()


def test_output_is_capped_even_with_long_paths(tmp_path, monkeypatch):
    deep = tmp_path / ("a_very_long_directory_name_for_testing_" * 5)
    deep.mkdir()
    for k in range(20):
        (deep / (f"module_with_a_long_name_number_{k}_" * 3 + ".py")).write_text("def add_row():\n    add_row()\n" * 5)
    monkeypatch.chdir(tmp_path)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        find.main(["add_row"])
    assert len(out.getvalue()) <= 4000
