from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_SRC = REPO_ROOT / 'apps' / 'vgo-cli' / 'src'
if str(CLI_SRC) not in sys.path:
    sys.path.insert(0, str(CLI_SRC))

from vgo_cli.version_reminder import build_update_reminder


def test_build_update_reminder_refreshes_stale_cache_and_emits_advisory(monkeypatch) -> None:
    calls: list[str] = []

    monkeypatch.setattr(
        'vgo_cli.version_reminder.refresh_installed_status',
        lambda repo_root, target_root, host_id: {
            'installed_version': '3.0.0',
            'installed_commit': 'old',
            'repo_default_branch': 'main',
        },
    )
    monkeypatch.setattr('vgo_cli.version_reminder.is_upstream_cache_stale', lambda status: True)

    def fake_refresh(repo_root, target_root, current_status):
        calls.append('refresh')
        return {
            **current_status,
            'remote_latest_version': '3.0.1',
            'remote_latest_commit': 'new',
            'update_available': True,
        }

    monkeypatch.setattr('vgo_cli.version_reminder.refresh_upstream_status', fake_refresh)

    message = build_update_reminder(REPO_ROOT, REPO_ROOT / '.tmp-target', 'codex')

    assert calls == ['refresh']
    assert 'update available' in message.lower()
    assert 'local=3.0.0@old' in message
    assert 'latest=3.0.1@new' in message


def test_build_update_reminder_uses_fresh_cache_without_refresh(monkeypatch) -> None:
    monkeypatch.setattr(
        'vgo_cli.version_reminder.refresh_installed_status',
        lambda repo_root, target_root, host_id: {
            'installed_version': '3.0.0',
            'installed_commit': 'old',
            'remote_latest_version': '3.0.1',
            'remote_latest_commit': 'new',
            'remote_latest_checked_at': '2026-04-09T00:00:00Z',
            'update_available': True,
        },
    )
    monkeypatch.setattr('vgo_cli.version_reminder.is_upstream_cache_stale', lambda status: False)
    monkeypatch.setattr(
        'vgo_cli.version_reminder.refresh_upstream_status',
        lambda repo_root, target_root, current_status: (_ for _ in ()).throw(AssertionError('should not refresh')),
    )

    message = build_update_reminder(REPO_ROOT, REPO_ROOT / '.tmp-target', 'codex')

    assert 'latest=3.0.1@new' in message


def test_build_update_reminder_returns_none_when_no_update_is_available(monkeypatch) -> None:
    monkeypatch.setattr(
        'vgo_cli.version_reminder.refresh_installed_status',
        lambda repo_root, target_root, host_id: {
            'installed_version': '3.0.1',
            'installed_commit': 'same',
            'remote_latest_version': '3.0.1',
            'remote_latest_commit': 'same',
            'update_available': False,
        },
    )
    monkeypatch.setattr('vgo_cli.version_reminder.is_upstream_cache_stale', lambda status: False)

    assert build_update_reminder(REPO_ROOT, REPO_ROOT / '.tmp-target', 'codex') is None


def test_build_update_reminder_swallows_refresh_failures(monkeypatch) -> None:
    monkeypatch.setattr(
        'vgo_cli.version_reminder.refresh_installed_status',
        lambda repo_root, target_root, host_id: {
            'installed_version': '3.0.0',
            'installed_commit': 'old',
            'repo_default_branch': 'main',
        },
    )
    monkeypatch.setattr('vgo_cli.version_reminder.is_upstream_cache_stale', lambda status: True)
    monkeypatch.setattr(
        'vgo_cli.version_reminder.refresh_upstream_status',
        lambda repo_root, target_root, current_status: (_ for _ in ()).throw(RuntimeError('network down')),
    )

    assert build_update_reminder(REPO_ROOT, REPO_ROOT / '.tmp-target', 'codex') is None
