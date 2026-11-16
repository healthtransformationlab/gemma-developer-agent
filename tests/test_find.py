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


def _tests_repo(tmp_path):
    files = {
        "pkg/table.py": "class Table:\n    def add_row(self, *cells):\n        pass\n",
        "pkg/console.py": "def render(t):\n    return t\n",
        "tests/test_table.py": "from pkg.table import Table\n\ndef test_one():\n    Table()\n",
        "tests/test_misc.py": "from pkg.table import Table\nTable().add_row(1)\nTable().add_row(2)\n",
        "tests/test_console.py": "from pkg.console import render\n",
        "docs_src/tutorial.py": "from pkg.table import Table\nTable().add_row('a')\n",
        "examples/test_demo.py": "from pkg.table import Table\nTable().add_row('a')\n",
    }
    for rel, text in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return tmp_path


def test_test_files_rank_by_names_with_the_top_files_own_test_raised(tmp_path):
    """#170: on the 129 development tasks, test files ranked by how many of the issue's names they mention, with
    test_<stem>.py of the top file raised, named a file the hidden tests change first in 61 and in the top 3 in 71."""
    root = str(_tests_repo(tmp_path))
    found = find.scan(root, ["Table", "add_row"])
    tests = find.test_files(root, found, "pkg/table.py")
    assert tests[0] == "tests/test_table.py", "test_<stem>.py of the top file comes first (1 name + 2)"
    assert tests[1] == "tests/test_misc.py", "then the test that mentions both names"
    assert "tests/test_console.py" not in tests, "a test that mentions none of the names is left out"
    assert not any(t.startswith(("docs_src/", "examples/")) for t in tests), "docs and examples are not tests"
    assert len(find.test_files(root, found, "pkg/table.py", limit=1)) == 1


def test_tests_mode_prints_the_tests_for_the_file_changed(tmp_path, monkeypatch):
    """#170: after an edit, `find.py --tests FILE NAME...` prints one line, the test files for the file changed. With
    the reference fix's file as the file changed, its first file was one the hidden tests change in 59 of the 129
    development tasks, and one of its first three in 66 (analysis/find_ranks.csv, find_tests_rank_num)."""
    monkeypatch.chdir(_tests_repo(tmp_path))
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert find.main(["--tests", "/workspace/pkg/table.py", "add_row"]) == 0
    assert out.getvalue().strip() == "Tests to run: python3 -m pytest tests/test_table.py tests/test_misc.py -x -q"


def test_tests_mode_with_no_test_file_says_what_to_do(tmp_path, monkeypatch):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "core.py").write_text("def solo():\n    pass\n")
    monkeypatch.chdir(tmp_path)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert find.main(["--tests", "pkg/core.py", "solo"]) == 1
    assert "No test file found for pkg/core.py" in out.getvalue()


def test_the_normal_output_has_no_tests_line(tmp_path, monkeypatch):
    monkeypatch.chdir(_tests_repo(tmp_path))
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert find.main(["add_row"]) == 0
    assert "Tests to run" not in out.getvalue()
