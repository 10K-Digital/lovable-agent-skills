---
description: Run test plans against your app in Lovable Preview mode via browser automation. Supports single plan, smoke, changed-only, or full end-to-end runs.
---

# Run Preview Tests

Execute test plans from `.lovable-agent/tests/plans/` against the live Preview app. Read the legacy
`.claude/lovable-claude/test/plans/` path when migration has not happened yet.

## Syntax

```
/lovable:test-run               # Ask which scope to run (smoke / changed / all / pick)
/lovable:test-run TP-003        # Run one specific plan
/lovable:test-run --smoke       # Run plans tagged "smoke" (fast verification)
/lovable:test-run --changed     # Run plans covering files changed since last sync/run
/lovable:test-run --all         # Full end-to-end run of all active plans
```

## Instructions

1. **Read the testing skill** (`skills/testing/SKILL.md`). The execution procedure is in `skills/testing/references/test-execution.md` - follow it exactly. Access handling is in `references/preview-access.md`.

2. **Prerequisites** (in order):
   - Workspace exists (`.lovable-agent/config.json` with `testing.enabled`) - else point to `/lovable:test-init`
   - Preview access valid: check `token_expires`; if expired, try logged-in session, else prompt for fresh URL (arrow icon next to the preview address bar; token lasts 7 days)
   - Browser automation available (Claude in Chrome) - else manual fallback checklist
   - Sync state: if a push just happened, apply the sync wait before testing

3. **Select plans** per the table in `test-execution.md`. With no arguments, ask:
   ```
   What should I run?
   A) Smoke suite ([N] plans, ~[est] min)
   B) Changed since last sync ([N] plans)
   C) Everything ([N] plans)
   D) Pick specific plans
   ```

4. **Execute each plan**:
   - Resolve the profile, substitute `{profile.*}` / `{timestamp}` placeholders
   - Navigate to preview (append `?__lovable_token=...` on first navigation if using token access)
   - Run each step, verify each Expected Result (UI / URL / console / network)
   - On failure: capture details, stop that plan, continue to the next
   - Honor `[MANUAL]` steps - never automate payments or destructive operations

5. **Record and report**:
   - Write `results/[date]-[slug].md` per `test-plan-format.md`
   - Update `last_run` / `last_result` in each plan's frontmatter
   - Show the summary (passed/failed, failure details with diagnosis + suggested fix)
   - For code-level failures, offer to investigate and fix now, then re-run the failed plan

## Safety

- Tests target **Preview**, not production
- Never echo the token anywhere
- Failures never block - report, suggest fixes, provide manual checklist as fallback
