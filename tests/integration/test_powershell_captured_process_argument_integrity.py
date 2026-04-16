from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]


def _require_powershell() -> str:
    powershell = shutil.which("pwsh") or shutil.which("powershell")
    if not powershell:
        pytest.skip("PowerShell executable not available in PATH")
    return powershell


def test_invoke_vibe_captured_process_preserves_multiline_prompt_as_single_argument(
    tmp_path: Path,
) -> None:
    powershell = _require_powershell()
    captured_args_path = tmp_path / "captured-args.json"
    script_path = tmp_path / "capture_args.py"
    stdout_path = tmp_path / "stdout.txt"
    stderr_path = tmp_path / "stderr.txt"
    prompt = "line1\nline two with spaces\nconsultation_role: discussion_consultant"
    script_path.write_text(
        "import json, pathlib, sys\n"
        "pathlib.Path(sys.argv[1]).write_text("
        "json.dumps(sys.argv[2:], ensure_ascii=False), encoding='utf-8')\n",
        encoding="utf-8",
    )

    command = f"""
. '{(REPO_ROOT / "scripts" / "runtime" / "VibeExecution.Common.ps1").as_posix()}'
$prompt = @'
{prompt}
'@
Invoke-VibeCapturedProcess `
    -Command '{shutil.which("python3") or sys.executable}' `
    -Arguments @(
        '{script_path.as_posix()}',
        '{captured_args_path.as_posix()}',
        '--flag',
        'value with spaces',
        $prompt
    ) `
    -WorkingDirectory '{REPO_ROOT.as_posix()}' `
    -TimeoutSeconds 10 `
    -StdOutPath '{stdout_path.as_posix()}' `
    -StdErrPath '{stderr_path.as_posix()}' | Out-Null
"""

    subprocess.run(
        [powershell, "-NoLogo", "-NoProfile", "-Command", command],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    captured_args = json.loads(captured_args_path.read_text(encoding="utf-8"))
    assert captured_args == ["--flag", "value with spaces", prompt]
