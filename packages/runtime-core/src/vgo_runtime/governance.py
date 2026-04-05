from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeGovernanceProfile:
    mode: str
    governance_scope: str = 'root_governed'
    freeze_before_requirement_doc: bool = True


def normalize_runtime_mode(mode: str | None) -> str:
    normalized = str(mode or 'interactive_governed').strip() or 'interactive_governed'
    if normalized != 'interactive_governed':
        raise ValueError(f'unsupported runtime mode: {mode}')
    return 'interactive_governed'


def choose_internal_grade(task_type: str) -> str:
    normalized = str(task_type).strip().lower()
    if normalized in {'coding', 'debug', 'review', 'research'}:
        return 'L'
    return 'M'


def build_governance_profile(mode: str | None, *, governance_scope: str = 'root_governed') -> RuntimeGovernanceProfile:
    return RuntimeGovernanceProfile(
        mode=normalize_runtime_mode(mode),
        governance_scope=governance_scope or 'root_governed',
    )
