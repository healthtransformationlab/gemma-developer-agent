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
    steps = _steps()
    first_reading = next(i for i, s in enumerate(steps) if "read_file" in s or "Read " in s)
    locate = next((i for i, s in enumerate(steps) if "grep" in s and "/workspace" in s), None)
    assert locate is not None, "no localization step: one run_command that greps /workspace"
    assert locate < first_reading, "localize before reading any file"
    assert "ls" in steps[locate] and re.search(r"tests?", steps[locate]), \
        "the localization step lists /workspace and leaves tests out of the grep"


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
DISTILLED_SHA256 = {    # Kaggle model omallo/gemma4-e4b-swe-agent-lora-from-31b, peft-lora-scale-1 v1, as downloaded (#125)
    "adapter_config.json": "e813359ce4ae43403e533f8937ba250743fe670536dc3a7b76de4dc294300949",
    "adapter_model.safetensors": "e7d5f6afed8f5a6c2e3b031646d95accd94749289366696039f4641bab396015",
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
    assert declared.get("agent.yaml") == "distilled", "the coder serves the distilled adapter (#125)"
    assert declared.get("code_analyzer.yaml") == "distilled", "so does the analyzer: one model, one adapter"
    for name in set(declared.values()):
        folder = ROOT / "adapters" / name
        assert re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name), f"adapter name {name!r} the harness refuses"
        config = json.loads((folder / "adapter_config.json").read_text())
        assert config["peft_type"] == "LORA" and config["r"] <= MAX_LORA_RANK
        assert (folder / "adapter_model.safetensors").is_file()


def test_distilled_files_match_the_downloaded_hashes():
    for fname, digest in DISTILLED_SHA256.items():
        got = hashlib.sha256((ROOT / "adapters" / "distilled" / fname).read_bytes()).hexdigest()
        assert got == digest, f"{fname} is not the downloaded distilled adapter file"
    assert not (ROOT / "adapters" / "copyfix").exists(), "one adapter: copyfix is swapped out in this entry"
