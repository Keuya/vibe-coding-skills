from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_SRC = ROOT / 'packages' / 'contracts' / 'src'
INSTALLER_SRC = ROOT / 'packages' / 'installer-core' / 'src'
for src in (CONTRACTS_SRC, INSTALLER_SRC):
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))

from vgo_contracts.discoverable_entry_surface import load_discoverable_entry_surface
from vgo_installer.discoverable_wrappers import build_wrapper_descriptors


def test_build_wrapper_descriptors_renders_all_discoverable_entries_for_codex() -> None:
    surface = load_discoverable_entry_surface(ROOT)

    rendered = build_wrapper_descriptors(
        host_id='codex',
        surface=surface,
    )

    assert sorted(rendered) == ['vibe', 'vibe-do', 'vibe-how', 'vibe-want']
    assert rendered['vibe-how'].relpath.as_posix() == 'commands/vibe-how.md'
    assert 'Vibe: How Do We Do It?' in rendered['vibe-how'].content
    assert 'Use the `vibe` skill' in rendered['vibe-how'].content
