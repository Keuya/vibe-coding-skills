from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = REPO_ROOT / "packages" / "runtime-core" / "src" / "vgo_runtime" / "router_contract_support.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("router_contract_support_unit", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_resolve_skill_md_path_prefers_hidden_internal_corpus_for_specialist(tmp_path: Path) -> None:
    module = _load_module()
    repo = module.RepoContext(
        repo_root=REPO_ROOT,
        config_root=REPO_ROOT / "config",
        bundled_skills_root=REPO_ROOT / "bundled" / "skills",
    )
    hidden_root = tmp_path / "skills" / "vibe" / "bundled" / "skills" / "scikit-learn"
    public_root = tmp_path / "skills" / "scikit-learn"
    hidden_root.mkdir(parents=True, exist_ok=True)
    public_root.mkdir(parents=True, exist_ok=True)
    hidden_descriptor = hidden_root / "SKILL.runtime-mirror.md"
    public_descriptor = public_root / "SKILL.md"
    hidden_descriptor.write_text("---\nname: scikit-learn\n---\n", encoding="utf-8")
    public_descriptor.write_text("---\nname: scikit-learn\ndescription: public shadow\n---\n", encoding="utf-8")

    resolved = module.resolve_skill_md_path(repo, "scikit-learn", str(tmp_path), "codex")

    assert resolved == hidden_descriptor


def test_resolve_skill_md_path_uses_canonical_vibe_entrypoint(tmp_path: Path) -> None:
    module = _load_module()
    repo = module.RepoContext(
        repo_root=REPO_ROOT,
        config_root=REPO_ROOT / "config",
        bundled_skills_root=REPO_ROOT / "bundled" / "skills",
    )
    vibe_root = tmp_path / "skills" / "vibe"
    vibe_root.mkdir(parents=True, exist_ok=True)
    descriptor = vibe_root / "SKILL.md"
    descriptor.write_text("---\nname: vibe\ndescription: governed runtime\n---\n", encoding="utf-8")

    resolved = module.resolve_skill_md_path(repo, "vibe", str(tmp_path), "codex")
    metadata = module.read_skill_descriptor(repo, "vibe", str(tmp_path), "codex")

    assert resolved == descriptor
    assert metadata["skill_md_path"] == str(descriptor)
    assert metadata["description"] == "governed runtime"


def test_resolve_repo_root_prefers_nearest_config_root_without_git(tmp_path: Path) -> None:
    module = _load_module()
    target_root = tmp_path / "target"
    installed_root = target_root / "skills" / "vibe"
    script_path = installed_root / "scripts" / "runtime" / "invoke-vibe-runtime.ps1"

    (target_root / "config").mkdir(parents=True, exist_ok=True)
    (target_root / "config" / "version-governance.json").write_text("{}\n", encoding="utf-8")
    (installed_root / "config").mkdir(parents=True, exist_ok=True)
    (installed_root / "config" / "version-governance.json").write_text("{}\n", encoding="utf-8")
    script_path.parent.mkdir(parents=True, exist_ok=True)
    script_path.write_text("# runtime\n", encoding="utf-8")

    resolved = module.resolve_repo_root(script_path)

    assert resolved == installed_root
