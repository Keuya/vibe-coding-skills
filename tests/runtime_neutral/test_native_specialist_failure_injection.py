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


def run_runtime(
    task: str,
    artifact_root: Path,
    *,
    governance_scope: str = "root",
    extra_env: dict[str, str] | None = None,
) -> dict[str, object]:
    shell = resolve_powershell()
    if shell is None:
        raise unittest.SkipTest("PowerShell executable not available in PATH")

    script_path = REPO_ROOT / "scripts/runtime/invoke-vibe-runtime.ps1"
    run_id = "pytest-native-failure-" + uuid.uuid4().hex[:10]
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
            f"-GovernanceScope {governance_scope} "
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
        check=True,
        env={**os.environ, **(extra_env or {})},
    )
    stdout = completed.stdout.strip()
    if stdout in ("", "null"):
        raise AssertionError(
            "invoke-vibe-runtime returned null payload. "
            f"stderr={completed.stderr.strip()}"
        )
    return json.loads(stdout)


def load_json(path: str | Path) -> dict[str, object]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def create_fake_codex_command(directory: Path, *, mode: str) -> Path:
    suffix = ".cmd" if os.name == "nt" else ""
    command_path = directory / f"codex{suffix}"
    if os.name == "nt":
        behaviors = {
            "malformed_json": (
                "> \"%OUT%\" echo {bad-json\r\n"
                "echo fake codex malformed\r\n"
                "exit /b 0\r\n"
            ),
            "missing_required_fields": (
                "> \"%OUT%\" echo {\"status\":\"completed\",\"summary\":\"missing arrays\"}\r\n"
                "echo fake codex schema gap\r\n"
                "exit /b 0\r\n"
            ),
            "missing_response": (
                "echo fake codex no response\r\n"
                "exit /b 0\r\n"
            ),
            "nonzero_with_response": (
                "> \"%OUT%\" echo {\"status\":\"completed\",\"summary\":\"fake codex wrote payload before failing\",\"verification_notes\":[\"nonzero exit injected\"],\"changed_files\":[],\"bounded_output_notes\":[\"failure injection\"]}\r\n"
                "echo fake codex nonzero with response\r\n"
                "exit /b 17\r\n"
            ),
        }
        behavior = behaviors[mode]
        command_path.write_text(
            "@echo off\r\n"
            "setlocal EnableDelayedExpansion\r\n"
            "set OUT=\r\n"
            ":loop\r\n"
            "if \"%~1\"==\"\" goto done\r\n"
            "if \"%~1\"==\"-o\" (\r\n"
            "  set OUT=%~2\r\n"
            "  shift\r\n"
            "  shift\r\n"
            "  goto loop\r\n"
            ")\r\n"
            "shift\r\n"
            "goto loop\r\n"
            ":done\r\n"
            "if \"%OUT%\"==\"\" exit /b 2\r\n"
            + behavior,
            encoding="utf-8",
        )
    else:
        behaviors = {
            "malformed_json": (
                "printf '%s' '{bad-json' > \"$OUT\"\n"
                "printf 'fake codex malformed\\n'\n"
                "exit 0\n"
            ),
            "missing_required_fields": (
                "printf '%s' '{\"status\":\"completed\",\"summary\":\"missing arrays\"}' > \"$OUT\"\n"
                "printf 'fake codex schema gap\\n'\n"
                "exit 0\n"
            ),
            "missing_response": (
                "printf 'fake codex no response\\n'\n"
                "exit 0\n"
            ),
            "nonzero_with_response": (
                "printf '%s' '{\"status\":\"completed\",\"summary\":\"fake codex wrote payload before failing\",\"verification_notes\":[\"nonzero exit injected\"],\"changed_files\":[],\"bounded_output_notes\":[\"failure injection\"]}' > \"$OUT\"\n"
                "printf 'fake codex nonzero with response\\n'\n"
                "exit 17\n"
            ),
        }
        behavior = behaviors[mode]
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
            + behavior,
            encoding="utf-8",
        )
        command_path.chmod(command_path.stat().st_mode | stat.S_IXUSR)
    return command_path


