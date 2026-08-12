---
name: lovable-deploy
description: >-
  Deploy Lovable backend work from any coding agent. Use for Supabase Edge Functions, database
  migrations, Lovable MCP setup, deployment verification, or deciding between MCP, browser, and
  manual fallbacks.
---

# Lovable Deployment

Use the following deterministic fallback order:

1. **Official Lovable MCP** at `https://mcp.lovable.dev` when the server and required operation are
   available. Read its tool schema and server instructions before calling it.
2. **Browser automation** against the configured Lovable project when MCP is unavailable or does not
   support the operation.
3. **Manual prompt** copied to the user when neither automation path is available.

Before deployment:

- Confirm GitHub has the latest commit and allow the normal GitHub → Lovable sync delay.
- Read `.lovable-agent/config.json` (or the legacy Claude configuration) for the project ID and mode.
- Scan the changed code for required secret *names* and report missing configuration without exposing
  values.
- Ask for confirmation before applying destructive or irreversible migrations.

After deployment, distinguish **accepted** (the agent received the request) from **verified** (the
response/logs or Preview checks confirm the result). Never claim verification from an asynchronous
MCP acknowledgement alone. If polling is supported, poll with a bounded timeout; otherwise report
the accepted state and give the manual verification step.

The existing `../yolo/` skill and `../yolo/references/mcp-workflows.md` contain the Claude browser
and MCP procedures. Keep them as compatibility references rather than creating a custom MCP server.
