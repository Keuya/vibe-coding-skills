from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

from .errors import CliError
from .repo import load_json


def report_external_fallback_usage(external_fallback_used: list[str], *, strict_offline: bool) -> None:
    uniq_fallback = ','.join(sorted(set(str(item) for item in external_fallback_used if str(item).strip())))
    if not uniq_fallback:
        return
    if strict_offline:
        raise CliError(f'StrictOffline rejected external fallback usage: {uniq_fallback}')
    print(f'[WARN] External fallback skills were used (non-reproducible install): {uniq_fallback}')


def _run_optional_install(command: list[str]) -> None:
    subprocess.run(command, capture_output=True, text=True)


def maybe_install_external_dependencies(repo_root: Path, install_mode: str) -> None:
    if shutil.which('npm'):
        _run_optional_install(['npm', 'install', '-g', 'claude-flow'])
        if install_mode == 'governed':
            _run_optional_install(['npm', 'install', '-g', '@th0rgal/ralph-wiggum'])
    if not shutil.which('scrapling'):
        _run_optional_install([sys.executable, '-m', 'pip', 'install', 'scrapling[ai]'])
    if shutil.which('xan') is None:
        print('[WARN] xan CLI not detected. Install manually (brew/pixi/conda/cargo) to enable large CSV acceleration.')
    ivy_probe = subprocess.run([sys.executable, '-c', 'import ivy'], capture_output=True, text=True)
    if ivy_probe.returncode != 0:
        print('[WARN] ivy Python package not detected. Install manually (pip install ivy) to enable framework-interop analyzer hints.')
    if shutil.which('fuck-u-code') is None:
        print('[WARN] fuck-u-code CLI not detected. Install manually if you want external quality-debt analyzer hints (quality-debt-overlay still works without it).')
