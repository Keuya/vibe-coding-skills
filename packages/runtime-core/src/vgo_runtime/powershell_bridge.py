from __future__ import annotations

import json
import locale
import os
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence


def _preferred_bridge_encodings() -> tuple[str, ...]:
    preferred = str(locale.getpreferredencoding(False) or "").strip()
    candidates = [
        "utf-8-sig",
        "utf-8",
        "utf-16",
        "utf-16-le",
        "utf-16-be",
        preferred,
    ]
    ordered: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        normalized = candidate.strip()
        if not normalized:
            continue
        dedupe_key = normalized.casefold()
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        ordered.append(normalized)
    return tuple(ordered)


def _preview_stream(value: bytes | str | None) -> str | None:
    if value in (None, b"", ""):
        return None
    if isinstance(value, bytes):
        if value.startswith(b"\xff\xfe"):
            text = value.decode("utf-16", errors="replace")
        elif value.startswith(b"\xfe\xff"):
            text = value.decode("utf-16-be", errors="replace")
        else:
            preview_encodings = ["utf-8-sig", str(locale.getpreferredencoding(False) or "").strip()]
            text: str | None = None
            for encoding in preview_encodings:
                normalized = encoding.strip()
                if not normalized:
                    continue
                try:
                    candidate = value.decode(normalized)
                except (LookupError, UnicodeDecodeError):
                    continue
                if "\ufffd" in candidate or "\x00" in candidate:
                    continue
                text = candidate
                break
            if text is None:
                for encoding in preview_encodings:
                    normalized = encoding.strip()
                    if not normalized:
                        continue
                    try:
                        candidate = value.decode(normalized, errors="replace")
                    except LookupError:
                        continue
                    if "\ufffd" in candidate or "\x00" in candidate:
                        continue
                    text = candidate
                    break
            if text is None:
                text = value.decode("latin-1", errors="replace")
        text = text.replace("\x00", "")
    else:
        text = value
    flattened = " ".join(text.split())
    if not flattened:
        return None
    if len(flattened) > 160:
        return flattened[:157] + "..."
    return flattened


def _resolve_bridge_timeout(timeout: float | None) -> float | None:
    if timeout is not None:
        return timeout
    raw = str(os.environ.get("VGO_POWERSHELL_BRIDGE_TIMEOUT_SECONDS") or "").strip()
    if not raw:
        return 300.0
    try:
        resolved = float(raw)
    except ValueError:
        return 300.0
    if resolved <= 0:
        return None
    return resolved


def _command_preview(command: Sequence[str]) -> str:
    preview = " ".join(str(part) for part in command[:8]).strip()
    if len(command) > 8:
        preview += " ..."
    return preview


def _decode_json_object_stdout(
    stdout: bytes | str | None,
    *,
    bridge_label: str,
    stderr: bytes | str | None = None,
) -> dict[str, Any]:
    stderr_preview = _preview_stream(stderr)
    if stdout is None:
        detail = f"; stderr={stderr_preview}" if stderr_preview else ""
        raise RuntimeError(f"{bridge_label} returned no stdout{detail}")

    if isinstance(stdout, str):
        payload_text = stdout.strip()
        if not payload_text:
            detail = f"; stderr={stderr_preview}" if stderr_preview else ""
            raise RuntimeError(f"{bridge_label} returned empty stdout{detail}")
        try:
            payload = json.loads(payload_text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"{bridge_label} returned invalid JSON stdout") from exc
        if not isinstance(payload, dict):
            raise RuntimeError(f"{bridge_label} returned non-object payload")
        return payload

    if not stdout.strip():
        detail = f"; stderr={stderr_preview}" if stderr_preview else ""
        raise RuntimeError(f"{bridge_label} returned empty stdout{detail}")

    decode_failures: list[str] = []
    last_json_error: tuple[str, json.JSONDecodeError] | None = None
    for encoding in _preferred_bridge_encodings():
        try:
            payload_text = stdout.decode(encoding)
        except UnicodeDecodeError:
            decode_failures.append(encoding)
            continue
        if not payload_text.strip():
            continue
        try:
            payload = json.loads(payload_text)
        except json.JSONDecodeError as exc:
            last_json_error = (encoding, exc)
            continue
        if not isinstance(payload, dict):
            raise RuntimeError(f"{bridge_label} returned non-object payload")
        return payload

    detail_parts: list[str] = []
    if decode_failures:
        detail_parts.append("decode failed for " + ", ".join(decode_failures))
    stdout_preview = _preview_stream(stdout)
    if stdout_preview:
        detail_parts.append(f"stdout={stdout_preview}")
    if last_json_error is not None:
        detail_parts.append(f"decoded-as-{last_json_error[0]}")
    if stderr_preview:
        detail_parts.append(f"stderr={stderr_preview}")
    detail = f" ({'; '.join(detail_parts)})" if detail_parts else ""
    if last_json_error is not None:
        raise RuntimeError(f"{bridge_label} returned invalid JSON stdout{detail}") from last_json_error[1]
    raise RuntimeError(f"{bridge_label} returned undecodable JSON stdout{detail}")


def run_powershell_json_command(
    command: Sequence[str],
    *,
    cwd: Path,
    bridge_label: str,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
) -> dict[str, Any]:
    resolved_timeout = _resolve_bridge_timeout(timeout)
    try:
        completed = subprocess.run(
            list(command),
            cwd=cwd,
            capture_output=True,
            check=False,
            env=dict(env) if env is not None else None,
            timeout=resolved_timeout,
        )
    except subprocess.TimeoutExpired as exc:
        detail_parts = [f"timeout={resolved_timeout}s", f"cwd={cwd}", f"command={_command_preview(command)}"]
        stdout_preview = _preview_stream(exc.stdout)
        stderr_preview = _preview_stream(exc.stderr)
        if stdout_preview:
            detail_parts.append(f"stdout={stdout_preview}")
        if stderr_preview:
            detail_parts.append(f"stderr={stderr_preview}")
        raise RuntimeError(f"{bridge_label} timed out ({'; '.join(detail_parts)})") from exc
    if completed.returncode != 0:
        detail_parts = [f"exit={completed.returncode}", f"cwd={cwd}", f"command={_command_preview(command)}"]
        stdout_preview = _preview_stream(completed.stdout)
        stderr_preview = _preview_stream(completed.stderr)
        if stdout_preview:
            detail_parts.append(f"stdout={stdout_preview}")
        if stderr_preview:
            detail_parts.append(f"stderr={stderr_preview}")
        raise RuntimeError(f"{bridge_label} failed ({'; '.join(detail_parts)})")
    return _decode_json_object_stdout(
        completed.stdout,
        bridge_label=bridge_label,
        stderr=completed.stderr,
    )
