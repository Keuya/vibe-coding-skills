from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
INSTALL_SCRIPT = REPO_ROOT / "install.sh"
UNINSTALL_SCRIPT = REPO_ROOT / "uninstall.sh"


class InstalledRuntimeUninstallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def install_host(self, host: str, target_root: Path) -> None:
        subprocess.run(
            [
                "bash",
                str(INSTALL_SCRIPT),
                "--host",
                host,
                "--target-root",
                str(target_root),
                "--profile",
                "full",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

    def uninstall_host(self, host: str, target_root: Path) -> dict[str, object]:
        result = subprocess.run(
            [
                "bash",
                str(UNINSTALL_SCRIPT),
                "--host",
                host,
                "--target-root",
                str(target_root),
                "--profile",
                "full",
                "--purge-empty-dirs",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_codex_installed_runtime_uninstall_removes_managed_payload_only(self) -> None:
        target_root = self.root / "codex-root"
        self.install_host("codex", target_root)
        sentinel = target_root / "commands" / "user.md"
        sentinel.write_text("user\n", encoding="utf-8")

        payload = self.uninstall_host("codex", target_root)

        self.assertFalse((target_root / "rules").exists())
        self.assertFalse((target_root / "config" / "plugins-manifest.codex.json").exists())
        self.assertTrue(sentinel.exists())
        self.assertIn("PASS", payload["gate_result"])

    def test_claude_code_uninstall_removes_vibe_managed_surface(self) -> None:
        target_root = self.root / "claude-root"
        self.install_host("claude-code", target_root)
        settings_path = target_root / "settings.json"
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        settings["user.keep"] = True
        settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
        sentinel = target_root / "commands" / "user.md"
        sentinel.write_text("user\n", encoding="utf-8")

        self.uninstall_host("claude-code", target_root)

        self.assertFalse((target_root / ".vibeskills").exists())
        self.assertTrue(sentinel.exists())
        if settings_path.exists():
            remaining = json.loads(settings_path.read_text(encoding="utf-8"))
            self.assertNotIn("vibeskills", remaining)
            self.assertTrue(remaining["user.keep"])

    def test_cursor_uninstall_removes_vibe_managed_surface(self) -> None:
        target_root = self.root / "cursor-root"
        self.install_host("cursor", target_root)
        sentinel = target_root / "commands" / "user.md"
        sentinel.write_text("user\n", encoding="utf-8")

        self.uninstall_host("cursor", target_root)

        self.assertFalse((target_root / ".vibeskills").exists())
        self.assertTrue(sentinel.exists())
        settings_path = target_root / "settings.json"
        if settings_path.exists():
            remaining = json.loads(settings_path.read_text(encoding="utf-8"))
            self.assertNotIn("vibeskills", remaining)

    def test_windsurf_uninstall_removes_runtime_core_preview_host_payload(self) -> None:
        target_root = self.root / "windsurf-root"
        self.install_host("windsurf", target_root)
        sentinel = target_root / "commands" / "user.md"
        sentinel.write_text("user\n", encoding="utf-8")

        self.uninstall_host("windsurf", target_root)

        self.assertFalse((target_root / "global_workflows" / "vibe.md").exists())
        self.assertFalse((target_root / ".vibeskills").exists())
        self.assertTrue(sentinel.exists())

    def test_openclaw_uninstall_removes_runtime_core_preview_host_payload(self) -> None:
        target_root = self.root / "openclaw-root"
        self.install_host("openclaw", target_root)
        sentinel = target_root / "commands" / "user.md"
        sentinel.write_text("user\n", encoding="utf-8")

        self.uninstall_host("openclaw", target_root)

        self.assertFalse((target_root / "global_workflows" / "vibe.md").exists())
        self.assertFalse((target_root / ".vibeskills").exists())
        self.assertTrue(sentinel.exists())

    def test_opencode_uninstall_removes_managed_payload_and_preserves_user_json(self) -> None:
        target_root = self.root / "opencode-root"
        self.install_host("opencode", target_root)
        settings_path = target_root / "opencode.json"
        settings_path.write_text(
            json.dumps(
                {
                    "vibeskills": {
                        "host_id": "opencode",
                        "managed": True,
                        "commands_root": str((target_root / "commands").resolve()),
                    },
                    "user.keep": True,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        sentinel = target_root / "commands" / "user.md"
        sentinel.write_text("user\n", encoding="utf-8")

        self.uninstall_host("opencode", target_root)

        self.assertFalse((target_root / ".vibeskills").exists())
        self.assertFalse((target_root / "command" / "vibe.md").exists())
        self.assertFalse((target_root / "agents" / "vibe-plan.md").exists())
        self.assertFalse((target_root / "opencode.json.example").exists())
        self.assertTrue(sentinel.exists())
        if settings_path.exists():
            remaining = json.loads(settings_path.read_text(encoding="utf-8"))
            self.assertNotIn("vibeskills", remaining)
            self.assertTrue(remaining["user.keep"])


if __name__ == "__main__":
    unittest.main()
