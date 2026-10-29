"""License byte identities and scope tripwires, not a legal certification."""

import hashlib
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/gstack-power-team"
SOURCE_DIGESTS = {
    "gstack-skills/LICENSE": "e56fbb5b3d95756f3fa1cfefa24732ec79f18ece1ad08a4e79e00df57e8b198c",
    "gstack-skills/NOTICE.md": "35b1b00d1421d6309ef379a4bb8b4c658783f8f19c4c5fd3f9f621b1e496daf0",
    "gstack-skills/licenses/Apache-2.0.txt": "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30",
    "gstack-skills/licenses/MIT-elaya.txt": "5f9af6ce7083838497676a8dfa651ad8e2559fdabd4586afc73587beec476b0e",
    "gstack-skills/licenses/MIT-hallmark.txt": "06088a8b94598626f27612dea42300154bf7be967c85d9d3eee4490cb056af7d",
    "gstack-skills/licenses/MIT-pstack.txt": "bc957ca6bee02792566a1a028d105e02e247c6e77cf057061674273da77b200e",
    "gstack-skills/licenses/MIT-skill-diet.txt": "2d20dfacd9742706e564470dc77438608a1e54b0ed46959f080709389209093c",
    "gstack-skills/licenses/MIT-tstack.txt": "8095f9a9f97d074131f6a2ce09b952d12c18b36f09f4e5df0517c4e64e82c851",
    "licenses/Apache-2.0-impeccable.txt": "02bb8c3b4e70190e3986c0404ad2fd8d639b4f534252d82379cc1b502b6d1812",
    "licenses/NOTICE-impeccable.md": "c60a093c2845fd9fb82f9c6f742ece31f379f8190b535309d32d66c45ccffdcb",
}


class LicenseCoverageTests(unittest.TestCase):
    def test_reviewed_primary_license_and_notice_bytes_are_preserved(self):
        for name, digest in SOURCE_DIGESTS.items():
            with self.subTest(path=name):
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)

    def test_installed_legal_copies_are_self_contained(self):
        sources = {
            "NOTICE.upstream.md": ROOT / "gstack-skills/NOTICE.md",
            "NOTICE.impeccable.md": ROOT / "licenses/NOTICE-impeccable.md",
            "licenses/Apache-2.0-impeccable.txt": ROOT / "licenses/Apache-2.0-impeccable.txt",
        }
        for path in (ROOT / "gstack-skills/licenses").glob("*.txt"):
            sources[f"licenses/{path.name}"] = path
        for target, source in sources.items():
            with self.subTest(path=target):
                self.assertEqual((PLUGIN / target).read_bytes(), source.read_bytes())
        for owner in ("Garry Tan", "Pablo Poo", "Elaya", "Nico Bailon"):
            self.assertIn(owner, (PLUGIN / "LICENSE").read_text())
        self.assertIn("Copyright 2025 Paul Bakaus", (PLUGIN / "licenses/Apache-2.0-impeccable.txt").read_text())

    def test_rewritten_files_carry_modification_notices(self):
        paths = list((PLUGIN / "skills").glob("*/SKILL.md")) + list((PLUGIN / "references").glob("*.md"))
        for path in paths:
            with self.subTest(path=path):
                self.assertIn("Modification notice: Rewritten and consolidated by Pablo Poo.", path.read_text())
                self.assertRegex(path.read_text(), r"\[NOTICE\]\([^)]*NOTICE\.md\)")
        catalog = json.loads((ROOT / "methodology/skill-catalog.json").read_text())
        self.assertIn("Rewritten and consolidated by Pablo Poo", catalog["modification_notice"])

    def test_combined_license_expression_and_no_author_contact(self):
        manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest["license"], "MIT AND Apache-2.0")
        self.assertEqual(manifest["author"], {"name": "Pablo Poo"})
        self.assertIn("Copyright (c) 2026 Pablo Poo", (ROOT / "LICENSE").read_text())

    def test_uncleared_archive_text_is_not_redistributed(self):
        manifest = (ROOT / "gstack-skills/MANIFEST.txt").read_text().splitlines()
        for name in ("design-review/SKILL.md", "plan-design-review/SKILL.md"):
            self.assertNotIn("gstack-skills/" + name, manifest)
            self.assertFalse((ROOT / "gstack-skills" / name).exists())

    def test_readme_links_instead_of_embedding_external_media(self):
        for path in (ROOT / "README.md", PLUGIN / "README.md"):
            self.assertNotRegex(path.read_text(), r"!\[[^\]]*\]\(|<img\b")

    def test_legal_document_links_resolve_inside_installable_package(self):
        for path in (PLUGIN / "NOTICE.md", PLUGIN / "README.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if re.match(r"[a-z]+://|#", target):
                    continue
                resolved = (path.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(resolved.is_relative_to(PLUGIN.resolve()))
                self.assertTrue(resolved.exists(), (path, target))


if __name__ == "__main__":
    unittest.main()
