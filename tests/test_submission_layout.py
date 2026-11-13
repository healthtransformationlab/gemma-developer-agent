"""The submission's layout, checked without the competition's packages (issue 59).

Pins what `adk_submission.validate_directory` cannot tell us is intended: the analyzer runs before the coder on every
task, its answer reaches the coder's prompt, and no prompt variable can end the agent by being unset (issue 33).
This is not the competition's validator; that check is the owner's, in a Kaggle kernel.

    python -m pytest tests/test_submission_layout.py -q
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_SUFFIXES = {".yaml", ".yml", ".md", ".txt", ".py", ".json", ".safetensors"}
SUBMISSION_PARTS = ["agent.yaml", "eval_config.yaml", "prompts", "sub_agents", "configs", "skills"]
GRAPH_TOOLS = {"get_code_neighbors", "search_similar_code", "get_code_subgraph"}


def load(path: Path):
    """Load a YAML file, resolving `!include` relative to the file that names it (rulebook, section 2)."""

    class Loader(yaml.SafeLoader):
        pass

    def include(loader: yaml.SafeLoader, node: yaml.Node):
        target = (path.parent / loader.construct_scalar(node)).resolve()
        assert target.is_file(), f"{path.name} includes a file that does not exist: {target}"
        return load(target) if target.suffix in {".yaml", ".yml"} else target.read_text()

    Loader.add_constructor("!include", include)
    return yaml.load(path.read_text(), Loader=Loader)


def sub_agent(root: dict, position: int) -> dict:
    return load(ROOT / root["sub_agents"][position]["config_path"])


def test_root_runs_the_analyzer_then_the_coder():
    root = load(ROOT / "agent.yaml")
    assert root["agent_class"] == "SequentialAgent"
    assert [ref["config_path"] for ref in root["sub_agents"]] == [
        "sub_agents/code_analyzer.yaml",
        "sub_agents/coder.yaml",
    ]


def test_analyzer_sees_the_issue_and_saves_its_answer():
    analyzer = sub_agent(load(ROOT / "agent.yaml"), 0)
    assert "{problem_description}" in analyzer["instruction"]
    assert analyzer["output_key"] == "code_map"


def test_analyzer_only_has_graph_tools():
    # Its tool results stay in the session the coder reads, so it gets no tool that returns file contents or edits.
    analyzer = sub_agent(load(ROOT / "agent.yaml"), 0)
    assert set(analyzer["tools"]) == GRAPH_TOOLS


def test_coder_reads_the_analyzers_answer_without_calling_anything():
    coder = sub_agent(load(ROOT / "agent.yaml"), 1)
    assert "{code_map?}" in coder["instruction"]
    assert not any(isinstance(tool, dict) and "agent_tool" in tool for tool in coder["tools"])
    assert {"edit_file", "run_command", "submit_patch"} <= set(coder["tools"])


def test_coder_compiles_what_it_edited_before_submitting():
    coder = sub_agent(load(ROOT / "agent.yaml"), 1)
    assert "python3 -m py_compile" in coder["instruction"]


def test_one_model_across_all_agents():
    root = load(ROOT / "agent.yaml")
    models = {sub_agent(root, i)["model"] for i in range(len(root["sub_agents"]))}
    if "model" in root:
        models.add(root["model"])
    assert len(models) == 1


def test_every_prompt_variable_but_the_issue_is_optional():
    # The evaluator always sets problem_description; a required variable that is not set ends the agent (issue 33).
    for prompt in (ROOT / "prompts").glob("*.md"):
        for name in re.findall(r"\{([a-z_]+\??)\}", prompt.read_text()):
            assert name == "problem_description" or name.endswith("?"), f"{prompt.name}: {{{name}}} is required"


def test_submission_files_have_allowed_extensions_and_no_symlinks():
    for part in SUBMISSION_PARTS:
        path = ROOT / part
        files = [path] if path.is_file() else [p for p in path.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
        for file in files:
            assert file.suffix in ALLOWED_SUFFIXES, file
            assert not file.is_symlink(), file


def agent_configs() -> list[Path]:
    """The root agent's file and every sub-agent file it names."""
    root = load(ROOT / "agent.yaml")
    return [ROOT / "agent.yaml"] + [ROOT / ref["config_path"] for ref in root.get("sub_agents", [])]


def test_every_skill_path_starts_at_the_submission_root():
    # The competition's compiler reads a skill's path from the submission's root, whichever file names it, and
    # refuses one that climbs out of a folder: `../skills/pipeline-doctor` in a sub-agent file ends every task
    # before it starts ("Path traversal attempted in skill"; adk-submission 0.2.13, `compile_submission`).
    for config in agent_configs():
        for skill in load(config).get("skills", []):
            assert ".." not in Path(skill).parts, f"{config.name}: {skill} climbs out of the submission"
            assert (ROOT / skill / "SKILL.md").is_file(), f"{config.name}: no SKILL.md under {skill} from the root"
