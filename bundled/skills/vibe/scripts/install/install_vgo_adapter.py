#!/usr/bin/env python3
import argparse
import json
import os
import stat
import shutil
import tempfile
from datetime import datetime
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
SKILL_ONLY_ACTIVATION_HOSTS = {
    "claude-code",
    "cursor",
    "windsurf",
    "openclaw",
    "opencode",
}
HOST_BRIDGE_COMMAND_CANDIDATES = {
    "claude-code": ["claude", "claude-code"],
    "cursor": ["cursor-agent", "cursor"],
    "windsurf": ["windsurf", "codeium"],
    "openclaw": ["openclaw"],
    "opencode": ["opencode"],
}
HOST_BRIDGE_COMMAND_ENV = {
    "claude-code": "VGO_CLAUDE_CODE_SPECIALIST_BRIDGE_COMMAND",
    "cursor": "VGO_CURSOR_SPECIALIST_BRIDGE_COMMAND",
    "windsurf": "VGO_WINDSURF_SPECIALIST_BRIDGE_COMMAND",
    "openclaw": "VGO_OPENCLAW_SPECIALIST_BRIDGE_COMMAND",
    "opencode": "VGO_OPENCODE_SPECIALIST_BRIDGE_COMMAND",
}

ledger_state = {
    "created_paths": set(),
    "managed_json_paths": set(),
    "template_generated": set(),
    "specialist_wrapper_paths": [],
}


def reset_ledger_state() -> None:
    for key, value in ledger_state.items():
        if isinstance(value, set):
            value.clear()
        elif isinstance(value, list):
            value.clear()
        else:
            ledger_state[key] = type(value)()


def track_created_path(path: Path | str) -> None:
    try:
        resolved = Path(path).resolve()
    except FileNotFoundError:
        resolved = Path(path)
    ledger_state["created_paths"].add(str(resolved))


def record_managed_json(path: Path) -> None:
    try:
        resolved = path.resolve()
    except FileNotFoundError:
        resolved = path
    ledger_state["managed_json_paths"].add(str(resolved))


def record_generated_from_template(path: Path) -> None:
    try:
        resolved = path.resolve()
    except FileNotFoundError:
        resolved = path
    ledger_state["template_generated"].add(str(resolved))


def record_specialist_wrapper(path: Path) -> None:
    try:
        resolved = str(path.resolve())
    except FileNotFoundError:
        resolved = str(path)
    if resolved not in ledger_state["specialist_wrapper_paths"]:
        ledger_state["specialist_wrapper_paths"].append(resolved)

def detect_platform_tag() -> str:
    if os.name == "nt":
        return "windows"
    if sys_platform().startswith("darwin"):
        return "macos"
    return "linux"


def sys_platform() -> str:
    return os.sys.platform.lower()


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def write_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def write_json_file(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def uses_skill_only_activation(host_id: str) -> bool:
    return (host_id or "").strip().lower() in SKILL_ONLY_ACTIVATION_HOSTS


def is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def same_path(left: Path, right: Path) -> bool:
    return left.resolve() == right.resolve()


def copy_dir_replace(src: Path, dst: Path):
    if not src.exists():
        return
    if same_path(src, dst):
        return

    src_resolved = src.resolve()
    dst_resolved = dst.resolve(strict=False)
    requires_staging = is_relative_to(src_resolved, dst_resolved) or is_relative_to(dst_resolved, src_resolved)

    if not requires_staging:
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        track_created_path(dst)
        return

    stage_root = Path(tempfile.mkdtemp(prefix="vgo-copy-tree-"))
    try:
        staged = stage_root / src.name
        shutil.copytree(src, staged)
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(staged, dst)
        track_created_path(dst)
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)


