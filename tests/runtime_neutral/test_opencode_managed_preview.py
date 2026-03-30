from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
INSTALLER = REPO_ROOT / "scripts" / "install" / "install_vgo_adapter.py"


class OpenCodeManagedPreviewTests(unittest.TestCase):
    def test_python_installer_materializes_opencode_host_closure_without_touching_real_config(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            target_root = Path(tempdir)
            result = subprocess.run(
                [
                    sys.executable,
                    str(INSTALLER),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--target-root",
                    str(target_root),
                    "--host",
                    "opencode",
                    "--profile",
                    "full",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(result.stdout)
            closure_path = target_root / ".vibeskills" / "host-closure.json"
            settings_path = target_root / "opencode.json"
            example_path = target_root / "opencode.json.example"

            self.assertEqual("opencode", payload["host_id"])
            self.assertEqual("preview-guidance", payload["install_mode"])
            self.assertTrue(closure_path.exists())
            self.assertFalse(settings_path.exists())
            self.assertTrue(example_path.exists())
            self.assertTrue((target_root / "commands" / "vibe.md").exists())
            self.assertTrue((target_root / "command" / "vibe.md").exists())
            self.assertTrue((target_root / "agents").exists())
            self.assertTrue((target_root / "agent").exists())
            closure = json.loads(closure_path.read_text(encoding="utf-8"))
            self.assertEqual([], closure["settings_materialized"])
            self.assertEqual("not-present", payload["legacy_opencode_config_cleanup"]["status"])

    def test_python_installer_repairs_legacy_vibe_node_without_touching_user_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            target_root = Path(tempdir)
            settings_path = target_root / "opencode.json"
            settings_path.write_text(
                json.dumps(
                    {
                        "$schema": "https://opencode.ai/config.json",
                        "mcp": {
                            "playwright": {
                                "enabled": True,
                                "type": "local",
                                "command": ["npx", "@playwright/mcp@latest"],
                            }
                        },
                        "vibeskills": {
                            "host_id": "opencode",
                            "managed": True,
                            "commands_root": str((target_root / "commands").resolve()),
                            "agents_root": str((target_root / "agents").resolve()),
                        },
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(INSTALLER),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--target-root",
                    str(target_root),
                    "--host",
                    "opencode",
                    "--profile",
                    "full",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            repaired = json.loads(settings_path.read_text(encoding="utf-8"))
            self.assertNotIn("vibeskills", repaired)
            self.assertIn("mcp", repaired)
            self.assertEqual("removed-owned-node", payload["legacy_opencode_config_cleanup"]["status"])
            self.assertEqual(["$schema", "mcp"], payload["legacy_opencode_config_cleanup"]["preserved_keys"])


if __name__ == "__main__":
    unittest.main()
