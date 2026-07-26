#!/usr/bin/env python3
"""Set the plugin version in .claude-plugin/plugin.json and print the result.

Takes a bump type (patch, minor, major, alpha, beta, rc) or an explicit
version. Only the version field is rewritten, so the file keeps its formatting.
"""

import json
import re
import sys
from pathlib import Path

MANIFEST = Path(".claude-plugin/plugin.json")
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?$")
BUMPS = ("patch", "minor", "major", "alpha", "beta", "rc")


def bump(current: str, kind: str) -> str:
    parts = SEMVER.match(current)
    if not parts:
        sys.exit(f"cannot parse current version {current!r}")
    major, minor, patch = (int(parts[i]) for i in (1, 2, 3))
    pre = parts[4]

    if kind == "major":
        return f"{major + 1}.0.0"
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    if kind == "patch":
        # a prerelease becomes the release it was leading up to
        return f"{major}.{minor}.{patch}" if pre else f"{major}.{minor}.{patch + 1}"

    if pre and pre.split(".")[0] == kind:
        tail = pre.split(".")
        count = int(tail[1]) + 1 if len(tail) > 1 and tail[1].isdigit() else 1
        return f"{major}.{minor}.{patch}-{kind}.{count}"
    base = f"{major}.{minor}.{patch}" if pre else f"{major}.{minor}.{patch + 1}"
    return f"{base}-{kind}.1"


def main(argv: list[str]) -> None:
    if len(argv) != 2:
        sys.exit(f"usage: bump-version.py <{'|'.join(BUMPS)}|X.Y.Z>")
    target = argv[1]
    text = MANIFEST.read_text()
    current = json.loads(text)["version"]

    if SEMVER.match(target):
        new = target
    elif target in BUMPS:
        new = bump(current, target)
    else:
        sys.exit(f"unknown bump type {target!r}")

    updated, count = re.subn(r'("version"\s*:\s*")[^"]+(")', rf"\g<1>{new}\g<2>", text, count=1)
    if count != 1:
        sys.exit("no version field found in the manifest")
    MANIFEST.write_text(updated)
    print(new)


if __name__ == "__main__":
    main(sys.argv)
