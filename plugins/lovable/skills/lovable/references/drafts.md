# Lovable Drafts

Drafts are Lovable's parallel versions of a project (released September 2026, extended to AI/MCP
clients and draft backends in November 2026). A draft is a copy of the project with its own chat,
preview, and edits. Nothing in a draft reaches the project until someone **accepts** it, and
accepting does **not** publish: the published app changes only when the main version is published.

Sources: <https://docs.lovable.dev/features/drafts>,
<https://docs.lovable.dev/integrations/lovable-mcp-server>, and the Lovable announcement
<https://lovable.dev/blog/introducing-drafts> (November 16, 2026). Re-check these pages when behavior
looks different; the docs and the announcement have described draft data isolation differently.

## Mental model

| Concept | Behavior |
| --- | --- |
| Draft | Branch-like copy with its own chat, preview URL, and edits |
| Update | Brings newer main-version edits into the draft (rebase-like; Lovable reworks overlapping edits) |
| Accept | Updates the draft if needed, then fast-forward merges it into the main version as one named group of edits; the draft becomes read-only |
| Delete / reject | Discards the draft's code edits; it cannot be restored |
| Publish | Separate step from the main version only; a draft has no Publish button |

- Drafts are available on all plans. Anyone with edit access can create, build in, update, accept,
  and delete drafts; view-only users can only view them. There is no documented limit on drafts.
- Lovable automatically removes a draft with no edits after 24 hours. Accepted drafts stay in
  history but cannot be built on; restore earlier versions through version history instead.
- When several drafts are accepted, Lovable processes them one at a time in an accept queue.

## Git sync

**Drafts do not support Git sync.** A draft never appears as a branch in the connected repository,
and its code reaches GitHub only after acceptance, when the merged edits sync to the default branch
like any other change (`get_draft` reports `merged_commit_sha`, the commit pushed to `main`).

Consequences for local agents:

- Do not look for, create, or push a Git branch to represent a Lovable draft. Local feature branches
  still do not sync with Lovable; only the configured `main` branch does.
- After an accept, pull `main` (respecting the normal clean-worktree and divergence rules) before
  continuing local work, so local code includes the accepted edits.
- Avoid editing the same files locally on `main` while a draft that touches them is pending. Lovable
  rebases the draft onto main on accept, but local and draft work should not race.

## Backend and data

Treat data isolation as **unknown until verified**:

- The MCP `create_draft`/`get_draft` results report the draft's backend in `backend_kind`, and the
  tool documentation warns that a draft **can share the live database**. Read `backend_kind` before
  any data-writing test in a draft.
- Lovable's November 16, 2026 announcement describes drafts on the built-in backend getting their own
  backend copy with example data that is cleared on accept or delete. The drafts documentation still
  says a draft uses the project's real data. Projects connected to their own Supabase write to the
  live database from drafts.
- If `backend_kind` (or the UI) does not clearly show an isolated draft backend, treat every insert,
  update, or delete performed in the draft preview as a **production write**: create clearly named
  test records, never modify existing records, and remember that deleting or rejecting the draft
  does **not** undo shared-database changes.

Schema and backend rules from drafts:

- Lovable prepares schema changes in a draft and applies them to the project's database **on
  accept**, then describes them in the main chat. Draft pages that depend on new tables may error in
  the draft preview until acceptance.
- Only **additive** schema changes are made from drafts. Lovable will not drop, rename, or change the
  type of a table or column from a draft; it adds columns and copies data, or points to the SQL editor
  (More → Database → Manage → SQL editor). Destructive changes keep the normal confirmation gate.
- Backend (edge) function code can be edited in a draft, but Lovable deploys functions **only from
  the main version**, after acceptance.
- Main-version-only changes: sign-in methods and social providers, secrets, file-storage settings
  (such as bucket visibility), enabling AI features, payments, email sending/domains, and enabling the
  built-in backend. A draft request for these is redirected to main.

## Credits