def copy_tree(src: Path, dst: Path):
    if not src.exists():
        return
    children = list(src.iterdir())
    dst.mkdir(parents=True, exist_ok=True)
    track_created_path(dst)
    for child in children:
        target = dst / child.name
        if child.is_dir():
            copy_dir_replace(child, target)
        else:
            if target.exists() and same_path(child, target):
                continue
            shutil.copy2(child, target)
            track_created_path(target)


def copy_file(src: Path, dst: Path):
    if src.exists() and dst.exists() and same_path(src, dst):
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    track_created_path(dst)


def ensure_executable(path: Path):
    current = path.stat().st_mode
    path.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def restore_skill_entrypoint_if_needed(skill_root: Path):
    skill_md = skill_root / "SKILL.md"
    mirror_md = skill_root / "SKILL.runtime-mirror.md"
    if skill_md.exists() or not mirror_md.exists():
        return
    mirror_md.rename(skill_md)


def parent_dir(path: Path | None) -> Path | None:
    if path is None:
        return None
    resolved = path.resolve()
    parent = resolved.parent
    if parent == resolved or parent == Path(parent.anchor):
        return None
    return parent


def skill_source_roots(repo_root: Path) -> list[Path]:
    canonical_skills_root = parent_dir(repo_root)
    workspace_root = parent_dir(canonical_skills_root)
    candidates = [
        canonical_skills_root,
        workspace_root / "skills" if workspace_root is not None else None,
        workspace_root / "superpowers" / "skills" if workspace_root is not None else None,
        repo_root / "bundled" / "superpowers-skills",
    ]
    roots: list[Path] = []
    for candidate in candidates:
        if candidate is None or not candidate.exists():
            continue
        if candidate not in roots:
            roots.append(candidate)
    return roots


def embedded_registry():
    return {
        "schema_version": 1,
        "default_adapter_id": "codex",
        "aliases": {"claude": "claude-code"},
        "adapters": [
            {
                "id": "codex",
                "status": "supported-with-constraints",
                "install_mode": "governed",
                "check_mode": "governed",
                "bootstrap_mode": "governed",
                "default_target_root": {"env": "CODEX_HOME", "rel": ".codex", "kind": "host-home"},
                "host_profile": "adapters/codex/host-profile.json",
                "settings_map": "adapters/codex/settings-map.json",
                "closure": "adapters/codex/closure.json",
                "manifest": "dist/host-codex/manifest.json",
            },
            {
                "id": "claude-code",
                "status": "preview",
                "install_mode": "preview-guidance",
                "check_mode": "preview-guidance",
                "bootstrap_mode": "preview-guidance",
                "default_target_root": {"env": "CLAUDE_HOME", "rel": ".claude", "kind": "host-home"},
                "host_profile": "adapters/claude-code/host-profile.json",
                "settings_map": "adapters/claude-code/settings-map.json",
                "closure": "adapters/claude-code/closure.json",
                "manifest": "dist/host-claude-code/manifest.json",
            },
            {
                "id": "cursor",
                "status": "preview",
                "install_mode": "preview-guidance",
                "check_mode": "preview-guidance",
                "bootstrap_mode": "preview-guidance",
                "default_target_root": {"env": "CURSOR_HOME", "rel": ".cursor", "kind": "host-home"},
                "host_profile": "adapters/cursor/host-profile.json",
                "settings_map": "adapters/cursor/settings-map.json",
                "closure": "adapters/cursor/closure.json",
                "manifest": "dist/host-cursor/manifest.json",
            },
            {
                "id": "windsurf",
                "status": "preview",
                "install_mode": "runtime-core",
                "check_mode": "runtime-core",
                "bootstrap_mode": "runtime-core",
                "default_target_root": {"env": "WINDSURF_HOME", "rel": ".codeium/windsurf", "kind": "host-home"},
                "host_profile": "adapters/windsurf/host-profile.json",
                "settings_map": "adapters/windsurf/settings-map.json",
                "closure": "adapters/windsurf/closure.json",
                "manifest": "dist/host-windsurf/manifest.json",
            },
            {
                "id": "openclaw",
                "status": "preview",
                "install_mode": "runtime-core",
                "check_mode": "runtime-core",
                "bootstrap_mode": "runtime-core",
                "default_target_root": {"env": "OPENCLAW_HOME", "rel": ".openclaw", "kind": "host-home"},
                "host_profile": "adapters/openclaw/host-profile.json",
                "settings_map": "adapters/openclaw/settings-map.json",
                "closure": "adapters/openclaw/closure.json",
                "manifest": "dist/host-openclaw/manifest.json",
            },
        ],
    }


