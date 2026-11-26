---
name: lovable-drafts
description: >-
  Work with Lovable drafts from any coding agent. Use when the user mentions drafts, wants to try a
  Lovable change without touching the main version, compare approaches, review or accept a draft,
  or when `deploy.use_drafts` is `prefer`. Covers the MCP draft tools, Git sync limits, data
  isolation checks, and acceptance gates.
---

# Lovable Drafts

Read [the drafts reference](../lovable/references/drafts.md) before creating, building in,
accepting, or rejecting a draft. Apply [prompt authorization](../lovable/references/prompt-authorization.md),
[credit efficiency](../lovable/references/credit-efficiency.md), and
[instruction boundaries](../lovable/references/instruction-boundaries.md).

Core rules:

1. A draft is a hosted, branch-like copy of the Lovable project. It is **not** a Git branch and does
   not sync to GitHub; its code reaches `main` only when the draft is accepted. Keep doing ordinary
   code changes locally and pushing to the configured `main` branch.
2. Use a draft only for work done by Lovable's hosted agent that the user should review first. Do not
   use drafts for main-only operations (secrets, sign-in methods, storage settings, payments, email,
   enabling AI or the built-in backend) or for edge-function deployment, which happens from main.
3. Before any data-writing test, read `backend_kind` from `create_draft`/`get_draft`. Unless it
   clearly shows an isolated draft backend, treat draft writes as production writes; rejecting or
   deleting a draft does not undo them.
4. Draft schema changes are additive and are applied to the project database on accept. Destructive
   schema changes keep the normal confirmation gate and are not made from drafts.
5. Build with one consolidated `send_message(..., draft_id)`; review with `get_diff(draft_id)` and the
   draft preview. Answer `awaiting_input` pauses only with the user's decision via
   `respond_to_approval`; never answer a pause with another `send_message`.
6. **Accept only on the user's explicit acceptance of that draft, even when YOLO is on.** Pass the
   summary shown to the user to `accept_draft`. On `pending`, wait with `get_draft`; never accept
   twice. After `merged`, pull `main` locally before continuing.
7. Accepting does not publish. Publishing and edge-function deployment remain separate main-version
   steps under the normal authorization rules.
8. Report the draft name, `backend_kind`, diff summary, preview link, and outcome (`merged`,
   `merged_with_warning`, `failed`, `needs_attention`, `rejected`, or `pending`). Never claim an
   accept finished from a `pending` result.
