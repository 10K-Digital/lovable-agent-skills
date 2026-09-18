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
    "yolo_mode": false,
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

`deploy.confirm_migrations: true` requests approval before each migration. The default is false;
YOLO on therefore runs ordinary in-scope migrations without repeated approval. Destructive or
irreversible database operations still require confirmation. `deploy.mode: manual` always returns
a prompt for the user to submit, even when YOLO is enabled.

## Provider shims

`deploy.yolo_mode` is the boolean standing authorization setting. Follow
[prompt authorization](prompt-authorization.md), including legacy fallback when the field is absent.
Preserve its value on reinitialization. `deploy.mode` alone never grants authorization.

- `AGENTS.md` is the canonical **local-agent** instruction entry point. Its managed rules belong
  inside `<!-- lovable-local-agent:start -->` / `<!-- lovable-local-agent:end -->` and must not be
  sent to Lovable chat or knowledge.
- `CLAUDE.md` remains generated for Claude Code and may contain a short pointer to `AGENTS.md`.
- `.lovable-agent/context.md` contains declarative facts only, not behavioral instructions.
- Project/Workspace knowledge is a separate Lovable-hosted control plane. Never synchronize it with
  local instruction files in either direction; see [instruction boundaries](instruction-boundaries.md).
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
