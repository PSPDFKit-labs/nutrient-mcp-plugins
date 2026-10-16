"""Builds the ZIP that OpenAI's plugin dashboard takes for plugins/nutrient.

The archive holds the plugin folder without Claude's manifest, so OpenAI reads only .codex-plugin/plugin.json, and
has fixed timestamps and order, so the same commit always produces the same bytes. ci/check.py runs first.

Usage: python3 ci/package_openai.py  ->  dist/nutrient-openai-<version>.zip
"""

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "nutrient"
# Keep review notes, local app mappings, credentials and unexpected files out of the public ZIP.
# Add new resources here deliberately when the plugin starts referencing them.
PACKAGE_FILES = (
    ".codex-plugin/plugin.json",
    ".mcp.json",
    "LICENSE",
    "README.md",
    "assets/logo.png",
    "skills/nutrient-documents/SKILL.md",
)

for path in (PLUGIN, *PLUGIN.rglob("*")):
    if path.is_symlink():
        sys.exit(f"FAIL symbolic links are not allowed in the plugin: {path.relative_to(ROOT)}")

subprocess.run([sys.executable, str(ROOT / "ci" / "check.py")], check=True)

manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text())
names = sorted(PACKAGE_FILES)
files = [PLUGIN / name for name in names]
for path in files:
    if not path.is_file():
        sys.exit(f"FAIL the package has no {path.relative_to(PLUGIN)}")
resources = [manifest["interface"][field] for field in ("logo", "composerIcon")]
resources.extend(path.relative_to(PLUGIN).as_posix() for path in (PLUGIN / "skills").rglob("*") if path.is_file())
for resource in resources:
    if resource.removeprefix("./") not in names:
        sys.exit(f"FAIL add referenced resource {resource} to PACKAGE_FILES")

output = ROOT / "dist" / f"nutrient-openai-{manifest['version']}.zip"
output.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
    for path, name in zip(files, names):
        entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
        entry.external_attr = 0o644 << 16
        entry.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(entry, path.read_bytes())

if output.stat().st_size > 100 * 1024 * 1024:
    output.unlink()
    sys.exit("FAIL the OpenAI package exceeds 100 MiB")

digest = hashlib.sha256(output.read_bytes()).hexdigest()
print("\n".join("  " + name for name in names))
print(f"PASS {output.relative_to(ROOT)} ({output.stat().st_size} bytes, sha256 {digest})")
