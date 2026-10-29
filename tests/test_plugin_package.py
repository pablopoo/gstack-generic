"""Structural tripwires for the methodology-only distributable, not content review."""

import json
from pathlib import Path
import stat
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/gstack-power-team"
MANIFEST = ".codex-plugin/plugin.json"
LEGAL_FILES = {
    "NOTICE.md", "NOTICE.upstream.md", "NOTICE.impeccable.md",
    "licenses/Apache-2.0.txt", "licenses/Apache-2.0-impeccable.txt",
    "licenses/MIT-elaya.txt", "licenses/MIT-hallmark.txt",
    "licenses/MIT-pstack.txt", "licenses/MIT-skill-diet.txt",
    "licenses/MIT-tstack.txt",
}
REFERENCES = {
    "references/collaboration-roles.md",
    "references/delegation-contract.md",
    "references/method-index.md",
    "references/process-map.md",
}
MANIFEST_KEYS = {
    "name", "version", "description", "author", "license", "keywords",
    "skills", "interface",
}
INTERFACE_KEYS = {
    "displayName", "shortDescription", "longDescription", "developerName",
    "category", "capabilities", "defaultPrompt", "brandColor",
}


def expected_files(catalog):
    return {"README.md", "LICENSE", MANIFEST, *REFERENCES, *LEGAL_FILES,
            "skills/gstack-team/SKILL.md"} | {
        f"skills/gstack-{skill['id']}/SKILL.md" for skill in catalog["skills"]
    }


def validate_package(plugin, catalog):
    """Fail closed on new payload paths, special files, or metadata surfaces."""
    allowed_files = expected_files(catalog)
    allowed_dirs = {
        parent.as_posix()
        for name in allowed_files
        for parent in Path(name).parents
        if parent != Path(".")
    }
    found_files = set()

    def visit(path):
        mode = path.lstat().st_mode
        relative = path.relative_to(plugin).as_posix()
        if stat.S_ISLNK(mode):
            raise ValueError(f"Symlink is not allowed: {relative}")
        if stat.S_ISDIR(mode):
            if path != plugin and relative not in allowed_dirs:
                raise ValueError(f"Unexpected directory: {relative}")
            for child in sorted(path.iterdir()):
                visit(child)
        elif stat.S_ISREG(mode):
            if relative not in allowed_files:
                raise ValueError(f"Unexpected file: {relative}")
            if mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                raise ValueError(f"Executable file is not allowed: {relative}")
            found_files.add(relative)
        else:
            raise ValueError(f"Non-regular payload is not allowed: {relative}")

    visit(plugin)
    missing = allowed_files - found_files
    if missing:
        raise ValueError(f"Missing files: {sorted(missing)}")

    manifest = json.loads((plugin / MANIFEST).read_text())

    def check_keys(value, allowed, location):
        if not isinstance(value, dict):
            raise ValueError(f"Expected metadata object: {location}")
        unexpected = value.keys() - allowed
        if unexpected:
            raise ValueError(f"Unexpected metadata in {location}: {sorted(unexpected)}")

    check_keys(manifest, MANIFEST_KEYS, "manifest")
    check_keys(manifest.get("author", {}), {"name"}, "author")
    check_keys(manifest.get("interface", {}), INTERFACE_KEYS, "interface")
    if manifest.get("skills") != "./skills/":
        raise ValueError("Skills must refer only to ./skills/")


class PluginPackageTests(unittest.TestCase):
    def test_repository_package_is_methodology_only(self):
        catalog = json.loads((ROOT / "methodology/skill-catalog.json").read_text())
        validate_package(PLUGIN, catalog)


class PackageGuardTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.plugin = Path(temporary.name) / "plugin"
        self.catalog = {"skills": [{"id": "review"}]}
        for name in expected_files(self.catalog):
            path = self.plugin / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Methodology\n")
        self.manifest = {"name": "fixture", "skills": "./skills/"}
        self.write_manifest()

    def write_manifest(self):
        (self.plugin / MANIFEST).write_text(json.dumps(self.manifest))

    def test_valid_fixture_is_accepted(self):
        validate_package(self.plugin, self.catalog)

    def test_author_contact_metadata_is_rejected(self):
        self.manifest["author"] = {"name": "Test", "email": "test@example.com"}
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "Unexpected metadata in author"):
            validate_package(self.plugin, self.catalog)

    def test_script_hook_and_mcp_payloads_are_rejected(self):
        for name in ("run.py", "hooks/hooks.json", ".mcp.json",
                     "skills/gstack-review/run.sh", "references/extra.md"):
            with self.subTest(path=name):
                path = self.plugin / name
                parent_existed = path.parent.exists()
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("payload\n")
                try:
                    with self.assertRaisesRegex(ValueError, "Unexpected (file|directory)"):
                        validate_package(self.plugin, self.catalog)
                finally:
                    path.unlink()
                    if not parent_existed:
                        path.parent.rmdir()

    def test_unexpected_empty_directory_is_rejected(self):
        (self.plugin / "agents").mkdir()
        with self.assertRaisesRegex(ValueError, "Unexpected directory: agents"):
            validate_package(self.plugin, self.catalog)

    def test_missing_expected_file_is_rejected(self):
        (self.plugin / "skills/gstack-review/SKILL.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing files"):
            validate_package(self.plugin, self.catalog)

    def test_symlinks_are_rejected_even_at_allowed_paths(self):
        for name, target in (("README.md", "LICENSE"),
                             ("references", "skills"),
                             ("LICENSE", "missing-target")):
            with self.subTest(path=name):
                path = self.plugin / name
                backup = path.with_name(path.name + ".original")
                path.rename(backup)
                path.symlink_to(target, target_is_directory=backup.is_dir())
                try:
                    with self.assertRaisesRegex(ValueError, "Symlink"):
                        validate_package(self.plugin, self.catalog)
                finally:
                    path.unlink()
                    backup.rename(path)

    def test_package_root_symlink_is_rejected(self):
        alias = self.plugin.with_name("alias")
        alias.symlink_to(self.plugin, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Symlink"):
            validate_package(alias, self.catalog)

    def test_each_executable_permission_is_rejected(self):
        path = self.plugin / "README.md"
        original = path.stat().st_mode
        for bit in (stat.S_IXUSR, stat.S_IXGRP, stat.S_IXOTH):
            with self.subTest(bit=bit):
                path.chmod(original | bit)
                with self.assertRaisesRegex(ValueError, "Executable file"):
                    validate_package(self.plugin, self.catalog)
        path.chmod(original)

    def test_runtime_and_unknown_metadata_entries_are_rejected(self):
        for key in ("hooks", "mcp", "mcpServers", "apps", "agents", "commands",
                    "scripts", "dependencies", "futureRuntime"):
            for value in ({}, "./runtime.json"):
                with self.subTest(key=key, value=value):
                    self.manifest[key] = value
                    self.write_manifest()
                    with self.assertRaisesRegex(ValueError, "Unexpected metadata"):
                        validate_package(self.plugin, self.catalog)
                    del self.manifest[key]

    def test_nested_metadata_cannot_add_runtime_entries(self):
        for section in ("author", "interface"):
            with self.subTest(section=section):
                self.manifest[section] = {"hooks": {}}
                self.write_manifest()
                with self.assertRaisesRegex(ValueError, "Unexpected metadata"):
                    validate_package(self.plugin, self.catalog)
                del self.manifest[section]

    def test_skills_cannot_redirect_outside_the_allowed_payload(self):
        for value in ("../skills/", "./runtime/", ["./skills/"], None):
            with self.subTest(value=value):
                self.manifest["skills"] = value
                self.write_manifest()
                with self.assertRaisesRegex(ValueError, "Skills must refer only"):
                    validate_package(self.plugin, self.catalog)


if __name__ == "__main__":
    unittest.main()
