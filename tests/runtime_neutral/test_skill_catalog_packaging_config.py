from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PACKAGING = REPO_ROOT / "config" / "skill-catalog-packaging.json"
CATALOG_PROFILES = REPO_ROOT / "config" / "skill-catalog-profiles.json"
CATALOG_GROUPS = REPO_ROOT / "config" / "skill-catalog-groups.json"
RUNTIME_PACKAGING = REPO_ROOT / "config" / "runtime-core-packaging.json"
MINIMAL_MANIFEST = REPO_ROOT / "config" / "runtime-core-packaging.minimal.json"
FULL_MANIFEST = REPO_ROOT / "config" / "runtime-core-packaging.full.json"

# These are the skills that belong to the runtime core and must NOT be
# distributed by the catalog (they travel with the vibe runtime payload).
RUNTIME_CORE_SKILLS = {
    "vibe",
    "dialectic",
    "local-vco-roles",
    "spec-kit-vibe-compat",
    "superclaude-framework-compat",
    "ralph-loop",
    "cancel-ralph",
    "tdd-guide",
    "think-harder",
}

# workflow-foundation group skills
WORKFLOW_FOUNDATION_SKILLS = {
    "brainstorming",
    "writing-plans",
    "subagent-driven-development",
    "systematic-debugging",
}

