from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_SRC = REPO_ROOT / 'apps' / 'vgo-cli' / 'src'
if str(CLI_SRC) not in sys.path:
    sys.path.insert(0, str(CLI_SRC))

from vgo_cli import external as cli_external


def test_run_optional_install_uses_bounded_timeout_and_does_not_raise(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    recorded: dict[str, object] = {}

    def fake_run(command: list[str], *, capture_output: bool, text: bool, timeout: int) -> subprocess.CompletedProcess[str]:
        recorded['command'] = command
        recorded['capture_output'] = capture_output
        recorded['text'] = text
        recorded['timeout'] = timeout
        raise subprocess.TimeoutExpired(command, timeout)

    monkeypatch.setattr(cli_external.subprocess, 'run', fake_run)

    cli_external._run_optional_install(['npm', 'install', '-g', 'claude-flow'])

    assert recorded == {
        'command': ['npm', 'install', '-g', 'claude-flow'],
        'capture_output': True,
        'text': True,
        'timeout': cli_external.OPTIONAL_INSTALL_TIMEOUT_SECONDS,
    }
    assert 'timed out' in capsys.readouterr().out
