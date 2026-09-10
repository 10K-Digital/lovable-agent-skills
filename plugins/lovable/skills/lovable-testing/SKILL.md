---
name: lovable-testing
description: >-
  Run and maintain Lovable Preview tests from Codex, Claude Code, or another Agent Skills runtime.
  Use for test-plan generation, smoke/changed/all runs, test workspace migration, preview token
  handling, or keeping tests synchronized with changed features.
---

# Lovable Preview Testing

The canonical user-project test workspace is:

```text
.lovable-agent/
├── config.json
├── context.md
├── preview-token.local       # ignored credential, never committed
└── tests/
    ├── plans/
    ├── profiles/
    └── results/
```

- Treat Preview as non-production. Mark destructive, paid, or irreversible steps `[MANUAL]`.
- Store only the base preview URL and token dates in `config.json`; store the token itself only in
  `.lovable-agent/preview-token.local`, after ensuring the path is in `.gitignore`.
- Prefer a valid stored token, then a logged-in browser session, then a manual checklist. Never block
  implementation solely because browser access is unavailable.
- After implementation or deployment, run the smallest affected plan set (`--changed` or `--smoke`)
  before offering `--all`.
- Keep `covers:` paths accurate and update the last-sync commit after a successful plan sync.
- Migrate `.claude/lovable-claude/test/` with `scripts/migrate-workspace.py`; preserve the legacy
  path as a read-compatible alias until the user opts into cleanup.

The existing `../testing/` skill and its references remain the Claude command implementation. Read
`../lovable/references/agent-config.md` for the neutral config schema and migration mapping.
