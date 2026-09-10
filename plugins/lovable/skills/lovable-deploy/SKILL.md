---
name: lovable-deploy
description: >-
  Deploy Lovable backend work from any coding agent. Use for Supabase Edge Functions, database
  migrations, Lovable MCP setup, deployment verification, or deciding between MCP, browser, and
  manual fallbacks.
---

# Lovable Deployment

## Lovable prompt authorization

Read `.lovable-agent/config.json` → `deploy.yolo_mode` first. An explicit boolean `true`
enables YOLO; `false` disables it. If the field is absent, use legacy `yolo_mode: on/true`
or **Status: on/true** in the CLAUDE.md Yolo Mode Configuration section. Missing or
unrecognized values mean off. An explicit neutral value takes precedence over legacy settings.
`deploy.mode: auto` selects transport; it does not enable YOLO.

- **YOLO on:** The user has granted standing authorization to submit Lovable prompts needed
  for the requested task, through MCP or browser, including prompts that consume Lovable credits.
  Proceed without asking again. A generic AGENTS.md, agent.md, or CLAUDE.md rule requiring
  confirmation before Lovable prompts applies only when YOLO is off; it is not a conflict or
  reason to stop when YOLO is on.
- **YOLO off:** Obtain user confirmation before submitting a Lovable prompt unless the current
  request already explicitly authorizes that submission. Preparing a prompt needs no confirmation.
- Preserve explicit task restrictions such as “do not deploy/publish,” platform approval
  requirements, and confirmation for destructive or irreversible database operations. YOLO
  authorizes in-scope prompts, not unrelated changes or automatic frontend publication.
- With `deploy.confirm_migrations: true`, confirm migration execution even with YOLO on.
  With false (the default), ordinary in-scope migrations need no repeated approval.
  Destructive or irreversible database operations still require confirmation. Auto-push and auto-deploy remain separate
  settings. Do not enable them merely because YOLO is on.

If `deploy.mode` is `manual`, return a prompt without submitting it. Otherwise use the configured
transport (`mcp` or `browser`); `auto` follows this fallback order:

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
- Apply the authorization and migration gates above; transport selection never grants authorization.

After deployment, distinguish **accepted** (the agent received the request) from **verified** (the
response/logs or Preview checks confirm the result). Never claim verification from an asynchronous
MCP acknowledgement alone. If polling is supported, poll with a bounded timeout; otherwise report
the accepted state and give the manual verification step.

Classify MCP failures before falling back: an unsupported operation, timeout, or unavailable server
uses browser automation; an authentication failure requires re-authentication or a manual handoff.
Do not retry authentication failures indefinitely, and never include preview tokens or secret values
in MCP requests, browser URLs, logs, or generated reports.

The existing `../yolo/` skill and `../yolo/references/mcp-workflows.md` contain the Claude browser
and MCP procedures. Keep them as compatibility references rather than creating a custom MCP server.
