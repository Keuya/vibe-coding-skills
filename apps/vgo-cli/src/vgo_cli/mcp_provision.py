from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .repo import load_json


RECEIPT_RELPATH = Path(".vibeskills") / "mcp-auto-provision.json"


@dataclass(frozen=True)
class ProvisionResult:
    status: str
    failure_reason: str | None = None
    next_step: str = "none"


class ProvisionExecutor:
    def attempt(
        self,
        *,
        strategy: str,
        server_name: str,
        contract: dict[str, Any],
        repo_root: Path,
        target_root: Path,
        host_id: str,
        allow_scripted_install: bool,
    ) -> ProvisionResult:
        if strategy == "host_native":
            return ProvisionResult(
                status="host_native_unavailable",
                next_step=f"Complete host-native registration for {server_name} in {host_id}.",
            )
        if not allow_scripted_install:
            return ProvisionResult(
                status="not_attempted_due_to_host_contract",
                next_step=f"Enable scripted install support before attempting {server_name}.",
            )
        return ProvisionResult(
            status="verification_failed",
            next_step=f"Verify the scripted CLI for {server_name} is available in PATH.",
        )


class FakeExecutor(ProvisionExecutor):
    def __init__(self, *, results: dict[tuple[str, str], ProvisionResult]) -> None:
        self.results = dict(results)

    def attempt(
        self,
        *,
        strategy: str,
        server_name: str,
        contract: dict[str, Any],
        repo_root: Path,
        target_root: Path,
        host_id: str,
        allow_scripted_install: bool,
    ) -> ProvisionResult:
        return self.results.get(
            (strategy, server_name),
            super().attempt(
                strategy=strategy,
                server_name=server_name,
                contract=contract,
                repo_root=repo_root,
                target_root=target_root,
                host_id=host_id,
                allow_scripted_install=allow_scripted_install,
            ),
        )


def load_registry(repo_root: Path) -> dict[str, Any]:
    return load_json(repo_root / "config" / "mcp-auto-provision.registry.json")


def build_receipt(
    *,
    host_id: str,
    profile: str,
    target_root: Path,
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "install_state": "installed_locally",
        "host_id": host_id,
        "profile": profile,
        "target_root": str(target_root),
        "mcp_auto_provision_attempted": True,
        "mcp_results": results,
    }


def write_receipt(target_root: Path, receipt: dict[str, Any]) -> Path:
    receipt_path = target_root / RECEIPT_RELPATH
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt_path


def attempt_server(
    *,
    repo_root: Path,
    target_root: Path,
    host_id: str,
    server_name: str,
    contract: dict[str, Any],
    allow_scripted_install: bool,
    executor: ProvisionExecutor,
) -> dict[str, Any]:
    strategy = str(contract["strategy"])
    result = executor.attempt(
        strategy=strategy,
        server_name=server_name,
        contract=contract,
        repo_root=repo_root,
        target_root=target_root,
        host_id=host_id,
        allow_scripted_install=allow_scripted_install,
    )
    return {
        "name": server_name,
        "category": str(contract["category"]),
        "attempt_required": True,
        "attempted": True,
        "provision_path": strategy,
        "verify_path": str(contract["verify_path"]),
        "status": result.status,
        "failure_reason": result.failure_reason,
        "next_step": result.next_step,
        "disclosure_mode": "final_report_only",
    }


def provision_required_mcp(
    *,
    repo_root: Path,
    target_root: Path,
    host_id: str,
    profile: str,
    allow_scripted_install: bool,
    executor: ProvisionExecutor | None = None,
) -> dict[str, Any]:
    registry = load_registry(repo_root)
    host_contract = dict((registry["hosts"] or {})[host_id])
    active_executor = executor or ProvisionExecutor()
    results = [
        attempt_server(
            repo_root=repo_root,
            target_root=target_root,
            host_id=host_id,
            server_name=server_name,
            contract=dict((host_contract["servers"] or {})[server_name]),
            allow_scripted_install=allow_scripted_install,
            executor=active_executor,
        )
        for server_name in list(host_contract["attempt_order"] or [])
    ]
    receipt = build_receipt(host_id=host_id, profile=profile, target_root=target_root, results=results)
    write_receipt(target_root, receipt)
    return receipt


def lookup_server(receipt: dict[str, Any], server_name: str) -> dict[str, Any]:
    for entry in receipt.get("mcp_results") or []:
        if str(entry.get("name")) == server_name:
            return dict(entry)
    raise KeyError(server_name)


def manual_follow_up_servers(receipt: dict[str, Any]) -> list[str]:
    follow_up: list[str] = []
    for entry in receipt.get("mcp_results") or []:
        if str(entry.get("status") or "") != "ready":
            follow_up.append(str(entry.get("name") or "unknown"))
    return follow_up
