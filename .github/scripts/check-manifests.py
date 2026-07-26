#!/usr/bin/env python3
"""Check the plugin and marketplace manifests before a release goes out."""

import json
import re
import sys
from pathlib import Path

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")

plugin = json.loads(Path(".claude-plugin/plugin.json").read_text())
market = json.loads(Path(".claude-plugin/marketplace.json").read_text())
style = Path("output-styles/Laconic.md").read_text()

problems = []
if plugin.get("name") != "laconic":
    problems.append(f"plugin name is {plugin.get('name')!r}")
if not SEMVER.match(plugin.get("version", "")):
    problems.append(f"version {plugin.get('version')!r} is not semver")
if not any(entry.get("name") == "laconic" for entry in market.get("plugins", [])):
    problems.append("marketplace has no laconic entry")
if not style.startswith("---"):
    problems.append("the output style is missing its frontmatter")
if "force-for-plugin: true" not in style:
    problems.append("the output style no longer applies itself")

if problems:
    sys.exit("release blocked\n" + "\n".join(f"  {p}" for p in problems))
print(f"manifests ok, version {plugin['version']}")