Messages sent in a draft cost the same credits as messages in main. Creating, updating, accepting,
and deleting drafts use no credits; an idle draft costs nothing. Through the MCP server, only
`create_project` and `send_message` consume credits; draft management tools are free.

## When to use a draft

Prefer a draft (when `deploy.use_drafts` is `prefer`, or when the user asks) for hosted Lovable work
that the user should review before it lands on main:

- exploratory or larger UI/feature changes requested from Lovable's hosted agent;
- comparing two approaches side by side;
- changes that need Lovable-side schema additions the user wants to review first.

Do **not** use a draft for: plain local edits (do them locally and push to `main`), main-only
operations listed above, edge-function deployment (main only), or destructive database work.

## MCP workflow

Official MCP tools (`https://mcp.lovable.dev`): `create_draft`, `list_drafts`, `get_draft`,
`rename_draft`, `get_diff` (with `draft_id`), `send_message` (with `draft_id`), `accept_draft`,
`reject_draft`. Read each tool's schema before calling it.

1. **Create**: `create_draft(project_id, label)`. Labels are up to 80 characters. An identical call
   within about two minutes returns the same draft; use a distinct label for another draft. Creating
   a draft does not send a message or start a build. Record `backend_kind`.
2. **Build**: `send_message(project_id, message, draft_id)` with one consolidated, minimal prompt
   (see [credit efficiency](credit-efficiency.md) and [instruction boundaries](instruction-boundaries.md)).
   On timeout, poll `get_message` with the original message ID; never resend.
3. **Handle pauses**: `awaiting_input` needs a human decision. Show the user the pending tool and its
   parameters, then pass their decision with `respond_to_approval`. Secret forms and credit
   check-ins are answered only in the Lovable editor. A new `send_message` supersedes a pause and
   rejects the pending tool, so never use it to answer one.
4. **Review**: `get_diff(project_id, draft_id)` (use `files_only` first for large changes) and the
   draft preview URL from `get_draft`. Summarize the change for the user in one line (≤ 300 chars).
5. **Accept** only after the user has reviewed the draft and explicitly accepted it:
   `accept_draft(project_id, draft_id, summary)`, passing the summary that was shown to the user.
   Outcomes: `merged`, `merged_with_warning` (report the reason), `failed` (report the reason; if
   `update_required` without `can_retry_accept`, update the draft first), `needs_attention` (the user
   must retry setup from the draft), `rejected`, or `pending` — on `pending`, call
   `get_draft(..., wait_seconds)` and never call `accept_draft` again.
6. **After merge**: pull `main` locally, then deploy edge functions or publish from main only if the
   task requires it and the normal authorization rules allow it.
7. **Discard**: `reject_draft` removes the draft's code edits without merging; it does not undo writes
   already made to a shared database. Confirm with the user before rejecting a draft that has edits.

## Authorization

- Creating a draft, building in it, and reading its diff follow the normal
  [prompt authorization](prompt-authorization.md) rules for Lovable prompts (YOLO or explicit request).
- **Accepting a draft always requires the user's explicit acceptance of that draft,
  even with YOLO on.** The Lovable MCP server requires it, and acceptance can change the shared database schema.
  YOLO authorizes publication through `main` for local commits, not accepting hosted drafts.
- Never accept, reject, or delete a draft created by another person without their owner's or the
  user's explicit instruction. Lovable shows who is working in each draft.
- Publishing after acceptance is a separate step and follows the normal publication rules.

## Browser workflow

Open the draft switcher by clicking the project name at the top of the editor, then **New draft**.
Rename, update, accept, and delete from the draft's ⋮ menu; **Accept** also appears at the top right
of the editor while viewing a draft. The command palette (Cmd/Ctrl+K) lists drafts under **Drafts**.
Status indicators: spinner (running), gray dot (updates available), blue dot (new changes), orange
question mark (Lovable waits for an answer), red triangle (last action failed; hover for the reason).
Each draft preview has its own address, so preview sign-in may need repeating.
