"""The edit-fallback skill's edit.py and install.py (#122).

edit.py is what the agent runs after edit_file says "old_string not found" or "occurs N times": a SEARCH/REPLACE
block on stdin, matched exactly, then unescaped, then ignoring spaces, then (for a short SEARCH only) to the closest
block, changing only the lines the agent meant to change. Each case below is one of the ways recorded edits failed
(analysis/fallback_replay.csv). Run: python -m pytest -q tests
"""

import ast
import importlib.util
import io
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True   # no __pycache__ in skills/: a .pyc in the submission is refused
SKILL = ROOT / "skills" / "edit-fallback"
SCRIPTS = SKILL / "scripts"


def _load(name):
    spec = importlib.util.spec_from_file_location(f"fallback_{name}", SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


edit = _load("edit")

FILE = '''import os


class Table:
    """A table of rows."""

    def add_row(self, *renderables, style=None):
        """Add a row of renderables."""
        self.rows.append(renderables)
        return self

    def add_column(self, header="", footer=""):
        """Add a column to the table."""
        self.columns.append((header, footer))
        return self
'''


def test_exact_match_is_applied():
    new, msg = edit.apply(FILE, "        self.rows.append(renderables)\n",
                          "        self.rows.append(list(renderables))\n")
    assert new == FILE.replace("self.rows.append(renderables)", "self.rows.append(list(renderables))")
    assert msg.startswith("matched lines 9-9")


def test_escaped_text_is_unescaped_once():
    doc = '\\"\\"\\"Add a row of renderables.\\"\\"\\"'
    search = '    def add_row(self, *renderables, style=None):\\n        ' + doc
    replace = '    def add_row(self, *renderables, style=None, end=False):\\n        ' + doc
    new, msg = edit.apply(FILE, search, replace)
    assert new == FILE.replace("style=None):", "style=None, end=False):")
    assert "after undoing escapes" in msg


def test_unescape_is_one_level_and_none_when_nothing_to_undo():
    assert edit.unescape('if c == "\\\\u200d":') == 'if c == "\\u200d":'
    assert edit.unescape('a\\nb') == "a\nb"
    assert edit.unescape("plain text") is None


def test_copy_error_keeps_the_files_own_line():
    # the QAT copy defect: a final "s" dropped from a line the agent copied but did not mean to change
    search = '        """Add a row of renderable."""\n        self.rows.append(renderables)'
    replace = '        """Add a row of renderable."""\n        self.rows.append(tuple(renderables))'
    new, msg = edit.apply(FILE, search, replace)
    assert new == FILE.replace("self.rows.append(renderables)", "self.rows.append(tuple(renderables))")
    assert '"""Add a row of renderables."""' in new and "renderable.\"\"\"" not in new
    assert msg.startswith("closest match")


def test_indentation_is_taken_from_the_file():
    search = "def add_column(self, header=\"\", footer=\"\"):\n    \"\"\"Add a column to the table.\"\"\""
    replace = ("def add_column(self, header=\"\", footer=\"\", width=None):\n"
               "    \"\"\"Add a column to the table.\"\"\"")
    new, _ = edit.apply(FILE, search, replace)
    assert '    def add_column(self, header="", footer="", width=None):\n' in new


def test_a_left_out_line_stays_in_the_file():
    search = ("    def add_row(self, *renderables, style=None):\n"
              "        self.rows.append(renderables)\n"
              "        return self")
    replace = ("    def add_row(self, *renderables, style=None):\n"
               "        self.rows.append(renderables)\n"
               "        self.dirty = True\n"
               "        return self")
    new, _ = edit.apply(FILE, search, replace)
    assert new == FILE.replace("        self.rows.append(renderables)\n        return self",
                               "        self.rows.append(renderables)\n        self.dirty = True\n        return self")
    assert '"""Add a row of renderables."""' in new


def test_left_out_line_where_replace_adds_lines_is_a_conflict():
    search = ("    def add_row(self, *renderables, style=None):\n"
              "        self.rows.append(renderables)")
    replace = ("    def add_row(self, *renderables, style=None):\n"
               "        renderables = [r for r in renderables if r is not None]\n"
               "        self.rows.append(renderables)")
    new, msg = edit.apply(FILE, search, replace)
    assert new is None
    assert "nothing changed" in msg and "   8  " in msg


def test_tool_call_debris_after_the_last_line_is_dropped():
    search = '        self.columns.append((header, footer))\n        return self\n",'
    replace = '        self.columns.append((header, footer, None))\n        return self'
    new, _ = edit.apply(FILE, search, replace)
    assert new == FILE.replace("self.columns.append((header, footer))", "self.columns.append((header, footer, None))")


def test_code_not_in_the_file_is_refused_with_the_closest_lines():
    new, msg = edit.apply(FILE, "    def remove_row(self, index):\n        del self.rows[index]",
                          "    def remove_row(self, index):\n        self.rows.pop(index)")
    assert new is None
    assert msg.startswith("SEARCH is not in the file")


def test_a_change_already_made_is_reported_not_repeated():
    done = FILE.replace("        return self\n\n    def add_column",
                        "        self.dirty = True\n        return self\n\n    def add_column")
    search = "        self.rows.append(renderables)\n        return self"
    replace = "        self.rows.append(renderables)\n        self.dirty = True\n        return self"
    new, msg = edit.apply(done, search, replace)
    assert new is None
    assert msg.startswith("REPLACE is already in the file")


def test_several_matches_list_their_lines_and_near_picks_one():
    new, msg = edit.apply(FILE, "        return self", "        return self  # chain")
    assert new is None
    assert msg.startswith("SEARCH occurs at lines 10, 15")
    new, _ = edit.apply(FILE, "        return self", "        return self  # chain", near=15)
    lines = new.splitlines()
    assert lines[14] == "        return self  # chain" and lines[9] == "        return self"


def test_a_long_search_gets_no_close_match():
    body = "\n".join(f"    value_{k} = compute_{k}(argument_{k})" for k in range(40))
    text = "def build():\n" + body + "\n    return value_0\n"
    search_lines = text.splitlines()[1:11]
    search_lines[3] = search_lines[3].replace("compute_", "compte_")   # one copy error in ten lines
    assert len(search_lines) > edit.MAX_FUZZY_LINES
    new, msg = edit.apply(text, "\n".join(search_lines), "\n".join(search_lines + ["    extra = 1"]))
    assert new is None
    assert msg.startswith(f"SEARCH has {len(search_lines)} lines")


def test_a_close_match_on_a_large_file_is_fast():
    text = "".join(f"def function_{k}(x):\n    return x + {k}\n\n" for k in range(2000))
    assert text.count("\n") > 5000
    t0 = time.perf_counter()
    new, _ = edit.apply(text, "def functon_1500(x):\n    return x + 1500", "def function_1500(x):\n    return x - 1500")
    assert time.perf_counter() - t0 < 1.0
    assert "return x - 1500" in new


def test_parse_blocks_reads_search_replace_and_old_new_markers():
    text = "<<<<<<< SEARCH\na\n=======\nb\n>>>>>>> REPLACE\n<<<<<<< OLD\nc\n=======\nd\n>>>>>>> NEW\n"
    assert edit.parse_blocks(text) == [("a", "b"), ("c", "d")]


def test_main_writes_on_success_and_exits_with_its_codes(tmp_path):
    f = tmp_path / "table.py"
    f.write_text(FILE)
    block = ("<<<<<<< SEARCH\n        self.rows.append(renderables)\n=======\n"
             "        self.rows.insert(0, renderables)\n>>>>>>> REPLACE\n")
    assert edit.main([str(f)], io.StringIO(block)) == 0
    assert "self.rows.insert(0, renderables)" in f.read_text()
    assert edit.main([str(f)], io.StringIO(block)) == 1          # SEARCH is gone now: nothing written
    assert edit.main([str(f)], io.StringIO("no block")) == 2
    assert edit.main([str(tmp_path / "missing.py")], io.StringIO(block)) == 2
    before = f.read_text()
    block2 = block.replace("rows.append(renderables)", "rows.insert(0, renderables)").replace(
        "rows.insert(0, renderables)\n>>>>>>>", "rows.insert(1, renderables)\n>>>>>>>")
    assert edit.main([str(f), "--dry-run"], io.StringIO(block2)) == 0
    assert f.read_text() == before


@pytest.mark.parametrize("name", ["edit", "find", "install"])
def test_scripts_parse_as_python_3_8_and_use_only_the_standard_library(name):
    src = (SCRIPTS / f"{name}.py").read_text()
    tree = ast.parse(src, feature_version=(3, 8))
    stdlib = set(sys.stdlib_module_names)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods = [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            mods = [(node.module or "").split(".")[0]]
        else:
            continue
        assert all(m in stdlib for m in mods), f"{name}.py imports outside the standard library: {mods}"
    for banned in (".removeprefix(", ".removesuffix(", "str | None", "list[", "dict[", "tuple["):
        assert banned not in src, f"{name}.py uses {banned!r}, newer than Python 3.8"   # match is caught by ast


def test_skill_is_named_in_kebab_case_and_matches_its_folder():
    head = (SKILL / "SKILL.md").read_text().split("---")[1]
    assert "name: edit-fallback" in head
    assert "description:" in head


def test_install_copies_the_helpers_and_prints_their_usage(tmp_path):
    install = _load("install")
    assert install.TARGET == "/tmp/h"
    target = tmp_path / "h"
    out = io.StringIO()
    assert install.main(target=str(target), out=out) == 0
    for helper in ("find.py", "edit.py"):
        assert (target / helper).read_text() == (SCRIPTS / helper).read_text()
    text = out.getvalue()
    assert "python3 /tmp/h/find.py" in text and "python3 /tmp/h/edit.py" in text   # the path the agent types
    assert "<<<<<<< SEARCH" in text and "--near" in text


def test_install_also_writes_where_the_subprocess_sandbox_maps_tmp(tmp_path, monkeypatch):
    """The subprocess sandbox rewrites /tmp in a command to its own folder, which it also sets as TMPDIR; Python
    code writing to a literal /tmp/h reaches the real /tmp (found by the end-to-end run of the harness, #122)."""
    install = _load("install")
    monkeypatch.setattr(install, "TARGET", str(tmp_path / "real_tmp" / "h"))
    monkeypatch.setenv("TMPDIR", str(tmp_path / "sandbox_tmp"))
    monkeypatch.delenv("EDIT_FALLBACK_DIR", raising=False)
    assert install.main(out=io.StringIO()) == 0
    for folder in (tmp_path / "real_tmp" / "h", tmp_path / "sandbox_tmp" / "h"):
        assert (folder / "edit.py").is_file() and (folder / "find.py").is_file()


def test_install_reports_when_it_cannot_write(tmp_path, monkeypatch):
    install = _load("install")
    blocker = tmp_path / "file"
    blocker.write_text("not a folder")
    out = io.StringIO()
    assert install.main(target=str(blocker / "h"), out=out) == 1
    assert "grep" in out.getvalue() and "edit_file" in out.getvalue()


def test_installed_helpers_run_as_commands(tmp_path):
    install = _load("install")
    install.main(target=str(tmp_path / "h"), out=io.StringIO())
    f = tmp_path / "m.py"
    f.write_text(FILE)
    block = "<<<<<<< SEARCH\n        return self\n=======\n        return None\n>>>>>>> REPLACE\n"
    r = subprocess.run([sys.executable, str(tmp_path / "h" / "edit.py"), str(f), "--near", "10"], input=block,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert f.read_text().splitlines()[9] == "        return None"
    r = subprocess.run([sys.executable, str(tmp_path / "h" / "find.py"), "add_row"], capture_output=True, text=True,
                       cwd=tmp_path)
    assert "m.py" in r.stdout


def test_install_runs_through_adks_own_skill_wrapper(tmp_path):
    """The scorer's path: ADK loads the skill folder and runs install.py with every script beside it."""
    adk = pytest.importorskip("google.adk.tools.skill_toolset")
    from google.adk.skills import _utils
    skill = _utils._load_skill_from_dir(SKILL)
    assert {"install.py", "find.py", "edit.py"} <= set(skill.resources.list_scripts())
    wrapper = adk._SkillScriptCodeExecutor(None, 60)._build_wrapper_code(skill, "scripts/install.py", None)
    script = tmp_path / "wrapped.py"
    script.write_text(wrapper)
    env = dict(os.environ, EDIT_FALLBACK_DIR=str(tmp_path / "h"))
    r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, cwd=tmp_path, env=env)
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "h" / "edit.py").read_text() == (SCRIPTS / "edit.py").read_text()
    assert (tmp_path / "h" / "find.py").read_text() == (SCRIPTS / "find.py").read_text()
    assert "find.py" in r.stdout
