"""Exercise the public ZIP boundary in disposable copies, without network access."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = {
    ".codex-plugin/plugin.json", ".mcp.json", "LICENSE", "README.md",
    "assets/logo.png", "skills/nutrient-documents/SKILL.md",
}


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("ci", "plugins", ".claude-plugin", ".agents"):
            shutil.copytree(ROOT / name, self.root / name, ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("README.md", "LICENSE"):
            shutil.copy2(ROOT / name, self.root / name)
        self.plugin = self.root / "plugins" / "nutrient"

    def build(self, success=True):
        result = subprocess.run([sys.executable, str(self.root / "ci/package_openai.py")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        if not success:
            self.assertFalse(list((self.root / "dist").glob("*.zip")))
        return result.stdout + result.stderr

    def edit_json(self, relative, edit):
        path = self.plugin / relative
        value = json.loads(path.read_text())
        edit(value)
        path.write_text(json.dumps(value))

    def test_reproducible_package_and_private_files_excluded(self):
        for name in (".env", ".app.json", "reviewer-credentials.txt"):
            (self.plugin / name).write_text("PACKAGING-CANARY-PRIVATE")
        self.build()
        archive_path, = (self.root / "dist").glob("*.zip")
        first = archive_path.read_bytes()
        self.build()
        self.assertEqual(first, archive_path.read_bytes())
        with zipfile.ZipFile(archive_path) as archive:
            self.assertEqual(set(archive.namelist()), EXPECTED)
            self.assertIsNone(archive.testzip())
            for name in archive.namelist():
                self.assertNotIn(b"PACKAGING-CANARY-PRIVATE", archive.read(name))
            manifest = json.loads(archive.read(".codex-plugin/plugin.json"))
            self.assertEqual(manifest["name"], "nutrient")
            self.assertEqual(manifest["mcpServers"], "./.mcp.json")
            self.assertLess(len(first), 100 * 1024 * 1024)

    def test_fixed_authentication_header_rejected(self):
        self.edit_json(".mcp.json", lambda m: m["mcpServers"]["nutrient"].update(
            headers={"Authorization": "Bearer PACKAGING-CANARY-PRIVATE"}))
        self.assertIn("FAIL .mcp.json", self.build(success=False))

    def test_nested_client_secret_rejected(self):
        self.edit_json(".codex-plugin/plugin.json", lambda m: m["extensions"]["com.openai"].update(
            auth={"clientSecret": "PACKAGING-CANARY-PRIVATE"}))
        self.assertIn("credential field clientSecret", self.build(success=False))

    def test_local_app_mapping_rejected(self):
        self.edit_json(".codex-plugin/plugin.json", lambda m: m.update(apps="./.app.json"))
        self.assertIn("no local apps or hooks", self.build(success=False))

    def test_nested_local_app_mapping_rejected(self):
        self.edit_json(".codex-plugin/plugin.json", lambda m: m["extensions"]["com.openai"].update(apps="./.app.json"))
        self.assertIn("no local apps or hooks", self.build(success=False))

    def test_symlink_to_external_file_rejected(self):
        outside = self.root / "private.txt"
        outside.write_text("PACKAGING-CANARY-PRIVATE")
        logo = self.plugin / "assets/logo.png"
        logo.unlink()
        logo.symlink_to(outside)
        self.assertIn("symbolic links", self.build(success=False))

    def test_non_boolean_annotation_rejected(self):
        path = self.root / "ci/tools-chatgpt.json"
        tools = json.loads(path.read_text())
        tools[0]["annotations"]["readOnlyHint"] = "false"
        path.write_text(json.dumps(tools))
        self.assertIn("explicit boolean tool annotations", self.build(success=False))


if __name__ == "__main__":
    unittest.main()
