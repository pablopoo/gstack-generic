import copy
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class UpdateWorkflowTests(unittest.TestCase):
    def test_added_removed_and_excluded_sources_remain_visible(self):
        m = module("compare_upstream")
        old = {"commit": "old", "files": {"review/sections/check.md": "a", "export/SKILL.md": "b", "gone.md": "c"}}
        new = {"commit": "new", "version": "2", "files": {"review/sections/check.md": "d", "export/SKILL.md": "e", "new/SKILL.md": "f"}}
        catalog = {"skills": [{"id": "assessment", "sources": ["review"]}], "excluded": [{"id": "export", "reason": "format operation"}]}
        report = m.compare(old, new, {"review/SKILL.md": "review", "export/SKILL.md": "export"}, catalog)
        rows = {r["path"]: r for r in report["changes"]}
        self.assertEqual(rows["review/sections/check.md"]["method"], "assessment")
        self.assertEqual(rows["export/SKILL.md"]["prior_exclusion"], "format operation")
        self.assertEqual(rows["gone.md"]["status"], "removed")
        self.assertEqual(rows["new/SKILL.md"]["status"], "added")
        self.assertIsNone(rows["new/SKILL.md"]["method"])
        self.assertTrue(all(r["decision"] == "pending" for r in rows.values()))

    def test_same_baseline_has_no_changes(self):
        m = module("compare_upstream")
        state = {"commit": "same", "version": "1", "files": {"SKILL.md": "x"}}
        self.assertEqual(m.compare(state, state, {}, {"skills": [], "excluded": []})["changes"], [])

    def test_instruction_scope_includes_templates_not_fixtures(self):
        m = module("compare_upstream")
        self.assertTrue(m.instruction_path("review/sections/check.md.tmpl"))
        self.assertTrue(m.instruction_path("licenses/NOTICE.txt"))
        self.assertFalse(m.instruction_path("test/fixtures/SKILL.md"))
        self.assertFalse(m.instruction_path("bin/run.ts"))

    def test_catalog_dispositions_cover_upstream_mapping(self):
        catalog = json.loads((ROOT / "methodology/skill-catalog.json").read_text())
        mapping = json.loads((ROOT / "methodology/upstream-map.json").read_text())
        sources = module("generate_methodologies").validate(catalog)
        self.assertEqual(sources, set(mapping.values()))
        self.assertEqual(len(mapping), len(sources))

    def test_duplicate_source_rejected(self):
        catalog = json.loads((ROOT / "methodology/skill-catalog.json").read_text())
        bad = copy.deepcopy(catalog)
        bad["skills"][1]["sources"].append(bad["skills"][0]["sources"][0])
        with self.assertRaises(ValueError):
            module("generate_methodologies").validate(bad)

    def test_rendered_bundle_matches_catalog_and_has_valid_headers(self):
        generator = module("generate_methodologies")
        catalog = json.loads(generator.CATALOG.read_text())
        expected = generator.outputs(catalog)
        for path, content in expected.items():
            with self.subTest(path=path):
                self.assertEqual(path.read_text(), content)
        skills = sorted((generator.PLUGIN / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), len(catalog["skills"]) + 1)
        for path in skills:
            with self.subTest(path=path):
                header = path.read_text().split("---", 2)[1]
                self.assertIn(f"name: {path.parent.name}\n", header)
                self.assertRegex(header, r"\ndescription: \S")

    def test_methodology_links_are_self_contained(self):
        plugin = ROOT / "plugins/gstack-power-team"
        for path in list((plugin / "skills").rglob("*.md")) + list((plugin / "references").rglob("*.md")):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
                with self.subTest(path=path, target=target):
                    self.assertNotIn("://", target)
                    resolved = (path.parent / target.split("#", 1)[0]).resolve()
                    self.assertTrue(resolved.is_relative_to(plugin.resolve()))
                    self.assertTrue(resolved.is_file())

    def test_installed_methods_have_no_operational_recipes(self):
        # A tripwire for accidental raw-source imports, not a semantic neutrality proof.
        plugin = ROOT / "plugins/gstack-power-team"
        forbidden = re.compile(
            r"```|https?://|~/|\{\{[A-Z_]+|"
            r"\b(?:gpt-\S+|Claude|Codex|Bash|AskUserQuestion|Playwright|"
            r"React|Next\.js|Django|Rails|Vercel|Supabase|GitHub|Bun|npm|pip)\b",
            re.IGNORECASE,
        )
        for path in list((plugin / "skills").rglob("*.md")) + list((plugin / "references").rglob("*.md")):
            with self.subTest(path=path):
                self.assertIsNone(forbidden.search(path.read_text()))

    def decision_example(self):
        return {"from_commit": "old", "to_commit": "new", "changes": [{"path": "review/SKILL.md", "status": "changed", "before": "a", "after": "b", "decision": "adapt", "reason": "Adds required evidence", "method": "review"}]}

    def test_complete_decision_accepted(self):
        report = self.decision_example()
        module("compare_upstream").validate_decisions(report, copy.deepcopy(report), {"skills": [{"id": "review"}]})

    def test_missing_pending_or_stale_decision_rejected(self):
        m = module("compare_upstream")
        report = self.decision_example()
        for kind in ("missing", "pending", "stale", "wrong-commit", "unknown-method", "no-reason", "duplicate"):
            with self.subTest(kind=kind):
                decision = copy.deepcopy(report)
                if kind == "missing": decision["changes"] = []
                elif kind == "pending": decision["changes"][0]["decision"] = "pending"
                elif kind == "stale": decision["changes"][0]["after"] = "different"
                elif kind == "wrong-commit": decision["to_commit"] = "different"
                elif kind == "unknown-method": decision["changes"][0]["method"] = "unknown"
                elif kind == "no-reason": decision["changes"][0]["reason"] = ""
                else: decision["changes"].append(copy.deepcopy(decision["changes"][0]))
                with self.assertRaises(ValueError):
                    m.validate_decisions(report, decision, {"skills": [{"id": "review"}]})


if __name__ == "__main__":
    unittest.main()
