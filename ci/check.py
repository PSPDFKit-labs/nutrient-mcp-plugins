#!/usr/bin/env python3
"""Checks the Nutrient Claude plugin without network access.

Run from the repository root: python3 ci/check.py
- Claude's and OpenAI's marketplace entries and manifests agree, and meet each directory's README, license and
  listing requirements.
- The bundled connector is the production Hosted MCP service over HTTP.
- The skill's frontmatter follows the Agent Skills format.
- Every identifier the skill puts in a code span is a tool, an input or output field, or an error code the service
  returns, according to ci/tools.json: the catalog Hosted MCP lists to a client that renders MCP Apps. Refresh it from
  the monorepo when the service changes (see AGENTS.md).
"""
import json
import pathlib
import re
import struct
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


def load(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as error:
        check(False, f"{path.relative_to(ROOT)} is readable JSON ({error})")
        return {}


def limit(value, maximum, message):
    check(isinstance(value, str) and 0 < len(value) <= maximum, f"{message} has 1 to {maximum} characters")


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


marketplace = load(ROOT / ".claude-plugin" / "marketplace.json")
manifest = load(PLUGIN / ".claude-plugin" / "plugin.json")
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

# OpenAI (ChatGPT and Codex): .codex-plugin/plugin.json shares .mcp.json and skills/ with Claude's manifest.
codex = load(PLUGIN / ".codex-plugin" / "plugin.json")
check(codex.get("name") == manifest.get("name") and codex.get("version") == manifest.get("version"),
      ".codex-plugin/plugin.json has the same name and version as .claude-plugin/plugin.json")
check(codex.get("mcpServers") == "./.mcp.json" and codex.get("skills") == "./skills/",
      ".codex-plugin/plugin.json uses the shared .mcp.json and skills/")
interface = codex.get("interface", {})
# OpenAI's submission limits (developers.openai.com/plugins/deploy/submission).
limit(codex.get("name"), 64, ".codex-plugin/plugin.json name")
limit(codex.get("description"), 4000, ".codex-plugin/plugin.json description")
limit(codex.get("author", {}).get("name"), 120, ".codex-plugin/plugin.json author.name")
for field, maximum in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000), ("developerName", 80), ("category", 120)):
    limit(interface.get(field), maximum, f".codex-plugin/plugin.json interface {field}")
for field in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL", "supportURL"):
    limit(interface.get(field), 1024, f".codex-plugin/plugin.json interface {field}")
    check(str(interface.get(field, "")).startswith("https://"), f".codex-plugin/plugin.json interface {field} is an https URL")
prompts, capabilities = interface.get("defaultPrompt", []), interface.get("capabilities", [])
check(len(prompts) <= 3 and all(isinstance(p, str) and 0 < len(p) <= 128 for p in prompts),
      ".codex-plugin/plugin.json interface defaultPrompt has at most 3 prompts of at most 128 characters")
check(len(capabilities) <= 20 and all(isinstance(c, str) and 0 < len(c) <= 120 for c in capabilities),
      ".codex-plugin/plugin.json interface capabilities has at most 20 entries of at most 120 characters")
for field in ("logo", "composerIcon"):
    image = (PLUGIN / interface.get(field, "missing")).resolve()
    data = image.read_bytes() if image.is_relative_to(PLUGIN) and image.is_file() else b""
    # A complete PNG: signature, then IHDR's width and height, ending with the IEND chunk.
    size = struct.unpack(">II", data[16:24]) if data[:8] == b"\x89PNG\r\n\x1a\n" and data.endswith(b"IEND\xaeB`\x82") else None
    check(size is not None and size[0] == size[1] and size[0] >= 48,
          f".codex-plugin/plugin.json {field} is a complete square PNG of at least 48 pixels inside the plugin")
openai_marketplace = load(ROOT / ".agents" / "plugins" / "marketplace.json")
openai_entries = [entry for entry in openai_marketplace.get("plugins", []) if entry.get("name") == codex.get("name")]
check(len(openai_entries) == 1 and (ROOT / openai_entries[0].get("source", {}).get("path", "")).resolve() == PLUGIN,
      ".agents/plugins/marketplace.json lists the plugin once, at plugins/nutrient")
check(len(openai_entries) == 1 and openai_entries[0].get("policy", {}).get("installation") in ("AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"),
      ".agents/plugins/marketplace.json gives the plugin a valid installation policy")

servers = load(PLUGIN / ".mcp.json").get("mcpServers", {})
check(list(servers) == ["nutrient"] and servers["nutrient"].get("type") == "http" and servers["nutrient"].get("url") == SERVICE,
      f".mcp.json declares one server, nutrient, at {SERVICE} over HTTP (OpenAI connects one server per plugin)")

skills = sorted((PLUGIN / "skills").glob("*/SKILL.md"))
check(len(skills) > 0, "the plugin has at least one skill")
tools = load(ROOT / "ci" / "tools.json")
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
print(f"PASS plugin {manifest['name']} {manifest['version']}: Claude and OpenAI manifests and marketplaces, README, license, "
      f"connector and {len(skills)} skill(s) against {len(tools)} tools")
