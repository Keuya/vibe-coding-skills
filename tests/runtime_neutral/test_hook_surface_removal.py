from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SETTINGS_CLAUDE = REPO_ROOT / "config" / "settings.template.claude.json"
SETTINGS_CODEX = REPO_ROOT / "config" / "settings.template.codex.json"
CLAUDE_CLOSURE = REPO_ROOT / "adapters" / "claude-code" / "closure.json"
CLAUDE_HOST_PROFILE = REPO_ROOT / "adapters" / "claude-code" / "host-profile.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


class ClaudeSettingsTemplateHookRemovalTests(unittest.TestCase):
    """Tests that the managed hook surface (write-guard, PreToolUse) has been
    removed from the Claude settings template.  This verifies the PR change
    that drops hookify and the hooks stanza from settings.template.claude.json."""

    def setUp(self) -> None:
        self.settings = load_json(SETTINGS_CLAUDE)

    def test_hookify_plugin_not_present_in_enabled_plugins(self) -> None:
        enabled_plugins = self.settings.get("enabledPlugins", {})
        self.assertNotIn(
            "hookify@claude-plugins-official",
            enabled_plugins,
            "hookify plugin must no longer appear in enabledPlugins",
        )

    def test_no_top_level_hooks_section(self) -> None:
        self.assertNotIn(
            "hooks",
            self.settings,
            "settings.template.claude.json must not contain a top-level 'hooks' key",
        )

    def test_skip_dangerous_mode_permission_prompt_still_present(self) -> None:
        # Regression guard: this field was retained; ensure the hooks removal
        # did not accidentally drop it.
        self.assertIn(
            "skipDangerousModePermissionPrompt",
            self.settings,
        )
        self.assertTrue(self.settings["skipDangerousModePermissionPrompt"])

    def test_enabled_plugins_section_still_present_and_non_empty(self) -> None:
        enabled_plugins = self.settings.get("enabledPlugins", {})
        self.assertIsInstance(enabled_plugins, dict)
        self.assertGreater(
            len(enabled_plugins),
            0,
            "enabledPlugins should still be populated with other plugins",
        )

    def test_claude_code_settings_plugin_still_enabled(self) -> None:
        # Verify a key plugin was NOT removed alongside hookify.
        enabled_plugins = self.settings.get("enabledPlugins", {})
        self.assertIn(
            "claude-code-settings@claude-code-settings",
            enabled_plugins,
            "claude-code-settings plugin must still be present",
        )

    def test_no_pretooluse_hook_entry(self) -> None:
        # Even if a 'hooks' key were somehow reintroduced, the PreToolUse
        # write-guard entry must not be present.
        hooks = self.settings.get("hooks", {})
        pretooluse_entries = hooks.get("PreToolUse", [])
        write_guard_present = any(
            isinstance(entry, dict)
            and str(entry.get("description", "")).strip() == "VibeSkills managed write guard"
            for entry in pretooluse_entries
        )
        self.assertFalse(
            write_guard_present,
            "VibeSkills managed write guard PreToolUse hook must not be in the template",
        )

    def test_no_write_guard_command_reference(self) -> None:
        raw_text = SETTINGS_CLAUDE.read_text(encoding="utf-8-sig")
        self.assertNotIn(
            "write-guard.js",
            raw_text,
            "write-guard.js must not appear anywhere in settings.template.claude.json",
        )


class CodexSettingsTemplateHookRemovalTests(unittest.TestCase):
    """Tests that the hooks_root and hooks sections have been removed from
    settings.template.codex.json as part of the managed hook surface removal."""

    def setUp(self) -> None:
        self.settings = load_json(SETTINGS_CODEX)

    def test_no_top_level_hooks_section(self) -> None:
        self.assertNotIn(
            "hooks",
            self.settings,
            "settings.template.codex.json must not contain a top-level 'hooks' key",
        )

    def test_vco_section_has_no_hooks_root(self) -> None:
        vco = self.settings.get("vco", {})
        self.assertNotIn(
            "hooks_root",
            vco,
            "vco section must not contain a hooks_root entry",
        )

    def test_vco_section_still_has_required_fields(self) -> None:
        # Regression guard: skill_root and mcp_profile are still required.
        vco = self.settings.get("vco", {})
        self.assertIn("skill_root", vco)
        self.assertIn("mcp_profile", vco)

    def test_env_section_still_present(self) -> None:
        self.assertIn("env", self.settings)
        env = self.settings["env"]
        self.assertIn("VCO_PROFILE", env)
        self.assertIn("VCO_CODEX_MODE", env)

    def test_no_write_guard_reference_anywhere(self) -> None:
        raw_text = SETTINGS_CODEX.read_text(encoding="utf-8-sig")
        self.assertNotIn(
            "write-guard",
            raw_text,
            "write-guard must not appear anywhere in settings.template.codex.json",
        )

    def test_file_is_valid_utf8_without_bom(self) -> None:
        # The old file had a UTF-8 BOM (﻿); the new file must be clean.
        raw_bytes = SETTINGS_CODEX.read_bytes()
        self.assertFalse(
            raw_bytes.startswith(b"\xef\xbb\xbf"),
            "settings.template.codex.json must not start with a UTF-8 BOM",
        )


