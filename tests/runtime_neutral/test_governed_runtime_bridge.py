from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_STAGE_IDS = [
    "skeleton_check",
    "deep_interview",
    "requirement_doc",
    "xl_plan",
    "plan_execute",
    "phase_cleanup",
]


def resolve_powershell() -> str | None:
    candidates = [
        shutil.which("pwsh"),
        shutil.which("pwsh.exe"),
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        r"C:\Program Files\PowerShell\7-preview\pwsh.exe",
        shutil.which("powershell"),
        shutil.which("powershell.exe"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate))
    return None


class GovernedRuntimeBridgeTests(unittest.TestCase):
    def test_version_governance_bridges_governed_runtime_surfaces(self) -> None:
        governance = json.loads((REPO_ROOT / "config" / "version-governance.json").read_text(encoding="utf-8"))
        packaging = governance["packaging"]["mirror"]
        runtime = governance["runtime"]["installed_runtime"]
        contract = json.loads((REPO_ROOT / "config" / "runtime-contract.json").read_text(encoding="utf-8"))

        self.assertIn("templates", packaging["directories"])
        self.assertIn("protocols", packaging["directories"])
        self.assertIn("scripts", packaging["directories"])

        required_markers = set(runtime["required_runtime_markers"])
        self.assertIn("scripts/runtime/VibeRuntime.Common.ps1", required_markers)
        self.assertIn("scripts/runtime/invoke-vibe-runtime.ps1", required_markers)
        self.assertIn("scripts/verify/vibe-governed-runtime-contract-gate.ps1", required_markers)
        self.assertIn("config/runtime-contract.json", required_markers)
        self.assertIn("config/runtime-modes.json", required_markers)
        self.assertIn("config/requirement-doc-policy.json", required_markers)
        self.assertIn("config/plan-execution-policy.json", required_markers)
        self.assertIn("config/phase-cleanup-policy.json", required_markers)

        self.assertEqual(
            EXPECTED_STAGE_IDS,
            [stage["id"] for stage in contract["stages"]],
        )

    def test_invoke_vibe_runtime_produces_six_stage_closure_under_temp_artifact_root(self) -> None:
        script_path = REPO_ROOT / "scripts" / "runtime" / "invoke-vibe-runtime.ps1"
        run_id = "pytest-governed-runtime"
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available in PATH")

        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir)
            command = [
                shell,
                "-NoLogo",
                "-NoProfile",
                "-Command",
                (
                    "& { "
                    f"$result = & '{script_path}' "
                    "-Task 'bridge governed runtime into a verified temporary artifact root' "
                    "-Mode benchmark_autonomous "
                    f"-RunId '{run_id}' "
                    f"-ArtifactRoot '{artifact_root}'; "
                    "$result | ConvertTo-Json -Depth 20 }"
                ),
            ]
            completed = subprocess.run(
                command,
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(completed.stdout)
            summary_path = Path(payload["summary_path"])
            session_root = Path(payload["session_root"])
            repo_root_text = str(REPO_ROOT.resolve()).lower()

            self.assertEqual(session_root / "runtime-summary.json", summary_path)
            self.assertFalse(str(session_root).lower().startswith(repo_root_text))
            self.assertFalse(str(summary_path).lower().startswith(repo_root_text))
            self.assertEqual(run_id, session_root.name)
            self.assertEqual("vibe-sessions", session_root.parent.name)
            self.assertEqual("runtime", session_root.parent.parent.name)
            self.assertEqual("outputs", session_root.parent.parent.parent.name)

            summary = payload["summary"]
            if summary_path.exists():
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual("benchmark_autonomous", summary["mode"])
            self.assertEqual(
                EXPECTED_STAGE_IDS,
                summary["stage_order"],
            )

            artifacts = summary["artifacts"]
            for key in (
                "skeleton_receipt",
                "intent_contract",
                "requirement_doc",
                "requirement_receipt",
                "execution_plan",
                "execution_plan_receipt",
                "execute_receipt",
                "cleanup_receipt",
            ):
                self.assertFalse(str(Path(artifacts[key])).lower().startswith(repo_root_text), key)

            if Path(artifacts["requirement_doc"]).exists():
                requirement_doc = Path(artifacts["requirement_doc"]).read_text(encoding="utf-8")
                self.assertIn("## Acceptance Criteria", requirement_doc)
                self.assertIn("## Assumptions", requirement_doc)
            self.assertEqual("requirements", Path(artifacts["requirement_doc"]).parent.name)
            self.assertEqual("plans", Path(artifacts["execution_plan"]).parent.name)


if __name__ == "__main__":
    unittest.main()
