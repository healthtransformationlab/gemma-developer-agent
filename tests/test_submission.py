"""The submission's prompt and files (#97).

The hidden test set comes from other repositories, so the prompt must not spend calls on this repository's own
conventions files unless a task's repository has them, must say where to look first, and must give the edit tool's
real argument names. Run: python -m pytest -q tests
"""

import hashlib
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROMPT = (ROOT / "prompts" / "system.md").read_text()
SUBMISSION = ["agent.yaml", "eval_config.yaml", "prompts", "configs", "sub_agents", "skills", "adapters"]
ALLOWED = {".yaml", ".yml", ".md", ".txt", ".py", ".json", ".safetensors"}   # docs/rulebook-notes.md
HARNESS_TOOLS = {"run_command", "read_file", "edit_file", "write_file", "get_status", "submit_patch",
                 "get_code_neighbors", "search_similar_code", "get_code_subgraph"}


def _steps() -> list[str]:
    """The numbered steps under 'Order of work', in order."""
    section = PROMPT.split("## Order of work", 1)[1].split("\n## ", 1)[0]
    return [s.strip() for s in re.split(r"\n(?=\d+\. )", section) if re.match(r"\d+\. ", s.strip())]


def _agent_tools() -> set[str]:
    def load(path):
        text = re.sub(r"!include \S+", '""', path.read_text())
        return yaml.safe_load(text)
    tools = set()
    for f in [ROOT / "agent.yaml", *sorted((ROOT / "sub_agents").glob("*.yaml"))]:
        for t in load(f).get("tools", []):
            tools.add(t if isinstance(t, str) else "agent_tool")
    return tools


def test_localization_is_the_first_step_after_naming_the_test():
    """#122: find.py ranked the reference fix's file first in 39 of 129 development tasks, against 12 for the grep it
    replaces (docs/fallback-scripts-study.md); grep stays as the fallback, tests left out."""
    steps = _steps()
    first_reading = next(i for i, s in enumerate(steps) if "read_file" in s or "Read " in s)
    locate = next((i for i, s in enumerate(steps) if "python3 /tmp/h/find.py" in s), None)
    assert locate is not None, "no localization step: one run_command with python3 /tmp/h/find.py"
    assert locate < first_reading, "localize before reading any file"
    assert "grep" in steps[locate] and "/workspace" in steps[locate] and re.search(r"tests", steps[locate]), \
        "keep grep over /workspace, tests left out, as the fallback when find.py finds nothing"


def test_conventions_and_pipeline_doctor_only_when_the_repository_has_them():
    step = next(s for s in _steps() if "AGENTS.md" in s)
    assert re.search(r"\bonly (if|when)\b", step), "read conventions files only if the first listing shows them"
    assert "pipeline-doctor" in step and re.search(r"only (if|when)", step.split("pipeline-doctor")[0][-300:] + step)


def test_edit_file_arguments_are_named_exactly():
    for name in ("filepath", "old_string", "new_string", "allow_multiple"):
        assert f"`{name}`" in PROMPT, f"the prompt must name edit_file's argument `{name}`"
    assert re.search(r"old_string`[^.]*read_file", PROMPT), "say old_string is copied from read_file output"
    assert re.search(r"(once|unique)", PROMPT), "say old_string must match exactly once"
    assert re.search(r"new file[^.]*`write_file`", PROMPT), "say new files are written with write_file"


def test_every_tool_the_prompt_names_is_given_to_the_agent():
    named = {t for t in HARNESS_TOOLS if f"`{t}`" in PROMPT}
    missing = named - _agent_tools()
    assert not missing, f"the prompt names tools agent.yaml doesn't give: {missing}"


def test_submission_files_have_allowed_extensions():
    bad = []
    for entry in SUBMISSION:
        p = ROOT / entry
        files = [p] if p.is_file() else [f for f in p.rglob("*") if f.is_file() and "__pycache__" not in f.parts]
        bad += [str(f.relative_to(ROOT)) for f in files if f.suffix not in ALLOWED]
    assert not bad, f"extensions the evaluator refuses: {bad}"


def test_prompt_keeps_its_placeholders():
    assert "{problem_description}" in PROMPT and "{hints?}" in PROMPT


