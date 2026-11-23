"""Deterministic tests for scripts/validate_plugin.py using temporary fixture repositories."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

import validate_plugin  # noqa: E402

VALID_README = " ".join(["word"] * 50)


def build_fixture(root: Path, skill_name: str = "sample-skill", description: str = "Use when testing.") -> None:
    """Write a minimal valid plugin repository under root."""
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({
        "name": "sample",
        "version": "1.0.0",
        "description": "Sample plugin",
        "author": {"name": "Tester"},
        "license": "MIT",
        "repository": "https://example.com/repo",
        "homepage": "https://example.com/repo",
    }), encoding="utf-8")
    skill_directory = root / "skills" / "sample-skill"
    skill_directory.mkdir(parents=True)
    (skill_directory / "SKILL.md").write_text(
        f"---\nname: {skill_name}\ndescription: \"{description}\"\nmetadata:\n  version: \"1\"\n---\n# Body\n",
        encoding="utf-8",
    )
    (root / "README.md").write_text(VALID_README, encoding="utf-8")
    (root / "LICENSE").write_text("MIT", encoding="utf-8")


class ValidatePluginTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    # Happy path
    def test_repository_itself_passes(self) -> None:
        report = validate_plugin.validate(REPOSITORY_ROOT)
        self.assertEqual(report.errors, [])

    def test_minimal_fixture_passes(self) -> None:
        build_fixture(self.root)
        self.assertTrue(validate_plugin.validate(self.root).passed)

    # Boundary conditions
    def test_description_at_limit_passes_and_over_limit_fails(self) -> None:
        build_fixture(self.root, description="a" * 1024)
        self.assertTrue(validate_plugin.validate(self.root).passed)
        shutil.rmtree(self.root)
        build_fixture(self.root, description="a" * 1025)
        self.assertFalse(validate_plugin.validate(self.root).passed)

    def test_readme_word_count_ignores_code_blocks(self) -> None:
        build_fixture(self.root)
        code_only = "short intro\n```\n" + VALID_README + "\n```\n"
        (self.root / "README.md").write_text(code_only, encoding="utf-8")
        report = validate_plugin.validate(self.root)
        self.assertTrue(any("README.md" in error for error in report.errors))

    def test_frontmatter_skips_nested_keys(self) -> None:
        parsed = validate_plugin.parse_frontmatter("---\nname: x\nmetadata:\n  name: y\n---\n")
        self.assertEqual(parsed, {"name": "x", "metadata": ""})

    # Failure cases
    def test_skill_name_must_match_directory(self) -> None:
        build_fixture(self.root, skill_name="other-name")
        report = validate_plugin.validate(self.root)
        self.assertTrue(any("must match directory" in error for error in report.errors))

    def test_uppercase_skill_name_fails(self) -> None:
        build_fixture(self.root, skill_name="Sample-Skill")
        self.assertFalse(validate_plugin.validate(self.root).passed)

    def test_unterminated_frontmatter_fails(self) -> None:
        self.assertIsNone(validate_plugin.parse_frontmatter("---\nname: x\n"))

    def test_junk_file_fails(self) -> None:
        build_fixture(self.root)
        (self.root / ".DS_Store").write_bytes(b"")
        self.assertFalse(validate_plugin.validate(self.root).passed)

    def test_hardcoded_secret_fails(self) -> None:
        build_fixture(self.root)
        (self.root / "notes.txt").write_text("key=sk-ant-" + "x" * 30, encoding="utf-8")
        report = validate_plugin.validate(self.root)
        self.assertTrue(any("secret" in error for error in report.errors))

    def test_missing_license_and_invalid_manifest_fail(self) -> None:
        build_fixture(self.root)
        (self.root / "LICENSE").unlink()
        (self.root / ".claude-plugin" / "plugin.json").write_text("{bad json", encoding="utf-8")
        report = validate_plugin.validate(self.root)
        self.assertTrue(any("LICENSE" in error for error in report.errors))
        self.assertTrue(any("invalid JSON" in error for error in report.errors))

    def test_marketplace_must_list_plugin(self) -> None:
        build_fixture(self.root)
        (self.root / ".claude-plugin" / "marketplace.json").write_text(
            json.dumps({"name": "m", "owner": {"name": "o"}, "plugins": [{"name": "other"}]}), encoding="utf-8"
        )
        report = validate_plugin.validate(self.root)
        self.assertTrue(any("not listed" in error for error in report.errors))


if __name__ == "__main__":
    unittest.main()