def resolve_registry(repo_root: Path):
    current = repo_root.resolve()
    while True:
        registry_path = current / "adapters" / "index.json"
        if registry_path.exists():
            return load_json(registry_path)
        if current.parent == current:
            break
        current = current.parent

    if (repo_root / "config" / "version-governance.json").exists():
        return embedded_registry()

    raise SystemExit(f"VGO adapter registry not found under repo root or ancestors: {repo_root}")


def resolve_adapter(repo_root: Path, host_id: str):
    registry = resolve_registry(repo_root)
    normalized = (host_id or registry.get("default_adapter_id") or "codex").strip().lower()
    normalized = registry.get("aliases", {}).get(normalized, normalized)
    for entry in registry.get("adapters", []):
        if entry.get("id") == normalized:
            return entry
    raise SystemExit(f"Unsupported VGO host id: {host_id}")


def resolve_target_root_for_adapter(adapter: dict, explicit_target_root: Path | None = None) -> Path:
    if explicit_target_root is not None:
        return explicit_target_root.resolve()

    target_spec = adapter.get("default_target_root") or {}
    env_name = target_spec.get("env") or ""
    rel = target_spec.get("rel") or ""
    env_value = os.environ.get(env_name, "").strip() if env_name else ""
    if env_value:
        return Path(env_value).expanduser().resolve()
    if not rel:
        raise SystemExit(f"Adapter '{adapter.get('id')}' does not define default_target_root.rel")
    rel_path = Path(rel)
    if rel_path.is_absolute():
        return rel_path.resolve()
    return (Path.home() / rel_path).expanduser().resolve()


def load_specialist_policy(repo_root: Path):
    return load_json(repo_root / "config" / "native-specialist-execution-policy.json")


def resolve_specialist_policy_entry(repo_root: Path, host_id: str):
    policy = load_specialist_policy(repo_root)
    for entry in policy.get("adapters", []):
        if entry.get("id") == host_id:
            return entry
    return None


def resolve_bridge_command(host_id: str) -> tuple[str | None, str | None]:
    env_name = HOST_BRIDGE_COMMAND_ENV.get(host_id)
    if env_name:
        env_value = os.environ.get(env_name, "").strip()
        if env_value:
            candidate = shutil.which(env_value)
            if candidate:
                return candidate, f"env:{env_name}"
            path_candidate = Path(env_value).expanduser()
            if path_candidate.exists():
                return str(path_candidate.resolve()), f"env:{env_name}"

    for candidate_name in HOST_BRIDGE_COMMAND_CANDIDATES.get(host_id, []):
        resolved = shutil.which(candidate_name)
        if resolved:
            return resolved, f"path:{candidate_name}"

    return None, None