class NativeSpecialistFailureInjectionTests(unittest.TestCase):
    TASK = "I have a failing test and stack trace. Debug systematically and execute specialist workflow."

    def run_failure_case(
        self, mode: str
    ) -> tuple[dict[str, object], dict[str, object], list[tuple[dict[str, object], dict[str, object]]]]:
        with tempfile.TemporaryDirectory() as tempdir:
            temp_path = Path(tempdir)
            fake_codex = create_fake_codex_command(temp_path, mode=mode)
            payload = run_runtime(
                task=self.TASK,
                artifact_root=temp_path,
                governance_scope="root",
                extra_env={
                    "VGO_ENABLE_NATIVE_SPECIALIST_EXECUTION": "1",
                    "VGO_DISABLE_NATIVE_SPECIALIST_EXECUTION": "0",
                    "VGO_CODEX_EXECUTABLE": str(fake_codex),
                },
            )
            summary = payload["summary"]
            execution_manifest = load_json(summary["artifacts"]["execution_manifest"])
            specialist_accounting = execution_manifest["specialist_accounting"]
            live_failures = [
                (unit, load_json(unit["result_path"]))
                for unit in list(specialist_accounting["failed_specialist_units"])
            ]
            self.assertGreaterEqual(len(live_failures), 1)
            self.assertEqual("live_native_failed", specialist_accounting["effective_execution_status"])
            self.assertGreaterEqual(int(specialist_accounting["attempted_specialist_unit_count"]), 1)
            self.assertEqual(0, int(specialist_accounting["executed_specialist_unit_count"]))
            self.assertGreaterEqual(int(specialist_accounting["failed_specialist_unit_count"]), 1)
            self.assertEqual("completed_with_failures", execution_manifest["status"])

            execution_proof = load_json(summary["artifacts"]["execution_proof_manifest"])
            self.assertEqual("live_native_failed", execution_proof["specialist_execution_status"])
            self.assertEqual(
                int(specialist_accounting["failed_specialist_unit_count"]),
                int(execution_proof["failed_specialist_unit_count"]),
            )
            return payload, execution_manifest, live_failures

    def test_malformed_json_response_is_recorded_as_live_native_failure(self) -> None:
        _, _, live_failures = self.run_failure_case("malformed_json")
        for unit, result in live_failures:
            with self.subTest(unit_id=unit.get("unit_id", "")):
                expected_artifacts = list(result["expected_artifacts"])
                self.assertEqual(1, len(expected_artifacts))
                self.assertEqual("failed", result["status"])
                self.assertEqual(0, int(result["exit_code"]))
                self.assertFalse(bool(result["verification_passed"]))
                self.assertTrue(bool(result["live_native_execution"]))
                self.assertFalse(bool(result["degraded"]))
                self.assertTrue(bool(expected_artifacts[0]["exists"]))
                self.assertTrue(result["response_parse_error"])
                self.assertNotEqual("native_specialist_response_missing", result["response_parse_error"])

    def test_missing_response_file_is_recorded_as_live_native_failure(self) -> None:
        _, _, live_failures = self.run_failure_case("missing_response")
        for unit, result in live_failures:
            with self.subTest(unit_id=unit.get("unit_id", "")):
                expected_artifacts = list(result["expected_artifacts"])
                self.assertEqual(1, len(expected_artifacts))
                self.assertEqual("failed", result["status"])
                self.assertEqual(0, int(result["exit_code"]))
                self.assertFalse(bool(result["verification_passed"]))
                self.assertTrue(bool(result["live_native_execution"]))
                self.assertFalse(bool(result["degraded"]))
                self.assertFalse(Path(result["response_json_path"]).exists())
                self.assertEqual("native_specialist_response_missing", result["response_parse_error"])
                self.assertFalse(bool(expected_artifacts[0]["exists"]))

    def test_missing_required_fields_fail_schema_validation(self) -> None:
        _, _, live_failures = self.run_failure_case("missing_required_fields")
        for unit, result in live_failures:
            with self.subTest(unit_id=unit.get("unit_id", "")):
                self.assertEqual("failed", result["status"])
                self.assertEqual(0, int(result["exit_code"]))
                self.assertFalse(bool(result["verification_passed"]))
                self.assertTrue(bool(result["live_native_execution"]))
                self.assertFalse(bool(result["degraded"]))
                self.assertIsNone(result["response_parse_error"])
                self.assertIn("missing_required_field:verification_notes", list(result["response_schema_errors"]))
                self.assertIn("missing_required_field:changed_files", list(result["response_schema_errors"]))
                self.assertIn("missing_required_field:bounded_output_notes", list(result["response_schema_errors"]))

    def test_nonzero_exit_with_response_is_not_misclassified_as_completed(self) -> None:
        _, _, live_failures = self.run_failure_case("nonzero_with_response")
        for unit, result in live_failures:
            with self.subTest(unit_id=unit.get("unit_id", "")):
                expected_artifacts = list(result["expected_artifacts"])
                self.assertEqual(1, len(expected_artifacts))
                self.assertEqual("failed", result["status"])
                self.assertEqual(17, int(result["exit_code"]))
                self.assertFalse(bool(result["verification_passed"]))
                self.assertTrue(bool(result["live_native_execution"]))
                self.assertFalse(bool(result["degraded"]))
                self.assertTrue(bool(expected_artifacts[0]["exists"]))
                self.assertIsNone(result["response_parse_error"])
                self.assertEqual(
                    "fake codex wrote payload before failing",
                    result["summary"],
                )


if __name__ == "__main__":
    unittest.main()
