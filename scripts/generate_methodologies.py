#!/usr/bin/env python3
"""Render the curated methods; authoring metadata stays outside the plugin."""

import argparse
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "gstack-power-team"
CATALOG = ROOT / "methodology" / "skill-catalog.json"
PHASES = {"discovery", "planning", "design", "implementation", "review", "verification", "handoff", "learning"}
CAPABILITIES = {"strategic-judgment", "implementation-and-validation", "bounded-evidence-work"}
MODIFICATION_NOTICE = "Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms:"


def validate(catalog):
    if catalog.get("schema") != 3:
        raise ValueError("Expected catalog schema 3")
    ids, sources = set(), set()
    for skill in catalog["skills"]:
        sid = skill["id"]
        if not re.fullmatch(r"[a-z][a-z0-9-]*", sid) or sid in ids or sid == "team":
            raise ValueError(f"Invalid or duplicate method: {sid}")
        ids.add(sid)
        if skill["phase"] not in PHASES or skill["capability"] not in CAPABILITIES:
            raise ValueError(f"Unknown phase or capability: {sid}")
        for key in ("title", "description", "output", "boundary"):
            if not isinstance(skill[key], str) or not skill[key].strip():
                raise ValueError(f"Missing {key}: {sid}")
        for key in ("inputs", "method", "sources"):
            if not skill[key] or not all(isinstance(v, str) and v.strip() for v in skill[key]):
                raise ValueError(f"Missing {key}: {sid}")
        for source in skill["sources"]:
            if source in sources:
                raise ValueError(f"Duplicate source disposition: {source}")
            sources.add(source)
    for entry in catalog["excluded"]:
        if entry["id"] in sources or not entry["reason"]:
            raise ValueError("Invalid exclusion")
        sources.add(entry["id"])
    return sources


def render(skill):
    inputs = "\n".join(f"- {s}" for s in skill["inputs"])
    criteria = "\n".join(f"- {s}" for s in skill["method"])
    return f'''---
name: gstack-{skill['id']}
description: {json.dumps(skill['description'])}
---

# {skill['title']}

{MODIFICATION_NOTICE} [NOTICE](../../NOTICE.md).

## Inputs

{inputs}

Use available evidence; identify missing information only when it changes the decision.

## Method

{criteria}

## Result

{skill['output']}

## Scope

{skill['boundary']}

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
'''


def outputs(catalog):
    result = {}
    legal_sources = {
        "NOTICE.upstream.md": ROOT / "gstack-skills/NOTICE.md",
        "NOTICE.impeccable.md": ROOT / "licenses/NOTICE-impeccable.md",
        "licenses/Apache-2.0-impeccable.txt": ROOT / "licenses/Apache-2.0-impeccable.txt",
    }
    for name in ("Apache-2.0.txt", "MIT-elaya.txt", "MIT-hallmark.txt",
                 "MIT-pstack.txt", "MIT-skill-diet.txt", "MIT-tstack.txt"):
        legal_sources[f"licenses/{name}"] = ROOT / "gstack-skills/licenses" / name
    for name, source in legal_sources.items():
        result[PLUGIN / name] = source.read_text(encoding="utf-8")
    index = ["# Method Index", "", f"{MODIFICATION_NOTICE} [NOTICE](../NOTICE.md).", "", "Select by the decision or result needed. These names identify methods, not executable commands.", "", "| Method | Use when |", "| --- | --- |"]
    roster = ["# Collaboration Responsibilities", "", f"{MODIFICATION_NOTICE} [NOTICE](../NOTICE.md).", "", "Responsibilities suggest capabilities to look for among available collaborators. They do not require an agent team, fixed intelligence tiers, or any particular execution environment. User-configured roles take precedence.", "", "| Method | Primary capability |", "| --- | --- |"]
    migration = ["# Methodology Selection", "", f"{MODIFICATION_NOTICE} [NOTICE](../NOTICE.md).", "", "Initial reduction: gstack adaptation 0.10.0, based on upstream 1.87.4.0. Later source additions follow the reviewed upstream lock. This table is authoring provenance and is not shipped in the plugin.", "", "| Source ID | Decision | Destination or reason |", "| --- | --- | --- |"]
    for skill in sorted(catalog["skills"], key=lambda s: s["id"]):
        sid = skill["id"]
        result[PLUGIN / "skills" / f"gstack-{sid}" / "SKILL.md"] = render(skill)
        link = f"[{skill['title']}](../skills/gstack-{sid}/SKILL.md)"
        index.append(f"| {link} | {skill['description']} |")
        roster.append(f"| {link} | {skill['capability']} |")
        for source in skill["sources"]:
            migration.append(f"| {source} | Retained or consolidated | {sid} |")
    for entry in catalog["excluded"]:
        migration.append(f"| {entry['id']} | Excluded | {entry['reason']} |")
    result[PLUGIN / "references" / "method-index.md"] = "\n".join(index) + "\n"
    result[PLUGIN / "references" / "collaboration-roles.md"] = "\n".join(roster) + "\n"
    result[ROOT / "methodology" / "selection.md"] = "\n".join(migration) + "\n"
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate generated content without writing")
    args = parser.parse_args()
    catalog = json.loads(CATALOG.read_text())
    validate(catalog)
    expected = outputs(catalog)
    expected_skills = {p for p in expected if p.name == "SKILL.md"}
    actual_skills = set((PLUGIN / "skills").glob("*/SKILL.md"))
    extra = actual_skills - expected_skills - {PLUGIN / "skills" / "gstack-team" / "SKILL.md"}
    if args.check:
        stale = [str(p.relative_to(ROOT)) for p, value in expected.items() if not p.exists() or p.read_text() != value]
        if stale or extra:
            raise SystemExit(f"Stale generated files: {stale}; unexpected skills: {sorted(map(str, extra))}")
    else:
        # Never prune unknown skills: migration is an explicit reviewed edit.
        if extra:
            raise SystemExit(f"Resolve retired skills before generation: {sorted(map(str, extra))}")
        for path, value in expected.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value)
    print(f"Validated {len(catalog['skills'])} methods" + ("; generated content matches" if args.check else "; rendered content"))


if __name__ == "__main__":
    main()
