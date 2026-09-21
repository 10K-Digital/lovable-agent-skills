---
name: lovable-testing
description: >-
  Create, maintain, and run Lovable Preview test plans across Codex, Claude Code, and compatible
  Agent Skills runtimes. Use for Preview access, test-plan sync, or smoke/changed/all runs.
---

# Lovable Preview Testing

Use this as the maintained Preview-testing workflow. The `testing` skill and `/lovable:test-*`
commands remain compatibility aliases.

1. Read only policy settings before selecting automation:

   ```bash
   python3 ~/.codex/skills/lovable-project/scripts/read-context.py --project . --section policies
   ```

   Read individual test plans, profiles, or the token file only when the selected operation needs
   them. Never preload the full config or inventory. The Preview token remains only in the ignored
   `.lovable-agent/preview-token.local` path.
2. Keep destructive, paid, or irreversible test steps `[MANUAL]`. Prefer the smallest affected
   plan set (`--changed` or `--smoke`) and treat Preview as non-production.
3. Use [test wizard](../testing/references/test-wizard.md) for setup and sync,
   [preview access](../testing/references/preview-access.md) for credentials, and
   [test execution](../testing/references/test-execution.md) for runs. These retained paths keep
   Claude commands working.
4. If browser access is unavailable, produce a manual checklist and continue. Record failures
   accurately and do not expose tokens in context, reports, or logs.

The legacy workspace `.claude/lovable-claude/test/` remains readable. Migrate it with
`scripts/migrate-workspace.py` without deleting it.
