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
# Claude's manifest, and files an editor or OS leaves behind.
EXCLUDED_DIRECTORIES = {".claude-plugin", "__pycache__"}
EXCLUDED_FILES = {".DS_Store", "Thumbs.db"}

subprocess.run([sys.executable, str(ROOT / "ci" / "check.py")], check=True)

manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text())
files = sorted(
    path for path in PLUGIN.rglob("*")
    if path.is_file() and path.name not in EXCLUDED_FILES
    and not EXCLUDED_DIRECTORIES & set(path.relative_to(PLUGIN).parts[:-1])
)
names = [path.relative_to(PLUGIN).as_posix() for path in files]
for required in (".codex-plugin/plugin.json", ".mcp.json"):
    if required not in names:
        sys.exit(f"FAIL the package has no {required}")

output = ROOT / "dist" / f"nutrient-openai-{manifest['version']}.zip"
output.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
    for path, name in zip(files, names):
        entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
        entry.external_attr = 0o644 << 16
        entry.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(entry, path.read_bytes())

digest = hashlib.sha256(output.read_bytes()).hexdigest()
print("\n".join("  " + name for name in names))
print(f"PASS {output.relative_to(ROOT)} ({output.stat().st_size} bytes, sha256 {digest})")
