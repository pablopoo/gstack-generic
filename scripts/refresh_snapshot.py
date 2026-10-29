#!/usr/bin/env python3
"""Refresh the literal upstream snapshot from committed Git objects only."""

import argparse
from pathlib import Path, PurePosixPath
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_NAME = "gstack-skills"
MANIFEST_NAME = "MANIFEST.txt"
LICENSE_NAME = "LICENSE"
NOTICE_NAME = "NOTICE.md"
NON_MIRRORED_PATHS = frozenset({
    "design-review/SKILL.md", "plan-design-review/SKILL.md",
})


def git(checkout, *args):
    return subprocess.run(
        ["git", "-C", str(checkout), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def canonical_skill_path(value):
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.as_posix() != value
        or not (value == "SKILL.md" or value.endswith("/SKILL.md"))
    ):
        raise ValueError(f"Not a canonical SKILL.md path: {value}")
    return value


def read_manifest(snapshot):
    manifest = snapshot / MANIFEST_NAME
    if manifest.is_symlink() or (manifest.exists() and not manifest.is_file()):
        raise ValueError(f"Snapshot destination is not a regular file: {manifest}")
    try:
        rows = manifest.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as error:
        raise ValueError(f"Missing snapshot manifest: {manifest}") from error
    source_paths = []
    prefix = f"{SNAPSHOT_NAME}/"
    for row in rows:
        if not row.startswith(prefix):
            raise ValueError(f"Unsupported manifest path: {row}")
        source_paths.append(canonical_skill_path(row[len(prefix) :]))
    if len(set(source_paths)) != len(source_paths):
        raise ValueError("Manifest contains duplicate paths")
    return source_paths


def blob_at(checkout, commit, path):
    rows = git(checkout, "ls-tree", "-rz", "--full-tree", commit, "--", path).split(b"\0")
    if not rows or not rows[0]:
        raise ValueError(f"Missing upstream source at {commit}: {path}")
    metadata, listed_path = rows[0].split(b"\t", 1)
    mode, kind, object_id = metadata.decode("ascii").split()
    if listed_path.decode("utf-8", "surrogateescape") != path:
        raise ValueError(f"Missing upstream source at {commit}: {path}")
    if kind != "blob" or mode not in {"100644", "100755"}:
        raise ValueError(f"Unsupported upstream object at {path}: mode {mode}, type {kind}")
    return git(checkout, "cat-file", "blob", object_id)


def ancillary_notices(checkout, commit):
    """Read optional notices from the pinned tree, never the checkout's files."""
    inventory = git(checkout, "ls-tree", "-rtz", "--full-tree", commit,
                    "--", NOTICE_NAME, "licenses")
    sources = {}
    for row in inventory.split(b"\0"):
        if not row:
            continue
        metadata, listed_path = row.split(b"\t", 1)
        mode, kind, object_id = metadata.decode("ascii").split()
        path = listed_path.decode("utf-8", "surrogateescape")
        is_license = path == "licenses" or path.startswith("licenses/")
        if is_license and kind == "tree" and mode == "040000":
            continue
        if (path == "licenses" or not (path == NOTICE_NAME or is_license)
                or kind != "blob" or mode not in {"100644", "100755"}):
            raise ValueError(f"Unsupported upstream object at {path}: mode {mode}, type {kind}")
        contents = git(checkout, "cat-file", "blob", object_id)
        try:
            contents.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(f"Upstream notice is not UTF-8 text: {path}") from error
        if b"\0" in contents:
            raise ValueError(f"Upstream notice is not text: {path}")
        sources[path] = contents
    return sources


def validate_snapshot_directory(snapshot):
    if snapshot.is_symlink():
        raise ValueError(f"Snapshot destination is a symlink: {snapshot}")
    if not snapshot.is_dir():
        raise ValueError(f"Snapshot root is not a directory: {snapshot}")


def validate_snapshot_path(snapshot, relative):
    current = snapshot
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"Snapshot destination is a symlink: {current}")
        if current.exists() and not current.is_dir():
            raise ValueError(f"Snapshot parent is not a directory: {current}")
    target = current / relative.parts[-1]
    if target.is_symlink():
        raise ValueError(f"Snapshot destination is a symlink: {target}")
    if target.exists() and not target.is_file():
        raise ValueError(f"Snapshot destination is not a regular file: {target}")


def refresh(root, checkout, commit, additions=(), check=False):
    """Refresh or verify a snapshot rooted at *root*.

    All source objects and local destination paths are validated before writes.
    """
    root = Path(root)
    checkout = Path(checkout)
    snapshot = root / SNAPSHOT_NAME
    validate_snapshot_directory(snapshot)
    manifest_paths = read_manifest(snapshot)
    additions = [canonical_skill_path(path) for path in additions]
    if len(set(additions)) != len(additions):
        raise ValueError("Duplicate --add path")
    if set(additions) & set(manifest_paths):
        raise ValueError("Duplicate --add path already listed in manifest")
    commit = git(checkout, "rev-parse", "--verify", f"{commit}^{{commit}}").decode().strip()

    paths = sorted((*manifest_paths, *additions))
    restricted = set(paths) & NON_MIRRORED_PATHS
    if restricted:
        raise ValueError(f"Not cleared for text redistribution; see NOTICE.md: {sorted(restricted)}")
    sources = {path: blob_at(checkout, commit, path) for path in paths}
    license_bytes = blob_at(checkout, commit, LICENSE_NAME)
    sources.update(ancillary_notices(checkout, commit))
    manifest_bytes = ("".join(f"{SNAPSHOT_NAME}/{path}\n" for path in paths)).encode("utf-8")

    destinations = {PurePosixPath(path): contents for path, contents in sources.items()}
    destinations[PurePosixPath(LICENSE_NAME)] = license_bytes
    destinations[PurePosixPath(MANIFEST_NAME)] = manifest_bytes
    for relative in destinations:
        validate_snapshot_path(snapshot, relative)

    stale = []
    for relative, expected in destinations.items():
        target = snapshot.joinpath(*relative.parts)
        if not target.is_file() or target.read_bytes() != expected:
            stale.append(target)
    if check:
        if stale:
            names = ", ".join(str(path.relative_to(root)) for path in stale)
            raise ValueError(f"Snapshot is stale: {names}")
        return paths

    for relative, contents in destinations.items():
        target = snapshot.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, help="Local upstream checkout; no upstream code is executed")
    parser.add_argument("--commit", required=True, help="Committed upstream revision to read")
    parser.add_argument("--add", action="append", default=[], metavar="PATH", help="Explicit upstream SKILL.md path to add")
    parser.add_argument("--check", action="store_true", help="Verify snapshot identities without writing")
    args = parser.parse_args()
    try:
        paths = refresh(ROOT, args.checkout, args.commit, args.add, args.check)
    except (ValueError, subprocess.CalledProcessError) as error:
        parser.error(str(error))
    action = "Verified" if args.check else "Refreshed"
    print(f"{action} {len(paths)} SKILL.md files at {args.commit}")


if __name__ == "__main__":
    main()
