from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSEMBLER_PATH = ROOT / 'tools' / 'build' / 'assemble_distribution.py'
BUNDLE_PATH = ROOT / 'tools' / 'release' / 'build_release_bundle.py'


def _load_module(module_name: str, module_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'unable to load module from {module_path}')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_distribution_build_creates_generated_outputs(tmp_path) -> None:
    assembler = _load_module('distribution_assembler', ASSEMBLER_PATH)
    bundle_builder = _load_module('release_bundle_builder', BUNDLE_PATH)

    dist_out = tmp_path / 'dist-out'
    manifest_path = dist_out / 'manifest.json'
    bundle_path = tmp_path / 'bundle-out' / 'release-bundle.json'

    assert not manifest_path.exists()
    manifest = assembler.assemble_distribution(dist_out, host_id='codex', profile='minimal')
    assert manifest_path.exists()
    payload = json.loads(manifest_path.read_text(encoding='utf-8'))
    assert payload['generated'] is True
    assert payload['inputs']['runtime_core_manifest'].endswith('config/runtime-core-packaging.minimal.json')
    assert payload['inputs']['skill_catalog_owner'] == 'skill-catalog'
    assert (dist_out / 'catalog' / 'profiles' / 'index.json').exists()

    bundle = bundle_builder.build_release_bundle(manifest_path, tmp_path / 'bundle-out')
    assert bundle_path.exists()
    bundle_payload = json.loads(bundle_path.read_text(encoding='utf-8'))
    assert bundle_payload['generated'] is True
    assert bundle_payload['distribution_manifest'] == str(manifest_path.resolve())
    assert bundle['host_id'] == manifest['host_id']
