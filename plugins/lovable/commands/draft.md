---
description: Build, review, accept, or discard a Lovable draft (parallel version) through the Lovable MCP server.
---

# Lovable Draft

Work on a Lovable draft: a hosted, branch-like copy of the project with its own chat and preview.
Follow the provider-neutral `lovable-drafts` skill (`skills/lovable-drafts/SKILL.md`) and its
reference `skills/lovable/references/drafts.md`.

## Usage

```
/lovable:draft new "<label>" <what Lovable should build>
/lovable:draft list
/lovable:draft review <draft>
/lovable:draft accept <draft>
/lovable:draft discard <draft>
```

## Instructions

1. Read `.lovable-agent/config.json` (or the legacy `CLAUDE.md`) for the project ID. Require the
   Lovable MCP server (`/lovable:connect-mcp`); otherwise explain the browser steps from the
   drafts reference.
2. **new**: apply prompt authorization (YOLO or an explicit request) and credit efficiency, then
   `create_draft` with the label, report `backend_kind`, and send one consolidated
   `send_message(..., draft_id)`. Never send main-only work (secrets, sign-in methods, storage
   settings, payments, email, edge-function deployment) to a draft.
3. **list**: `list_drafts` and show name, status, and update/queue state.
4. **review**: `get_diff` with `draft_id` (`files_only` first for large drafts) plus the preview link
   from `get_draft`; give a one-line summary.
5. **accept**: show the summary and ask the user to accept this specific draft. Call `accept_draft`
   with that summary only after the user explicitly accepts, even when YOLO is on. On `pending`, wait
   with `get_draft`; never accept twice. After `merged`, pull `main`. Accepting does not publish.
6. **discard**: confirm, then `reject_draft`. Warn that writes already made to a shared database are
   not undone.
7. Never put secrets or preview tokens in MCP parameters or reports.
