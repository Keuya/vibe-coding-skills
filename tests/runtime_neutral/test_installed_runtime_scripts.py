from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class InstalledRuntimeScriptsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.target_root = self.root / "target-a"
        self.target_root.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def install_shell_runtime(self, host: str = "codex") -> None:
        cmd = [
            "bash",
            str(REPO_ROOT / "install.sh"),
            "--host",
            host,
            "--profile",
            "full",
            "--target-root",
            str(self.target_root),
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)

    def assert_nested_runtime_skill_entrypoints_sanitized(self, target_root: Path) -> None:
        nested_skills_root = target_root / "skills" / "vibe" / "bundled" / "skills"
        self.assertTrue(nested_skills_root.exists())
        self.assertEqual([], sorted(nested_skills_root.glob("*/SKILL.md")))
        for name in ("vibe", "ralph-loop", "cancel-ralph", "xan"):
            self.assertTrue((nested_skills_root / name / "SKILL.runtime-mirror.md").exists())

    def test_shell_install_quarantines_legacy_agents_duplicate_for_default_codex_root(self) -> None:
        home_root = self.root / "home"
        target_root = home_root / ".codex"
        duplicate_root = home_root / ".agents" / "skills" / "vibe"
        target_root.mkdir(parents=True, exist_ok=True)
        duplicate_root.mkdir(parents=True, exist_ok=True)
        (duplicate_root / "SKILL.md").write_text(
            "---\nname: vibe\ndescription: legacy duplicate\n---\n",
            encoding="utf-8",
        )

        env = os.environ.copy()
        env["HOME"] = str(home_root)

        cmd = [
            "bash",
            str(REPO_ROOT / "install.sh"),
            "--host",
            "codex",
            "--profile",
            "full",
            "--target-root",
            str(target_root),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)

        self.assertIn("Quarantined duplicate Codex-discovered vibe skill", result.stdout)
        self.assertTrue((target_root / "skills" / "vibe" / "SKILL.md").exists())
        self.assertFalse(duplicate_root.exists())
        quarantined = list((home_root / ".agents" / "skills-disabled").glob("vibe.codex-duplicate-*"))
        self.assertEqual(1, len(quarantined))
        self.assertTrue((quarantined[0] / "SKILL.md").exists())

    def test_shell_install_does_not_mutate_agents_duplicate_for_custom_codex_target_root(self) -> None:
        home_root = self.root / "home"
        target_root = home_root / "custom-codex-root"
        duplicate_root = home_root / ".agents" / "skills" / "vibe"
        target_root.mkdir(parents=True, exist_ok=True)
        duplicate_root.mkdir(parents=True, exist_ok=True)
        (duplicate_root / "SKILL.md").write_text(
            "---\nname: vibe\ndescription: legacy duplicate\n---\n",
            encoding="utf-8",
        )

        env = os.environ.copy()
        env["HOME"] = str(home_root)

        cmd = [
            "bash",
            str(REPO_ROOT / "install.sh"),
            "--host",
            "codex",
            "--profile",
            "full",
            "--target-root",
            str(target_root),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)

        self.assertNotIn("Quarantined duplicate Codex-discovered vibe skill", result.stdout)
        self.assertTrue((target_root / "skills" / "vibe" / "SKILL.md").exists())
        self.assertTrue(duplicate_root.exists())
        self.assertFalse((home_root / ".agents" / "skills-disabled").exists())

    def test_shell_check_fails_when_legacy_agents_duplicate_is_reintroduced(self) -> None:
        home_root = self.root / "home"
        target_root = home_root / ".codex"
        target_root.mkdir(parents=True, exist_ok=True)

        env = os.environ.copy()
        env["HOME"] = str(home_root)

        install_cmd = [
            "bash",
            str(REPO_ROOT / "install.sh"),
            "--host",
            "codex",
            "--profile",
            "full",
            "--target-root",
            str(target_root),
        ]
        subprocess.run(install_cmd, capture_output=True, text=True, check=True, env=env)

        duplicate_root = home_root / ".agents" / "skills" / "vibe"
        duplicate_root.mkdir(parents=True, exist_ok=True)
        (duplicate_root / "SKILL.md").write_text(
            "---\nname: vibe\ndescription: legacy duplicate\n---\n",
            encoding="utf-8",
        )

        installed_root = target_root / "skills" / "vibe"
        check_cmd = [
            "bash",
            str(installed_root / "check.sh"),
            "--host",
            "codex",
            "--profile",
            "full",
            "--target-root",
            str(target_root),
        ]
        check_result = subprocess.run(check_cmd, capture_output=True, text=True, env=env)
        self.assertNotEqual(0, check_result.returncode)
        self.assertIn("duplicate Codex-discovered vibe skill surface", check_result.stdout)
        self.assertNotIn("safe_parent_dir: command not found", check_result.stderr)

    def test_installed_shell_scripts_work_without_repo_level_adapter_registry(self) -> None:
        self.install_shell_runtime()
        self.assert_nested_runtime_skill_entrypoints_sanitized(self.target_root)

        installed_root = self.target_root / "skills" / "vibe"
        check_cmd = [
            "bash",
            str(installed_root / "check.sh"),
            "--host",
            "codex",
            "--profile",
            "full",
            "--target-root",
            str(self.target_root),
        ]
        check_result = subprocess.run(check_cmd, capture_output=True, text=True, check=True)
        self.assertIn("=== VCO Adapter Health Check ===", check_result.stdout)
        self.assertNotIn("VGO adapter registry not found", check_result.stdout)
        self.assertNotIn("VGO adapter registry not found", check_result.stderr)

    def test_installed_runtime_bootstrap_supports_openclaw_without_self_deleting_source(self) -> None:
        self.install_shell_runtime(host="openclaw")

        installed_root = self.target_root / "skills" / "vibe"
        env = os.environ.copy()
        env["HOME"] = str(self.root / "home")
        env["OPENCLAW_HOME"] = str(self.target_root)
        bootstrap_cmd = [
            "bash",
            str(installed_root / "scripts" / "bootstrap" / "one-shot-setup.sh"),
            "--host",
            "openclaw",
            "--profile",
            "full",
            "--target-root",
            str(self.target_root),
        ]
        bootstrap_result = subprocess.run(bootstrap_cmd, capture_output=True, text=True, check=True, env=env)

        self.assertIn("Host                  : openclaw", bootstrap_result.stdout)
        self.assertIn("One-shot setup completed.", bootstrap_result.stdout)
        self.assertTrue((installed_root / "SKILL.md").exists())
        self.assertTrue((self.target_root / "mcp_config.json").exists())

    def test_shell_install_prunes_stale_managed_entries_without_recursive_dir_wipe(self) -> None:
        self.install_shell_runtime()

        managed_root = self.target_root / "skills" / "vibe"
        stale_file = managed_root / "config" / "stale.json"
        stale_dir = managed_root / "docs" / "obsolete-dir"
        stale_nested_file = stale_dir / "note.md"

        stale_file.parent.mkdir(parents=True, exist_ok=True)
        stale_dir.mkdir(parents=True, exist_ok=True)
        stale_file.write_text("stale\n", encoding="utf-8")
        stale_nested_file.write_text("obsolete\n", encoding="utf-8")

        self.install_shell_runtime()

        self.assertFalse(stale_file.exists())
        self.assertFalse(stale_nested_file.exists())
        self.assertFalse(stale_dir.exists())

        install_script = (self.target_root / "skills" / "vibe" / "install.sh").read_text(encoding="utf-8")
        self.assertNotIn("rm -rf", install_script)

    def test_installed_powershell_scripts_work_without_repo_level_adapter_registry(self) -> None:
        if shutil.which("pwsh") is None:
            self.skipTest("pwsh not available")

        install_cmd = [
            "pwsh",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(REPO_ROOT / "install.ps1"),
            "-HostId",
            "codex",
            "-Profile",
            "full",
            "-TargetRoot",
            str(self.target_root),
        ]
        subprocess.run(install_cmd, capture_output=True, text=True, check=True)
        self.assert_nested_runtime_skill_entrypoints_sanitized(self.target_root)

        installed_root = self.target_root / "skills" / "vibe"
        check_cmd = [
            "pwsh",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(installed_root / "check.ps1"),
            "-HostId",
            "codex",
            "-Profile",
            "full",
            "-TargetRoot",
            str(self.target_root),
        ]
        check_result = subprocess.run(check_cmd, capture_output=True, text=True, check=True)
        self.assertIn("=== VCO Adapter Health Check ===", check_result.stdout)
        self.assertNotIn("VGO adapter registry not found", check_result.stdout)
        self.assertNotIn("VGO adapter registry not found", check_result.stderr)

    def test_powershell_install_quarantines_legacy_agents_duplicate_for_default_codex_root(self) -> None:
        if shutil.which("pwsh") is None:
            self.skipTest("pwsh not available")

        home_root = self.root / "home"
        target_root = home_root / ".codex"
        duplicate_root = home_root / ".agents" / "skills" / "vibe"
        target_root.mkdir(parents=True, exist_ok=True)
        duplicate_root.mkdir(parents=True, exist_ok=True)
        (duplicate_root / "SKILL.md").write_text(
            "---\nname: vibe\ndescription: legacy duplicate\n---\n",
            encoding="utf-8",
        )

        env = os.environ.copy()
        env["HOME"] = str(home_root)

        install_cmd = [
            "pwsh",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(REPO_ROOT / "install.ps1"),
            "-HostId",
            "codex",
            "-Profile",
            "full",
            "-TargetRoot",
            str(target_root),
        ]
        result = subprocess.run(install_cmd, capture_output=True, text=True, check=True, env=env)

        self.assertIn("Quarantined duplicate Codex-discovered vibe skill", result.stderr + result.stdout)
        self.assertTrue((target_root / "skills" / "vibe" / "SKILL.md").exists())
        self.assertFalse(duplicate_root.exists())
        quarantined = list((home_root / ".agents" / "skills-disabled").glob("vibe.codex-duplicate-*"))
        self.assertEqual(1, len(quarantined))
        self.assertTrue((quarantined[0] / "SKILL.md").exists())

    def test_powershell_check_fails_when_legacy_agents_duplicate_is_reintroduced(self) -> None:
        if shutil.which("pwsh") is None:
            self.skipTest("pwsh not available")

        home_root = self.root / "home"
        target_root = home_root / ".codex"
        target_root.mkdir(parents=True, exist_ok=True)

        env = os.environ.copy()
        env["HOME"] = str(home_root)

        install_cmd = [
            "pwsh",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(REPO_ROOT / "install.ps1"),
            "-HostId",
            "codex",
            "-Profile",
            "full",
            "-TargetRoot",
            str(target_root),
        ]
        subprocess.run(install_cmd, capture_output=True, text=True, check=True, env=env)

        duplicate_root = home_root / ".agents" / "skills" / "vibe"
        duplicate_root.mkdir(parents=True, exist_ok=True)
        (duplicate_root / "SKILL.md").write_text(
            "---\nname: vibe\ndescription: legacy duplicate\n---\n",
            encoding="utf-8",
        )

        installed_root = target_root / "skills" / "vibe"
        check_cmd = [
            "pwsh",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(installed_root / "check.ps1"),
            "-HostId",
            "codex",
            "-Profile",
            "full",
            "-TargetRoot",
            str(target_root),
        ]
        check_result = subprocess.run(check_cmd, capture_output=True, text=True, env=env)
        self.assertNotEqual(0, check_result.returncode)
        self.assertIn("duplicate Codex-discovered vibe skill surface", check_result.stdout)


if __name__ == "__main__":
    unittest.main()
