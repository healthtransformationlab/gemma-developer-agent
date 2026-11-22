"""Behavior/literal fallback in find.py when an issue names ≤2 code identifiers (#106)."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location(
    "fallback_find", ROOT / "skills" / "edit-fallback" / "scripts" / "find.py"
)
find = importlib.util.module_from_spec(spec)
spec.loader.exec_module(find)


def _repo(tmp_path):
    files = {
        "pkg/__init__.py": "",
        "pkg/oauth.py": (
            '"""OAuth2 security schemes and scopes for OpenAPI."""\n'
            "def declare_scopes(scheme, scopes):\n"
            "    # attach scopes to the security scheme\n"
            "    return scheme\n"
            "def deduplicate_schemes(items):\n"
            "    return items\n"
        ),
        "pkg/routing.py": "def add_api_route(path):\n    return path\n",
        "pkg/errors.py": "MESSAGE = 'row has too many cells'\n",
        "tests/test_oauth.py": "from pkg.oauth import declare_scopes\n",
    }
    for rel, text in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return tmp_path


def test_literal_error_string_from_issue_finds_the_file(tmp_path):
    root = str(_repo(tmp_path))
    issue = "Bug: raises ValueError with 'row has too many cells' when validating"
    ranked = find.rank_for_issue(root, ["ValueError"], issue)
    assert ranked[0][0] == "pkg/errors.py"
    assert ranked[0][2]  # one-line reason


def test_stemmed_behavior_words_match_function_docstring_and_comment(tmp_path):
    root = str(_repo(tmp_path))
    issue = (
        "Fix OAuth2 scopes in OpenAPI when a parent dependency declares scopes "
        "and a sub-dependency security scheme is cached without scopes."
    )
    # ≤2 code identifiers: OpenAPI only (OAuth2 is camel-ish but we pass what localize would)
    ranked = find.rank_for_issue(root, ["OpenAPI"], issue)
    paths = [r[0] for r in ranked]
    assert "pkg/oauth.py" in paths[:3]
    assert paths.index("pkg/oauth.py") < paths.index("pkg/routing.py") if "pkg/routing.py" in paths else True
    row = next(r for r in ranked if r[0] == "pkg/oauth.py")
    assert row[1]  # best function name
    assert "scope" in row[2].lower() or "oauth" in row[2].lower() or "scheme" in row[2].lower()


def test_rank_for_issue_returns_at_most_eight_with_function_and_reason(tmp_path):
    root = str(_repo(tmp_path))
    for i in range(12):
        (tmp_path / "pkg" / f"extra{i}.py").write_text(
            f'"""scopes security scheme helper {i}"""\n'
            f"def handle_scopes_{i}():\n    # scopes\n    return {i}\n"
        )
    ranked = find.rank_for_issue(root, ["OpenAPI"], "Fix scopes on security schemes in OpenAPI")
    assert len(ranked) <= 8
    for rel, func, reason, score in ranked:
        assert rel.endswith(".py")
        assert isinstance(func, str) and isinstance(reason, str) and reason
        assert score > 0


def test_fallback_does_not_change_ranking_when_more_than_two_identifiers(tmp_path):
    root = str(_repo(tmp_path))
    issue = "anything about scopes and schemes ignored when many names"
    with_ids = find.rank_for_issue(
        root, ["declare_scopes", "deduplicate_schemes", "add_api_route"], issue
    )
    # same as identifier-only: declare_scopes file should lead
    assert with_ids[0][0] == "pkg/oauth.py"
    assert with_ids[0][1] in ("declare_scopes", "deduplicate_schemes")


def test_code_identifier_count_ignores_free_text(tmp_path):
    assert find.code_identifier_count(["OpenAPI", "row has too many cells"]) == 1
    assert find.code_identifier_count(["a", "b", "c"]) == 3
