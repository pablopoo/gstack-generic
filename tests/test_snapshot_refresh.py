import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "refresh_snapshot.py"


def load_module():
    spec = importlib.util.spec_from_file_location("refresh_snapshot", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(repo, *args, input=None):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        input=input,
        stdout=subprocess.PIPE,
    ).stdout


def commit(repo, files):
    for name, content in files.items():
        target = repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    git(repo, "add", ".")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "snapshot")
    return git(repo, "rev-parse", "HEAD").decode().strip()


class SnapshotRefreshTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.upstream = self.root / "upstream"
        self.snapshot = self.root / "snapshot"
        self.upstream.mkdir()
        self.snapshot.mkdir()
        git(self.upstream, "init", "-b", "main")
        (self.snapshot / "gstack-skills").mkdir()
        (self.snapshot / "gstack-skills" / "MANIFEST.txt").write_text("gstack-skills/alpha/SKILL.md\n")
        (self.snapshot / "gstack-skills" / "LICENSE").write_bytes(b"old license\n")
        (self.snapshot / "gstack-skills" / "README.md").write_text("snapshot metadata\n")
        self.module = load_module()

    def tearDown(self):
        self.tempdir.cleanup()

    def refresh(self, commit_id, additions=(), check=False):
        return self.module.refresh(self.snapshot, self.upstream, commit_id, additions, check)

    def test_uses_pinned_commit_not_dirty_or_untracked_upstream_files(self):
        commit_id = commit(self.upstream, {"alpha/SKILL.md": b"committed\n", "LICENSE": b"license\n"})
        (self.upstream / "alpha" / "SKILL.md").write_bytes(b"dirty\n")
        (self.upstream / "untracked" / "SKILL.md").parent.mkdir()
        (self.upstream / "untracked" / "SKILL.md").write_bytes(b"untracked\n")

        self.refresh(commit_id)

        self.assertEqual(b"committed\n", (self.snapshot / "gstack-skills/alpha/SKILL.md").read_bytes())
        self.assertEqual(b"license\n", (self.snapshot / "gstack-skills/LICENSE").read_bytes())
        self.assertFalse((self.snapshot / "gstack-skills/untracked/SKILL.md").exists())
        self.assertEqual("snapshot metadata\n", (self.snapshot / "gstack-skills/README.md").read_text())

    def test_uncleared_sources_cannot_be_restored_by_add_or_manifest(self):
        commit_id = commit(self.upstream, {"alpha/SKILL.md": b"alpha\n", "LICENSE": b"license\n"})
        manifest = self.snapshot / "gstack-skills/MANIFEST.txt"
        original = manifest.read_text()
        for name in self.module.NON_MIRRORED_PATHS:
            for through_manifest in (False, True):
                with self.subTest(path=name, through_manifest=through_manifest):
                    manifest.write_text(original + (f"gstack-skills/{name}\n" if through_manifest else ""))
                    with self.assertRaisesRegex(ValueError, "Not cleared for text redistribution"):
                        self.refresh(commit_id, additions=() if through_manifest else (name,))
                    self.assertEqual(b"old license\n", (self.snapshot / "gstack-skills/LICENSE").read_bytes())
        manifest.write_text(original)

    def test_additions_require_explicit_canonical_paths_and_update_manifest(self):
        commit_id = commit(
            self.upstream,
            {"alpha/SKILL.md": b"alpha\n", "test-audit/SKILL.md": b"audit\n", "LICENSE": b"license\n"},
        )

        self.refresh(commit_id)
        self.assertFalse((self.snapshot / "gstack-skills/test-audit/SKILL.md").exists())
        self.refresh(commit_id, additions=("test-audit/SKILL.md",))

        self.assertEqual(
            "gstack-skills/alpha/SKILL.md\ngstack-skills/test-audit/SKILL.md\n",
            (self.snapshot / "gstack-skills/MANIFEST.txt").read_text(),
        )
        self.refresh(commit_id, check=True)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.refresh(commit_id, additions=("test-audit/SKILL.md",))

    def test_missing_source_preflight_leaves_snapshot_unchanged(self):
        commit_id = commit(self.upstream, {"alpha/SKILL.md": b"new\n", "LICENSE": b"license\n"})
        before = {path.relative_to(self.snapshot): path.read_bytes() for path in self.snapshot.rglob("*") if path.is_file()}

        with self.assertRaisesRegex(ValueError, "Missing upstream source"):
            self.refresh(commit_id, additions=("deslop-shared-libs/SKILL.md",))

        after = {path.relative_to(self.snapshot): path.read_bytes() for path in self.snapshot.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_rejects_non_directory_parent_before_any_writes(self):
        commit_id = commit(
            self.upstream,
            {"alpha/SKILL.md": b"alpha\n", "beta/SKILL.md": b"beta\n", "LICENSE": b"license\n"},
        )
        (self.snapshot / "gstack-skills/beta").write_bytes(b"not a directory\n")
        before = {path.relative_to(self.snapshot): path.read_bytes() for path in self.snapshot.rglob("*") if path.is_file()}

        with self.assertRaisesRegex(ValueError, "not a directory"):
            self.refresh(commit_id, additions=("beta/SKILL.md",))

        after = {path.relative_to(self.snapshot): path.read_bytes() for path in self.snapshot.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_rejects_nonregular_license_before_any_writes(self):
        commit_id = commit(self.upstream, {"alpha/SKILL.md": b"alpha\n", "LICENSE": b"license\n"})
        (self.snapshot / "gstack-skills/LICENSE").unlink()
        (self.snapshot / "gstack-skills/LICENSE").mkdir()
        before = {path.relative_to(self.snapshot): path.read_bytes() for path in self.snapshot.rglob("*") if path.is_file()}

        with self.assertRaisesRegex(ValueError, "regular file"):
            self.refresh(commit_id)

        after = {path.relative_to(self.snapshot): path.read_bytes() for path in self.snapshot.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_rejects_local_symlink_before_any_writes(self):
        commit_id = commit(self.upstream, {"alpha/SKILL.md": b"alpha\n", "LICENSE": b"license\n"})
        license_path = self.snapshot / "gstack-skills/LICENSE"
        license_path.unlink()
        license_path.symlink_to(self.root / "outside")

        with self.assertRaisesRegex(ValueError, "symlink"):
            self.refresh(commit_id)

        self.assertTrue(license_path.is_symlink())
        self.assertFalse((self.snapshot / "gstack-skills/alpha/SKILL.md").exists())

    def test_rejects_traversal_and_symlink_objects(self):
        commit_id = commit(self.upstream, {"alpha/SKILL.md": b"alpha\n", "LICENSE": b"license\n"})
        with self.assertRaisesRegex(ValueError, "canonical"):
            self.refresh(commit_id, additions=("../alpha/SKILL.md",))

        git(self.upstream, "update-index", "--add", "--cacheinfo", "120000," + git(self.upstream, "hash-object", "-w", "--stdin", input=b"target").decode().strip() + ",linked/SKILL.md")
        git(self.upstream, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "symlink")
        symlink_commit = git(self.upstream, "rev-parse", "HEAD").decode().strip()
        with self.assertRaisesRegex(ValueError, "Unsupported upstream object"):
            self.refresh(symlink_commit, additions=("linked/SKILL.md",))

    def test_check_reports_stale_snapshot_without_writing(self):
        commit_id = commit(
            self.upstream,
            {"alpha/SKILL.md": b"expected\n", "test-audit/SKILL.md": b"audit\n", "LICENSE": b"license\n"},
        )
        before = (self.snapshot / "gstack-skills/MANIFEST.txt").read_bytes()

        with self.assertRaisesRegex(ValueError, "test-audit/SKILL.md"):
            self.refresh(commit_id, additions=("test-audit/SKILL.md",), check=True)

        self.assertEqual(before, (self.snapshot / "gstack-skills/MANIFEST.txt").read_bytes())

    def test_ancillary_notices_use_exact_pinned_inventory_and_bytes(self):
        ancillary = {
            "NOTICE.md": b"Pinned notice\r\nCopyright \xc2\xa9\n",
            "licenses/MIT.txt": b"MIT license\r\n",
            "licenses/vendor/NOTICE": b"Vendor notice without final newline",
        }
        pinned = commit(self.upstream, {
            "alpha/SKILL.md": b"alpha\n", "LICENSE": b"license\n", **ancillary,
        })
        commit(self.upstream, {"NOTICE.md": b"later notice\n", "licenses/later.txt": b"later\n"})
        (self.upstream / "licenses/MIT.txt").write_bytes(b"dirty\n")
        (self.upstream / "licenses/untracked.txt").write_bytes(b"untracked\n")
        local_notice = self.snapshot / "gstack-skills/licenses/local.txt"
        local_notice.parent.mkdir()
        local_notice.write_bytes(b"preserve local notice\n")

        self.refresh(pinned)

        for name, contents in ancillary.items():
            with self.subTest(path=name):
                self.assertEqual(contents, (self.snapshot / "gstack-skills" / name).read_bytes())
        self.assertFalse((local_notice.parent / "later.txt").exists())
        self.assertFalse((local_notice.parent / "untracked.txt").exists())
        self.assertEqual(b"preserve local notice\n", local_notice.read_bytes())
        self.assertEqual("snapshot metadata\n", (self.snapshot / "gstack-skills/README.md").read_text())
        self.refresh(pinned, check=True)

    def test_check_detects_changed_or_missing_ancillary_notices_without_writes(self):
        ancillary = {"NOTICE.md": b"notice\n", "licenses/MIT.txt": b"license\n"}
        pinned = commit(self.upstream, {
            "alpha/SKILL.md": b"alpha\n", "LICENSE": b"license\n", **ancillary,
        })
        self.refresh(pinned)
        for name, contents in ancillary.items():
            for missing in (False, True):
                with self.subTest(path=name, missing=missing):
                    target = self.snapshot / "gstack-skills" / name
                    if missing:
                        target.unlink()
                    else:
                        target.write_bytes(b"stale\n")
                    with self.assertRaisesRegex(ValueError, name):
                        self.refresh(pinned, check=True)
                    self.assertEqual(None if missing else b"stale\n",
                                     target.read_bytes() if target.exists() else None)
                    target.write_bytes(contents)

    def test_unsafe_ancillary_destinations_fail_preflight_before_any_writes(self):
        pinned = commit(self.upstream, {
            "alpha/SKILL.md": b"alpha\n", "LICENSE": b"new license\n",
            "NOTICE.md": b"notice\n", "licenses/MIT.txt": b"MIT\n",
            "licenses/vendor/NOTICE": b"vendor\n",
        })
        outside = self.root / "outside"
        outside.write_bytes(b"untouched\n")
        for name, kind in (("NOTICE.md", "symlink"), ("NOTICE.md", "directory"),
                           ("licenses", "symlink"), ("licenses", "file"),
                           ("licenses/MIT.txt", "symlink"), ("licenses/MIT.txt", "directory"),
                           ("licenses/vendor", "symlink"), ("licenses/vendor", "file")):
            with self.subTest(path=name, kind=kind):
                target = self.snapshot / "gstack-skills" / name
                target.parent.mkdir(parents=True, exist_ok=True)
                if kind == "symlink":
                    target.symlink_to(outside)
                elif kind == "directory":
                    target.mkdir()
                else:
                    target.write_bytes(b"not a directory\n")
                try:
                    with self.assertRaisesRegex(ValueError, "Snapshot (destination|parent)"):
                        self.refresh(pinned)
                    self.assertEqual(b"old license\n", (self.snapshot / "gstack-skills/LICENSE").read_bytes())
                    self.assertFalse((self.snapshot / "gstack-skills/alpha/SKILL.md").exists())
                    self.assertEqual("gstack-skills/alpha/SKILL.md\n",
                                     (self.snapshot / "gstack-skills/MANIFEST.txt").read_text())
                    self.assertEqual(b"untouched\n", outside.read_bytes())
                finally:
                    if target.is_dir() and not target.is_symlink():
                        target.rmdir()
                    else:
                        target.unlink()
                    licenses = self.snapshot / "gstack-skills/licenses"
                    if licenses.exists():
                        shutil.rmtree(licenses)

    def test_ancillary_source_symlinks_and_nonregular_objects_are_rejected(self):
        base = commit(self.upstream, {"alpha/SKILL.md": b"alpha\n", "LICENSE": b"license\n"})
        for name, mode in (("NOTICE.md", "120000"), ("licenses", "120000"),
                           ("licenses/vendor/NOTICE", "120000"), ("NOTICE.md/child", "100644"),
                           ("NOTICE.md", "160000"), ("licenses/vendor", "160000")):
            with self.subTest(path=name, mode=mode):
                git(self.upstream, "read-tree", base)
                object_id = (base if mode == "160000" else
                             git(self.upstream, "hash-object", "-w", "--stdin", input=b"target").decode().strip())
                git(self.upstream, "update-index", "--add", "--cacheinfo", f"{mode},{object_id},{name}")
                tree = git(self.upstream, "write-tree").decode().strip()
                pinned = git(self.upstream, "-c", "user.name=Test", "-c", "user.email=test@example.com",
                             "commit-tree", tree, "-p", base, input=b"unsafe notice\n").decode().strip()
                with self.assertRaisesRegex(ValueError, "Unsupported upstream object"):
                    self.refresh(pinned)
                self.assertEqual(b"old license\n", (self.snapshot / "gstack-skills/LICENSE").read_bytes())
                self.assertFalse((self.snapshot / "gstack-skills/alpha/SKILL.md").exists())

    def test_nontext_ancillary_sources_fail_before_writes(self):
        for name, contents in (("NOTICE.md", b"invalid \xff"),
                               ("licenses/binary", b"contains\0NUL")):
            with self.subTest(path=name):
                pinned = commit(self.upstream, {
                    "alpha/SKILL.md": b"alpha\n", "LICENSE": b"license\n", name: contents,
                })
                with self.assertRaisesRegex(ValueError, "not (UTF-8 )?text"):
                    self.refresh(pinned)
                self.assertEqual(b"old license\n", (self.snapshot / "gstack-skills/LICENSE").read_bytes())
                self.assertFalse((self.snapshot / "gstack-skills/alpha/SKILL.md").exists())
                (self.upstream / name).unlink()

    def test_absent_optional_notices_preserve_existing_local_notices(self):
        pinned = commit(self.upstream, {"alpha/SKILL.md": b"alpha\n", "LICENSE": b"license\n"})
        for name in ("NOTICE.md", "licenses/local.txt"):
            target = self.snapshot / "gstack-skills" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"local notice\n")
        self.refresh(pinned)
        self.refresh(pinned, check=True)
        for name in ("NOTICE.md", "licenses/local.txt"):
            self.assertEqual(b"local notice\n", (self.snapshot / "gstack-skills" / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
