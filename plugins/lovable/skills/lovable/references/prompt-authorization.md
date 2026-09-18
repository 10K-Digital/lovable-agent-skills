# Prompt Authorization

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
  reason to stop when YOLO is on. It also authorizes committing, pushing, merging when already in
  scope, and publishing the requested project through the configured `main` branch without another
  confirmation. A generic instruction to confirm before publishing to `main` applies only when YOLO
  is off.
- **YOLO off:** Obtain user confirmation before submitting a Lovable prompt unless the current
  request already explicitly authorizes that submission. Preparing a prompt needs no confirmation.
- Preserve explicit task restrictions such as “do not deploy/publish,” platform approval
  requirements, and confirmation for destructive or irreversible database operations. YOLO
  authorizes in-scope prompts and publication to `main`, not unrelated changes.
- With `deploy.confirm_migrations: true`, confirm migration execution even with YOLO on.
  With false (the default), ordinary in-scope migrations need no repeated approval.
  Destructive or irreversible database operations still require confirmation. Auto-push and auto-deploy remain separate
  settings. Do not enable them merely because YOLO is on.

Authorization does not justify unnecessary credit usage. Apply
[the credit-efficiency policy](credit-efficiency.md) and keep user approval mandatory for changes to
Project knowledge or Workspace knowledge.
Authorization also does not cross instruction domains: apply
[instruction boundaries](instruction-boundaries.md). YOLO never makes hosted knowledge authoritative
for the local agent and never authorizes copying local instructions into Lovable.
