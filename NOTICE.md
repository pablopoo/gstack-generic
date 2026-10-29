# License and Source Scope

Original adaptation contributions: Copyright (c) 2026 Pablo Poo, MIT; see
[LICENSE](LICENSE). This does not relicense third-party material. This repository
and its installable plugin are mixed-license distributions, not MIT-only works.

## Distribution Inventory

| Surface | Distributed material and applicable scope |
| --- | --- |
| `plugins/gstack-power-team/` | Rewritten methodology, shared references and metadata; MIT contributions with retained Apache-2.0-derived guidance. Package expression: `MIT AND Apache-2.0`, not a choice between licenses. Its self-contained [NOTICE](plugins/gstack-power-team/NOTICE.md) and complete license copies travel with installation. |
| `methodology/skill-catalog.json` and generated selections | Adapted authoring text underlying those methods; the same third-party scope and modification notice apply. Mappings, hashes and review decisions identify the selected source and editorial changes; they do not import the referenced code. |
| `scripts/`, `tests/`, original documentation and packaging | Original maintenance contributions under MIT. Standard-library imports are not vendored dependencies. No package-manager/runtime dependency code is redistributed. |
| `gstack-skills/` | Selected literal upstream text, licenses and notices; not installed. The source files listed in MANIFEST.txt remain byte-identical to their pinned originals. Original MIT and relevant Apache-2.0 terms are preserved, not replaced by the root MIT license. |

The fixed comparison source is [garrytan/gstack at
9f44f188d117b5aa714c7698aa29bc5c7785cbfa](https://github.com/garrytan/gstack/tree/9f44f188d117b5aa714c7698aa29bc5c7785cbfa),
upstream version 1.91.317.0. Its complete [NOTICE](gstack-skills/NOTICE.md),
[MIT license](gstack-skills/LICENSE), and [third-party license texts](gstack-skills/licenses/)
are retained. Upstream's descriptions of files outside the selected snapshot
are provenance, not claims that those implementations are included here.

## Third-Party Chain

The installed [scope table](plugins/gstack-power-team/NOTICE.md) maps the methods
to Garry Tan, Paul Bakaus/impeccable, Elaya, Nico Bailon, and the other upstream
credits. Conservative notice retention does not assert that every referenced
project's code is bundled. Full upstream notices also credit Hallmark contributors,
Google LLC, Theo Browne and Lauren Tan. Their original notices are retained even
where only source identifiers, independently stated ideas, or no related code is
distributed. No upstream or third-party trademark endorsement is claimed.

The primary impeccable license at
[87d8f6d686782561fb572758d9a9bb8596a1a0e7](https://github.com/pbakaus/impeccable/tree/87d8f6d686782561fb572758d9a9bb8596a1a0e7)
adds `Copyright 2025 Paul Bakaus` to its Apache text. Its complete license and
NOTICE are retained in the plugin in addition to the generic Apache text supplied
by gstack. The impeccable NOTICE credits ehmo's MIT platform-design references;
those platform files are not included in this distribution. The upstream
DESIGN.md notice identifies a format implementation, not copied specification
text; the implementation and specification are not vendored here.

Apache section 4 obligations are handled with complete license copies, retained
notices, and prominent modification notices on rewritten skills/references and
their catalog source. Rewriting or generating a file does not remove those
obligations. The generator emits the notices; package checks require legal files
and verify their source identities. See [the update process](methodology/UPDATE.md).

## Material Not Redistributed

- No upstream executables, browser/runtime libraries, diagram-render HTML,
  React, Mermaid, Excalidraw, font binaries or their transitive dependencies are
  included. The archived diagram-render license inventory describes the
  upstream bundle only. Original Mermaid diagram source in our README is not
  a redistribution of the Mermaid implementation.
- The two source texts `design-review/SKILL.md` and
  `plan-design-review/SKILL.md` are intentionally not mirrored. They contain
  externally attributed design summaries (including Steve Krug and, in the
  first file, an OpenAI design article) for which this review did not establish
  a separate text-redistribution grant. This is a conservative distribution
  boundary, not an allegation of infringement. Their source IDs and pinned
  hashes remain for comparison; the references point to upstream rather than
  copying these texts. No book, article, or screenshot is sublicensed by us.
- Methodology references to established concepts, such as documentation types,
  do not incorporate the external framework's implementation or documentation
  prose. The original snapshot's bibliographic references are not relicensing
  statements.
- The README links to official installation help rather than embedding its
  screenshot. No general redistribution permission for that image was
  established. External sites and images remain under their owners' terms;
  hyperlinks do not apply this repository's license to their content.

This inventory records the current deliverable and selected primary evidence;
it is not a legal opinion or certification of all upstream ownership. Earlier
Git revisions and cached plugin packages retain their earlier contents and
notices; this correction does not rewrite them. Reassess scope and permissions
before adding new upstream text, assets, notices, or runtime payloads.
