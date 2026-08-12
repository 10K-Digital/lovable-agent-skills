# Lovable Agent Test Workspace

User projects keep provider-neutral Preview test artifacts here:

- `plans/` — test plans (`TP-NNN-slug.md`)
- `profiles/` — test personas with test-only credentials
- `results/` — dated run reports

The preview token is stored only at `.lovable-agent/preview-token.local` and is gitignored. Existing
`.claude/lovable-claude/test/` workspaces can be migrated with
`plugins/lovable/scripts/migrate-workspace.py`.
