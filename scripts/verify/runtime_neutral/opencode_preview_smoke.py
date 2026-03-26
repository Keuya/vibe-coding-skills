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

        opencode_cli = shutil.which("opencode")
        cli_probe = {
            "present": bool(opencode_cli),
            "binary": opencode_cli,
            "debug_paths": None,
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
                warnings.append("opencode debug paths failed in isolated env")

            debug_skill = run([opencode_cli, "debug", "skill"], cwd=repo_root, env=env)
            skill_hits = ("\"name\": \"vibe\"" in debug_skill["stdout"]) or ("skills/vibe/SKILL.md" in debug_skill["stdout"])
            cli_probe["debug_skill_detects_vibe"] = skill_hits
            if debug_skill["returncode"] != 0:
                warnings.append("opencode debug skill failed in isolated env")
            if not skill_hits:
                warnings.append("opencode debug skill did not enumerate the installed vibe skill in the isolated OpenCode root")
                cli_probe["notes"].append("This matches the known 1.2.27 discovery drift and is treated as a preview blocker, not a smoke failure.")

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
