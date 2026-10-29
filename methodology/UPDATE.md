# Updating the Curated Methodologies

This is a maintainer workflow, outside the installed plugin. The plugin contains methods only. Upstream is evidence for improvements, not an instruction source to execute or copy into the curated skills.

## Source Of Truth

- `skill-catalog.json` defines the selected methods, their distinctive inputs, decisions, outputs, boundaries, and legacy source IDs.
- `upstream-map.json` links original upstream skill paths to those legacy IDs.
- `upstream-lock.json` pins the reviewed commit and content identities for instruction text, including supporting documents and templates.
- `selection.md` records consolidation and exclusions. It is generated from the catalog.
- The separate `gstack-skills` directory preserves literal upstream text for comparison; it is never packaged or installed.

## Compare And Classify

1. Obtain an upstream checkout and select a specific commit. Do not run its setup, helpers, hooks, or examples. The comparison reads committed objects, ignoring working-tree modifications.
2. From this repository, run `python3 scripts/compare_upstream.py /path/to/upstream`. Retain the JSON report as the review record. An unchanged baseline produces an empty change list.
3. Read relevant differences at the reported commits, including changed sections and templates. Added paths are always surfaced, even if they have no existing mapping. Shared documents may affect several methods; inspect each affected method rather than relying only on the suggested owner.
4. Give every changed path a `decision` of `adapt`, `already-covered`, or `exclude`, plus a concrete `reason`. For the first two, set `method` to a current catalog ID. A previously excluded source must still be examined when it changes. For a multi-method change, record the additional method IDs and rationale in the reason.

## Selection Rules

Retain an idea when it changes a reusable decision, evidence standard, dependency, or completion criterion. It must remain useful without a named product, command, file format, platform, model, setup procedure, or runtime integration.

Merge ideas into an existing method when they share a trigger and deliverable. Add a method only for a distinct decision or artifact that cannot be expressed clearly in the existing catalog. Exclude installation, execution recipes, cloud delivery, environment repair, provider selection, and output-format conversions. Preserve the abstract lesson when it is independently valuable.

Rephrase methods from understanding; never perform blind substitutions of tool names in upstream instructions. Keep local development scope, report-only boundaries, actual evidence, optional collaboration, and the user's available capabilities. Do not turn advisory improvements into universal blocking gates.

## Adapt And Validate

Review licensing before redistribution: read the pinned upstream LICENSE and
NOTICE and any original notices they identify, not just the root license label.
Update the root/package scope inventories, retain complete applicable texts in
the installed package, and mark modified derivative files. The generator emits
modification marks and copies the reviewed legal texts; update the explicit
source list, legal byte-identity tests and package allowlist together when scope
changes. Legal files may name sources; methodology instructions remain agnostic.
Do not restore `refresh_snapshot.NON_MIRRORED_PATHS` without resolving their text
permissions and reviewing the exclusion policy. Comparison hashes can track a
source without redistributing its prose. Verify asset permissions before adding
embedded media; use links when redistribution permission is not established.

1. Edit the catalog, preserving its source dispositions. Update the upstream path mapping for new or renamed sources; record a reason for exclusions. A deleted source does not automatically delete a useful methodology.
2. For renamed or removed curated skills, explicitly review and remove only their generated files. The generator refuses unexpected skills instead of deleting them automatically.
3. Run `python3 scripts/generate_methodologies.py`, then `python3 scripts/generate_methodologies.py --check` and `python3 -m unittest discover -s tests`.
4. Check every relative link and skill header. Read changed methods for tool assumptions, vague criteria, accidental execution authority, and duplicated triggers. Where behavior changes materially, exercise a representative scenario; structural validation does not prove agent behavior.
5. Update the plugin version and attribution. Refresh manifest-listed raw snapshot files byte-for-byte from the same pinned commit with `python3 scripts/refresh_snapshot.py /path/to/upstream --commit <full-commit>`. Explicitly approved additions use repeated `--add path/to/SKILL.md` arguments; removals require a reviewed manifest edit. The helper also refreshes LICENSE, optional NOTICE.md, and text under licenses/ from that commit. It preflights committed sources and destinations before writing, ignores dirty upstream content, and never runs upstream code. It preserves unmatched local notices rather than silently deleting them. Update snapshot metadata separately and retain applicable attribution in the installed license when adapting third-party material. Verify bytes with the same command and `--check` (omit already accepted additions). The baseline also tracks supporting text that is not copied into the snapshot.
6. Before replacing the active lock, ensure its previous accepted review is committed in repository history; if it is still uncommitted, preserve it in `updates/<previous-version>-review.json`. After adaptations and validation are complete, run `python3 scripts/compare_upstream.py /path/to/upstream --accept /path/to/reviewed-report.json`. This verifies commit identities, changed-file evidence, and complete dispositions before advancing the lock; it never edits the curated methods. The full decision record is retained in the lock and repository history or the explicit archive.
7. Review the resulting diff, install the new local plugin version, and verify installed contents match the source. Commit and push when authorized. Other machines must refresh their marketplace and installed version separately.

The comparison covers Markdown, Markdown templates, text notices, VERSION, and LICENSE. It intentionally does not interpret runtime source code; when release notes identify behavior implemented only in code, inspect that evidence explicitly and record the resulting methodological decision. No automatic comparison can decide semantic applicability.

The test suite checks generated content, headers, internal links, source dispositions, snapshot identities, legal byte identities, modification marks, and common accidental operational imports. The package guard allows only the catalog-derived skills, coordinator, four shared references, README, LICENSE, three notice documents, seven license texts, and packaging metadata; it rejects unexpected files or directories, executable files, symlinks, and runtime metadata. Deliberate packaging changes require reviewing this allowlist, not bypassing it. These structural and terminology checks are tripwires, not semantic proof; review meaning and representative behavior separately. Keep release-specific decisions and validation limits in `updates/<plugin-version>.md`; the accepted lock retains every changed-path disposition.

## Initial Reduction

The 1.0.0 baseline is upstream 1.87.4.0 at `a6b3a57512ca6d5c6aa5b68f74f736195021f96e`. The reduction preserves the preceding 0.10.0 work on review freshness, health coverage, and evidence-based risk assessment. Existing operational names and duplicate challenge variants are consolidated or excluded in `selection.md`; the coordinator remains the process entry point.
