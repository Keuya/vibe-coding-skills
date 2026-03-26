#!/usr/bin/env python3
import argparse
import json
import shutil
from pathlib import Path

REQUIRED_CORE = [
    "dialectic",
    "local-vco-roles",
    "spec-kit-vibe-compat",
    "superclaude-framework-compat",
    "ralph-loop",
    "cancel-ralph",
    "tdd-guide",
    "think-harder",
]
REQUIRED_WORKFLOW = [
    "brainstorming",
    "writing-plans",
    "subagent-driven-development",
    "systematic-debugging",
]
OPTIONAL_WORKFLOW = [
    "requesting-code-review",
    "receiving-code-review",
    "verification-before-completion",
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def write_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def copy_tree(src: Path, dst: Path):
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for child in src.iterdir():
        target = dst / child.name
        if child.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(child, target)
        else:
            shutil.copy2(child, target)


def copy_file(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def resolve_adapter(repo_root: Path, host_id: str):
    registry = load_json(repo_root / "adapters" / "index.json")
    normalized = (host_id or registry.get("default_adapter_id") or "codex").strip().lower()
    normalized = registry.get("aliases", {}).get(normalized, normalized)
    for entry in registry.get("adapters", []):
        if entry.get("id") == normalized:
            return entry
    raise SystemExit(f"Unsupported VGO host id: {host_id}")


def sync_vibe_canonical(repo_root: Path, target_root: Path, target_rel: str):
    governance = load_json(repo_root / "config" / "version-governance.json")
    canonical_root = (repo_root / governance["source_of_truth"]["canonical_root"]).resolve()
    target_vibe_root = target_root / target_rel
    for rel in governance["packaging"]["mirror"]["files"]:
        src = canonical_root / rel
        if src.exists():
            copy_file(src, target_vibe_root / rel)
    for rel in governance["packaging"]["mirror"]["directories"]:
        src = canonical_root / rel
        dst = target_vibe_root / rel
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)


def ensure_skill_present(target_root: Path, name: str, required: bool, allow_fallback: bool, fallback_sources, external_used, missing):
    skill_md = target_root / "skills" / name / "SKILL.md"
    if skill_md.exists():
        return
    if allow_fallback:
        for src in fallback_sources:
            src_path = Path(src)
            if src_path.exists():
                copy_tree(src_path, target_root / "skills" / name)
                external_used.add(name)
                break
    if required and not skill_md.exists():
        missing.add(name)


def install_runtime_core(repo_root: Path, target_root: Path, profile: str, allow_fallback: bool):
    packaging = load_json(repo_root / "config" / "runtime-core-packaging.json")
    for rel in packaging["directories"]:
        (target_root / rel).mkdir(parents=True, exist_ok=True)
    for entry in packaging["copy_directories"]:
        copy_tree(repo_root / entry["source"], target_root / entry["target"])
    for entry in packaging["copy_files"]:
        src = repo_root / entry["source"]
        if not src.exists():
            if entry.get("optional"):
                continue
            raise SystemExit(f"Runtime-core packaging source missing: {src}")
        copy_file(src, target_root / entry["target"])

    target_rel = packaging.get("canonical_vibe_mirror", {}).get("target_relpath", "skills/vibe")
    sync_vibe_canonical(repo_root, target_root, target_rel)

    canonical_skills_root = repo_root.parent
    workspace_root = canonical_skills_root.parent
    workspace_skills_root = workspace_root / "skills"
    workspace_superpowers_root = workspace_root / "superpowers" / "skills"
    bundled_superpowers_root = repo_root / "bundled" / "superpowers-skills"

    external_used = set()
    missing = set()

    for name in REQUIRED_CORE:
        ensure_skill_present(
            target_root,
            name,
            True,
            allow_fallback,
            [
                canonical_skills_root / name,
                workspace_skills_root / name,
                workspace_superpowers_root / name,
                bundled_superpowers_root / name,
            ],
            external_used,
            missing,
        )
    for name in REQUIRED_WORKFLOW:
        ensure_skill_present(
            target_root,
            name,
            True,
            allow_fallback,
            [
                workspace_skills_root / name,
                workspace_superpowers_root / name,
                bundled_superpowers_root / name,
                canonical_skills_root / name,
            ],
            external_used,
            missing,
        )
    if profile == "full":
        for name in OPTIONAL_WORKFLOW:
            ensure_skill_present(
                target_root,
                name,
                False,
                allow_fallback,
                [
                    workspace_skills_root / name,
                    workspace_superpowers_root / name,
                    bundled_superpowers_root / name,
                    canonical_skills_root / name,
                ],
                external_used,
                missing,
            )

    if missing:
        raise SystemExit("Missing required vendored skills: " + ", ".join(sorted(missing)))

    return sorted(external_used)


def install_codex_payload(repo_root: Path, target_root: Path):
    copy_tree(repo_root / "rules", target_root / "rules")
    copy_tree(repo_root / "agents" / "templates", target_root / "agents" / "templates")
    copy_tree(repo_root / "mcp", target_root / "mcp")
    (target_root / "config").mkdir(parents=True, exist_ok=True)
    copy_file(repo_root / "config" / "plugins-manifest.codex.json", target_root / "config" / "plugins-manifest.codex.json")
    settings_path = target_root / "settings.json"
    if not settings_path.exists():
        copy_file(repo_root / "config" / "settings.template.codex.json", settings_path)


def install_claude_guidance_payload(repo_root: Path, target_root: Path):
    # Hook and preview-settings installation are intentionally frozen until
    # cross-host compatibility issues are resolved.
    return


def install_opencode_guidance_payload(repo_root: Path, target_root: Path):
    commands_root = repo_root / "config" / "opencode" / "commands"
    agents_root = repo_root / "config" / "opencode" / "agents"
    example_config = repo_root / "config" / "opencode" / "opencode.json.example"

    copy_tree(commands_root, target_root / "commands")
    copy_tree(commands_root, target_root / "command")
    copy_tree(agents_root, target_root / "agents")
    copy_tree(agents_root, target_root / "agent")
    if example_config.exists():
        copy_file(example_config, target_root / "opencode.json.example")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--profile", choices=("minimal", "full"), default="full")
    parser.add_argument("--allow-external-skill-fallback", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    target_root = Path(args.target_root).resolve()
    target_root.mkdir(parents=True, exist_ok=True)
    adapter = resolve_adapter(repo_root, args.host)
    external_used = install_runtime_core(repo_root, target_root, args.profile, args.allow_external_skill_fallback)
    mode = adapter["install_mode"]
    if mode == "governed":
        install_codex_payload(repo_root, target_root)
    elif mode == "preview-guidance":
        if adapter["id"] == "claude-code":
            install_claude_guidance_payload(repo_root, target_root)
        elif adapter["id"] == "opencode":
            install_opencode_guidance_payload(repo_root, target_root)
        else:
            raise SystemExit(f"Unsupported preview-guidance adapter id: {adapter['id']}")
    elif mode != "runtime-core":
        raise SystemExit(f"Unsupported adapter install mode: {mode}")

    write_json(
        {
            "host_id": adapter["id"],
            "install_mode": mode,
            "target_root": str(target_root),
            "external_fallback_used": external_used,
        }
    )


if __name__ == "__main__":
    main()
