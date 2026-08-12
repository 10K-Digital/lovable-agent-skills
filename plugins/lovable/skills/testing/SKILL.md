---
name: testing
description: |
  Preview testing skill for Lovable projects. Activates when:
  - preview_testing: on in CLAUDE.md
  - Running /lovable:test-init, /lovable:test-run, or /lovable:test-sync commands
  - After implementing a new feature when test plans exist (suggest test updates)
  - After auto-deploy completes when test_after_deploy: on
  - Any mention of "test in preview", "preview testing", "test plans", "e2e tests in Lovable"

  Tests the running app in Lovable Preview mode via browser automation.
  Manages standardized test plans, test profiles, and results in .lovable-agent/tests/ while
  preserving .claude/lovable-claude/test/ as a backward-compatible alias.
  Keeps test plans in sync with the codebase as features are added.
---

# Preview Testing Skill

This skill tests Lovable apps **in Preview mode** - the live, running version of the app - using
browser automation. The canonical workspace is `.lovable-agent/tests/`; the legacy
`.claude/lovable-claude/test/` workspace remains supported and can be migrated with
`scripts/migrate-workspace.py`.

## When to Activate

1. **Preview testing is enabled** in `.lovable-agent/config.json` or the legacy CLAUDE.md
   (`Preview Testing → Status: on`)
2. **User runs testing commands**:
   - `/lovable:test-init` - Test wizard (scaffold workspace, create test plans)
   - `/lovable:test-run` - Execute test plans in Preview mode
   - `/lovable:test-sync` - Resync test plans with new/changed features
3. **After implementing a feature** (when test workspace exists):
   - Suggest adding/updating unit tests AND test plans for the new feature
   - If `test_after_implementation: on`, run the affected test plans automatically
4. **After auto-deploy** (yolo mode integration):
   - If `test_after_deploy: on`, run smoke-level test plans after deployment
5. **User mentions preview testing** in any form

## How Preview Access Works

Lovable Preview is the running app inside the Lovable editor. There are two ways to access it for testing:

### Method 1: Logged-in Browser (simplest)

If the user is logged in to Lovable in Chrome (Claude in Chrome extension), navigate directly to the Lovable project preview. No token needed.

### Method 2: Tokenized Preview URL (works without login)

Lovable exposes a shareable preview URL with an access token:

```
https://preview--[app-name].lovable.app/?__lovable_token=[JWT]
```

- The user gets this URL by opening their Lovable project in **preview mode** and clicking the **arrow icon at the top, next to the address bar** - this opens the preview in a new tab with the token in the URL.
- **The token is valid for 7 days.** After expiry, ask the user to capture a fresh URL.
- The token is a credential - **never commit it to git**. Store it in
  `.lovable-agent/preview-token.local` (gitignored); accept the legacy token path during migration.

See `references/preview-access.md` for full procedures: capture, storage, expiry detection, and re-prompting.

### Access Priority

1. Valid stored token → use tokenized preview URL (most reliable, no login dependency)
2. No/expired token + user logged in to Lovable in Chrome → use logged-in browser session
3. Neither → ask the user to either log in or provide a fresh preview URL with token
4. Fallback: provide manual test checklist for the user to run themselves (never block)

## Test Workspace Structure

All testing artifacts live in a standardized folder in the **user's project**:

```
.lovable-agent/
├── config.json
├── context.md
├── preview-token.local    # Preview token ONLY - gitignored
└── tests/
    ├── README.md
    ├── plans/
    ├── profiles/
    └── results/
```

The legacy alias remains readable:

```
.claude/lovable-claude/test/
├── README.md              # Explains the workspace (generated)
├── test-config.json       # Preview URL (no token), settings, coverage state
├── preview-token.local    # Preview token ONLY - gitignored, 7-day validity
├── plans/                 # Test plans (one file per plan)
│   ├── TP-001-user-signup.md
│   ├── TP-002-create-project.md
│   └── ...
├── profiles/              # Test user profiles (test accounts, personas, data)
│   ├── default.json
│   └── admin.json
└── results/               # Test run results (one file per run)
    └── 2026-06-10-TP-001.md
```

See `references/test-plan-format.md` for the standardized formats of every file type.

## Core Functionality

### 1. Test Wizard (`/lovable:test-init`)

Guided creation of the test workspace:
1. Scaffold `.lovable-agent/tests/` and `.lovable-agent/config.json` structure
2. Capture preview URL + token (or detect logged-in browser)
3. Scan the codebase to identify the app's **main user actions** (routes, forms, auth flows, CRUD operations, edge function calls)
4. Suggest test plans for each main action, ask guided questions to refine them
5. Create test user profiles
6. Write standardized test plan files
7. Record coverage state (git commit hash) in `.lovable-agent/config.json` under `testing`

See `references/test-wizard.md` for the complete wizard procedure.

### 2. Test Execution (`/lovable:test-run`)

