# Test Execution: Running Plans in Lovable Preview

Browser automation workflow for `/lovable:test-run` and automatic post-implementation / post-deploy runs.

## Prerequisites Check

Before any run:

1. **Workspace exists**: `.lovable-agent/config.json` with `testing.enabled` present
   - If not: "No test workspace found. Run `/lovable:test-init` first."
2. **Preview access valid**: per `preview-access.md` (token unexpired, or logged-in session)
3. **Browser automation available**: Claude in Chrome extension connected
   - If not → manual fallback (below)
4. **Code is synced**: if there are unpushed commits or a push happened < `sync_wait_seconds` ago, the Preview may not reflect the latest code (see "Sync wait")

## Selecting Plans

| Invocation | Plans selected |
|------------|----------------|
| `/lovable:test-run TP-003` | That plan only |
| `/lovable:test-run --smoke` | `status: active` plans tagged `smoke` |
| `/lovable:test-run --all` | All `status: active` plans |
| `/lovable:test-run --changed` | Active plans whose `covers:` paths intersect files changed since `last_synced_commit` (or since the last run if more recent): `git diff --name-only [ref] HEAD` |
| Post-implementation trigger | Same as `--changed` scoped to the files just edited |
| Post-deploy trigger | Per `test_after_deploy` config: smoke or all |

Run order: `smoke` plans first, then by priority (high → low), then by ID. If a login-dependent plan is selected, ensure an auth plan or login step runs first in the same session.

## Sync Wait

The Preview reflects code synced from GitHub. After a push:

```
1. Note push time
2. Wait sync_wait_seconds (default 120s) OR poll:
   - Reload preview, check for a marker of the new change (new text/element)
   - Poll every 20s, max 3 minutes
3. If unsure whether sync landed, say so in the result:
   "⚠️ Could not confirm Preview reflects commit abc1234 - results may be stale"
```

## Execution Workflow (per plan)

### Performance: model and tool choices

Same hybrid approach as the yolo skill:
- **Haiku-level operations**: clicking refs, `form_input` fills, key presses, navigation, polling
- **Sonnet-level operations**: page understanding, deciding pass/fail, error diagnosis
- Prefer `read_page`/`find` + refs over screenshots; `form_input` over click+type

### Steps

1. **Resolve profile**: load `profiles/[plan.profile].json`; substitute `{profile.xxx}` and `{timestamp}` placeholders in steps

2. **Navigate to start**:
   - URL = `preview_url` + plan's starting route
   - Append `?__lovable_token=[token]` on the FIRST navigation of the session (token sets a session; subsequent navigations within the tab usually don't need it - re-append if access is lost)
   - Wait for app render (root populated), up to 30s cold start

3. **Open observation channels**:
   - Clear/read console messages baseline
   - Note network request baseline

4. **Execute each step** from the plan's steps table:
   - Perform the Action (click / fill / navigate / wait)
   - Verify the Expected Result:
     - **UI**: element/text present via `find` or `read_page`
     - **URL**: current URL matches expectation
     - **Console**: no new errors (ignore third-party noise per yolo testing-procedures filtering rules)
     - **Network**: expected request fired with expected status
   - On match → step PASS, continue
   - On mismatch → retry verification once after 3s (async rendering), then step FAIL
   - `[MANUAL]` steps → stop automation, ask the user to perform it, or mark plan `blocked` if unattended

5. **On step failure**:
   - Capture: failing step number, expected vs actual, console errors, failed network requests (status + response body if readable)
   - Stop the plan (later steps depend on earlier ones)
   - Mark plan FAIL, continue with the NEXT plan (don't abort the run)

6. **Cleanup**: perform the plan's Cleanup section (e.g., delete created test entities) when feasible

## Recording Results

After the run:

1. Write `results/[YYYY-MM-DD]-[run-slug].md` per `test-plan-format.md`
2. Update each executed plan's frontmatter: `last_run`, `last_result`
3. Report a summary to the user:

```
🧪 Preview Test Run - smoke suite (3 plans)

✅ TP-001 User signup with email (38s)
✅ TP-002 Login and logout (21s)
❌ TP-004 Invite team member - failed at step 3
   Expected: success toast
   Actual: POST /functions/v1/send-invite → 500
   "RESEND_API_KEY is not configured"

Result: 2/3 passed
📄 Full report: .lovable-agent/tests/results/2026-06-10-smoke.md

Suggested fix for TP-004: add RESEND_API_KEY in Cloud → Secrets, redeploy, re-run:
/lovable:test-run TP-004
```

4. **Offer to fix failures**: when a failure traces to code (not config), offer to investigate and fix it now. After fixing + pushing, re-run the failed plan.

## Manual Fallback

If browser automation is unavailable or repeatedly fails, never block:

```
❌ Can't run automated preview tests ([reason])

Manual checklist for TP-001 (User signup with email):
1. Open [preview_url with token note]
2. Go to /signup - expect: form with email + password
3. Fill test+[timestamp]@example.com / TestPass!2026 - expect: no validation errors
4. Click "Sign up" - expect: redirect to /dashboard
5. Check DevTools console - expect: no errors

Tell me the results and I'll record them in results/.
```

If the user reports results, write the result file with `Trigger: manual (user-executed)`.

## Safety Rules

- **Test against Preview, not production** - unless the user explicitly asks for a production smoke check
- **Never execute real payments, real bulk sends, or destructive operations on non-test data** - those steps are `[MANUAL]` by format rules; honor them
- **Only test apps the user owns** - the preview URL/token comes from the user's own Lovable project
- **Don't echo tokens** in output, results files, or commit messages
- Test data should be clearly synthetic (test+ emails, "Test" prefixed names) so it's identifiable and cleanable
