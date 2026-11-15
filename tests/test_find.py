"""The edit-fallback skill's find.py (#122): the repository's Python files ranked by the issue's names, tests, docs
and examples left out, with matching line numbers. On the 129 development tasks it put the reference fix's file first
in 43, against 12 for the prompt's grep | head -40 (analysis/find_ranks.csv). Run: python -m pytest -q tests
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
