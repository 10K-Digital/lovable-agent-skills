---
name: lovable-sync
description: >-
  Synchronize Lovable projects with GitHub safely. Use when pulling the latest main branch, checking
  GitHub/Lovable drift, initializing `.lovable-agent`, migrating the legacy Claude test workspace,
  or committing and pushing changes for Lovable two-way sync.
---

# Lovable GitHub Sync

Treat GitHub `main` as the source that Lovable synchronizes from.

- Read `.lovable-agent/config.json` first. Honor `sync.branch`, `sync.auto_sync`, and
  `sync.auto_push`; fall back to the legacy `CLAUDE.md` settings when the neutral file is absent.
- Before pulling, require a clean worktree. Fetch first, compare local/remote/base, and stop with a
  clear conflict message when branches diverge. Never discard user changes.
- Before pushing, inspect the diff, keep secrets out of commits, and confirm the intended branch.
  Auto-push is allowed only on the configured branch (normally `main`).
- Lovable frontend changes sync from GitHub automatically. Edge functions and migrations may still
  require a Lovable deployment prompt; use `lovable-deploy` for that decision.
- Run `scripts/migrate-workspace.py` when a project has `.claude/lovable-claude/test/`. The migration
  is idempotent, copies non-secret test artifacts, and keeps both token paths ignored.
- If sync fails, provide the manual Git commands and leave the worktree recoverable.

Use the Claude hook adapters in `../hooks/` when running under Claude Code. The same shell hooks can
be referenced by the optional `hooks/codex-hooks.json` definitions in runtimes that support hooks.