def materialize_host_specialist_wrapper(target_root: Path, host_id: str, bridge_command: str | None):
    tools_root = target_root / ".vibeskills" / "bin"
    tools_root.mkdir(parents=True, exist_ok=True)
    track_created_path(tools_root)

    wrapper_py = tools_root / f"{host_id}-specialist-wrapper.py"
    embedded_command = json.dumps(bridge_command or "")
    bridge_env_name = f"VGO_{host_id.upper().replace('-', '_')}_SPECIALIST_BRIDGE_COMMAND"
    wrapper_py.write_text(
        (
            "#!/usr/bin/env python3\n"
            "import os\n"
            "import subprocess\n"
            "import sys\n\n"
            f"HOST_ID = {json.dumps(host_id)}\n"
            f"TARGET_COMMAND = {embedded_command}\n\n"
            "def main() -> int:\n"
            f"    command = TARGET_COMMAND or os.environ.get({json.dumps(bridge_env_name)}, '').strip()\n"
            "    if not command:\n"
            "        sys.stderr.write(f'host specialist bridge command unavailable for {HOST_ID}\\n')\n"
            "        return 3\n"
            "    return subprocess.run([command, *sys.argv[1:]], check=False).returncode\n\n"
            "if __name__ == '__main__':\n"
            "    raise SystemExit(main())\n"
        ),
        encoding="utf-8",
    )
    ensure_executable(wrapper_py)
    record_specialist_wrapper(wrapper_py)

    platform_tag = detect_platform_tag()
    if platform_tag == "windows":
        launcher = tools_root / f"{host_id}-specialist-wrapper.cmd"
        launcher.write_text(
            (
                "@echo off\r\n"
                "setlocal\r\n"
                "set SCRIPT_DIR=%~dp0\r\n"
                "if exist \"%LocalAppData%\\Programs\\Python\\Python311\\python.exe\" (\r\n"
                "  set PY_CMD=%LocalAppData%\\Programs\\Python\\Python311\\python.exe\r\n"
                ") else if exist \"%ProgramFiles%\\Python311\\python.exe\" (\r\n"
                "  set PY_CMD=%ProgramFiles%\\Python311\\python.exe\r\n"
                ") else (\r\n"
                "  set PY_CMD=py -3\r\n"
                ")\r\n"
                "%PY_CMD% \"%SCRIPT_DIR%\\" + wrapper_py.name + "\" %*\r\n"
            ),
            encoding="utf-8",
        )
    else:
        launcher = tools_root / f"{host_id}-specialist-wrapper.sh"
        launcher.write_text(
            (
                "#!/usr/bin/env sh\n"
                "set -eu\n"
                "SCRIPT_DIR=$(CDPATH= cd -- \"$(dirname -- \"$0\")\" && pwd)\n"
                "if command -v python3 >/dev/null 2>&1; then\n"
                "  PYTHON_BIN=python3\n"
                "elif command -v python >/dev/null 2>&1; then\n"
                "  PYTHON_BIN=python\n"
                "else\n"
                "  echo 'python runtime unavailable for host specialist wrapper' >&2\n"
                "  exit 127\n"
                "fi\n"
                f"exec \"$PYTHON_BIN\" \"$SCRIPT_DIR/{wrapper_py.name}\" \"$@\"\n"
            ),
            encoding="utf-8",
        )
        ensure_executable(launcher)
    record_specialist_wrapper(launcher)

    return {
        "platform": platform_tag,
        "launcher_path": str(launcher.resolve()),
        "script_path": str(wrapper_py.resolve()),
        "ready": bool(bridge_command),
        "bridge_command": bridge_command,
    }


def merge_json_object(path: Path, patch: dict):
    existing = {}
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
    merged = dict(existing)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(existing.get(key), dict):
            next_value = dict(existing[key])
            next_value.update(value)
            merged[key] = next_value
        else:
            merged[key] = value
    write_json_file(path, merged)


def path_points_inside_target_root(value: object, target_root: Path) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    candidate = Path(value.strip()).expanduser()
    if not candidate.is_absolute():
        candidate = target_root / candidate
    try:
        candidate.resolve(strict=False).relative_to(target_root.resolve())
        return True
    except ValueError:
        return False


def is_owned_legacy_opencode_vibeskills_node(node: object, target_root: Path) -> bool:
    if not isinstance(node, dict):
        return False
    host_id = str(node.get("host_id") or "").strip().lower()
    if host_id and host_id != "opencode":
        return False
    if bool(node.get("managed", False)):
        return True
    for key in (
        "commands_root",
        "command_root_compat",
        "agents_root",
        "agent_root_compat",
        "specialist_wrapper",
    ):
        if path_points_inside_target_root(node.get(key), target_root):
            return True
    return False


