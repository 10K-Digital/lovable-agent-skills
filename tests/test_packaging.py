from __future__ import annotations

import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MIGRATOR = ROOT / "plugins" / "lovable" / "scripts" / "migrate-workspace.py"
ARCHITECTURE_DETECTOR = ROOT / "plugins" / "lovable" / "scripts" / "detect-architecture.py"
POLICY_READER = ROOT / "plugins" / "lovable" / "scripts" / "read-project-policy.py"
SOURCE_INTEGRITY = ROOT / "plugins" / "lovable" / "scripts" / "source-integrity.py"
STANDALONE_INSTALLER = ROOT / "plugins" / "lovable" / "scripts" / "install-standalone.py"
CONTEXT_READER = ROOT / "plugins" / "lovable" / "skills" / "lovable-project" / "scripts" / "read-context.py"
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


class PackagingTests(unittest.TestCase):
    def test_codex_plugin_manifest_and_mcp_validate(self) -> None:
        manifest = json.loads((ROOT / "plugins/lovable/.codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], "lovable")
        self.assertTrue(SEMVER.fullmatch(manifest["version"]))
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["mcpServers"], json.loads((ROOT / "plugins/lovable/.mcp.json").read_text()))
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

    def test_architecture_detector_handles_vite_and_tanstack_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "vite.config.ts").write_text("export default {}\n")
            result = subprocess.run(
                [sys.executable, str(ARCHITECTURE_DETECTOR), str(root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(json.loads(result.stdout)["architecture"], "vite-spa")
            (root / "vite.config.ts").unlink()
            (root / "app.config.ts").write_text("export default {}\n")
            result = subprocess.run(
                [sys.executable, str(ARCHITECTURE_DETECTOR), str(root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(json.loads(result.stdout)["architecture"], "tanstack-start")

    def test_architecture_detector_checks_tanstack_package_before_vite_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "vite.config.ts").write_text("export default {}\n")
            (root / "package.json").write_text(json.dumps({
                "dependencies": {"@tanstack/react-start": "^1.0.0"}
            }))
            result = subprocess.run(
                [sys.executable, str(ARCHITECTURE_DETECTOR), str(root)],
                text=True, capture_output=True, check=False,
            )
            detected = json.loads(result.stdout)
            self.assertEqual(detected["architecture"], "tanstack-start")
            self.assertIn("package.json:dependencies", detected["markers"])

    def test_architecture_detector_does_not_treat_router_scripts_as_start(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "vite.config.ts").write_text("export default {}\n")
            (root / "package.json").write_text(json.dumps({
                "dependencies": {"@tanstack/react-router": "^1.0.0"},
                "scripts": {"generate": "tsr generate # tanstack router"},
            }))
            result = subprocess.run(
                [sys.executable, str(ARCHITECTURE_DETECTOR), str(root)],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(json.loads(result.stdout)["architecture"], "vite-spa")

    def test_fallback_contract_documents_mcp_failure_classes(self) -> None:
        deploy = (ROOT / "plugins/lovable/skills/lovable-deploy/SKILL.md").read_text().lower()
        for term in ("unsupported operation", "timeout", "authentication failure", "browser automation", "manual"):
            self.assertIn(term, deploy)

    def test_source_identity_is_reproducible_and_can_check_a_copy(self) -> None:
        plugin = ROOT / "plugins/lovable"
        first = subprocess.run(
            [sys.executable, str(SOURCE_INTEGRITY), "--source", str(plugin)],
            text=True, capture_output=True, check=False,
        )
        second = subprocess.run(
            [sys.executable, str(SOURCE_INTEGRITY), "--source", str(plugin), "--check", str(plugin)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(json.loads(first.stdout), json.loads(second.stdout))

    def test_source_identity_includes_executable_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            copied = Path(tempdir) / "lovable"
            shutil.copytree(ROOT / "plugins/lovable", copied)
            candidate = copied / "hooks" / "auto-sync.sh"
            mode = candidate.stat().st_mode
            os.chmod(candidate, mode & ~0o111 if mode & 0o111 else mode | 0o100)
            result = subprocess.run(
                [sys.executable, str(SOURCE_INTEGRITY), "--source", str(ROOT / "plugins/lovable"),
                 "--check", str(copied)],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("sha256", result.stderr)

    def test_standalone_install_preserves_existing_entry_and_records_source(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "skills"
            old_entry = target / "lovable-project"
            old_entry.mkdir(parents=True)
            (old_entry / "preserve.txt").write_text("old skill\n")
            install = subprocess.run(
                [sys.executable, str(STANDALONE_INSTALLER), "--source", str(ROOT / "plugins/lovable"),
                 "--target", str(target), "--install"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(install.returncode, 0, install.stdout + install.stderr)
            self.assertTrue((target / "lovable-project").is_symlink())
            self.assertTrue(any(target.glob(".lovable-standalone-backups/*/lovable-project/preserve.txt")))
            manifest = json.loads((target / ".lovable-standalone-manifest.json").read_text())
            self.assertIn("commit", manifest)
            self.assertIn("sha256", manifest["identity"])
            checked = subprocess.run(
                [sys.executable, str(STANDALONE_INSTALLER), "--source", str(ROOT / "plugins/lovable"),
                 "--target", str(target), "--check"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_standalone_install_refuses_removed_source_skill_without_removing_link(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            source = Path(tempdir) / "source"
            target = Path(tempdir) / "skills"
            shutil.copytree(ROOT / "plugins/lovable", source)
            installed = subprocess.run(
                [sys.executable, str(STANDALONE_INSTALLER), "--source", str(source),
                 "--target", str(target), "--install"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            shutil.rmtree(source / "skills" / "testing")
            reinstalled = subprocess.run(
                [sys.executable, str(STANDALONE_INSTALLER), "--source", str(source),
                 "--target", str(target), "--install"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(reinstalled.returncode, 2)
            self.assertIn("removes installed skills", reinstalled.stderr)
            self.assertTrue((target / "testing").is_symlink())
            checked = subprocess.run(
                [sys.executable, str(STANDALONE_INSTALLER), "--source", str(source),
                 "--target", str(target), "--check"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(checked.returncode, 1)
            self.assertIn("inventory differs", checked.stderr)


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

    def test_migration_preserves_explicit_deployment_preferences(self) -> None:
        for enabled in (True, False):
            with self.subTest(yolo_mode=enabled):
                config_path = self.root / ".lovable-agent/config.json"
                config_path.parent.mkdir(exist_ok=True)
                deploy = {
                    "mode": "browser", "yolo_mode": enabled,
                    "confirm_migrations": True, "custom_setting": "preserve",
                }
                config_path.write_text(json.dumps({"deploy": deploy}))
                result = self.run_migrator()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(json.loads(config_path.read_text())["deploy"], deploy)

    def test_migration_does_not_grant_yolo_authorization_from_transport(self) -> None:
        result = self.run_migrator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        deploy = json.loads((self.root / ".lovable-agent/config.json").read_text())["deploy"]
        self.assertEqual(deploy["mode"], "auto")
        self.assertFalse(deploy.get("yolo_mode", False))
        self.assertFalse(deploy["confirm_migrations"])

    def test_dry_run_does_not_write(self) -> None:
        result = self.run_migrator("--dry-run")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.root / ".lovable-agent/config.json").exists())
        self.assertIn("DRY RUN", result.stdout)


class PolicyReaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        config_dir = self.root / ".lovable-agent"
        config_dir.mkdir()
        self.secret = "test-only-" + secrets.token_hex(12)
        (config_dir / "config.json").write_text(json.dumps({
            "schema_version": 1,
            "project": {"lovable_url": "https://lovable.dev/projects/private"},
            "sync": {"branch": "main", "auto_push": False, "custom": self.secret},
            "deploy": {
                "mode": "mcp", "yolo_mode": False, "auto_deploy": True,
                "control_priority": ["lovable-mcp", "in-app-browser", "manual"],
                "confirm_migrations": True,
            },
            "testing": {"enabled": True, "access_method": "token", "preview_url": self.secret},
            "inventory": {
                "edge_functions": ["send-email", {"name": "internal", "value": self.secret}],
                "migrations": ["001.sql"],
                "secrets": [{"name": "RESEND_API_KEY", "value": self.secret}], "extra": self.secret,
            },
        }))

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_reader(self, section: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(POLICY_READER), "--project", str(self.root), "--section", section],
            text=True, capture_output=True, check=False,
        )

    def test_policies_are_whitelisted_and_secret_safe(self) -> None:
        result = self.run_reader("policies")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(self.secret, result.stdout)
        self.assertEqual(json.loads(result.stdout), {
            "deploy": {
                "auto_deploy": True, "confirm_migrations": True,
                "control_priority": ["lovable-mcp", "in-app-browser", "manual"],
                "mode": "mcp", "yolo_mode": False,
            },
            "schema_version": 1,
            "sync": {"auto_push": False, "branch": "main"},
            "testing": {"access_method": "token", "enabled": True},
        })

    def test_inventory_requires_explicit_selection_and_redacts_secrets(self) -> None:
        result = self.run_reader("inventory")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(self.secret, result.stdout)
        self.assertEqual(json.loads(result.stdout), {
            "inventory": {"edge_functions": ["send-email"], "migrations": ["001.sql"]}
        })

    def test_reader_preserves_false_yolo_authorization(self) -> None:
        result = self.run_reader("policies")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIs(json.loads(result.stdout)["deploy"]["yolo_mode"], False)

    def test_standalone_context_entrypoint_resolves_the_plugin_policy_reader(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CONTEXT_READER), "--project", str(self.root), "--section", "policies"],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["deploy"]["yolo_mode"])

    def test_reader_fails_closed_for_invalid_or_nested_policy_values(self) -> None:
        config_path = self.root / ".lovable-agent/config.json"
        config = json.loads(config_path.read_text())
        config["deploy"]["yolo_mode"] = {"secret": self.secret}
        config["deploy"]["confirm_migrations"] = "true"
        config["testing"]["enabled"] = 1
        config_path.write_text(json.dumps(config))
        result = self.run_reader("policies")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(self.secret, result.stderr)
        self.assertIn("deploy.yolo_mode", result.stderr)

    def test_reader_accepts_older_partial_schema_without_migration(self) -> None:
        config_path = self.root / ".lovable-agent/config.json"
        config_path.write_text(json.dumps({"deploy": {"mode": "browser"}}))
        result = self.run_reader("policies")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"deploy": {"mode": "browser"}})
        self.assertEqual(json.loads(config_path.read_text()), {"deploy": {"mode": "browser"}})

    def test_present_policy_sections_must_be_objects(self) -> None:
        config_path = self.root / ".lovable-agent/config.json"
        for section in ("deploy", "sync", "testing"):
            for invalid in (None, ["yolo_mode", False], self.secret, False):
                with self.subTest(section=section, invalid_type=type(invalid).__name__):
                    config_path.write_text(json.dumps({section: invalid}))
                    result = self.run_reader("policies")
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertIn(section, result.stderr)
                    self.assertNotIn(self.secret, result.stderr)

    def test_inventory_names_exclude_urls_and_paths(self) -> None:
        config_path = self.root / ".lovable-agent/config.json"
        config_path.write_text(json.dumps({"inventory": {"edge_functions": ["valid-name", "https://example.test/?token=" + self.secret, "../private"], "migrations": ["20260101_init.sql"]}}))
        result = self.run_reader("inventory")
        self.assertEqual(result.returncode, 0)
        self.assertNotIn(self.secret, result.stdout)
        self.assertEqual(json.loads(result.stdout)["inventory"]["edge_functions"], ["valid-name"])


if __name__ == "__main__":
    unittest.main()
