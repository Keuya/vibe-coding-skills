from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RepoContext:
    repo_root: Path
    config_root: Path
    bundled_skills_root: Path


def resolve_repo_root(start_path: Path) -> Path:
    current = start_path.resolve()
    if current.is_file():
        current = current.parent

    candidates: list[Path] = []
    while True:
        if (current / "config" / "version-governance.json").exists():
            candidates.append(current)
        if current.parent == current:
            break
        current = current.parent

    if not candidates:
        raise RuntimeError(f"Unable to resolve VCO repo root from: {start_path}")

    git_candidates = [candidate for candidate in candidates if (candidate / ".git").exists()]
    return git_candidates[-1] if git_candidates else candidates[-1]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def normalize_text(value: str | None) -> str:
    if value is None:
        return ""
    return str(value).strip().casefold()


def normalize_keyword_list(values: list[Any] | None) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for value in values or []:
        token = normalize_text(str(value))
        if not token or token in seen:
            continue
        normalized.append(token)
        seen.add(token)
    return normalized


def keyword_ratio(prompt_lower: str, keywords: list[Any] | None) -> float:
    rows = normalize_keyword_list(keywords)
    if not rows:
        return 0.0
    hits = sum(1 for keyword in rows if keyword in prompt_lower)
    denominator = min(3, len(rows))
    return round(min(1.0, hits / denominator), 4)


def candidate_name_score(prompt_lower: str, candidate: str) -> float:
    candidate_lower = normalize_text(candidate)
    if not candidate_lower:
        return 0.0
    if candidate_lower in prompt_lower:
        return 1.0

    pieces = [piece for piece in re.split(r"[-_/ ]+", candidate_lower) if piece]
    if not pieces:
        return 0.0
    hits = sum(1 for piece in pieces if piece in prompt_lower)
    return round(hits / len(pieces), 4)


def resolve_home_directory() -> Path:
    candidates = [
        os.environ.get("HOME"),
        os.environ.get("USERPROFILE"),
    ]
    home_drive = os.environ.get("HOMEDRIVE")
    home_path = os.environ.get("HOMEPATH")
    if home_drive and home_path:
        candidates.append(f"{home_drive}{home_path}")

    for candidate in candidates:
        if candidate:
            return Path(candidate).expanduser().resolve()
    return Path.home().resolve()


def resolve_target_root(target_root: str | None = None) -> Path:
    if target_root:
        return Path(target_root).expanduser().resolve()
    if os.environ.get("CODEX_HOME"):
        return Path(os.environ["CODEX_HOME"]).expanduser().resolve()
    return (resolve_home_directory() / ".codex").resolve()


def resolve_requested_canonical(requested_skill: str | None, alias_map: dict[str, Any]) -> str | None:
    if not requested_skill:
        return None
    requested = normalize_text(str(requested_skill).lstrip("$"))
    if not requested:
        return None

    aliases = alias_map.get("aliases") or {}
    for alias, canonical in aliases.items():
        if normalize_text(alias) == requested:
            return normalize_text(str(canonical))
    return requested


def get_pack_default_candidate(pack: dict[str, Any], task_type: str, filtered_candidates: list[str], all_candidates: list[str]) -> str | None:
    defaults = pack.get("defaults_by_task") or {}
    preferred = normalize_text(defaults.get(task_type))
    if preferred and preferred in filtered_candidates:
        return preferred
    if preferred and preferred in all_candidates:
        return preferred
    return filtered_candidates[0] if filtered_candidates else (all_candidates[0] if all_candidates else None)


