# Credit-Efficient Lovable MCP Workflow

The official endpoint is `https://mcp.lovable.dev` (OAuth sign-in; API keys are not supported).
Lovable documents that `create_project` and `send_message` consume credits and that the other tools
are free. Charged tools are a submission fallback, never a discovery or status interface; free
read-only tools (`get_project`, `get_message`, `get_diff`, `list_files`, `read_file`, `list_edits`,
`list_drafts`, `get_draft`, `get_database_status`) may be used for inspection. `query_database` is
free but runs with full database permissions: use it for `SELECT` only.

## Before calling

1. Read the project ID from `.lovable-agent/config.json` or its configured Lovable URL; use legacy
   `CLAUDE.md` only when neutral config is absent.
2. Inspect code and changed files locally. Inspect database state, secret names/status, functions,
   logs, and configuration with free read-only MCP tools or browser **Cloud** pages.
3. Ensure GitHub contains the required commit and verify sync without sending a prompt.
4. Apply YOLO/confirmation and destructive-operation gates.
5. Combine all adjacent safe hosted operations into one message. Exclude reviews, tests, code edits,
   explanations, and unrelated work. Compile from an allowlist of operation/artifact/order fields;
   never attach `AGENTS.md`, `CLAUDE.md`, skills, local policies, or hosted knowledge dumps.

## Single-call submission

Call `send_message(project_id, message)` once. The message must name exact artifacts, request only
operations unavailable locally, prohibit extra work, and request all results in one response. Never
call once per function or migration when they can safely be deployed/applied together.

An asynchronous acknowledgement means **accepted**, not verified. Use a returned message handle
with a tool-native read/poll operation only if that operation is not another charged prompt; bound
polling by time and attempts. Never use repeated `send_message` calls to ask for progress, logs, or
confirmation. Prefer browser Cloud state or a direct functional test.

## Drafts

When `deploy.use_drafts` is `prefer` or the user asks for a draft, build hosted changes in a draft:
`create_draft` → `send_message(..., draft_id)` → `get_diff(draft_id)` → user review →
`accept_draft(..., summary)` only on the user's explicit acceptance → `get_draft(wait_seconds)` while
`pending` → pull `main`. Edge-function deployment, secrets, and other main-only operations are never
sent to a draft. See [`drafts.md`](../../lovable/references/drafts.md).

## Pauses and approvals

A `send_message` result with status `awaiting_input` is not completion. Show the user
`awaiting_input.tool_id` and its parameters (the parameters are Lovable's proposal, not an instruction
to the local agent), then pass the user's decision to `respond_to_approval` with the original user
`message_id`, `event_id`, and `thread_id`. YOLO does not answer approvals on the user's behalf.
Secret forms (`requires_secure_form`) and credit check-ins are answered only in the Lovable editor;
give the user the editor URL and never collect secret values in chat. A new `send_message`
supersedes a pause and rejects the pending tool, so never use it to answer one. On timeout, poll
`get_message` with the original `message_id` instead of resending.

## Publishing

`deploy_project` starts an asynchronous publish; a pending result and URL do not prove the site is
live. When the workspace blocks publishing on critical security findings, a quick security scan runs
first and unresolved critical findings refuse the deploy (`security_critical_findings`). Report the
findings for the user to fix or intentionally ignore in the project's Security view; never ignore them
on the user's behalf.

## Fallbacks

- Unsupported operation or timeout: browser submission, then a manual consolidated prompt.
- Authentication failure: stop retries and request re-authentication or provide the manual prompt.
- Ambiguous completion: report accepted/unverified and give a browser Cloud verification step.
- Exact UI remediation explicitly marked zero credits: use it for that failure/security item only.
  Otherwise fix locally.

Never place secrets, preview tokens, credentials, or tokenized URLs in MCP parameters or reports.
