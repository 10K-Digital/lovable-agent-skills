from __future__ import annotations

import json
import re
import secrets
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MIGRATOR = ROOT / "plugins" / "lovable" / "scripts" / "migrate-workspace.py"
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


class PackagingTests(unittest.TestCase):
    def test_codex_plugin_manifest_and_mcp_validate(self) -> None:
        manifest = json.loads((ROOT / "plugins/lovable/.codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], "lovable")
        self.assertTrue(SEMVER.fullmatch(manifest["version"]))
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["mcpServers"], "./.mcp.json")
        interface = manifest["interface"]
        for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
            self.assertTrue(interface[field])
        self.assertLessEqual(len(interface["defaultPrompt"]), 3)
        self.assertTrue((ROOT / "plugins/lovable/skills").is_dir())
        self.assertFalse(set(manifest) & {"hooks"})
        claude_manifest = json.loads((ROOT / "plugins/lovable/plugin.json").read_text())
        self.assertEqual(claude_manifest["hooks"], "./hooks/claude-hooks.json")
        claude_hooks = json.loads((ROOT / "plugins/lovable/hooks/claude-hooks.json").read_text())["hooks"]
        self.assertEqual(set(claude_hooks), {"Start", "Stop"})

    def test_marketplace_points_at_repository_plugin(self) -> None:
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["source"]["path"], "./plugins/lovable")
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
        self.assertEqual(entry["policy"]["authentication"], "ON_INSTALL")

    def test_official_lovable_mcp_is_streamable_http_config(self) -> None:
        mcp = json.loads((ROOT / "plugins/lovable/.mcp.json").read_text())
        server = mcp["lovable"]
        self.assertEqual(server["type"], "http")
        self.assertEqual(server["url"], "https://mcp.lovable.dev")

    def test_bundled_hooks_include_codex_and_claude_start_events(self) -> None:
        hooks = json.loads((ROOT / "plugins/lovable/hooks/hooks.json").read_text())["hooks"]
        self.assertIn("SessionStart", hooks)
        self.assertIn("Start", hooks)
        self.assertIn("Stop", hooks)
        self.assertIn("PLUGIN_ROOT", hooks["SessionStart"][0]["hooks"][0]["command"])

    def test_skills_have_agent_skills_metadata(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_skills.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class MigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        legacy = self.root / ".claude/lovable-claude/test"
        (legacy / "plans").mkdir(parents=True)
        (legacy / "profiles").mkdir()
        (legacy / "results").mkdir()
        (legacy / "test-config.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "preview_url": "https://preview--demo.lovable.app",
                    "access_method": "token",
                    "token_captured": "2026-08-12",
                    "token_expires": "2026-08-19",
                    "test_after_deploy": "smoke",
                    "last_synced_commit": "abc1234",
                }
            )
        )
        (legacy / "plans/TP-001-demo.md").write_text("# demo\n")
        self.preview_token = "test-only-" + secrets.token_hex(8)
        (legacy / "preview-token.local").write_text(self.preview_token + "\n")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_migrator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(MIGRATOR), str(self.root), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_migration_is_idempotent_and_keeps_token_out_of_config(self) -> None:
        first = self.run_migrator()
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        second = self.run_migrator()
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)

        config_path = self.root / ".lovable-agent/config.json"
        config = json.loads(config_path.read_text())
        self.assertEqual(config["testing"]["preview_url"], "https://preview--demo.lovable.app")
        self.assertNotIn(self.preview_token, config_path.read_text())
        self.assertEqual(
            (self.root / ".lovable-agent/preview-token.local").read_text(),
            self.preview_token + "\n",
        )
        self.assertEqual(
            (self.root / ".lovable-agent/tests/plans/TP-001-demo.md").read_text(), "# demo\n"
        )
        gitignore = (self.root / ".gitignore").read_text()
        self.assertIn(".lovable-agent/preview-token.local", gitignore)
        self.assertIn(".claude/lovable-claude/test/preview-token.local", gitignore)

    def test_dry_run_does_not_write(self) -> None:
        result = self.run_migrator("--dry-run")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.root / ".lovable-agent/config.json").exists())
        self.assertIn("DRY RUN", result.stdout)


if __name__ == "__main__":
    unittest.main()
