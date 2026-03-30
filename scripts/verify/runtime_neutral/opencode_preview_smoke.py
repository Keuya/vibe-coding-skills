#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


EXPECTED_FILES = [
    "skills/vibe/SKILL.md",
    "skills/brainstorming/SKILL.md",
    "commands/vibe.md",
    "commands/vibe-implement.md",
    "commands/vibe-review.md",
    "command/vibe.md",
    "command/vibe-implement.md",
    "command/vibe-review.md",
    "agents/vibe-plan.md",
    "agents/vibe-implement.md",
    "agents/vibe-review.md",
    "agent/vibe-plan.md",
    "agent/vibe-implement.md",
    "agent/vibe-review.md",
    "opencode.json.example",
]


def run(cmd, cwd, env=None):
    completed = subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        text=True,
        capture_output=True,
    )
    return {
        "cmd": cmd,
        "cwd": str(cwd),
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def detect_skill_hit(stdout: str) -> bool:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        payload = None

    if isinstance(payload, list):
        for entry in payload:
            if isinstance(entry, dict) and entry.get("name") == "vibe":
                return True

    return ("\"name\": \"vibe\"" in stdout) or ("skills/vibe/SKILL.md" in stdout)


def skill_output_looks_truncated(stdout: str) -> bool:
    stripped = stdout.rstrip()
    return stripped.startswith("[") and not stripped.endswith("]")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--write-artifacts", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    install_sh = repo_root / "install.sh"
    check_sh = repo_root / "check.sh"
    artifact_path = repo_root / "outputs" / "verify" / "opencode-preview-smoke.json"

    failures = []
    warnings = []

    with tempfile.TemporaryDirectory(prefix="vgo-opencode-preview-") as tmp:
        tmp_root = Path(tmp)
        target_root = tmp_root / ".config" / "opencode"
        target_root.mkdir(parents=True, exist_ok=True)
        real_config_path = target_root / "opencode.json"
        write_json(
            real_config_path,
            {
                "$schema": "https://opencode.ai/config.json",
                "mcp": {
                    "playwright": {
                        "enabled": True,
                        "type": "local",
                        "command": ["npx", "@playwright/mcp@latest"],
                    }
                },
                "vibeskills": {
                    "host_id": "opencode",
                    "managed": True,
                    "commands_root": str((target_root / "commands").resolve()),
                    "command_root_compat": str((target_root / "command").resolve()),
                    "agents_root": str((target_root / "agents").resolve()),
                    "agent_root_compat": str((target_root / "agent").resolve()),
                    "specialist_wrapper": str((target_root / ".vibeskills" / "bin" / "opencode-specialist-wrapper.sh").resolve()),
                },
            },
        )

        install_result = run(
            ["bash", str(install_sh), "--host", "opencode", "--target-root", str(target_root)],
            cwd=repo_root,
            env=os.environ.copy(),
        )
        if install_result["returncode"] != 0:
            failures.append("install.sh --host opencode failed")

        check_result = run(
            ["bash", str(check_sh), "--host", "opencode", "--target-root", str(target_root)],
            cwd=repo_root,
            env=os.environ.copy(),
        )
        if check_result["returncode"] != 0:
            failures.append("check.sh --host opencode failed")

        missing_files = [rel for rel in EXPECTED_FILES if not (target_root / rel).exists()]
        if missing_files:
            failures.append("expected preview payload missing")

        repaired_real_config = None
        if not real_config_path.exists():
            failures.append("preview install removed the real opencode.json instead of repairing it")
        else:
            try:
                repaired_real_config = json.loads(real_config_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                failures.append("preview install left a non-parseable real opencode.json")
            else:
                if "vibeskills" in repaired_real_config:
                    failures.append("preview install did not remove the legacy vibe-owned vibeskills node from the real opencode.json")
                if "mcp" not in repaired_real_config:
                    failures.append("preview install did not preserve host-managed mcp settings in the real opencode.json")

        opencode_cli = shutil.which("opencode")
        cli_probe = {
            "present": bool(opencode_cli),
            "binary": opencode_cli,
            "real_config_after_install": repaired_real_config,
            "debug_paths": None,
            "debug_config": None,
            "debug_skill_detects_vibe": None,
            "debug_agent_detects_vibe_plan": None,
            "notes": [],
        }

        if opencode_cli:
            env = os.environ.copy()
            env["HOME"] = str(tmp_root)
            env["XDG_CONFIG_HOME"] = str(tmp_root / ".config")
            env["XDG_DATA_HOME"] = str(tmp_root / ".local" / "share")
            env["XDG_STATE_HOME"] = str(tmp_root / ".local" / "state")
            env["XDG_CACHE_HOME"] = str(tmp_root / ".cache")

            debug_paths = run([opencode_cli, "debug", "paths"], cwd=repo_root, env=env)
            cli_probe["debug_paths"] = debug_paths
            if debug_paths["returncode"] != 0:
                failures.append("opencode debug paths failed in isolated env")

            debug_config = run([opencode_cli, "debug", "config"], cwd=repo_root, env=env)
            cli_probe["debug_config"] = debug_config
            if debug_config["returncode"] != 0:
                failures.append("opencode debug config failed in isolated env after preview install")

            debug_skill = run([opencode_cli, "debug", "skill"], cwd=repo_root, env=env)
            cli_probe["debug_skill"] = debug_skill
            skill_hits = detect_skill_hit(debug_skill["stdout"])
            cli_probe["debug_skill_detects_vibe"] = skill_hits
            if debug_skill["returncode"] != 0:
                warnings.append("opencode debug skill failed in isolated env")
            if not skill_hits:
                warning = "opencode debug skill did not enumerate the installed vibe skill in the isolated OpenCode root"
                if skill_output_looks_truncated(debug_skill["stdout"]):
                    warning += " (CLI output appears truncated)"
                    cli_probe["notes"].append(
                        "OpenCode debug skill can emit truncated skill dumps when many skills are installed; debug config and debug agent remain the authoritative startup proof surfaces."
                    )
                warnings.append(warning)

            debug_agent = run([opencode_cli, "debug", "agent", "vibe-plan"], cwd=repo_root, env=env)
            cli_probe["debug_agent_detects_vibe_plan"] = debug_agent["returncode"] == 0 and "vibe-plan" in (debug_agent["stdout"] + debug_agent["stderr"])
            if not cli_probe["debug_agent_detects_vibe_plan"]:
                failures.append("opencode debug agent vibe-plan did not recognize the installed preview agent")
                cli_probe["notes"].append("Custom agent discovery is part of the preview wrapper contract and must work.")
            cli_probe["debug_agent"] = debug_agent

        result = "PASS" if not failures else "FAIL"
        payload = {
            "gate": "opencode-preview-smoke",
            "result": result,
            "repo_root": str(repo_root),
            "target_root": str(target_root),
            "expected_files": EXPECTED_FILES,
            "missing_files": missing_files,
            "install": install_result,
            "check": check_result,
            "opencode_cli": cli_probe,
            "failures": failures,
            "warnings": warnings,
        }

        if args.write_artifacts:
            write_json(artifact_path, payload)

        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if failures:
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
