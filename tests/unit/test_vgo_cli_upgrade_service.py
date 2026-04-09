from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_SRC = REPO_ROOT / 'apps' / 'vgo-cli' / 'src'
if str(CLI_SRC) not in sys.path:
    sys.path.insert(0, str(CLI_SRC))

from vgo_cli.errors import CliError
from vgo_cli.upgrade_service import reset_repo_to_official_head, upgrade_runtime


def test_upgrade_runtime_noops_when_install_is_already_current(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo_root = tmp_path / 'repo'
    target_root = tmp_path / 'target'

    monkeypatch.setattr(
        'vgo_cli.upgrade_service.refresh_installed_status',
        lambda repo_root, target_root, host_id: {
            'installed_version': '3.0.1',
            'installed_commit': 'same',
            'remote_latest_version': '3.0.1',
            'remote_latest_commit': 'same',
            'update_available': False,
        },
    )
    monkeypatch.setattr('vgo_cli.upgrade_service.refresh_upstream_status', lambda repo_root, target_root, current_status: current_status)
    monkeypatch.setattr('vgo_cli.upgrade_service.reset_repo_to_official_head', lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError('should not reset repo')))
    monkeypatch.setattr('vgo_cli.upgrade_service.reinstall_runtime', lambda **kwargs: (_ for _ in ()).throw(AssertionError('should not reinstall')))
    monkeypatch.setattr('vgo_cli.upgrade_service.run_upgrade_check', lambda **kwargs: (_ for _ in ()).throw(AssertionError('should not run check')))

    result = upgrade_runtime(
        repo_root=repo_root,
        target_root=target_root,
        host_id='codex',
        profile='full',
        frontend='shell',
        install_external=False,
        strict_offline=False,
        require_closed_ready=False,
        allow_external_skill_fallback=False,
        skip_runtime_freshness_gate=False,
    )

    assert result['changed'] is False
    assert 'already current' in capsys.readouterr().out.lower()


def test_upgrade_runtime_refreshes_repo_reinstalls_and_checks_when_update_is_available(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    repo_root = tmp_path / 'repo'
    target_root = tmp_path / 'target'
    steps: list[str] = []
    statuses = iter(
        [
            {
                'installed_version': '3.0.0',
                'installed_commit': 'old',
                'repo_default_branch': 'main',
            },
            {
                'installed_version': '3.0.1',
                'installed_commit': 'new',
                'remote_latest_version': '3.0.1',
                'remote_latest_commit': 'new',
                'update_available': False,
            },
        ]
    )

    monkeypatch.setattr('vgo_cli.upgrade_service.refresh_installed_status', lambda repo_root, target_root, host_id: next(statuses))

    def fake_refresh_upstream(repo_root: Path, target_root: Path, current_status: dict[str, object]) -> dict[str, object]:
        steps.append('refresh')
        merged = dict(current_status)
        merged.update(
            {
                'remote_latest_version': '3.0.1',
                'remote_latest_commit': 'new',
                'update_available': True,
                'repo_default_branch': 'main',
            }
        )
        return merged

    monkeypatch.setattr('vgo_cli.upgrade_service.refresh_upstream_status', fake_refresh_upstream)
    monkeypatch.setattr('vgo_cli.upgrade_service.reset_repo_to_official_head', lambda repo_root, branch: steps.append(f'reset:{branch}'))
    monkeypatch.setattr('vgo_cli.upgrade_service.reinstall_runtime', lambda **kwargs: steps.append('reinstall'))
    monkeypatch.setattr(
        'vgo_cli.upgrade_service.run_upgrade_check',
        lambda **kwargs: (steps.append('check') or subprocess.CompletedProcess(args=['check'], returncode=0, stdout='', stderr='')),
    )

    result = upgrade_runtime(
        repo_root=repo_root,
        target_root=target_root,
        host_id='codex',
        profile='full',
        frontend='shell',
        install_external=False,
        strict_offline=False,
        require_closed_ready=False,
        allow_external_skill_fallback=False,
        skip_runtime_freshness_gate=False,
    )

    assert steps == ['refresh', 'reset:main', 'reinstall', 'check']
    assert result['changed'] is True
    assert result['before']['installed_version'] == '3.0.0'
    assert result['after']['installed_version'] == '3.0.1'


def test_upgrade_runtime_propagates_refresh_failures(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    repo_root = tmp_path / 'repo'
    target_root = tmp_path / 'target'

    monkeypatch.setattr(
        'vgo_cli.upgrade_service.refresh_installed_status',
        lambda repo_root, target_root, host_id: {'installed_version': '3.0.0', 'installed_commit': 'old'},
    )
    monkeypatch.setattr(
        'vgo_cli.upgrade_service.refresh_upstream_status',
        lambda repo_root, target_root, current_status: (_ for _ in ()).throw(CliError('refresh failed')),
    )

    with pytest.raises(CliError, match='refresh failed'):
        upgrade_runtime(
            repo_root=repo_root,
            target_root=target_root,
            host_id='codex',
            profile='full',
            frontend='shell',
            install_external=False,
            strict_offline=False,
            require_closed_ready=False,
            allow_external_skill_fallback=False,
            skip_runtime_freshness_gate=False,
        )


def test_upgrade_runtime_propagates_check_failures(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    repo_root = tmp_path / 'repo'
    target_root = tmp_path / 'target'
    statuses = iter(
        [
            {'installed_version': '3.0.0', 'installed_commit': 'old', 'repo_default_branch': 'main'},
            {'installed_version': '3.0.1', 'installed_commit': 'new'},
        ]
    )

    monkeypatch.setattr('vgo_cli.upgrade_service.refresh_installed_status', lambda repo_root, target_root, host_id: next(statuses))
    monkeypatch.setattr(
        'vgo_cli.upgrade_service.refresh_upstream_status',
        lambda repo_root, target_root, current_status: {
            **current_status,
            'remote_latest_version': '3.0.1',
            'remote_latest_commit': 'new',
            'update_available': True,
            'repo_default_branch': 'main',
        },
    )
    monkeypatch.setattr('vgo_cli.upgrade_service.reset_repo_to_official_head', lambda repo_root, branch: None)
    monkeypatch.setattr('vgo_cli.upgrade_service.reinstall_runtime', lambda **kwargs: None)
    monkeypatch.setattr(
        'vgo_cli.upgrade_service.run_upgrade_check',
        lambda **kwargs: (_ for _ in ()).throw(CliError('check failed')),
    )

    with pytest.raises(CliError, match='check failed'):
        upgrade_runtime(
            repo_root=repo_root,
            target_root=target_root,
            host_id='codex',
            profile='full',
            frontend='shell',
            install_external=False,
            strict_offline=False,
            require_closed_ready=False,
            allow_external_skill_fallback=False,
            skip_runtime_freshness_gate=False,
        )


def test_reset_repo_to_official_head_discards_local_changes_before_switch(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    repo_root = tmp_path / 'repo'
    repo_root.mkdir(parents=True)
    commands: list[list[str]] = []

    def fake_run_subprocess(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        assert cwd == repo_root
        return subprocess.CompletedProcess(command, 0, stdout='', stderr='')

    monkeypatch.setattr('vgo_cli.upgrade_service.run_subprocess', fake_run_subprocess)

    reset_repo_to_official_head(repo_root, 'main')

    assert commands == [
        ['git', 'reset', '--hard', 'HEAD'],
        ['git', 'clean', '-fd'],
        ['git', 'checkout', '-B', 'main', 'FETCH_HEAD'],
        ['git', 'reset', '--hard', 'FETCH_HEAD'],
    ]
