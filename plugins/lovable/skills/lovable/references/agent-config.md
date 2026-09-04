# Neutral Agent Configuration

`.lovable-agent/config.json` is the provider-neutral project contract. It contains settings and
secret metadata, never secret values. The file is intentionally JSON so Codex, Claude Code, and
other agents can read it without a provider-specific parser.

## Schema

```json
{
  "schema_version": 1,
  "project": {
    "name": "my-lovable-app",
    "production_url": "https://my-app.lovable.app",
    "lovable_url": "https://lovable.dev/projects/PROJECT_ID",
    "github_url": "https://github.com/owner/repo",
    "backend": "lovable-cloud",
    "supabase_ref": "",
    "architecture": "vite-spa"
  },
  "sync": {
    "branch": "main",
    "auto_sync": true,
    "auto_push": false
  },
  "deploy": {
    "mode": "auto",
    "confirm_migrations": false,
    "test_after_deploy": "off"
  },
  "testing": {
    "enabled": true,
    "preview_url": "https://preview--my-app.lovable.app",
    "access_method": "token",
    "token_captured": "2026-08-12",
    "token_expires": "2026-08-19",
    "test_after_implementation": false,
    "test_after_deploy": "smoke",
    "last_synced_commit": "abc1234"
  },
  "inventory": {
    "edge_functions": [],
    "migrations": [],
    "secrets": [
      {"name": "RESEND_API_KEY", "status": "configured", "used_in": ["send-email"]}
    ]
  }
}
```

Allowed deployment modes are `auto`, `mcp`, `browser`, and `manual`. Testing access methods are
`token` and `browser-login`; test-after-deploy is `off`, `smoke`, or `all`.

`deploy.mode` set to anything other than `manual` (i.e. `auto`, `mcp`, or `browser`) is the
yolo-mode equivalent: the user's standing authorization for the agent to deploy edge functions and
apply database migrations via Lovable automatically, with no per-operation confirmation. In that
case `confirm_migrations` should normally be `false`; set it to `true` to keep a confirmation
prompt before destructive/irreversible migrations even in an automated deploy mode. When
`deploy.mode` is `manual`, the agent never deploys directly — it always hands back a prompt for the
user to run in Lovable themselves.

## Provider shims

- `AGENTS.md` is the canonical instruction entry point.
- `CLAUDE.md` remains generated for Claude Code and may contain a short pointer to `AGENTS.md`.
- Existing command paths and `.claude/lovable-claude/test/` remain valid during migration.

## Migration mapping

| Legacy path | Canonical path |
| --- | --- |
| `.claude/lovable-claude/test/test-config.json` | `.lovable-agent/config.json` → `testing` |
| `.claude/lovable-claude/test/plans/` | `.lovable-agent/tests/plans/` |
| `.claude/lovable-claude/test/profiles/` | `.lovable-agent/tests/profiles/` |
| `.claude/lovable-claude/test/results/` | `.lovable-agent/tests/results/` |
| `.claude/lovable-claude/test/preview-token.local` | `.lovable-agent/preview-token.local` |

The migration copies artifacts without overwriting existing canonical files and never prints token
contents. Run it repeatedly safely; use `--dry-run` to inspect actions first.