def select_pack_candidate(
    prompt_lower: str,
    candidates: list[str],
    task_type: str,
    requested_canonical: str | None,
    skill_keyword_index: dict[str, Any],
    routing_rules: dict[str, Any],
    pack: dict[str, Any],
    candidate_selection_config: dict[str, Any],
) -> dict[str, Any]:
    if not candidates:
        return {
            "selected": None,
            "score": 0.0,
            "reason": "no_candidates",
            "ranking": [],
            "top1_top2_gap": 0.0,
            "filtered_out_by_task": [],
        }

    if requested_canonical and requested_canonical in candidates:
        return {
            "selected": requested_canonical,
            "score": 1.0,
            "reason": "requested_skill",
            "ranking": [
                {
                    "skill": requested_canonical,
                    "score": 1.0,
                    "keyword_score": 1.0,
                    "name_score": 1.0,
                    "positive_score": 1.0,
                    "negative_score": 0.0,
                    "canonical_for_task_hit": 1.0,
                }
            ],
            "top1_top2_gap": 1.0,
            "filtered_out_by_task": [],
        }

    selection_cfg = skill_keyword_index.get("selection") or {}
    selection_weights = selection_cfg.get("weights") or {}
    weight_keyword = float(selection_weights.get("keyword_match", 0.85))
    weight_name = float(selection_weights.get("name_match", 0.15))
    fallback_min = float(selection_cfg.get("fallback_to_first_when_score_below", 0.15))

    positive_bonus = float(candidate_selection_config.get("rule_positive_keyword_bonus", 0.2))
    negative_penalty = float(candidate_selection_config.get("rule_negative_keyword_penalty", 0.25))
    canonical_bonus = float(candidate_selection_config.get("canonical_for_task_bonus", 0.12))

    rules = (routing_rules.get("skills") or {}) if routing_rules else {}
    filtered_candidates: list[str] = []
    blocked_by_task: list[str] = []
    for candidate in candidates:
        rule = rules.get(candidate) or {}
        task_allow = [normalize_text(item) for item in (rule.get("task_allow") or [])]
        if not task_allow or task_type in task_allow:
            filtered_candidates.append(candidate)
        else:
            blocked_by_task.append(candidate)

    default_candidate = get_pack_default_candidate(pack, task_type, filtered_candidates, candidates)
    if not filtered_candidates:
        fallback = default_candidate or candidates[0]
        return {
            "selected": fallback,
            "score": 0.0,
            "reason": "fallback_task_default_after_task_filter" if default_candidate else "fallback_first_candidate_after_task_filter",
            "ranking": [],
            "top1_top2_gap": 0.0,
            "filtered_out_by_task": blocked_by_task,
        }

    scored: list[dict[str, Any]] = []
    keywords_by_skill = skill_keyword_index.get("skills") or {}
    for ordinal, candidate in enumerate(filtered_candidates):
        skill_entry = keywords_by_skill.get(candidate) or {}
        keyword_score = keyword_ratio(prompt_lower, skill_entry.get("keywords") or [])
        name_score = candidate_name_score(prompt_lower, candidate)

        rule = rules.get(candidate) or {}
        positive_score = keyword_ratio(prompt_lower, rule.get("positive_keywords") or [])
        negative_score = keyword_ratio(prompt_lower, rule.get("negative_keywords") or [])
        canonical_for_task = [normalize_text(item) for item in (rule.get("canonical_for_task") or [])]
        canonical_hit = 1.0 if task_type in canonical_for_task else 0.0

        score = (
            (weight_keyword * keyword_score)
            + (weight_name * name_score)
            + (positive_bonus * positive_score)
            - (negative_penalty * negative_score)
            + (canonical_bonus * canonical_hit)
        )
        score = round(max(0.0, min(1.0, score)), 4)
        scored.append(
            {
                "skill": candidate,
                "score": score,
                "keyword_score": round(keyword_score, 4),
                "name_score": round(name_score, 4),
                "positive_score": round(positive_score, 4),
                "negative_score": round(negative_score, 4),
                "canonical_for_task_hit": round(canonical_hit, 4),
                "ordinal": ordinal,
            }
        )

    ranked = sorted(scored, key=lambda row: (-row["score"], -row["keyword_score"], -row["positive_score"], row["ordinal"]))
    top = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None
    gap = round(max(0.0, float(top["score"]) - float(second["score"] if second else 0.0)), 4)

    if top["score"] < fallback_min:
        fallback = default_candidate or filtered_candidates[0]
        default_row = next((row for row in ranked if row["skill"] == fallback), top)
        return {
            "selected": fallback,
            "score": float(default_row["score"]),
            "reason": "fallback_task_default" if fallback == default_candidate else "fallback_first_candidate",
            "ranking": ranked[:6],
            "top1_top2_gap": gap,
            "filtered_out_by_task": blocked_by_task,
        }

    return {
        "selected": top["skill"],
        "score": float(top["score"]),
        "reason": "keyword_ranked",
        "ranking": ranked[:6],
        "top1_top2_gap": gap,
        "filtered_out_by_task": blocked_by_task,
    }


