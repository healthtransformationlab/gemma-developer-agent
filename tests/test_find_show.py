"""find.py --show prints the top functions' code; --read prints several ranges in one call (#206)."""
import importlib.util
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("show_find", ROOT / "skills" / "edit-fallback" / "scripts" / "find.py")
find = importlib.util.module_from_spec(spec)
spec.loader.exec_module(find)


def _repo(tmp_path):
    long_body = "".join("    x%d = %d  # a padded line so three ranges overflow\n" % (i, i) for i in range(80))
    files = {
        "pkg/__init__.py": "",
        "pkg/table.py": (
            "class Table:\n"
            "    def add_row(self, *cells):\n"
            "        if len(cells) > self.width:\n"
            "            raise ValueError('row has too many cells')\n"
            "        return cells\n"
            "\n"
            "def render_table(table):\n"
            "    return table.add_row()\n"
        ),
        "pkg/big.py": "def huge_function():\n" + long_body + "    return x1\n",
        "tests/test_table.py": "from pkg.table import Table\n",
    }
    for rel, text in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return tmp_path


def _run(tmp_path, monkeypatch, *args):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(find, "root_dir", lambda: str(tmp_path))
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = find.main(list(args))
    return code, buf.getvalue()


def test_without_show_the_output_is_unchanged(tmp_path, monkeypatch):
    _repo(tmp_path)
    code, out = _run(tmp_path, monkeypatch, "add_row")
    assert code == 0 and "Code of the functions" not in out and "pkg/table.py" in out


def test_show_prints_the_top_functions_source_with_line_numbers(tmp_path, monkeypatch):
    _repo(tmp_path)
    code, out = _run(tmp_path, monkeypatch, "--show", "add_row")
    assert code == 0
    assert "Code of the functions to read first:" in out
    assert "pkg/table.py:2-5" in out
    assert "   4: " in out and "row has too many cells" in out
    assert len(out) <= find.SHOW_TOTAL_CHARS + 1


def test_a_long_function_is_cut_with_a_read_hint(tmp_path, monkeypatch):
    _repo(tmp_path)
    code, out = _run(tmp_path, monkeypatch, "huge_function", "--show")
    assert code == 0
    assert "more lines: --read pkg/big.py:" in out
    shown = [l for l in out.splitlines() if l[:6].strip().rstrip(":").isdigit()]
    assert len(shown) <= find.SHOW_FUNC_LINES


def test_show_works_with_the_issue_fallback(tmp_path, monkeypatch):
    _repo(tmp_path)
    code, out = _run(tmp_path, monkeypatch, "--issue", "Adding a row with too many cells raises an error", "--show")
    assert code == 0 and "Code of the functions to read first:" in out and "row has too many cells" in out


def test_read_prints_several_ranges_in_one_call(tmp_path, monkeypatch):
    _repo(tmp_path)
    code, out = _run(tmp_path, monkeypatch, "--read", "pkg/table.py:2-4", "pkg/table.py:7-8")
    assert code == 0
    assert "== pkg/table.py:2-4" in out and "== pkg/table.py:7-8" in out
    assert "   2: " in out and "   8: " in out


def test_read_caps_the_total_and_says_so(tmp_path, monkeypatch):
    _repo(tmp_path)
    code, out = _run(tmp_path, monkeypatch, "--read", "pkg/big.py:1-82", "pkg/big.py:1-82", "pkg/big.py:1-82")
    assert code == 0 and len(out) <= find.SHOW_TOTAL_CHARS + 1 and "(cut)" in out


def test_read_reports_a_missing_file_and_a_bad_range(tmp_path, monkeypatch):
    _repo(tmp_path)
    code, out = _run(tmp_path, monkeypatch, "--read", "pkg/nope.py:1-5", "pkg/table.py:9-x")
    assert "pkg/nope.py: no such file" in out and "pkg/table.py:9-x: use FILE:START-END" in out