class ClaudeAdapterClosureHookRemovalTests(unittest.TestCase):
    """Tests that all managed hook surface entries have been removed from
    adapters/claude-code/closure.json as described in the PR."""

    def setUp(self) -> None:
        self.closure = load_json(CLAUDE_CLOSURE)

    def test_write_guard_not_in_repo_managed_payload(self) -> None:
        payload = self.closure.get("repo_managed_payload", [])
        for entry in payload:
            self.assertNotIn(
                "write-guard",
                str(entry),
                "write-guard must not appear in repo_managed_payload",
            )

    def test_hook_entry_not_in_repo_managed_payload(self) -> None:
        payload = self.closure.get("repo_managed_payload", [])
        for entry in payload:
            self.assertNotIn(
                "hook",
                str(entry).lower(),
                f"hook reference must not appear in repo_managed_payload: {entry!r}",
            )

    def test_write_guard_not_in_host_state_written(self) -> None:
        host_state = self.closure.get("host_state_written", [])
        for entry in host_state:
            self.assertNotIn(
                "write-guard",
                str(entry),
                "write-guard must not appear in host_state_written",
            )

    def test_hook_entry_not_in_host_state_written(self) -> None:
        host_state = self.closure.get("host_state_written", [])
        for entry in host_state:
            self.assertNotIn(
                "hook",
                str(entry).lower(),
                f"hook reference must not appear in host_state_written: {entry!r}",
            )

    def test_managed_hook_surface_check_not_in_verification_contract(self) -> None:
        contract = self.closure.get("verification_contract", [])
        self.assertNotIn(
            "managed Claude hook surface check",
            contract,
            "managed Claude hook surface check must be removed from verification_contract",
        )

    def test_managed_claude_settings_presence_check_still_in_verification_contract(self) -> None:
        # Regression guard: the settings presence check (not hook) must be retained.
        contract = self.closure.get("verification_contract", [])
        self.assertIn(
            "managed Claude settings presence check",
            contract,
            "managed Claude settings presence check must still be in verification_contract",
        )

    def test_hook_entry_not_in_uninstall_contract_shared_json_targets(self) -> None:
        uninstall = self.closure.get("uninstall_contract", {})
        shared = uninstall.get("shared_json_targets", [])
        for entry in shared:
            self.assertNotIn(
                "hook",
                str(entry).lower(),
                f"hook reference must not appear in shared_json_targets: {entry!r}",
            )

    def test_uninstall_contract_shared_json_targets_has_vibeskills_stanza(self) -> None:
        uninstall = self.closure.get("uninstall_contract", {})
        shared = uninstall.get("shared_json_targets", [])
        self.assertIn(
            "settings.json vibeskills stanza",
            shared,
            "vibeskills stanza must remain in shared_json_targets",
        )

    def test_write_guard_not_in_uninstall_contract_owned_payload(self) -> None:
        uninstall = self.closure.get("uninstall_contract", {})
        owned = uninstall.get("owned_payload", [])
        for entry in owned:
            self.assertNotIn(
                "write-guard",
                str(entry),
                "write-guard must not appear in uninstall_contract owned_payload",
            )

    def test_host_managed_boundaries_reflects_settings_surface_only(self) -> None:
        boundaries = self.closure.get("host_managed_boundaries", [])
        for boundary in boundaries:
            self.assertNotIn(
                "write-guard",
                str(boundary),
                "write-guard surface must not appear in host_managed_boundaries",
            )
        # The boundary description should reference "settings surface", not the old compound surface.
        last_boundary = boundaries[-1] if boundaries else ""
        self.assertIn(
            "settings surface",
            last_boundary,
            "host_managed_boundaries should reference 'settings surface'",
        )

    def test_settings_managed_vibeskills_stanza_still_in_host_state_written(self) -> None:
        # Regression guard: the vibeskills stanza entry should remain.
        host_state = self.closure.get("host_state_written", [])
        self.assertIn(
            "settings.json managed vibeskills stanza",
            host_state,
        )


class ClaudeAdapterHostProfileHookRemovalTests(unittest.TestCase):
    """Tests that hook-related language has been removed from
    adapters/claude-code/host-profile.json."""

    def setUp(self) -> None:
        self.profile = load_json(CLAUDE_HOST_PROFILE)

    def test_settings_surface_notes_does_not_mention_hook(self) -> None:
        notes = self.profile.get("settings_surface", {}).get("notes", "")
        self.assertNotIn(
            "hook",
            notes.lower(),
            "settings_surface notes must not reference hooks",
        )

    def test_settings_surface_notes_does_not_mention_write_guard(self) -> None:
        notes = self.profile.get("settings_surface", {}).get("notes", "")
        self.assertNotIn(
            "write-guard",
            notes,
            "settings_surface notes must not reference write-guard",
        )

    def test_host_managed_surfaces_does_not_mention_write_guard(self) -> None:
        surfaces = self.profile.get("host_managed_surfaces", [])
        for surface in surfaces:
            self.assertNotIn(
                "write-guard",
                str(surface),
                "write-guard must not appear in host_managed_surfaces",
            )

    def test_host_managed_surfaces_references_settings_surface(self) -> None:
        surfaces = self.profile.get("host_managed_surfaces", [])
        last_surface = surfaces[-1] if surfaces else ""
        self.assertIn(
            "settings surface",
            last_surface,
            "host_managed_surfaces should reference 'settings surface'",
        )

    def test_settings_surface_managed_by_repo(self) -> None:
        # Regression guard: settings are still managed by the repo.
        self.assertTrue(
            self.profile.get("settings_surface", {}).get("managed_by_repo"),
        )

    def test_settings_surface_notes_mentions_vibeskills_stanza(self) -> None:
        notes = self.profile.get("settings_surface", {}).get("notes", "")
        self.assertIn(
            "vibeskills",
            notes.lower(),
            "settings_surface notes must still describe the vibeskills-managed stanza",
        )

    def test_no_write_guard_reference_anywhere_in_file(self) -> None:
        raw_text = CLAUDE_HOST_PROFILE.read_text(encoding="utf-8")
        self.assertNotIn(
            "write-guard",
            raw_text,
            "write-guard must not appear anywhere in host-profile.json",
        )


if __name__ == "__main__":
    unittest.main()