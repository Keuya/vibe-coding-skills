from __future__ import annotations

import os
from pathlib import Path

from .mcp_provision import provision_required_mcp
from .external import report_external_fallback_usage
from .install_gates import run_offline_gate, run_runtime_freshness_gate
from .installer_bridge import refresh_install_ledger_payload
from .output import print_json_payload, print_install_completion_report
from .skill_surface import quarantine_codex_duplicate_skill_surface


def reconcile_install_postconditions(
    repo_root: Path,
    target_root: Path,
    host_id: str,
    *,
    profile: str,
    install_external: bool,
    frontend: str,
    external_fallback_used: list[str],
    strict_offline: bool,
    skip_runtime_freshness_gate: bool,
    include_frontmatter: bool,
) -> dict[str, object]:
    if strict_offline:
        run_offline_gate(repo_root, target_root)
    report_external_fallback_usage(external_fallback_used, strict_offline=strict_offline)
    quarantine_codex_duplicate_skill_surface(target_root, host_id)
    run_runtime_freshness_gate(
        repo_root,
        target_root,
        skip_gate=skip_runtime_freshness_gate,
        include_frontmatter=include_frontmatter,
    )
    install_receipt = refresh_install_ledger_payload(repo_root, target_root)
    mcp_receipt = provision_required_mcp(
        repo_root=repo_root,
        target_root=target_root,
        host_id=host_id,
        profile=profile,
        allow_scripted_install=install_external,
    )
    if os.environ.get('VGO_SUPPRESS_INSTALL_COMPLETION_REPORT', '').strip() != '1':
        print_install_completion_report(
            frontend,
            host_id=host_id,
            profile=profile,
            target_root=target_root,
            install_receipt=install_receipt,
            mcp_receipt=mcp_receipt,
        )
    return {
        'install_receipt': install_receipt,
        'mcp_receipt': mcp_receipt,
    }