def resolve_skill_md_path(repo: RepoContext, skill: str, target_root: str | None) -> Path | None:
    bundled = repo.bundled_skills_root / skill / "SKILL.md"
    if bundled.exists():
        return bundled
    installed = resolve_target_root(target_root) / "skills" / skill / "SKILL.md"
    return installed if installed.exists() else None


def read_skill_descriptor(repo: RepoContext, skill: str, target_root: str | None) -> dict[str, Any]:
    path = resolve_skill_md_path(repo, skill, target_root)
    description = None
    if path and path.exists():
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        if lines and lines[0].strip() == "---":
            for line in lines[1:20]:
                if line.strip() == "---":
                    break
                if line.lower().startswith("description:"):
                    description = line.split(":", 1)[1].strip()
                    break
    return {
        "skill": skill,
        "description": description,
        "skill_md_path": str(path) if path else None,
    }


def build_confirm_ui(repo: RepoContext, route_result: dict[str, Any], target_root: str | None) -> dict[str, Any] | None:
    if route_result["route_mode"] != "confirm_required" or not route_result.get("selected"):
        return None

    selected = route_result["selected"]
    ranking = []
    for row in route_result.get("ranked", []):
        if row["pack_id"] == selected["pack_id"]:
            ranking = row.get("candidate_ranking", [])
            break
    if not ranking:
        ranking = [{"skill": selected["skill"], "score": selected["selection_score"]}]

    options = []
    for index, row in enumerate(ranking[:5], start=1):
        descriptor = read_skill_descriptor(repo, row["skill"], target_root)
        options.append(
            {
                "option_id": index,
                "skill": row["skill"],
                "pack_id": selected["pack_id"],
                "score": row.get("score"),
                "description": descriptor["description"],
                "skill_md_path": descriptor["skill_md_path"],
            }
        )

    rendered: list[str] = []
    if route_result.get("hazard_alert_required") and route_result.get("hazard_alert"):
        hazard = route_result["hazard_alert"]
        rendered.append(str(hazard.get("title") or "FALLBACK HAZARD ALERT"))
        rendered.append(str(hazard.get("message") or "This result came from a fallback or degraded path and is not equivalent to standard success."))
        if hazard.get("reason"):
            rendered.append(f"Trigger reason: `{hazard['reason']}`.")
        if hazard.get("recovery_action"):
            rendered.append(str(hazard["recovery_action"]))
        rendered.append("")
    rendered.append(f"Route confirmation required for pack `{selected['pack_id']}`.")
    for option in options:
        score = option["score"]
        score_text = f" (score={round(float(score), 4)})" if score is not None else ""
        if option["description"]:
            rendered.append(f"{option['option_id']}. `{option['skill']}`{score_text} - {option['description']}")
        else:
            rendered.append(f"{option['option_id']}. `{option['skill']}`{score_text}")
    rendered.append("Reply with the option number or `$<skill>` to choose explicitly.")

    return {
        "enabled": True,
        "pack_id": selected["pack_id"],
        "selected_skill": selected["skill"],
        "options": options,
        "rendered_text": "\n".join(rendered),
        "hazard_alert_required": bool(route_result.get("hazard_alert_required")),
        "truth_level": route_result.get("truth_level"),
        "degradation_state": route_result.get("degradation_state"),
        "hazard_alert": route_result.get("hazard_alert"),
    }


def build_fallback_truth(route_result: dict[str, Any], fallback_policy: dict[str, Any] | None) -> dict[str, Any]:
    policy = fallback_policy or {}
    truth_contract = policy.get("truth_contract", {}) if isinstance(policy, dict) else {}
    fallback_active = bool(
        route_result.get("route_mode") == "legacy_fallback"
        or route_result.get("route_reason") == "legacy_fallback_guard"
        or route_result.get("legacy_fallback_guard_applied")
    )
    degradation_state = (
        truth_contract.get("fallback_guarded_state", "fallback_guarded")
        if route_result.get("legacy_fallback_guard_applied")
        else truth_contract.get("fallback_degradation_state", "fallback_active")
        if fallback_active
        else "standard"
    )
    truth_level = (
        truth_contract.get("fallback_truth_level", "non_authoritative")
        if fallback_active
        else truth_contract.get("standard_truth_level", "authoritative")
    )
    hazard_alert_required = bool(policy.get("require_hazard_alert", True) and fallback_active)
    hazard_alert = None
    if hazard_alert_required:
        hazard_alert = {
            "title": policy.get("hazard_alert_title", "FALLBACK HAZARD ALERT"),
            "severity": policy.get("hazard_alert_severity", "critical"),
            "reason": route_result.get("legacy_fallback_original_reason") or route_result.get("route_reason"),
            "message": policy.get(
                "hazard_summary",
                "This result came from a fallback or degraded path and is not equivalent to standard success.",
            ),
            "recovery_action": policy.get(
                "hazard_recovery_action",
                "Repair the primary path or restore missing dependencies before claiming authoritative success.",
            ),
            "manual_review_required": bool(truth_contract.get("manual_review_required", True)),
        }
    return {
        "fallback_active": fallback_active,
        "hazard_alert_required": hazard_alert_required,
        "truth_level": truth_level,
        "degradation_state": degradation_state,
        "non_authoritative": truth_level != "authoritative",
        "hazard_alert": hazard_alert,
    }


