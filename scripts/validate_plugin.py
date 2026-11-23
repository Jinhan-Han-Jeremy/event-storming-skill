"""Structure validator for the event-storming Claude plugin.

Checks the repository against the Claude plugin directory submission rules and the
Agent Skills SKILL.md specification so problems are caught before portal review.
Standard library only: no dependencies to install.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$")
SKILL_NAME_MAX_LENGTH = 64
SKILL_DESCRIPTION_MAX_LENGTH = 1024
README_MINIMUM_WORDS = 40
JUNK_FILE_NAMES = frozenset({".DS_Store", "Thumbs.db", "desktop.ini"})
JUNK_DIRECTORY_NAMES = frozenset({"__MACOSX"})
IGNORED_DIRECTORY_NAMES = frozenset({".git", "__pycache__", ".venv", "graphify-out"})
SECRET_PATTERNS = (
    re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"),
)


@dataclass
class ValidationReport:
    """Collects validation errors; an empty error list means the plugin passes."""

    errors: list[str] = field(default_factory=list)

    def add(self, message: str) -> None:
        # State mutation: appends one error to the report.
        self.errors.append(message)

    @property
    def passed(self) -> bool:
        return not self.errors


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse top-level scalar keys of a YAML frontmatter block; return None if absent."""
    lines = text.replace("\r\n", "\n").split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, str] = {}
    # Walk lines until the closing fence; nested (indented) keys such as metadata.* are skipped.
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        # Data transformation: strip surrounding quotes from scalar values.
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return None


def load_json(path: Path, report: ValidationReport) -> dict | None:
    """Read and decode a JSON file, recording a report error on failure."""
    try:
        # Data I/O: read the manifest from disk.
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.add(f"{path.as_posix()}: file is missing")
    except json.JSONDecodeError as error:
        report.add(f"{path.as_posix()}: invalid JSON ({error.msg} at line {error.lineno})")
    return None


def validate_plugin_manifest(root: Path, report: ValidationReport) -> dict | None:
    """Validate .claude-plugin/plugin.json and return it for cross-checks."""
    manifest = load_json(root / ".claude-plugin" / "plugin.json", report)
    if manifest is None:
        return None
    name = manifest.get("name", "")
    if not SKILL_NAME_PATTERN.match(str(name)):
        report.add("plugin.json: 'name' must be kebab-case")
    if not SEMVER_PATTERN.match(str(manifest.get("version", ""))):
        report.add("plugin.json: 'version' must be semantic (e.g. 1.0.0)")
    # Filter: each publication field must be present and non-empty.
    for required_key in ("description", "author", "license", "repository", "homepage"):
        if not manifest.get(required_key):
            report.add(f"plugin.json: '{required_key}' is required for directory listing")
    author = manifest.get("author")
    if isinstance(author, dict) and not author.get("name"):
        report.add("plugin.json: 'author.name' is required")
    return manifest


def validate_marketplace_manifest(root: Path, plugin_name: str | None, report: ValidationReport) -> None:
    """Validate the optional marketplace.json and ensure it lists this plugin."""
    path = root / ".claude-plugin" / "marketplace.json"
    if not path.exists():
        return
    marketplace = load_json(path, report)
    if marketplace is None:
        return
    if not marketplace.get("name") or not isinstance(marketplace.get("owner"), dict):
        report.add("marketplace.json: 'name' and 'owner' are required")
    listed_names = {entry.get("name") for entry in marketplace.get("plugins", [])}
    if plugin_name and plugin_name not in listed_names:
        report.add(f"marketplace.json: plugin '{plugin_name}' is not listed")


def validate_skill(skill_directory: Path, report: ValidationReport) -> None:
    """Validate one skills/<name>/SKILL.md against the Agent Skills specification."""
    skill_file = skill_directory / "SKILL.md"
    label = skill_file.relative_to(skill_directory.parent.parent).as_posix()
    if not skill_file.is_file():
        report.add(f"{label}: SKILL.md is missing")
        return
    frontmatter = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
    if frontmatter is None:
        report.add(f"{label}: YAML frontmatter is missing or unterminated")
        return
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    # Branching: each rule from the spec is reported independently so all problems surface at once.
    if name != skill_directory.name:
        report.add(f"{label}: 'name' ({name!r}) must match directory name ({skill_directory.name!r})")
    if not SKILL_NAME_PATTERN.match(name) or len(name) > SKILL_NAME_MAX_LENGTH:
        report.add(f"{label}: 'name' must be lowercase kebab-case, max {SKILL_NAME_MAX_LENGTH} chars")
    if not description:
        report.add(f"{label}: 'description' is required")
    elif len(description) > SKILL_DESCRIPTION_MAX_LENGTH:
        report.add(f"{label}: 'description' exceeds {SKILL_DESCRIPTION_MAX_LENGTH} chars")


def count_prose_words(markdown: str) -> int:
    """Count README words outside fenced code blocks."""
    # Data filter: drop fenced code blocks, which the directory excludes from the word count.
    prose = re.sub(r"```.*?```", " ", markdown, flags=re.DOTALL)
    return len(prose.split())


def validate_repository_files(root: Path, report: ValidationReport) -> None:
    """Check README, LICENSE, junk files, and hardcoded secrets across the repository."""
    readme = root / "README.md"
    if not readme.is_file():
        report.add("README.md is missing")
    elif count_prose_words(readme.read_text(encoding="utf-8")) < README_MINIMUM_WORDS:
        report.add(f"README.md must contain at least {README_MINIMUM_WORDS} words of prose")
    if not (root / "LICENSE").is_file():
        report.add("LICENSE is missing")
    # Loop: scan every tracked-looking file once for junk names and secret patterns.
    for path in root.rglob("*"):
        if IGNORED_DIRECTORY_NAMES.intersection(path.relative_to(root).parts):
            continue
        relative = path.relative_to(root).as_posix()
        if path.name in JUNK_FILE_NAMES or (path.is_dir() and path.name in JUNK_DIRECTORY_NAMES):
            report.add(f"{relative}: OS junk file must be removed")
            continue
        if path.is_file() and path.stat().st_size < 1_000_000:
            content = path.read_text(encoding="utf-8", errors="ignore")
            if any(pattern.search(content) for pattern in SECRET_PATTERNS):
                report.add(f"{relative}: looks like a hardcoded secret")


def validate(root: Path) -> ValidationReport:
    """Run every check and return the aggregated report."""
    report = ValidationReport()
    manifest = validate_plugin_manifest(root, report)
    validate_marketplace_manifest(root, manifest.get("name") if manifest else None, report)
    skills_root = root / "skills"
    skill_directories = sorted(path for path in skills_root.iterdir() if path.is_dir()) if skills_root.is_dir() else []
    if not skill_directories:
        report.add("skills/: at least one skill directory is required")
    for skill_directory in skill_directories:
        validate_skill(skill_directory, report)
    validate_repository_files(root, report)
    # Return: report with zero errors means the repository is ready to submit.
    return report


def main(argv: list[str]) -> int:
    """CLI entry point; exits 0 on success and 1 when any check fails."""
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parent.parent
    report = validate(root)
    for error in report.errors:
        print(f"ERROR {error}")
    print("PASS: plugin structure is valid" if report.passed else f"FAIL: {len(report.errors)} error(s)")
    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
