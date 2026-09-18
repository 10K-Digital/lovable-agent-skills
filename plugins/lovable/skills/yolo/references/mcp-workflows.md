# Credit-Efficient Lovable MCP Workflow

The official endpoint is `https://mcp.lovable.dev`. Treat each Lovable MCP invocation as potentially
charged. MCP is a submission fallback, not a discovery or inspection interface.

## Before calling

1. Read the project ID from `.lovable-agent/config.json` or its configured Lovable URL; use legacy
   `CLAUDE.md` only when neutral config is absent.
2. Inspect code and changed files locally. Inspect database state, secret names/status, functions,
   logs, and configuration in browser **Cloud** pages.
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

## Fallbacks

- Unsupported operation or timeout: browser submission, then a manual consolidated prompt.
- Authentication failure: stop retries and request re-authentication or provide the manual prompt.
- Ambiguous completion: report accepted/unverified and give a browser Cloud verification step.
- Exact UI remediation explicitly marked zero credits: use it for that failure/security item only.
  Otherwise fix locally.

Never place secrets, preview tokens, credentials, or tokenized URLs in MCP parameters or reports.