def route_prompt(
    prompt: str,
    grade: str,
    task_type: str,
    requested_skill: str | None = None,
    target_root: str | None = None,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    grade = normalize_text(grade)
    task_type = normalize_text(task_type)
    repo_path = repo_root or resolve_repo_root(Path(__file__))
    repo = RepoContext(
        repo_root=repo_path,
        config_root=repo_path / "config",
        bundled_skills_root=repo_path / "bundled" / "skills",
    )

    prompt_lower = normalize_text(prompt)
    pack_manifest = load_json(repo.config_root / "pack-manifest.json")
    alias_map = load_json(repo.config_root / "skill-alias-map.json")
    thresholds_cfg = load_json(repo.config_root / "router-thresholds.json")
    skill_keyword_index = load_json(repo.config_root / "skill-keyword-index.json")
    fallback_policy = load_json(repo.config_root / "fallback-governance.json")
    routing_rules = load_json(repo.config_root / "skill-routing-rules.json")

    requested_canonical = resolve_requested_canonical(requested_skill, alias_map)
    threshold_values = thresholds_cfg.get("thresholds") or {}
    candidate_selection_cfg = thresholds_cfg.get("candidate_selection") or {}
    min_top_gap = float(threshold_values.get("min_top1_top2_gap", 0.08))
    min_candidate_signal_confirm = float(threshold_values.get("min_candidate_signal_for_confirm_override", 0.2))
    min_candidate_signal_auto = float(threshold_values.get("min_candidate_signal_for_auto_route", 0.6))
    auto_route_threshold = float(threshold_values.get("auto_route", 0.7))
    confirm_required_threshold = float(threshold_values.get("confirm_required", 0.45))
    fallback_threshold = float(threshold_values.get("fallback_to_legacy_below", 0.45))
    enforce_confirm_on_legacy_fallback = bool(thresholds_cfg.get("safety", {}).get("enforce_confirm_on_legacy_fallback", False))

    pack_results: list[dict[str, Any]] = []
    for pack in pack_manifest.get("packs") or []:
        grade_allow = [normalize_text(item) for item in (pack.get("grade_allow") or [])]
        task_allow = [normalize_text(item) for item in (pack.get("task_allow") or [])]
        if grade_allow and grade not in grade_allow:
            continue
        if task_allow and task_type not in task_allow:
            continue

        selection = select_pack_candidate(
            prompt_lower=prompt_lower,
            candidates=[normalize_text(item) for item in (pack.get("skill_candidates") or [])],
            task_type=task_type,
            requested_canonical=requested_canonical,
            skill_keyword_index=skill_keyword_index,
            routing_rules=routing_rules,
            pack=pack,
            candidate_selection_config=candidate_selection_cfg,
        )
        trigger_ratio = keyword_ratio(prompt_lower, pack.get("trigger_keywords") or [])
        priority_signal = min(max(float(pack.get("priority", 0)) / 100.0, 0.0), 1.0)
        score = ((0.5 * trigger_ratio) + (0.4 * float(selection["score"])) + (0.1 * priority_signal))
        score = round(max(0.0, min(1.0, score)), 4)
        candidate_signal = round(
            max(0.0, min(1.0, (0.75 * float(selection["score"])) + (0.25 * float(selection["top1_top2_gap"])))),
            4,
        )
        pack_results.append(
            {
                "pack_id": normalize_text(pack.get("id")),
                "score": score,
                "selected_candidate": selection["selected"],
                "candidate_selection_reason": selection["reason"],
                "candidate_selection_score": round(float(selection["score"]), 4),
                "candidate_ranking": selection["ranking"],
                "candidate_top1_top2_gap": round(float(selection["top1_top2_gap"]), 4),
                "candidate_signal": candidate_signal,
                "candidate_filtered_out_by_task": selection["filtered_out_by_task"],
            }
        )

    ranked = sorted(pack_results, key=lambda row: (-row["score"], row["pack_id"]))
    top = ranked[0] if ranked else None
    confidence = float(top["score"]) if top else 0.0
    top_gap = float(top["candidate_top1_top2_gap"]) if top else 0.0
    candidate_signal = float(top["candidate_signal"]) if top else 0.0
    can_override = bool(
        top
        and top["candidate_selection_reason"] in {"keyword_ranked", "requested_skill"}
        and candidate_signal >= min_candidate_signal_confirm
    )
    can_auto_route = bool(
        top
        and top["candidate_selection_reason"] in {"keyword_ranked", "requested_skill"}
        and candidate_signal >= min_candidate_signal_auto
        and top_gap >= min_top_gap
    )

    if not top:
        route_mode = "legacy_fallback"
        route_reason = "no_eligible_pack"
    elif confidence < fallback_threshold:
        if can_auto_route:
            route_mode = "pack_overlay"
            route_reason = "candidate_signal_auto_route"
            confidence = max(confidence, auto_route_threshold)
        elif can_override:
            route_mode = "confirm_required"
            route_reason = "candidate_signal_override"
            confidence = max(confidence, confirm_required_threshold)
        else:
            route_mode = "legacy_fallback"
            route_reason = "confidence_below_fallback"
    elif top_gap < min_top_gap:
        route_mode = "confirm_required"
        route_reason = "top_candidates_too_close"
    elif confidence < auto_route_threshold:
        if can_auto_route:
            route_mode = "pack_overlay"
            route_reason = "candidate_signal_auto_route"
            confidence = max(confidence, auto_route_threshold)
        else:
            route_mode = "confirm_required"
            route_reason = "confidence_requires_confirmation"
    else:
        route_mode = "pack_overlay"
        route_reason = "auto_route"

    legacy_fallback_guard_applied = False
    legacy_fallback_original_reason = None
    if route_mode == "legacy_fallback" and enforce_confirm_on_legacy_fallback:
        legacy_fallback_original_reason = route_reason
        route_mode = "confirm_required"
        route_reason = "legacy_fallback_guard"
        confidence = max(confidence, confirm_required_threshold)
        legacy_fallback_guard_applied = True

    result = {
        "prompt": prompt,
        "grade": grade,
        "task_type": task_type,
        "route_mode": route_mode,
        "route_reason": route_reason,
        "confidence": round(confidence, 4),
        "top1_top2_gap": round(top_gap, 4),
        "candidate_signal": round(candidate_signal, 4),
        "legacy_fallback_guard_applied": legacy_fallback_guard_applied,
        "legacy_fallback_original_reason": legacy_fallback_original_reason,
        "alias": {
            "requested_input": requested_skill,
            "requested_canonical": requested_canonical,
        },
        "thresholds": {
            "auto_route": auto_route_threshold,
            "confirm_required": confirm_required_threshold,
            "fallback_to_legacy_below": fallback_threshold,
            "min_top1_top2_gap": min_top_gap,
            "min_candidate_signal_for_confirm_override": min_candidate_signal_confirm,
            "min_candidate_signal_for_auto_route": min_candidate_signal_auto,
            "enforce_confirm_on_legacy_fallback": enforce_confirm_on_legacy_fallback,
        },
        "selected": (
            {
                "pack_id": top["pack_id"],
                "skill": top["selected_candidate"],
                "selection_reason": top["candidate_selection_reason"],
                "selection_score": top["candidate_selection_score"],
                "top1_top2_gap": top["candidate_top1_top2_gap"],
                "candidate_signal": top["candidate_signal"],
                "filtered_out_by_task": top["candidate_filtered_out_by_task"],
            }
            if top
            else None
        ),
        "ranked": ranked[:3],
        "runtime_neutral_bridge": {
            "enabled": True,
            "engine": "python",
            "host": "runtime_neutral",
        },
    }
    result.update(build_fallback_truth(result, fallback_policy))

    confirm_ui = build_confirm_ui(repo, result, target_root)
    if confirm_ui:
        result["confirm_ui"] = confirm_ui
    return result
