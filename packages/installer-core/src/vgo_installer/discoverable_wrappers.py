from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from vgo_contracts.discoverable_entry_surface import DiscoverableEntry, DiscoverableEntrySurface


@dataclass(frozen=True, slots=True)
class WrapperDescriptor:
    entry_id: str
    relpath: Path
    content: str


def _frontmatter_lines(host_id: str, entry: DiscoverableEntry) -> list[str]:
    lines = [
        "---",
        f"description: Launch {entry.display_name} through the canonical governed Vibe runtime.",
    ]
    if host_id == "opencode":
        lines.append("agent: vibe-plan")
    lines.append("---")
    return lines


def _body_lines(entry: DiscoverableEntry) -> list[str]:
    grade_line = "yes" if entry.allow_grade_flags else "no"
    return [
        "Use the `vibe` skill and follow its governed runtime contract for this request.",
        "",
        f"Wrapper entry: {entry.display_name} (`{entry.id}`)",
        f"Default stop target: `{entry.requested_stage_stop}`",
        f"Public grade flags allowed: {grade_line}",
        "",
        "Request:",
        "$ARGUMENTS",
    ]


def build_wrapper_descriptors(host_id: str, surface: DiscoverableEntrySurface) -> dict[str, WrapperDescriptor]:
    descriptors: dict[str, WrapperDescriptor] = {}
    for entry in surface.entries:
        content = "\n".join([*_frontmatter_lines(host_id, entry), "", *_body_lines(entry), ""]) + "\n"
        descriptors[entry.id] = WrapperDescriptor(
            entry_id=entry.id,
            relpath=Path("commands") / f"{entry.id}.md",
            content=content,
        )
    return descriptors


def _host_command_surface_relpaths(host_id: str) -> tuple[Path, ...]:
    normalized = (host_id or "").strip().lower()
    if normalized == "opencode":
        return (Path("commands"), Path("command"))
    if normalized in {"claude-code", "cursor", "windsurf", "openclaw"}:
        return ()
    return (Path("commands"),)


def materialize_host_visible_wrappers(
    *,
    target_root: Path,
    host_id: str,
    surface: DiscoverableEntrySurface,
) -> list[Path]:
    descriptors = build_wrapper_descriptors(host_id, surface)
    written: list[Path] = []
    for rel_root in _host_command_surface_relpaths(host_id):
        root = target_root / rel_root
        root.mkdir(parents=True, exist_ok=True)
        for descriptor in descriptors.values():
            destination = root / descriptor.relpath.name
            destination.write_text(descriptor.content, encoding="utf-8")
            written.append(destination)
    return written
