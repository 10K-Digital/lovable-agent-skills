---
description: Migrate the legacy Claude Lovable workspace to the provider-neutral .lovable-agent contract.
---

# Migrate Lovable Agent Workspace

Use this command when a project already has `.claude/lovable-claude/test/` or a Claude-only
`CLAUDE.md` and should also work with Codex or another Agent Skills runtime.

## Instructions

1. Read `skills/lovable-project/SKILL.md` and `skills/lovable/references/agent-config.md`.
2. Run `python3 <plugin-root>/scripts/migrate-workspace.py --dry-run .` and show the proposed changes.
3. After the user confirms, run the same script without `--dry-run`.
4. Ensure `.gitignore` contains both token paths before copying any token:
   - `.lovable-agent/preview-token.local`
   - `.claude/lovable-claude/test/preview-token.local`
5. Create or preserve `AGENTS.md` and keep `CLAUDE.md` as a compatibility shim. Do not delete the
   legacy workspace automatically; it remains readable until the user explicitly cleans it up.
6. Validate that `config.json` contains no token or secret values, then report the migrated files.