MAX_LORA_RANK = 128     # the competition's vLLM max_lora_rank (HARNESS_README.md, section 3.1)
COPYFIX_SHA256 = {      # Kaggle dataset michi883/ple-proj-svd-r128, as its description publishes them (#108)
    "adapter_config.json": "3786855f2b3ea33e66d32d5ce5aacef61afc2882f92358dd36164c5f104dfbe1",
    "adapter_model.safetensors": "9ce83a7cad3d8523c14750696dca06ee1ca89f50813047ae390ee00c7f17c888",
}


def _declared_adapters() -> dict[str, str]:
    found = {}
    for f in [ROOT / "agent.yaml", *sorted((ROOT / "sub_agents").glob("*.yaml"))]:
        m = re.search(r"^adapter:\s*(\S+)", f.read_text(), re.M)
        if m:
            found[f.name] = m.group(1)
    return found


def test_declared_adapters_exist_and_fit_the_server():
    declared = _declared_adapters()
    assert declared.get("agent.yaml") == "copyfix", "the coder serves the copyfix adapter (#108)"
    assert declared.get("code_analyzer.yaml") == "copyfix", "so does the analyzer: one model, one adapter"
    for name in set(declared.values()):
        folder = ROOT / "adapters" / name
        assert re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name), f"adapter name {name!r} the harness refuses"
        config = json.loads((folder / "adapter_config.json").read_text())
        assert config["peft_type"] == "LORA" and config["r"] <= MAX_LORA_RANK
        assert (folder / "adapter_model.safetensors").is_file()


def test_copyfix_files_match_the_published_hashes():
    for fname, digest in COPYFIX_SHA256.items():
        got = hashlib.sha256((ROOT / "adapters" / "copyfix" / fname).read_bytes()).hexdigest()
        assert got == digest, f"{fname} is not the published copyfix file"


def test_helpers_are_installed_first_with_no_other_argument():
    """#122: run_skill_script runs install.py in the sandbox; array arguments can hang the tool-call parser (forum
    #746336, #753973), so the call names only the skill and the script."""
    steps = _steps()
    install = next((i for i, s in enumerate(steps) if "`run_skill_script`" in s), None)
    assert install is not None and install <= next(i for i, s in enumerate(steps) if "find.py" in s)
    step = steps[install]
    assert "`edit-fallback`" in step and "`scripts/install.py`" in step
    assert re.search(r"no other argument", step) and "`args`" in step, "say: no other argument, never `args`"
    assert re.search(r"[Ii]f the install (call )?fails", step) and "grep" in step, \
        "if the install fails, the agent goes on with grep: the skill must never be what sinks a task"
    text = re.sub(r"!include \S+", '""', (ROOT / "agent.yaml").read_text())
    assert "skills/edit-fallback" in yaml.safe_load(text)["skills"]


def test_a_failed_edit_goes_to_edit_py_never_the_same_old_string():
    """#122: after a failed edit the agent made a successful retry 7 times in 43; edit.py matches through escapes,
    spacing and small copy errors, says when a change is already made, and lists the lines of several matches."""
    editing = PROMPT.split("## Editing", 1)[1].split("\n## ", 1)[0]
    assert "python3 /tmp/h/edit.py" in editing and "<<<<<<< SEARCH" in editing and ">>>>>>> REPLACE" in editing
    assert "--near" in editing and re.search(r"already", editing)
    assert re.search(r"never\s+(send\s+)?the\s+same\s+`old_string`", editing)
    assert re.search(r"[Ii]f `?/tmp/h/edit.py`? is missing[^.]*re-read", editing), \
        "without the helpers, fall back to re-reading the lines and retrying once with a shorter anchor"


def test_submission_has_no_bytecode_cache():
    """#122: the bundle copies these folders as they are, and the evaluator refuses a .pyc (forum #749200); the
    tests load the skill's scripts without writing one."""
    found = [str(f.relative_to(ROOT)) for entry in SUBMISSION if (ROOT / entry).is_dir()
             for f in (ROOT / entry).rglob("*") if f.name == "__pycache__" or f.suffix == ".pyc"]
    assert not found, f"bytecode caches in the submission: {found}"
