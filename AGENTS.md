# Lovable Agent Instructions

This repository contains the Lovable Agent Skills plugin and its Claude Code compatibility layer.
These instructions are the provider-neutral source of truth for Codex, Claude Code, and other
coding agents.

## Start here

1. Read `.lovable-agent/config.json` for repository-safe defaults.
2. Read the relevant skill under `plugins/lovable/skills/` before changing a workflow.
3. Preserve the Claude Code commands in `plugins/lovable/commands/` and hooks in
   `plugins/lovable/hooks/` unless a change explicitly updates their compatibility behavior.

## Project contracts

- Canonical user-project state lives in `.lovable-agent/`.
- `AGENTS.md` is the neutral instruction file. `CLAUDE.md` is a compatibility shim and may retain
  Claude-specific repository notes.
- The legacy `.claude/lovable-claude/test/` workspace remains supported. Use
  `plugins/lovable/scripts/migrate-workspace.py` to migrate it to `.lovable-agent/tests/`.
- Never put preview tokens, API keys, OAuth credentials, or secret values in tracked files,
  generated context, logs, MCP messages, or commit messages. The only token file is the ignored
  `.lovable-agent/preview-token.local` (with the legacy path supported during migration).
- Prefer the official Lovable MCP at `https://mcp.lovable.dev`; fall back to browser automation,
  then provide a manual prompt. Confirm destructive database operations before submission.
- Codex discovers the bundled `plugins/lovable/hooks/hooks.json` by convention. It includes
  `SessionStart`/`Stop` events plus the existing Claude `Start` compatibility event; review and trust
  hooks before enabling them.
- Keep version values synchronized in `.codex-plugin/plugin.json`, `plugins/lovable/plugin.json`,
  `.claude-plugin/marketplace.json`, and `CHANGELOG.md`.

## Validation

Run these checks before publishing changes:

```bash
python3 scripts/validate_skills.py
python3 /Users/felipematossardinhapinto/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 -m unittest discover -s tests -v
```

The repository's Codex marketplace entry is `.agents/plugins/marketplace.json`; its plugin source
is `./plugins/lovable`. The Claude marketplace entry remains `.claude-plugin/marketplace.json` and
points to the same plugin directory.
