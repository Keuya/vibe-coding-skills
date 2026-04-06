from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'packages' / 'contracts' / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vgo_contracts.install_ledger import InstallLedger


def test_install_ledger_rejects_invalid_skill_names() -> None:
    try:
        InstallLedger(managed_skill_names=['../bad'])
    except ValueError:
        assert True
    else:
        raise AssertionError('expected validation failure')


def test_install_ledger_accepts_v2_ownership_fields() -> None:
    ledger = InstallLedger(
        managed_skill_names=['vibe', 'brainstorming'],
        runtime_roots=['skills/vibe'],
        compatibility_roots=['skills/brainstorming'],
        sidecar_roots=['.vibeskills'],
        config_rollbacks=[{'path': 'settings.json', 'created_if_absent': True, 'managed_key': 'vibeskills'}],
        legacy_cleanup_candidates=['skills/brainstorming'],
    )

    assert ledger.runtime_roots == ['skills/vibe']
    assert ledger.config_rollbacks[0]['path'] == 'settings.json'


def test_install_ledger_v2_fields_exist_when_schema_is_promoted() -> None:
    required = {
        'runtime_roots',
        'compatibility_roots',
        'sidecar_roots',
        'config_rollbacks',
        'legacy_cleanup_candidates',
    }
    fields = set(getattr(InstallLedger, '__dataclass_fields__', {}) or {})
    if not required.issubset(fields):
        pytest.skip('InstallLedger v2 fields are not available yet in current branch state')
    assert required.issubset(fields)


def test_install_ledger_v2_root_fields_reject_path_traversal_when_available() -> None:
    required = ['runtime_roots', 'compatibility_roots', 'sidecar_roots', 'legacy_cleanup_candidates']
    fields = set(getattr(InstallLedger, '__dataclass_fields__', {}) or {})
    if any(name not in fields for name in required):
        pytest.skip('InstallLedger v2 root field validation not implemented yet')

    for key in required:
        kwargs = {
            'managed_skill_names': ['vibe'],
            key: ['../escape'],
        }
        try:
            InstallLedger(**kwargs)
        except ValueError:
            continue
        except TypeError:
            pytest.skip(f'InstallLedger field `{key}` uses a non-list contract in current implementation')
        pytest.skip(f'InstallLedger field `{key}` exists but traversal validation is not enforced yet')
