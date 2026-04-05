from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


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


def run_governed_runtime(task: str, artifact_root: Path, env: dict[str, str] | None = None) -> dict[str, object]:
    shell = resolve_powershell()
    if shell is None:
        raise unittest.SkipTest("PowerShell executable not available in PATH")

    script_path = REPO_ROOT / "scripts" / "runtime" / "invoke-vibe-runtime.ps1"
    run_id = "pytest-memory-runtime-" + uuid.uuid4().hex[:10]
    command = [
        shell,
        "-NoLogo",
        "-NoProfile",
        "-Command",
        (
            "& { "
            f"$result = & '{script_path}' "
            f"-Task '{task}' "
            "-Mode interactive_governed "
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
        encoding="utf-8",
        env=env,
        check=True,
    )
    stdout = completed.stdout.strip()
    if stdout in ("", "null"):
        raise AssertionError(
            "invoke-vibe-runtime returned null payload. "
            f"stderr={completed.stderr.strip()}"
        )
    return json.loads(stdout)


class MemoryRuntimeActivationTests(unittest.TestCase):
    def test_runtime_emits_stage_aware_memory_activation_report(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            payload = run_governed_runtime(
                "Plan and debug a governed runtime enhancement with long-horizon continuity needs.",
                artifact_root=Path(tempdir),
            )
            summary = payload["summary"]
            artifacts = summary["artifacts"]

            self.assertIn("memory_activation_report", artifacts)
            self.assertIn("memory_activation_markdown", artifacts)

            report_path = Path(artifacts["memory_activation_report"])
            markdown_path = Path(artifacts["memory_activation_markdown"])

            self.assertTrue(report_path.exists())
            self.assertTrue(markdown_path.exists())

            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["run_id"], report["run_id"])
            self.assertEqual("shadow", report["policy"]["mode"])
            self.assertEqual("advisory_first_post_route_only", report["policy"]["routing_contract"])
            self.assertEqual("state_store", report["policy"]["canonical_owners"]["session"])
            self.assertEqual("Serena", report["policy"]["canonical_owners"]["project_decision"])
            self.assertEqual("ruflo", report["policy"]["canonical_owners"]["short_term_semantic"])
            self.assertEqual("Cognee", report["policy"]["canonical_owners"]["long_term_graph"])

            stages = report["stages"]
            self.assertEqual(
                [
                    "skeleton_check",
                    "deep_interview",
                    "requirement_doc",
                    "xl_plan",
                    "plan_execute",
                    "phase_cleanup",
                ],
                [stage["stage"] for stage in stages],
            )

            skeleton = stages[0]
            self.assertEqual("fallback_local_digest", skeleton["read_actions"][0]["status"])
            self.assertLessEqual(
                len(skeleton["read_actions"][0]["items"]),
                skeleton["read_actions"][0]["budget"]["top_k"],
            )

            deep_interview = stages[1]
            self.assertEqual("deferred_no_project_key", deep_interview["read_actions"][0]["status"])

            requirement_stage = stages[2]
            self.assertGreaterEqual(requirement_stage["context_injection"]["injected_item_count"], 1)
            self.assertLessEqual(
                requirement_stage["context_injection"]["estimated_tokens"],
                requirement_stage["context_injection"]["budget"]["max_tokens"],
            )

            execute_stage = stages[4]
            self.assertGreaterEqual(execute_stage["write_actions"][0]["item_count"], 1)
            self.assertTrue(Path(execute_stage["write_actions"][0]["artifact_path"]).exists())
            self.assertIn(
                execute_stage["write_actions"][0]["status"],
                {"fallback_local_artifact", "backend_write"},
            )

            cleanup_stage = stages[5]
            self.assertEqual("guarded_no_write", cleanup_stage["write_actions"][0]["status"])
            self.assertTrue(Path(cleanup_stage["write_actions"][1]["artifact_path"]).exists())
            self.assertEqual("generated_local_fold", cleanup_stage["write_actions"][1]["status"])

            summary_block = report["summary"]
            self.assertEqual(6, summary_block["stage_count"])
            self.assertGreaterEqual(summary_block["fallback_event_count"], 1)
            self.assertGreaterEqual(summary_block["artifact_count"], 3)
            self.assertTrue(summary_block["budget_guard_respected"])

    def test_runtime_reads_and_writes_real_memory_backends_across_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            temp_root = Path(tempdir)
            backend_root = temp_root / "backends"
            env = os.environ.copy()
            env["VIBE_MEMORY_BACKEND_ROOT"] = str(backend_root)
            env["SERENA_PROJECT_KEY"] = "pytest-memory-project"

            first = run_governed_runtime(
                "XL approved decision: keep api worker runtime continuity and graph relationship between api worker and planner.",
                artifact_root=temp_root / "run-1",
                env=env,
            )
            first_report = json.loads(
                Path(first["summary"]["artifacts"]["memory_activation_report"]).read_text(encoding="utf-8")
            )
            first_execute = first_report["stages"][4]
            first_cleanup = first_report["stages"][5]

            self.assertEqual("backend_write", first_execute["write_actions"][1]["status"])
            self.assertEqual("backend_write", first_cleanup["write_actions"][0]["status"])
            self.assertEqual("backend_write", first_cleanup["write_actions"][2]["status"])

            second = run_governed_runtime(
                "XL follow-up api worker continuity review with decision reuse and graph dependency recall.",
                artifact_root=temp_root / "run-2",
                env=env,
            )
            second_report = json.loads(
                Path(second["summary"]["artifacts"]["memory_activation_report"]).read_text(encoding="utf-8")
            )

            skeleton = second_report["stages"][0]
            deep_interview = second_report["stages"][1]
            execute_stage = second_report["stages"][4]

            self.assertGreaterEqual(len(skeleton["read_actions"]), 2)
            self.assertEqual("backend_read", skeleton["read_actions"][1]["status"])
            self.assertGreaterEqual(skeleton["read_actions"][1]["item_count"], 1)

            self.assertEqual("backend_read", deep_interview["read_actions"][0]["status"])
            self.assertGreaterEqual(deep_interview["read_actions"][0]["item_count"], 1)

            self.assertGreaterEqual(len(execute_stage["read_actions"]), 1)
            self.assertEqual("backend_read", execute_stage["read_actions"][0]["status"])
            self.assertGreaterEqual(execute_stage["read_actions"][0]["item_count"], 1)

            requirement_text = Path(second["summary"]["artifacts"]["requirement_doc"]).read_text(encoding="utf-8")
            self.assertIn("## Memory Context", requirement_text)
            self.assertIn("Serena decision:", requirement_text)

            plan_text = Path(second["summary"]["artifacts"]["execution_plan"]).read_text(encoding="utf-8")
            self.assertIn("## Memory Context", plan_text)
            self.assertIn("Cognee relation:", plan_text)


if __name__ == "__main__":
    unittest.main()
