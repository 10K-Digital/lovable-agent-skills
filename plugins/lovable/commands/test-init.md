---
description: Test wizard - scans your codebase, suggests test plans for your app's main actions, and sets up provider-neutral Preview testing in .lovable-agent/tests/.
---

# Initialize Preview Testing

Set up automated testing of this Lovable app in Preview mode via browser automation.

## Syntax

```
/lovable:test-init              # Full wizard
/lovable:test-init --refresh-token   # Only update the preview URL/token
```

## Instructions

1. **Read the testing skill** (`skills/testing/SKILL.md`) and its references for full context. The detailed procedures live in:
   - `skills/testing/references/test-wizard.md` - scanning + question flow (THE main procedure for this command)
   - `skills/testing/references/preview-access.md` - preview URL/token capture and storage
   - `skills/testing/references/test-plan-format.md` - file formats to generate

2. **Handle `--refresh-token`**: if this flag is present, skip the wizard - just ask for a fresh preview URL with token, process it per `preview-access.md`, update `.lovable-agent/config.json` and `.lovable-agent/preview-token.local`, confirm, and stop.

3. **Check for an existing workspace** at `.lovable-agent/tests/`, then check the legacy
   `.claude/lovable-claude/test/` path:
   - If it exists, ask:
     ```
     A test workspace already exists ([N] plans, last synced [date]).

     A) Update it (add missing plans for new features) → runs /lovable:test-sync
     B) Reconfigure settings only (access, automation toggles)
     C) Start over (archives existing plans to plans/archive/)

     Reply A, B, or C:
     ```

4. **Run the wizard** per `test-wizard.md`:
   - **Phase 1**: Scan the codebase (architecture-aware: `src/` for Vite SPA, `app/` for TanStack Start) for routes, forms/mutations, auth flows, edge function calls, roles, and existing unit tests
   - **Phase 2**: Present findings + suggested test plan list
   - **Phase 3**: Ask the guided questions ONE at a time (preview access, plan selection, profiles, per-plan refinements, automation settings)
   - **Phase 4**: Generate the workspace (folders, gitignore entry FIRST, token file, neutral config,
     plans, profiles, README) and add the Preview Testing Configuration section to `AGENTS.md` and
     `CLAUDE.md`
   - **Phase 5**: Verify preview access and offer to run the smoke suite

5. **Preview access notes** (critical):
   - The tokenized preview URL looks like `https://preview--[app].lovable.app/?__lovable_token=[JWT]`
   - User captures it: Lovable project → preview mode → **arrow icon at the top next to the address bar** → copy URL from the new tab
   - Token is valid **7 days** - decode `exp` from the JWT payload and store the expiry date in `.lovable-agent/config.json`
   - The token goes ONLY in `.lovable-agent/preview-token.local`, which MUST be in `.gitignore` before
     you write it. Never put the token in `AGENTS.md`, `CLAUDE.md`, `config.json`, commit messages, or
     chat output.
   - Alternatively the user can stay logged in to Lovable in Chrome (`access_method: browser-login`)

6. **CLAUDE.md section to add** (after the Yolo Mode section, or after Project Conventions if no yolo section):

   ```markdown
   ## Preview Testing Configuration

   > Tests run against the Lovable Preview app via browser automation.
   > Test plans live in `.lovable-agent/tests/` (legacy `.claude/lovable-claude/test/` remains supported).

   - **Status**: on
   - **Preview URL**: [base preview URL, no token]
   - **Access Method**: [token / browser-login]
   - **Token Captured**: [date] (valid ~7 days - run `/lovable:test-init --refresh-token` to renew)
   - **Test After Implementation**: [on / off]
   - **Test After Deploy**: [off / smoke / all]
   - **Last Test Sync**: [commit hash]

   **Commands:** `/lovable:test-run [TP-NNN | --all | --changed | --smoke]` · `/lovable:test-sync`

   **Maintenance rule:** when implementing a new feature, also add/update unit tests and
   test plans for it (or run `/lovable:test-sync`). Keep `covers:` paths in plans accurate.
   ```

7. **Final summary**: list created plans, profiles, access status, and the smoke-run offer.

## Safety

- Never block: if browser automation/preview access fails, still generate the plans - they double as manual test checklists
- Test credentials only in profiles - never real user passwords or production secrets
- This is a beta feature - mention that Lovable UI/preview behavior changes may require re-capturing the URL