# optional-review group skills
OPTIONAL_REVIEW_SKILLS = {
    "requesting-code-review",
    "receiving-code-review",
    "verification-before-completion",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


class CatalogPackagingManifestTests(unittest.TestCase):
    """Tests for the new config/skill-catalog-packaging.json manifest."""

    def setUp(self) -> None:
        self.manifest = load_json(CATALOG_PACKAGING)

    def test_manifest_file_exists(self) -> None:
        self.assertTrue(CATALOG_PACKAGING.exists())

    def test_schema_version_is_present_and_integer(self) -> None:
        self.assertIn("schema_version", self.manifest)
        self.assertIsInstance(self.manifest["schema_version"], int)

    def test_package_id_is_skill_catalog(self) -> None:
        self.assertEqual("skill-catalog", self.manifest["package_id"])

    def test_catalog_root_points_to_bundled_skills(self) -> None:
        self.assertEqual("bundled/skills", self.manifest["catalog_root"])

    def test_profiles_manifest_points_to_catalog_profiles_file(self) -> None:
        self.assertEqual(
            "config/skill-catalog-profiles.json",
            self.manifest["profiles_manifest"],
        )

    def test_groups_manifest_points_to_catalog_groups_file(self) -> None:
        self.assertEqual(
            "config/skill-catalog-groups.json",
            self.manifest["groups_manifest"],
        )

    def test_referenced_profiles_manifest_exists(self) -> None:
        profiles_path = REPO_ROOT / self.manifest["profiles_manifest"]
        self.assertTrue(
            profiles_path.exists(),
            f"profiles_manifest reference {self.manifest['profiles_manifest']!r} must exist",
        )

    def test_referenced_groups_manifest_exists(self) -> None:
        groups_path = REPO_ROOT / self.manifest["groups_manifest"]
        self.assertTrue(
            groups_path.exists(),
            f"groups_manifest reference {self.manifest['groups_manifest']!r} must exist",
        )


class CatalogGroupsManifestTests(unittest.TestCase):
    """Tests for the new config/skill-catalog-groups.json manifest."""

    def setUp(self) -> None:
        self.groups_doc = load_json(CATALOG_GROUPS)

    def test_groups_file_exists(self) -> None:
        self.assertTrue(CATALOG_GROUPS.exists())

    def test_schema_version_is_present(self) -> None:
        self.assertIn("schema_version", self.groups_doc)

    def test_groups_key_present(self) -> None:
        self.assertIn("groups", self.groups_doc)
        self.assertIsInstance(self.groups_doc["groups"], dict)

    def test_workflow_foundation_group_exists(self) -> None:
        groups = self.groups_doc["groups"]
        self.assertIn("workflow-foundation", groups)

    def test_optional_review_group_exists(self) -> None:
        groups = self.groups_doc["groups"]
        self.assertIn("optional-review", groups)

    def test_workflow_foundation_contains_expected_skills(self) -> None:
        skills = set(self.groups_doc["groups"]["workflow-foundation"]["skills"])
        self.assertEqual(WORKFLOW_FOUNDATION_SKILLS, skills)

    def test_optional_review_contains_expected_skills(self) -> None:
        skills = set(self.groups_doc["groups"]["optional-review"]["skills"])
        self.assertEqual(OPTIONAL_REVIEW_SKILLS, skills)

    def test_no_group_contains_runtime_core_skills(self) -> None:
        groups = self.groups_doc["groups"]
        for group_name, group_def in groups.items():
            skill_list = group_def.get("skills", [])
            for skill in skill_list:
                self.assertNotIn(
                    skill,
                    RUNTIME_CORE_SKILLS,
                    f"Group {group_name!r} must not contain runtime-core skill {skill!r}",
                )

    def test_all_group_skill_names_are_non_empty_strings(self) -> None:
        groups = self.groups_doc["groups"]
        for group_name, group_def in groups.items():
            for skill in group_def.get("skills", []):
                self.assertIsInstance(skill, str)
                self.assertTrue(
                    len(skill.strip()) > 0,
                    f"Group {group_name!r} contains an empty skill name",
                )

    def test_no_group_skill_names_contain_path_separators(self) -> None:
        groups = self.groups_doc["groups"]
        for group_name, group_def in groups.items():
            for skill in group_def.get("skills", []):
                self.assertNotIn(
                    "/",
                    skill,
                    f"Group {group_name!r} skill {skill!r} must not be a path",
                )
                self.assertNotIn(
                    "\\",
                    skill,
                    f"Group {group_name!r} skill {skill!r} must not be a path",
                )


class CatalogProfilesManifestTests(unittest.TestCase):
    """Tests for the new config/skill-catalog-profiles.json manifest."""

    def setUp(self) -> None:
        self.profiles_doc = load_json(CATALOG_PROFILES)
        self.groups_doc = load_json(CATALOG_GROUPS)

    def test_profiles_file_exists(self) -> None:
        self.assertTrue(CATALOG_PROFILES.exists())

    def test_schema_version_is_present(self) -> None:
        self.assertIn("schema_version", self.profiles_doc)

    def test_profiles_key_present(self) -> None:
        self.assertIn("profiles", self.profiles_doc)
        self.assertIsInstance(self.profiles_doc["profiles"], dict)

    def test_foundation_workflow_profile_exists(self) -> None:
        self.assertIn("foundation-workflow", self.profiles_doc["profiles"])

    def test_default_full_profile_exists(self) -> None:
        self.assertIn("default-full", self.profiles_doc["profiles"])

    def test_foundation_workflow_references_workflow_foundation_group(self) -> None:
        profile = self.profiles_doc["profiles"]["foundation-workflow"]
        self.assertIn("workflow-foundation", profile["groups"])

    def test_foundation_workflow_does_not_include_all_bundled(self) -> None:
        profile = self.profiles_doc["profiles"]["foundation-workflow"]
        self.assertFalse(
            profile["include_all_bundled"],
            "foundation-workflow profile must not include_all_bundled",
        )

    def test_foundation_workflow_has_empty_exclude_skills(self) -> None:
        profile = self.profiles_doc["profiles"]["foundation-workflow"]
        self.assertEqual(
            [],
            profile["exclude_skills"],
            "foundation-workflow must have an empty exclude_skills list",
        )

    def test_default_full_includes_all_bundled(self) -> None:
        profile = self.profiles_doc["profiles"]["default-full"]
        self.assertTrue(
            profile["include_all_bundled"],
            "default-full profile must set include_all_bundled=true",
        )

    def test_default_full_references_both_groups(self) -> None:
        profile = self.profiles_doc["profiles"]["default-full"]
        self.assertIn("workflow-foundation", profile["groups"])
        self.assertIn("optional-review", profile["groups"])

    def test_default_full_excludes_runtime_core_skills(self) -> None:
        profile = self.profiles_doc["profiles"]["default-full"]
        excluded = set(profile["exclude_skills"])
        self.assertEqual(
            RUNTIME_CORE_SKILLS,
            excluded,
            "default-full must exclude exactly the runtime-core skill set",
        )

    def test_all_profile_groups_reference_known_groups(self) -> None:
        known_groups = set(self.groups_doc["groups"].keys())
        for profile_name, profile in self.profiles_doc["profiles"].items():
            for group in profile.get("groups", []):
                self.assertIn(
                    group,
                    known_groups,
                    f"Profile {profile_name!r} references unknown group {group!r}",
                )

    def test_each_profile_has_required_fields(self) -> None:
        required_fields = {"groups", "skills", "include_all_bundled", "exclude_skills"}
        for profile_name, profile in self.profiles_doc["profiles"].items():
            for field in required_fields:
                self.assertIn(
                    field,
                    profile,
                    f"Profile {profile_name!r} missing required field {field!r}",
                )

    def test_profile_skills_are_lists(self) -> None:
        for profile_name, profile in self.profiles_doc["profiles"].items():
            self.assertIsInstance(
                profile.get("skills"),
                list,
                f"Profile {profile_name!r} 'skills' must be a list",
            )

    def test_profile_exclude_skills_do_not_overlap_group_skills(self) -> None:
        # Excluded skills should be runtime-core, not catalog skills.
        # Catalog-group skills should not be in the exclude list.
        for profile_name, profile in self.profiles_doc["profiles"].items():
            excluded = set(profile.get("exclude_skills", []))
            for group_name in profile.get("groups", []):
                group_skills = set(
                    self.groups_doc["groups"].get(group_name, {}).get("skills", [])
                )
                overlap = excluded & group_skills
                self.assertEqual(
                    set(),
                    overlap,
                    f"Profile {profile_name!r} excludes skills that are also in group "
                    f"{group_name!r}: {overlap}",
                )


class RuntimePackagingCatalogSplitTests(unittest.TestCase):
    """Tests for the runtime-core-packaging.json changes that delegate catalog
    installation to the separate skill-catalog-packaging.json manifest."""

    def setUp(self) -> None:
        self.runtime_pkg = load_json(RUNTIME_PACKAGING)
        self.minimal = load_json(MINIMAL_MANIFEST)
        self.full = load_json(FULL_MANIFEST)
        self.catalog_pkg = load_json(CATALOG_PACKAGING)

    def test_runtime_packaging_declares_catalog_packaging_manifest(self) -> None:
        self.assertIn("catalog_packaging_manifest", self.runtime_pkg)
        self.assertEqual(
            "config/skill-catalog-packaging.json",
            self.runtime_pkg["catalog_packaging_manifest"],
        )

    def test_runtime_packaging_catalog_manifest_path_exists(self) -> None:
        manifest_path = REPO_ROOT / self.runtime_pkg["catalog_packaging_manifest"]
        self.assertTrue(
            manifest_path.exists(),
            "catalog_packaging_manifest path referenced in runtime-core-packaging.json must exist",
        )

    def test_runtime_packaging_copy_directories_does_not_include_bundled_skills(self) -> None:
        copy_dirs = self.runtime_pkg.get("copy_directories", [])
        sources = [d.get("source", "") for d in copy_dirs]
        self.assertNotIn(
            "bundled/skills",
            sources,
            "bundled/skills must not be listed in runtime-core-packaging.json copy_directories",
        )

    def test_minimal_manifest_has_runtime_profile_field(self) -> None:
        self.assertIn("runtime_profile", self.minimal)
        self.assertEqual("core-default", self.minimal["runtime_profile"])

    def test_minimal_manifest_has_catalog_profile_field(self) -> None:
        self.assertIn("catalog_profile", self.minimal)
        self.assertEqual("foundation-workflow", self.minimal["catalog_profile"])

    def test_full_manifest_has_runtime_profile_field(self) -> None:
        self.assertIn("runtime_profile", self.full)
        self.assertEqual("core-default", self.full["runtime_profile"])

    def test_full_manifest_has_catalog_profile_field(self) -> None:
        self.assertIn("catalog_profile", self.full)
        self.assertEqual("default-full", self.full["catalog_profile"])

    def test_minimal_manifest_has_empty_skills_allowlist(self) -> None:
        self.assertIn("skills_allowlist", self.minimal)
        self.assertEqual(
            [],
            self.minimal["skills_allowlist"],
            "minimal manifest skills_allowlist must be empty; catalog selection is now "
            "delegated to the catalog profile",
        )

    def test_minimal_manifest_copy_bundled_skills_is_false(self) -> None:
        self.assertFalse(
            self.minimal.get("copy_bundled_skills"),
            "minimal manifest must have copy_bundled_skills=false",
        )

    def test_full_manifest_copy_bundled_skills_is_false(self) -> None:
        self.assertFalse(
            self.full.get("copy_bundled_skills"),
            "full manifest must have copy_bundled_skills=false",
        )

    def test_minimal_manifest_copy_directories_does_not_include_bundled_skills(self) -> None:
        copy_dirs = self.minimal.get("copy_directories", [])
        sources = [d.get("source", "") for d in copy_dirs]
        self.assertNotIn(
            "bundled/skills",
            sources,
            "bundled/skills must not be in minimal manifest copy_directories",
        )

    def test_full_manifest_copy_directories_does_not_include_bundled_skills(self) -> None:
        copy_dirs = self.full.get("copy_directories", [])
        sources = [d.get("source", "") for d in copy_dirs]
        self.assertNotIn(
            "bundled/skills",
            sources,
            "bundled/skills must not be in full manifest copy_directories",
        )

    def test_minimal_catalog_profile_is_known_profile(self) -> None:
        catalog_profiles_doc = load_json(CATALOG_PROFILES)
        catalog_profile = self.minimal["catalog_profile"]
        self.assertIn(
            catalog_profile,
            catalog_profiles_doc["profiles"],
            f"minimal catalog_profile {catalog_profile!r} must exist in skill-catalog-profiles.json",
        )

    def test_full_catalog_profile_is_known_profile(self) -> None:
        catalog_profiles_doc = load_json(CATALOG_PROFILES)
        catalog_profile = self.full["catalog_profile"]
        self.assertIn(
            catalog_profile,
            catalog_profiles_doc["profiles"],
            f"full catalog_profile {catalog_profile!r} must exist in skill-catalog-profiles.json",
        )

    def test_minimal_and_full_share_same_runtime_profile(self) -> None:
        self.assertEqual(
            self.minimal["runtime_profile"],
            self.full["runtime_profile"],
            "Both minimal and full packaging manifests must declare the same runtime_profile",
        )

    def test_minimal_and_full_use_distinct_catalog_profiles(self) -> None:
        self.assertNotEqual(
            self.minimal["catalog_profile"],
            self.full["catalog_profile"],
            "Minimal and full packaging manifests must reference different catalog profiles",
        )

    def test_runtime_packaging_profile_manifests_still_declared(self) -> None:
        profile_manifests = self.runtime_pkg.get("profile_manifests", {})
        self.assertIn("minimal", profile_manifests)
        self.assertIn("full", profile_manifests)

    def test_minimal_and_full_package_ids_are_distinct(self) -> None:
        self.assertNotEqual(
            self.minimal["package_id"],
            self.full["package_id"],
        )

    def test_minimal_manifest_profile_field_is_minimal(self) -> None:
        self.assertEqual("minimal", self.minimal["profile"])

    def test_full_manifest_profile_field_is_full(self) -> None:
        self.assertEqual("full", self.full["profile"])


if __name__ == "__main__":
    unittest.main()