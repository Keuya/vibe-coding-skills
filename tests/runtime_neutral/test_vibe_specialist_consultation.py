from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FREEZE_SCRIPT = REPO_ROOT / "scripts" / "runtime" / "Freeze-RuntimeInputPacket.ps1"
RUNTIME_SCRIPT = REPO_ROOT / "scripts" / "runtime" / "invoke-vibe-runtime.ps1"
CONSULTATION_SCRIPT = REPO_ROOT / "scripts" / "runtime" / "VibeConsultation.Common.ps1"
RUNTIME_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeRuntime.Common.ps1"
EXECUTION_COMMON = REPO_ROOT / "scripts" / "runtime" / "VibeExecution.Common.ps1"
SPECIALIST_TASK = "I have a failing test and a stack trace. Help me debug systematically before proposing fixes."


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


def _ps_single_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def load_json(path: str | Path) -> dict[str, object]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def freeze_runtime_packet(task: str, artifact_root: Path) -> dict[str, object]:
    shell = resolve_powershell()
    if shell is None:
        raise unittest.SkipTest("PowerShell executable not available in PATH")

    run_id = "pytest-consult-freeze-" + uuid.uuid4().hex[:10]
    completed = subprocess.run(
        [
            shell,
            "-NoLogo",
            "-NoProfile",
            "-Command",
            (
                "& { "
                f"$result = & '{FREEZE_SCRIPT}' "
                f"-Task '{task}' "
                "-Mode interactive_governed "
                f"-RunId '{run_id}' "
                f"-ArtifactRoot '{artifact_root}'; "
                "$result | ConvertTo-Json -Depth 20 }"
            ),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        env=dict(os.environ),
    )
    return json.loads(completed.stdout)


def run_runtime(
    task: str,
    artifact_root: Path,
    *,
    extra_env: dict[str, str] | None = None,
    check: bool = True,
) -> dict[str, object] | subprocess.CompletedProcess[str]:
    shell = resolve_powershell()
    if shell is None:
        raise unittest.SkipTest("PowerShell executable not available in PATH")

    run_id = "pytest-consult-runtime-" + uuid.uuid4().hex[:10]
    completed = subprocess.run(
        [
            shell,
            "-NoLogo",
            "-NoProfile",
            "-Command",
            (
                "& { "
                f"$result = & '{RUNTIME_SCRIPT}' "
                f"-Task '{task}' "
                "-Mode interactive_governed "
                f"-RunId '{run_id}' "
                f"-ArtifactRoot '{artifact_root}'; "
                "$result | ConvertTo-Json -Depth 20 }"
            ),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=check,
        env={**os.environ, **(extra_env or {})},
    )
    if check:
        return json.loads(completed.stdout)
    return completed


def create_fake_codex_command(directory: Path) -> Path:
    suffix = ".cmd" if os.name == "nt" else ""
    command_path = directory / f"codex{suffix}"
    if os.name == "nt":
        command_path.write_text(
            "@echo off\r\n"
            "setlocal EnableDelayedExpansion\r\n"
            "set OUT=\r\n"
            ":loop\r\n"
            "if \"%~1\"==\"\" goto done\r\n"
            "if /I \"%~1\"==\"-o\" (\r\n"
            "  set OUT=%~2\r\n"
            "  shift\r\n"
            "  shift\r\n"
            "  goto loop\r\n"
            ")\r\n"
            "shift\r\n"
            "goto loop\r\n"
            ":done\r\n"
            "if \"%OUT%\"==\"\" exit /b 2\r\n"
            "> \"%OUT%\" echo {\"status\":\"completed\",\"summary\":\"Consulted specialist and produced bounded guidance.\",\"consultation_notes\":[\"Validate the failing path before proposing a fix.\"],\"adoption_notes\":[\"Use the systematic-debugging workflow to shape requirement and plan wording.\"],\"verification_notes\":[\"Consultation stayed read-only and returned structured guidance.\"]}\r\n"
            "echo fake codex consultation ok\r\n"
            "exit /b 0\r\n",
            encoding="utf-8",
        )
    else:
        command_path.write_text(
            "#!/usr/bin/env sh\n"
            "OUT=''\n"
            "while [ \"$#\" -gt 0 ]; do\n"
            "  case \"$1\" in\n"
            "    -o)\n"
            "      OUT=\"$2\"\n"
            "      shift 2\n"
            "      ;;\n"
            "    *)\n"
            "      shift\n"
            "      ;;\n"
            "  esac\n"
            "done\n"
            "if [ -z \"$OUT\" ]; then\n"
            "  exit 2\n"
            "fi\n"
            "printf '%s' '{\"status\":\"completed\",\"summary\":\"Consulted specialist and produced bounded guidance.\",\"consultation_notes\":[\"Validate the failing path before proposing a fix.\"],\"adoption_notes\":[\"Use the systematic-debugging workflow to shape requirement and plan wording.\"],\"verification_notes\":[\"Consultation stayed read-only and returned structured guidance.\"]}' > \"$OUT\"\n"
            "printf 'fake codex consultation ok\\n'\n",
            encoding="utf-8",
        )
        command_path.chmod(command_path.stat().st_mode | stat.S_IXUSR)
    return command_path


def create_incomplete_fake_codex_command(directory: Path) -> Path:
    suffix = ".cmd" if os.name == "nt" else ""
    command_path = directory / f"codex-incomplete{suffix}"
    if os.name == "nt":
        command_path.write_text(
            "@echo off\r\n"
            "setlocal EnableDelayedExpansion\r\n"
            "set OUT=\r\n"
            ":loop\r\n"
            "if \"%~1\"==\"\" goto done\r\n"
            "if /I \"%~1\"==\"-o\" (\r\n"
            "  set OUT=%~2\r\n"
            "  shift\r\n"
            "  shift\r\n"
            "  goto loop\r\n"
            ")\r\n"
            "shift\r\n"
            "goto loop\r\n"
            ":done\r\n"
            "if \"%OUT%\"==\"\" exit /b 2\r\n"
            "> \"%OUT%\" echo {\"status\":\"completed\",\"summary\":\"\",\"consultation_notes\":[],\"adoption_notes\":[],\"verification_notes\":[]}\r\n"
            "echo fake codex incomplete consultation\r\n"
            "exit /b 0\r\n",
            encoding="utf-8",
        )
    else:
        command_path.write_text(
            "#!/usr/bin/env sh\n"
            "OUT=''\n"
            "while [ \"$#\" -gt 0 ]; do\n"
            "  case \"$1\" in\n"
            "    -o)\n"
            "      OUT=\"$2\"\n"
            "      shift 2\n"
            "      ;;\n"
            "    *)\n"
            "      shift\n"
            "      ;;\n"
            "  esac\n"
            "done\n"
            "if [ -z \"$OUT\" ]; then\n"
            "  exit 2\n"
            "fi\n"
            "printf '%s' '{\"status\":\"completed\",\"summary\":\"\",\"consultation_notes\":[],\"adoption_notes\":[],\"verification_notes\":[]}' > \"$OUT\"\n"
            "printf 'fake codex incomplete consultation\\n'\n",
            encoding="utf-8",
        )
        command_path.chmod(command_path.stat().st_mode | stat.S_IXUSR)
    return command_path


class VibeSpecialistConsultationTests(unittest.TestCase):
    def test_consultation_window_invokes_specialist_and_emits_progressive_disclosure(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available in PATH")

        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir)
            fake_codex = create_fake_codex_command(artifact_root)
            freeze_payload = freeze_runtime_packet(SPECIALIST_TASK, artifact_root)
            packet_path = Path(freeze_payload["packet_path"])
            run_id = "pytest-consult-window-" + uuid.uuid4().hex[:10]
            prompt_seed_path = artifact_root / "discussion-seed.md"
            prompt_seed_path.write_text("# Intent\nNeed systematic debugging guidance before freezing requirements.\n", encoding="utf-8")

            ps_script = (
                "& { "
                f". {_ps_single_quote(str(RUNTIME_COMMON))}; "
                f". {_ps_single_quote(str(EXECUTION_COMMON))}; "
                f". {_ps_single_quote(str(CONSULTATION_SCRIPT))}; "
                f"$runtime = Get-VibeRuntimeContext -ScriptPath {_ps_single_quote(str(CONSULTATION_SCRIPT))}; "
                f"$packet = Get-Content -LiteralPath {_ps_single_quote(str(packet_path))} -Raw -Encoding UTF8 | ConvertFrom-Json; "
                f"$sessionRoot = Ensure-VibeSessionRoot -RepoRoot $runtime.repo_root -RunId {_ps_single_quote(run_id)} -Runtime $runtime -ArtifactRoot {_ps_single_quote(str(artifact_root))}; "
                f"$result = Invoke-VibeSpecialistConsultationWindow "
                f"-Task {_ps_single_quote(SPECIALIST_TASK)} "
                f"-RunId {_ps_single_quote(run_id)} "
                f"-SessionRoot $sessionRoot "
                f"-RepoRoot $runtime.repo_root "
                f"-WindowId 'discussion' "
                f"-Stage 'deep_interview' "
                f"-SourceArtifactPath {_ps_single_quote(str(prompt_seed_path))} "
                f"-Recommendations @($packet.specialist_recommendations) "
                f"-Policy $runtime.specialist_consultation_policy; "
                "$result | ConvertTo-Json -Depth 20 }"
            )
            completed = subprocess.run(
                [shell, "-NoLogo", "-NoProfile", "-Command", ps_script],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                env={
                    **os.environ,
                    "VGO_ENABLE_NATIVE_SPECIALIST_EXECUTION": "1",
                    "VGO_DISABLE_NATIVE_SPECIALIST_EXECUTION": "0",
                    "VGO_CODEX_EXECUTABLE": str(fake_codex),
                },
            )
            payload = json.loads(completed.stdout)
            receipt = load_json(payload["receipt_path"])

            self.assertEqual("discussion", receipt["window_id"])
            self.assertEqual("deep_interview", receipt["stage"])
            self.assertGreaterEqual(len(list(receipt["approved_consultation"])), 1)
            self.assertGreaterEqual(len(list(receipt["consulted_units"])), 1)
            self.assertGreaterEqual(len(list(receipt["user_disclosures"])), 1)

            disclosure = next(
                item for item in list(receipt["user_disclosures"]) if item["skill_id"] == "systematic-debugging"
            )
            self.assertTrue(disclosure["why_now"])
            self.assertTrue(Path(disclosure["native_skill_entrypoint"]).is_absolute())
            self.assertTrue(Path(disclosure["native_skill_entrypoint"]).exists())
            self.assertIn("systematic-debugging", disclosure["rendered_text"])
            self.assertIn(disclosure["native_skill_entrypoint"], disclosure["rendered_text"])

            consulted = next(
                item for item in list(receipt["consulted_units"]) if item["skill_id"] == "systematic-debugging"
            )
            self.assertEqual("completed", consulted["status"])
            self.assertTrue(bool(consulted["live_native_execution"]))
            self.assertEqual([], list(consulted["observed_changed_files"]))
            self.assertTrue(Path(consulted["response_json_path"]).exists())
            self.assertTrue(Path(consulted["prompt_path"]).exists())
            self.assertTrue(Path(consulted["schema_path"]).exists())
            self.assertGreaterEqual(len(list(consulted["consultation_notes"])), 1)
            self.assertGreaterEqual(len(list(consulted["adoption_notes"])), 1)
            self.assertGreaterEqual(len(list(consulted["verification_notes"])), 1)

    def test_runtime_projects_consultation_truth_into_summary_requirement_and_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir)
            payload = run_runtime(
                SPECIALIST_TASK,
                artifact_root,
                extra_env={"VGO_DISABLE_NATIVE_SPECIALIST_EXECUTION": "1"},
            )
            summary = payload["summary"]
            artifacts = summary["artifacts"]

            self.assertIn("discussion_specialist_consultation", artifacts)
            self.assertIn("planning_specialist_consultation", artifacts)
            self.assertIn("specialist_lifecycle_disclosure", artifacts)

            discussion_receipt = load_json(artifacts["discussion_specialist_consultation"])
            planning_receipt = load_json(artifacts["planning_specialist_consultation"])
            lifecycle_disclosure = load_json(artifacts["specialist_lifecycle_disclosure"])
            requirement_receipt = load_json(artifacts["requirement_receipt"])
            plan_receipt = load_json(artifacts["execution_plan_receipt"])
            requirement_doc = Path(artifacts["requirement_doc"]).read_text(encoding="utf-8")
            execution_plan = Path(artifacts["execution_plan"]).read_text(encoding="utf-8")

            for receipt in (discussion_receipt, planning_receipt):
                self.assertTrue(bool(receipt["enabled"]))
                self.assertGreaterEqual(len(list(receipt["approved_consultation"])), 1)
                self.assertGreaterEqual(len(list(receipt["user_disclosures"])), 1)
                disclosure = next(
                    item for item in list(receipt["user_disclosures"]) if item["skill_id"] == "systematic-debugging"
                )
                self.assertTrue(disclosure["why_now"])
                self.assertTrue(Path(disclosure["native_skill_entrypoint"]).is_absolute())
                self.assertTrue(Path(disclosure["native_skill_entrypoint"]).exists())

            specialist_consultation = summary["specialist_consultation"]
            self.assertTrue(bool(specialist_consultation["enabled"]))
            self.assertEqual(2, int(specialist_consultation["window_count"]))
            self.assertEqual(
                ["discussion", "planning"],
                [str(window["window_id"]) for window in list(specialist_consultation["windows"])],
            )
            self.assertGreaterEqual(int(specialist_consultation["user_disclosure_count"]), 2)
            self.assertNotIn("specialist_consultation", summary["specialist_user_disclosure"])

            specialist_lifecycle = summary["specialist_lifecycle_disclosure"]
            self.assertTrue(bool(specialist_lifecycle["enabled"]))
            self.assertEqual("routing_consultation_execution_separated", specialist_lifecycle["truth_model"])
            self.assertEqual(
                ["discussion_routing", "discussion_consultation", "planning_consultation", "execution_dispatch"],
                [str(layer["layer_id"]) for layer in list(specialist_lifecycle["layers"])],
            )
            self.assertGreaterEqual(int(specialist_lifecycle["skill_count"]), 1)
            self.assertIn("systematic-debugging", specialist_lifecycle["rendered_text"])
            self.assertEqual("routing_consultation_execution_separated", lifecycle_disclosure["truth_model"])
            routing_layer = next(
                item for item in list(lifecycle_disclosure["layers"]) if item["layer_id"] == "discussion_routing"
            )
            routed_entry = next(
                item for item in list(routing_layer["skills"]) if item["skill_id"] == "systematic-debugging"
            )
            self.assertTrue(routed_entry["why_now"])
            self.assertTrue(Path(routed_entry["native_skill_entrypoint"]).is_absolute())
            self.assertTrue(Path(routed_entry["native_skill_entrypoint"]).exists())

            self.assertEqual(artifacts["discussion_specialist_consultation"], requirement_receipt["discussion_consultation_path"])
            self.assertEqual(artifacts["planning_specialist_consultation"], plan_receipt["planning_consultation_path"])
            self.assertEqual(artifacts["specialist_lifecycle_disclosure"], requirement_receipt["specialist_lifecycle_disclosure_path"])
            self.assertEqual(artifacts["specialist_lifecycle_disclosure"], plan_receipt["specialist_lifecycle_disclosure_path"])
            self.assertIn("host_stage_disclosure", artifacts)
            host_stage_disclosure = load_json(artifacts["host_stage_disclosure"])
            self.assertTrue(bool(host_stage_disclosure["enabled"]))
            self.assertEqual("progressive_host_stage_disclosure", host_stage_disclosure["mode"])
            self.assertEqual(4, int(host_stage_disclosure["event_count"]))
            self.assertEqual(4, int(host_stage_disclosure["last_sequence"]))
            self.assertEqual(
                [
                    "discussion_routing_frozen",
                    "discussion_consultation_completed",
                    "planning_consultation_completed",
                    "execution_dispatch_confirmed",
                ],
                [str(event["event_id"]) for event in list(host_stage_disclosure["events"])],
            )
            self.assertEqual(
                ["discussion_routing", "discussion_consultation", "planning_consultation", "execution_dispatch"],
                [str(event["segment_id"]) for event in list(host_stage_disclosure["events"])],
            )
            self.assertEqual([1, 2, 3, 4], [int(event["sequence"]) for event in list(host_stage_disclosure["events"])])
            self.assertIn("Vibe routed these Skills", host_stage_disclosure["rendered_text"])
            self.assertIn("Vibe approved these Skills for execution", host_stage_disclosure["rendered_text"])
            execution_event = next(
                item for item in list(host_stage_disclosure["events"]) if item["segment_id"] == "execution_dispatch"
            )
            routed_skill = next(item for item in list(execution_event["skills"]) if item["skill_id"] == "systematic-debugging")
            self.assertTrue(Path(routed_skill["native_skill_entrypoint"]).is_absolute())
            self.assertTrue(Path(routed_skill["native_skill_entrypoint"]).exists())
            self.assertEqual(host_stage_disclosure, summary["host_stage_disclosure"])
            self.assertIn("host_user_briefing", artifacts)
            host_user_briefing_doc = Path(artifacts["host_user_briefing"]).read_text(encoding="utf-8")
            host_user_briefing = summary["host_user_briefing"]
            self.assertTrue(bool(host_user_briefing["enabled"]))
            self.assertTrue(bool(host_user_briefing["freeze_gate_passed"]))
            self.assertEqual(
                ["discussion_routing", "discussion_consultation", "planning_consultation", "execution_dispatch"],
                [str(segment["segment_id"]) for segment in list(host_user_briefing["segments"])],
            )
            self.assertIn("Vibe routed these Skills", host_user_briefing["rendered_text"])
            self.assertIn("Vibe consulted these Skills during discussion", host_user_briefing["rendered_text"])
            self.assertIn("freeze gate: passed", host_user_briefing["rendered_text"])
            self.assertIn("Vibe approved these Skills for execution", host_user_briefing["rendered_text"])
            self.assertIn("systematic-debugging", host_user_briefing["rendered_text"])
            self.assertIn(host_user_briefing["rendered_text"], host_user_briefing_doc)
            self.assertEqual(artifacts["host_user_briefing"], payload["host_user_briefing_path"])
            self.assertEqual(host_user_briefing, payload["host_user_briefing"])
            self.assertIn("## Specialist Consultation", requirement_doc)
            self.assertIn("## Specialist Consultation", execution_plan)
            self.assertIn("## Unified Specialist Lifecycle Disclosure", requirement_doc)
            self.assertIn("## Unified Specialist Lifecycle Disclosure", execution_plan)
            self.assertIn("systematic-debugging", requirement_doc)
            self.assertIn("systematic-debugging", execution_plan)

    def test_live_consultation_with_empty_guidance_is_degraded_and_fails_freeze_gate(self) -> None:
        shell = resolve_powershell()
        if shell is None:
            self.skipTest("PowerShell executable not available in PATH")

        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir)
            fake_codex = create_incomplete_fake_codex_command(artifact_root)
            freeze_payload = freeze_runtime_packet(SPECIALIST_TASK, artifact_root)
            packet_path = Path(freeze_payload["packet_path"])
            run_id = "pytest-consult-window-invalid-" + uuid.uuid4().hex[:10]
            prompt_seed_path = artifact_root / "discussion-seed.md"
            prompt_seed_path.write_text("# Intent\nNeed systematic debugging guidance before freezing requirements.\n", encoding="utf-8")

            ps_script = (
                "& { "
                f". {_ps_single_quote(str(RUNTIME_COMMON))}; "
                f". {_ps_single_quote(str(EXECUTION_COMMON))}; "
                f". {_ps_single_quote(str(CONSULTATION_SCRIPT))}; "
                f"$runtime = Get-VibeRuntimeContext -ScriptPath {_ps_single_quote(str(CONSULTATION_SCRIPT))}; "
                f"$packet = Get-Content -LiteralPath {_ps_single_quote(str(packet_path))} -Raw -Encoding UTF8 | ConvertFrom-Json; "
                f"$sessionRoot = Ensure-VibeSessionRoot -RepoRoot $runtime.repo_root -RunId {_ps_single_quote(run_id)} -Runtime $runtime -ArtifactRoot {_ps_single_quote(str(artifact_root))}; "
                f"$result = Invoke-VibeSpecialistConsultationWindow "
                f"-Task {_ps_single_quote(SPECIALIST_TASK)} "
                f"-RunId {_ps_single_quote(run_id)} "
                f"-SessionRoot $sessionRoot "
                f"-RepoRoot $runtime.repo_root "
                f"-WindowId 'discussion' "
                f"-Stage 'deep_interview' "
                f"-SourceArtifactPath {_ps_single_quote(str(prompt_seed_path))} "
                f"-Recommendations @($packet.specialist_recommendations) "
                f"-Policy $runtime.specialist_consultation_policy; "
                "$result | ConvertTo-Json -Depth 20 }"
            )
            completed = subprocess.run(
                [shell, "-NoLogo", "-NoProfile", "-Command", ps_script],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                env={
                    **os.environ,
                    "VGO_ENABLE_NATIVE_SPECIALIST_EXECUTION": "1",
                    "VGO_DISABLE_NATIVE_SPECIALIST_EXECUTION": "0",
                    "VGO_CODEX_EXECUTABLE": str(fake_codex),
                },
            )
            payload = json.loads(completed.stdout)
            receipt = load_json(payload["receipt_path"])

            self.assertEqual([], list(receipt["consulted_units"]))
            self.assertGreaterEqual(len(list(receipt["degraded"])), 1)
            degraded = next(
                item for item in list(receipt["degraded"]) if item["skill_id"] == "systematic-debugging"
            )
            self.assertTrue(bool(degraded["live_native_execution"]))
            self.assertFalse(bool(degraded["verification_passed"]))
            self.assertIn("freeze_gate", receipt)
            self.assertFalse(bool(receipt["freeze_gate"]["passed"]))
            self.assertIn(
                "live_degraded_result:systematic-debugging",
                list(receipt["freeze_gate"]["errors"]),
            )

    def test_runtime_blocks_freeze_when_live_consultation_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            artifact_root = Path(tempdir)
            fake_codex = create_incomplete_fake_codex_command(artifact_root)
            completed = run_runtime(
                SPECIALIST_TASK,
                artifact_root,
                extra_env={
                    "VGO_ENABLE_NATIVE_SPECIALIST_EXECUTION": "1",
                    "VGO_DISABLE_NATIVE_SPECIALIST_EXECUTION": "0",
                    "VGO_CODEX_EXECUTABLE": str(fake_codex),
                },
                check=False,
            )

            self.assertNotEqual(0, completed.returncode)
            combined_output = f"{completed.stdout}\n{completed.stderr}"
            self.assertIn("specialist consultation freeze gate failed", combined_output)
