#!/usr/bin/env python3
"""Compare pinned upstream instruction text without running upstream code."""

import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "methodology" / "upstream-lock.json"
MAPPING = ROOT / "methodology" / "upstream-map.json"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, stdout=subprocess.PIPE).stdout


def instruction_path(path):
    parts = Path(path).parts
    if any(p in {"test", "tests", "fixtures", "node_modules", ".git", ".github"} for p in parts):
        return False
    return path in {"VERSION", "LICENSE"} or path.endswith((".md", ".md.tmpl", ".txt"))


def inventory(repo):
    commit = git(repo, "rev-parse", "HEAD").decode().strip()
    entries = {}
    for row in git(repo, "ls-tree", "-rz", "--full-tree", commit).split(b"\0"):
        if not row:
            continue
        metadata, raw_path = row.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        path = raw_path.decode()
        if not instruction_path(path):
            continue
        if kind != "blob" or mode not in {"100644", "100755"}:
            raise ValueError(f"Unsupported instruction entry: {path}")
        entries[path] = oid
    version = git(repo, "show", f"{commit}:VERSION").decode().strip()
    return {"schema": 1, "commit": commit, "version": version, "files": entries}


def compare(baseline, current, mapping, catalog):
    targets = {src: s["id"] for s in catalog["skills"] for src in s["sources"]}
    excluded = {s["id"]: s["reason"] for s in catalog["excluded"]}
    changes = []
    for path in sorted(baseline["files"].keys() | current["files"].keys()):
        before, after = baseline["files"].get(path), current["files"].get(path)
        if before == after:
            continue
        legacy = mapping.get(path)
        if legacy is None:
            owners = [(str(Path(p).parent), source) for p, source in mapping.items() if Path(p).parent != Path('.')]
            matches = [(prefix, source) for prefix, source in owners if path.startswith(prefix + '/')]
            if matches:
                legacy = max(matches, key=lambda pair: len(pair[0]))[1]
        changes.append({"path": path, "status": "added" if before is None else "removed" if after is None else "changed", "before": before, "after": after, "legacy_id": legacy, "method": targets.get(legacy), "prior_exclusion": excluded.get(legacy), "decision": "pending"})
    return {"from_commit": baseline["commit"], "to_commit": current["commit"], "upstream_version": current["version"], "changes": changes}


def validate_decisions(report, decisions, catalog):
    if (decisions.get("from_commit"), decisions.get("to_commit")) != (report["from_commit"], report["to_commit"]):
        raise ValueError("Decision report does not match the current comparison")
    rows = decisions.get("changes", [])
    by_path = {row["path"]: row for row in rows}
    if len(by_path) != len(rows) or set(by_path) != {c["path"] for c in report["changes"]}:
        raise ValueError("Every changed path needs exactly one decision")
    valid = {s["id"] for s in catalog["skills"]}
    for change in report["changes"]:
        row = by_path[change["path"]]
        if any(row.get(k) != change[k] for k in ("status", "before", "after")):
            raise ValueError("Decision evidence changed; compare again")
        if row.get("decision") not in {"adapt", "already-covered", "exclude"} or not row.get("reason", "").strip():
            raise ValueError("Decisions require a disposition and rationale")
        if row["decision"] != "exclude" and row.get("method") not in valid:
            raise ValueError("Adapted or covered changes require a valid method")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkout", type=Path, help="Local upstream checkout; committed text only")
    parser.add_argument("--accept", type=Path, help="Reviewed comparison JSON with decisions; advance baseline only")
    args = parser.parse_args()
    baseline = json.loads(LOCK.read_text())
    current = inventory(args.checkout)
    mapping = json.loads(MAPPING.read_text())
    catalog = json.loads((ROOT / "methodology" / "skill-catalog.json").read_text())
    report = compare(baseline, current, mapping, catalog)
    if args.accept:
        decisions = json.loads(args.accept.read_text())
        validate_decisions(report, decisions, catalog)
        # Preserve the rationale beside the exact baseline, never overwrite skills.
        current["review"] = decisions
        LOCK.write_text(json.dumps(current, indent=2) + "\n")
        print(f"Baseline advanced to {current['commit']}; curated skills were not modified")
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
