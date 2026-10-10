#!/usr/bin/env python3
"""Checks the Nutrient Claude plugin without network access.

Run from the repository root: python3 ci/check.py
- The marketplace entry, the plugin manifest and the directory's README and license requirements agree.
- The bundled connector is the production Hosted MCP service over HTTP.
- The skill's frontmatter follows the Agent Skills format.
- Every identifier the skill puts in a code span is a tool, an input or output field, or an error code the service
  returns, according to ci/tools.json: the catalog Hosted MCP lists to a client that renders MCP Apps. Refresh it from
  the monorepo when the service changes (see AGENTS.md).
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "nutrient"
SERVICE = "https://mcp.nutrient.io/mcp"
# Error codes Hosted MCP returns (hosted-mcp/src/Nutrient.Mcp/DwsClient.cs and ToolResults.cs); they aren't schema fields.
ERROR_CODES = {"outcome_unknown", "idempotency_conflict"}
# Code spans that aren't identifiers.
NOT_IDENTIFIERS = {"mcp.nutrient.io"}

failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


def words(markdown):
    prose = re.sub(r"```.*?```", "", markdown, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9][\w'-]*", prose))


def collect(node, names):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "properties" and isinstance(value, dict):
                names.update(value)
            collect(value, names)
    elif isinstance(node, list):
        for item in node:
            collect(item, names)


marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
manifest = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
entries = [entry for entry in marketplace.get("plugins", []) if entry.get("name") == manifest.get("name")]
check(len(entries) == 1, "marketplace.json lists the plugin once by its manifest name")
if entries:
    entry = entries[0]
    check((ROOT / entry.get("source", "")).resolve() == PLUGIN, "the marketplace entry's source is plugins/nutrient")
    check(entry.get("version") == manifest.get("version"), "the marketplace entry's version matches plugin.json")

check(manifest.get("name") == "nutrient", "plugin.json name is nutrient, the plugin's permanent identity")
check(re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", "")) is not None, "plugin.json version is MAJOR.MINOR.PATCH")
for field in ("displayName", "description", "author", "license"):
    check(bool(manifest.get(field)), f"plugin.json has {field}")
for folder in (ROOT, PLUGIN):
    readme = folder / "README.md"
    check(readme.exists() and words(readme.read_text()) >= 40, f"{readme.relative_to(ROOT)} has at least 40 words of prose")
    check((folder / "LICENSE").exists(), f"{(folder / 'LICENSE').relative_to(ROOT)} exists")

servers = json.loads((PLUGIN / ".mcp.json").read_text()).get("mcpServers", {})
check(servers.get("nutrient", {}).get("type") == "http" and servers.get("nutrient", {}).get("url") == SERVICE,
      f".mcp.json connects to {SERVICE} over HTTP")

skills = sorted((PLUGIN / "skills").glob("*/SKILL.md"))
check(len(skills) > 0, "the plugin has at least one skill")
tools = json.loads((ROOT / "ci" / "tools.json").read_text())
known = {tool["name"] for tool in tools}
collect(tools, known)
for skill_file in skills:
    skill = skill_file.read_text().replace("\r\n", "\n")
    folder = skill_file.parent.name
    front = re.match(r"^---\nname: ([a-z0-9-]{1,64})\ndescription: ([^\n]{1,1024})\n---\n", skill)
    check(front is not None and front.group(1) == folder,
          f"{folder}: frontmatter names the skill after its folder and has a one-line description of at most 1024 characters")
    named = sorted({span for span in re.findall(r"`([a-z_]+(?:\.[a-z_]+)*)`", skill)} - NOT_IDENTIFIERS)
    unknown = [name for name in named if not all(part in known for part in name.split(".")) and name not in ERROR_CODES]
    check(not unknown, f"{folder}: names only tools, fields and error codes the service lists; unknown: {', '.join(unknown)}")

if failures:
    print("\n".join("FAIL " + failure for failure in failures))
    sys.exit(1)
print(f"PASS plugin {manifest['name']} {manifest['version']}: marketplace, manifest, README, license, connector and "
      f"{len(skills)} skill(s) against {len(tools)} tools")