def sanitize_legacy_opencode_config(target_root: Path) -> dict[str, object]:
    settings_path = target_root / "opencode.json"
    receipt: dict[str, object] = {
        "path": str(settings_path.resolve()),
        "status": "not-present",
    }
    if not settings_path.exists():
        return receipt

    try:
        payload = json.loads(settings_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        receipt["status"] = "parse-failed"
        return receipt

    if not isinstance(payload, dict):
        receipt["status"] = "non-object"
        return receipt

    vibeskills_node = payload.get("vibeskills")
    if vibeskills_node is None:
        receipt["status"] = "already-clean"
        return receipt
    if not is_owned_legacy_opencode_vibeskills_node(vibeskills_node, target_root):
        receipt["status"] = "foreign-node-preserved"
        return receipt

    next_payload = dict(payload)
    del next_payload["vibeskills"]
    if next_payload:
        write_json_file(settings_path, next_payload)
        receipt["status"] = "removed-owned-node"
        receipt["preserved_keys"] = sorted(next_payload.keys())
    else:
        settings_path.unlink()
        receipt["status"] = "removed-owned-node-and-deleted-empty-file"
    return receipt


def materialize_host_settings(target_root: Path, adapter: dict, wrapper_info: dict):
    host_id = adapter["id"]
    materialized = []
    if uses_skill_only_activation(host_id):
        settings_path = target_root / ".vibeskills" / "host-settings.json"
        host_settings = {
            "schema_version": 1,
            "host_id": host_id,
            "managed": True,
            "skills_root": str((target_root / "skills").resolve()),
            "runtime_skill_entry": str((target_root / "skills" / "vibe" / "SKILL.md").resolve()),
            "explicit_vibe_skill_invocation": ["$vibe", "/vibe"],
            "specialist_wrapper": {
                "launcher_path": wrapper_info["launcher_path"],
                "script_path": wrapper_info["script_path"],
                "ready": wrapper_info["ready"],
            },
        }
        commands_root = target_root / "commands"
        agents_root = target_root / "agents"
        workflow_root = target_root / "global_workflows"
        mcp_config = target_root / "mcp_config.json"
        if commands_root.exists():
            host_settings["commands_root"] = str(commands_root.resolve())
        if agents_root.exists():
            host_settings["agents_root"] = str(agents_root.resolve())
        if workflow_root.exists():
            host_settings["workflow_root"] = str(workflow_root.resolve())
        if mcp_config.exists():
            host_settings["mcp_config"] = str(mcp_config.resolve())
        write_json_file(settings_path, host_settings)
        materialized.append(str(settings_path.resolve()))
        record_managed_json(settings_path)
        track_created_path(settings_path)
    return materialized


def materialize_host_closure(repo_root: Path, target_root: Path, adapter: dict):
    host_id = adapter["id"]
    bridge_command, bridge_source = resolve_bridge_command(host_id)
    wrapper_info = materialize_host_specialist_wrapper(target_root, host_id, bridge_command)
    settings_materialized = materialize_host_settings(target_root, adapter, wrapper_info)
    commands_root = target_root / "commands"
    closure_state = "closed_ready" if wrapper_info["ready"] else "configured_offline_unready"
    closure = {
        "schema_version": 1,
        "host_id": host_id,
        "platform": detect_platform_tag(),
        "target_root": str(target_root.resolve()),
        "install_mode": adapter["install_mode"],
        "skills_root": str((target_root / "skills").resolve()),
        "runtime_skill_entry": str((target_root / "skills" / "vibe" / "SKILL.md").resolve()),
        "commands_root": str(commands_root.resolve()),
        "global_workflows_root": str((target_root / "global_workflows").resolve()),
        "mcp_config_path": str((target_root / "mcp_config.json").resolve()),
        "host_closure_state": closure_state,
        "commands_materialized": commands_root.exists(),
        "settings_materialized": settings_materialized,
        "specialist_wrapper": {
            "launcher_path": wrapper_info["launcher_path"],
            "script_path": wrapper_info["script_path"],
            "ready": wrapper_info["ready"],
            "bridge_command": bridge_command,
            "bridge_source": bridge_source,
        },
    }
    closure_path = target_root / ".vibeskills" / "host-closure.json"
    write_json_file(closure_path, closure)
    return closure_path, closure


def is_closed_ready_required(adapter: dict) -> bool:
    return (adapter.get("install_mode") or "").strip().lower() != "governed"


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
            copy_dir_replace(src, dst)

def generated_nested_compatibility_suffix(governance: dict) -> Path | None:
    topology = governance.get("mirror_topology") or {}
    targets = topology.get("targets") or []
    bundled_path = None
    nested_path = None
    nested_materialization_mode = None

    for target in targets:
        target_id = str(target.get("id") or "").strip().lower()
        if target_id == "bundled":
            bundled_path = str(target.get("path") or "").strip()
        elif target_id == "nested_bundled":
            nested_path = str(target.get("path") or "").strip()
            nested_materialization_mode = str(target.get("materialization_mode") or "").strip()

    source = governance.get("source_of_truth") or {}
    if not bundled_path:
        bundled_path = str(source.get("bundled_root") or "bundled/skills/vibe").strip()
    if not nested_path:
        nested_path = str(source.get("nested_bundled_root") or "").strip()
    if not nested_path:
        nested_path = f"{bundled_path}/{bundled_path}"
    if not nested_materialization_mode:
        nested_materialization_mode = "release_install_only"
    if nested_materialization_mode != "release_install_only":
        return None

    bundled_norm = bundled_path.replace("\\", "/").strip("/")
    nested_norm = nested_path.replace("\\", "/").strip("/")
    prefix = f"{bundled_norm}/"
    if not nested_norm.startswith(prefix):
        return None

    suffix = nested_norm[len(prefix) :].strip("/")
    if not suffix:
        return None

    return Path(*suffix.split("/"))


def materialize_generated_nested_compatibility(governance: dict, installed_root: Path):
    suffix = generated_nested_compatibility_suffix(governance)
    if suffix is None:
        return

    nested_root = installed_root / suffix
    if same_path(installed_root, nested_root):
        return

    if nested_root.exists():
        shutil.rmtree(nested_root)

    packaging = governance.get("packaging") or {}
    mirror = packaging.get("mirror") or {}
    for rel in mirror.get("files") or []:
        src = installed_root / rel
        if src.exists():
            copy_file(src, nested_root / rel)
    for rel in mirror.get("directories") or []:
        src = installed_root / rel
        if src.exists():
            copy_dir_replace(src, nested_root / rel)


def runtime_core_vibe_relpath(repo_root: Path) -> str:
    packaging = load_json(repo_root / "config" / "runtime-core-packaging.json")
    return packaging.get("canonical_vibe_mirror", {}).get("target_relpath", "skills/vibe")


def write_install_ledger(
    repo_root: Path,
    target_root: Path,
    adapter: dict,
    mode: str,
    profile: str,
    canonical_vibe_rel: str,
    external_fallback_used: list[str],
):
    ledger_path = target_root / ".vibeskills" / "install-ledger.json"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger = {
        "schema_version": 1,
        "host_id": adapter["id"],
        "install_mode": mode,
        "profile": profile,
        "target_root": str(target_root.resolve()),
        "runtime_root": str(target_root.resolve()),
        "canonical_vibe_root": str((target_root / canonical_vibe_rel).resolve()),
        "created_paths": sorted(ledger_state["created_paths"]),
        "managed_json_paths": sorted(ledger_state["managed_json_paths"]),
        "generated_from_template_if_absent": sorted(ledger_state["template_generated"]),
        "specialist_wrapper_paths": ledger_state["specialist_wrapper_paths"],
        "external_fallback_used": external_fallback_used,
        "timestamp": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "ownership_source": "install-ledger",
    }
    write_json_file(ledger_path, ledger)
    track_created_path(ledger_path)


def ensure_skill_present(target_root: Path, name: str, required: bool, allow_fallback: bool, fallback_sources, external_used, missing):
    skill_md = target_root / "skills" / name / "SKILL.md"
    if skill_md.exists():
        return
    if allow_fallback:
        for src in fallback_sources:
            src_path = Path(src)
            if src_path.exists():
                destination = target_root / "skills" / name
                copy_tree(src_path, destination)
                restore_skill_entrypoint_if_needed(destination)
                external_used.add(name)
                break
    if required and not skill_md.exists():
        missing.add(name)


def install_runtime_core(repo_root: Path, target_root: Path, profile: str, allow_fallback: bool, adapter: dict):
    packaging = load_json(repo_root / "config" / "runtime-core-packaging.json")
    governance = load_json(repo_root / "config" / "version-governance.json")
    include_command_surfaces = not uses_skill_only_activation(adapter["id"])
    runtime_directories = [
        rel for rel in packaging["directories"]
        if include_command_surfaces or rel != "commands"
    ]
    for rel in runtime_directories:
        (target_root / rel).mkdir(parents=True, exist_ok=True)
        track_created_path(target_root / rel)
    copy_directories = [
        entry for entry in packaging["copy_directories"]
        if include_command_surfaces or entry["target"] != "commands"
    ]
    for entry in copy_directories:
        copy_tree(repo_root / entry["source"], target_root / entry["target"])
        if entry["target"] == "skills":
            for skill_dir in (target_root / "skills").iterdir():
                if skill_dir.is_dir():
                    restore_skill_entrypoint_if_needed(skill_dir)
    for entry in packaging["copy_files"]:
        src = repo_root / entry["source"]
        if not src.exists():
            if entry.get("optional"):
                continue
            raise SystemExit(f"Runtime-core packaging source missing: {src}")
        copy_file(src, target_root / entry["target"])

    target_rel = packaging.get("canonical_vibe_mirror", {}).get("target_relpath", "skills/vibe")
    sync_vibe_canonical(repo_root, target_root, target_rel)
    materialize_generated_nested_compatibility(governance, target_root / target_rel)

    roots = skill_source_roots(repo_root)

    external_used = set()
    missing = set()

    for name in REQUIRED_CORE:
        ensure_skill_present(
            target_root,
            name,
            True,
            allow_fallback,
            [
                root / name for root in roots
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
                root / name for root in roots[1:] + roots[:1]
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
                    root / name for root in roots[1:] + roots[:1]
                ],
                external_used,
                missing,
            )

    if missing:
        raise SystemExit("Missing required vendored skills: " + ", ".join(sorted(missing)))

    return sorted(external_used)


def install_codex_payload(repo_root: Path, target_root: Path):
    copy_tree(repo_root / "rules", target_root / "rules")
    track_created_path(target_root / "rules")
    copy_tree(repo_root / "agents" / "templates", target_root / "agents" / "templates")
    track_created_path(target_root / "agents" / "templates")
    copy_tree(repo_root / "mcp", target_root / "mcp")
    track_created_path(target_root / "mcp")
    (target_root / "config").mkdir(parents=True, exist_ok=True)
    track_created_path(target_root / "config")
    copy_file(repo_root / "config" / "plugins-manifest.codex.json", target_root / "config" / "plugins-manifest.codex.json")
    settings_path = target_root / "settings.json"
    if not settings_path.exists():
        copy_file(repo_root / "config" / "settings.template.codex.json", settings_path)
        record_generated_from_template(settings_path)
    track_created_path(settings_path)
    record_managed_json(settings_path)


def install_claude_guidance_payload(repo_root: Path, target_root: Path):
    # Hook and preview-settings installation are intentionally frozen until
    # cross-host compatibility issues are resolved.
    return


def install_opencode_guidance_payload(repo_root: Path, target_root: Path):
    example_config = repo_root / "config" / "opencode" / "opencode.json.example"
    if example_config.exists():
        copy_file(example_config, target_root / "opencode.json.example")

def install_runtime_core_mode_payload(repo_root: Path, target_root: Path, adapter: dict):
    if uses_skill_only_activation(adapter["id"]):
        return
    commands_root = repo_root / "commands"
    if commands_root.exists():
        copy_tree(commands_root, target_root / "global_workflows")
        track_created_path(target_root / "global_workflows")

    mcp_template = repo_root / "mcp" / "servers.template.json"
    mcp_config = target_root / "mcp_config.json"
    if mcp_template.exists() and not mcp_config.exists():
        copy_file(mcp_template, mcp_config)
        record_generated_from_template(mcp_config)
    track_created_path(mcp_config)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--profile", choices=("minimal", "full"), default="full")
    parser.add_argument("--allow-external-skill-fallback", action="store_true")
    parser.add_argument("--require-closed-ready", action="store_true")
    args = parser.parse_args()

    reset_ledger_state()

    repo_root = Path(args.repo_root).resolve()
    target_root = Path(args.target_root).resolve()
    target_root.mkdir(parents=True, exist_ok=True)
    track_created_path(target_root)
    adapter = resolve_adapter(repo_root, args.host)
    external_used = install_runtime_core(repo_root, target_root, args.profile, args.allow_external_skill_fallback, adapter)
    mode = adapter["install_mode"]
    legacy_opencode_config_cleanup = None
    if mode == "governed":
        install_codex_payload(repo_root, target_root)
    elif mode == "preview-guidance":
        if adapter["id"] == "opencode":
            install_opencode_guidance_payload(repo_root, target_root)
        elif adapter["id"] in {"claude-code", "cursor"}:
            install_claude_guidance_payload(repo_root, target_root)
        else:
            raise SystemExit(f"Unsupported preview-guidance adapter id: {adapter['id']}")
    elif mode == "runtime-core":
        install_runtime_core_mode_payload(repo_root, target_root, adapter)
    else:
        raise SystemExit(f"Unsupported adapter install mode: {mode}")

    closure_path, closure = materialize_host_closure(repo_root, target_root, adapter)
    require_closed_ready_effective = bool(args.require_closed_ready and is_closed_ready_required(adapter))
    if require_closed_ready_effective and closure["host_closure_state"] != "closed_ready":
        raise SystemExit(
            "Host closure for "
            f"'{adapter['id']}' is not closed_ready "
            f"(got '{closure['host_closure_state']}'). "
            "Configure the host specialist bridge command first, then retry install."
        )

    canonical_vibe_rel = runtime_core_vibe_relpath(repo_root)
    write_install_ledger(
        repo_root,
        target_root,
        adapter,
        mode,
        args.profile,
        canonical_vibe_rel,
        external_used,
    )

    write_json(
        {
            "host_id": adapter["id"],
            "install_mode": mode,
            "target_root": str(target_root),
            "external_fallback_used": external_used,
            "host_closure_path": str(closure_path),
            "host_closure_state": closure["host_closure_state"],
            "settings_materialized": closure["settings_materialized"],
            "legacy_opencode_config_cleanup": legacy_opencode_config_cleanup,
            "specialist_wrapper_ready": bool(closure["specialist_wrapper"]["ready"]),
            "require_closed_ready_requested": bool(args.require_closed_ready),
            "require_closed_ready_effective": require_closed_ready_effective,
        }
    )


if __name__ == "__main__":
    main()
