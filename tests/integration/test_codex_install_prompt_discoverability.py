from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_codex_install_prompts_require_real_host_root_for_direct_vibe_discovery() -> None:
    zh_prompt = (REPO_ROOT / "docs/install/prompts/full-version-install.md").read_text(encoding="utf-8")
    en_prompt = (REPO_ROOT / "docs/install/prompts/full-version-install.en.md").read_text(encoding="utf-8")
    zh_rules = (REPO_ROOT / "docs/install/installation-rules.md").read_text(encoding="utf-8")
    en_rules = (REPO_ROOT / "docs/install/installation-rules.en.md").read_text(encoding="utf-8")

    assert 'CODEX_HOME="$HOME/.codex" bash ./install.sh --host codex --profile full' in zh_prompt
    assert 'CODEX_HOME="$HOME/.codex" bash ./check.sh --host codex --profile full' in zh_prompt
    assert "~/.codex" in zh_prompt
    assert "$vibe" in zh_prompt

    assert 'CODEX_HOME="$HOME/.codex" bash ./install.sh --host codex --profile full' in en_prompt
    assert 'CODEX_HOME="$HOME/.codex" bash ./check.sh --host codex --profile full' in en_prompt
    assert "~/.codex" in en_prompt
    assert "$vibe" in en_prompt

    assert "~/.codex" in zh_rules
    assert "$vibe" in zh_rules
    assert "~/.codex" in en_rules
    assert "$vibe" in en_rules


def test_codex_reference_docs_prefer_real_host_root_over_isolated_fallback() -> None:
    zh_recommended = (REPO_ROOT / "docs/install/recommended-full-path.md").read_text(encoding="utf-8")
    en_recommended = (REPO_ROOT / "docs/install/recommended-full-path.en.md").read_text(encoding="utf-8")
    zh_cold_start = (REPO_ROOT / "docs/cold-start-install-paths.md").read_text(encoding="utf-8")
    en_cold_start = (REPO_ROOT / "docs/cold-start-install-paths.en.md").read_text(encoding="utf-8")
    zh_entry = (REPO_ROOT / "docs/install/one-click-install-release-copy.md").read_text(encoding="utf-8")
    en_entry = (REPO_ROOT / "docs/install/one-click-install-release-copy.en.md").read_text(encoding="utf-8")

    assert 'CODEX_HOME="$HOME/.codex" bash ./scripts/bootstrap/one-shot-setup.sh --host codex --profile full' in zh_recommended
    assert 'CODEX_HOME="$HOME/.codex" bash ./check.sh --host codex --profile full --deep' in zh_recommended
    assert "$vibe" in zh_recommended

    assert 'CODEX_HOME="$HOME/.codex" bash ./scripts/bootstrap/one-shot-setup.sh --host codex --profile full' in en_recommended
    assert 'CODEX_HOME="$HOME/.codex" bash ./check.sh --host codex --profile full --deep' in en_recommended
    assert "$vibe" in en_recommended

    assert 'CODEX_HOME="$HOME/.codex" bash ./scripts/bootstrap/one-shot-setup.sh --host codex --profile full' in zh_cold_start
    assert "$vibe" in zh_cold_start

    assert 'CODEX_HOME="$HOME/.codex" bash ./scripts/bootstrap/one-shot-setup.sh --host codex --profile full' in en_cold_start
    assert "$vibe" in en_cold_start

    assert "~/.codex" in zh_entry
    assert "$vibe" in zh_entry
    assert "~/.codex" in en_entry
    assert "$vibe" in en_entry