Execute test plans against the Preview app via browser automation:
- Navigate to preview (tokenized URL or logged-in session)
- Execute each test plan step-by-step (clicks, form fills, navigation)
- Verify expected results (UI state, console errors, network responses)
- Write results to `results/` and report a summary

Modes:
- `--all`: run every test plan (planned end-to-end run)
- `--changed`: run only plans affected by recent changes (after each implementation)
- `--smoke`: run only plans tagged `smoke`
- `[plan-id]`: run one specific plan

See `references/test-execution.md` for browser automation workflows.

### 3. Test Resync (`/lovable:test-sync`)

Keep tests in sync with the codebase as features are added:
1. Compare current codebase against `testing.last_synced_commit` in `.lovable-agent/config.json`
2. Identify new/changed features (new routes, components, edge functions, migrations)
3. Map them against existing test plans → find **coverage gaps**
4. Suggest new test plans and updates to stale ones
5. Also check unit test coverage gaps (if the project has a test framework)
6. Update `.lovable-agent/config.json` with the new testing sync point

### 4. Continuous Test Maintenance (after each feature)

When preview testing is enabled and Claude implements a new feature in the project:

1. **Add/update unit tests** for the new code (if the project has a test framework)
2. **Add/update test plans** covering the new user-facing behavior
3. If `test_after_implementation: on` → run the affected test plans in Preview immediately
4. If `test_after_implementation: off` → remind the user: "New feature lacks a test plan - run `/lovable:test-sync` to update coverage"

This keeps the test suite alive instead of letting it rot.

## Configuration in CLAUDE.md

The skill reads these fields from the user's CLAUDE.md:

```markdown
## Preview Testing Configuration

- **Status**: on
- **Preview URL**: https://preview--my-app.lovable.app
- **Access Method**: token   # token | browser-login
- **Token Captured**: 2026-06-10 (valid ~7 days)
- **Test After Implementation**: on   # run affected plans after each feature
- **Test After Deploy**: smoke        # off | smoke | all - run after yolo auto-deploy
- **Last Test Sync**: [commit hash]
```

**Configuration options:**
- **Status**: Enable/disable preview testing entirely
- **Access Method**: `token` (tokenized preview URL) or `browser-login` (user logged in to Lovable)
- **Test After Implementation**: Run affected test plans automatically after implementing each feature
- **Test After Deploy**: What to run after yolo auto-deploy (`off`, `smoke`, or `all`)

The actual token is NEVER in `AGENTS.md`, `CLAUDE.md`, or config JSON - only in the ignored
`.lovable-agent/preview-token.local`.

## Integration with Other Features

### With Yolo Mode (auto-deploy)

When both yolo mode and preview testing are enabled, the post-deploy verification gains a fourth level:

- Level 1-3: existing deployment verification (logs, console, functional) - see yolo skill
- **Level 4: Preview test plans** - run `smoke` (or `all`) test plans against the Preview app per `Test After Deploy` setting

### With Auto-Push

After auto-push of frontend changes (which sync to Lovable in 1-2 minutes), wait for sync before running preview tests so the Preview reflects the pushed code. See `references/test-execution.md` → "Sync wait".

### With /lovable:init

`/lovable:init` asks about preview testing (Question 8.7) and can capture the preview URL/token during setup, then offers to run `/lovable:test-init` to build the initial test plans.

## Error Handling

**Golden rule: never block the user.** Every automation failure has a manual fallback.

**Token expired:**
```
🔑 Preview token expired (captured [date], valid 7 days)

To capture a fresh one:
1. Open your Lovable project in preview mode
2. Click the arrow icon at the top, next to the address bar
3. Copy the URL from the new tab (contains ?__lovable_token=...)
4. Paste it here

Or log in to Lovable in Chrome and I'll use your session instead.
```

**Browser automation unavailable:**
```
❌ Browser automation unavailable (Claude in Chrome extension required)

Manual test checklist for [plan-id]:
[numbered steps + expected results from the plan]

Report results back and I'll record them in results/.
```

**Preview app shows error / blank page:**
- Capture console errors and screenshot description
- Check if a deploy/sync is still in progress (wait + retry once)
- Report findings with suggested fixes - do not mark tests passed

**Test failure:**
- Record exact step that failed, expected vs actual, console/network errors
- Write a FAIL result file
- Offer to investigate and fix the underlying code

## Reference Files

1. **`references/preview-access.md`** - Capturing, storing, and validating preview URLs and tokens; access priority; expiry handling
2. **`references/test-plan-format.md`** - Standardized formats for test plans, profiles, config, results, and the workspace README
3. **`references/test-wizard.md`** - Codebase scanning for main user actions; guided question flow; plan generation
4. **`references/test-execution.md`** - Browser automation workflows for executing plans in Preview; verification; results reporting

---

*This skill closes the loop: code → push → deploy → **test in the real running app** → fix → repeat.*
