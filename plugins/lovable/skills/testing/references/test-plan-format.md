# Test Workspace: Standardized File Formats

Every file in `.lovable-agent/tests/` follows these formats. Always use them - consistency is what lets
`/lovable:test-run` and `/lovable:test-sync` work reliably across sessions. The legacy
`.claude/lovable-claude/test/` path is accepted during migration.

## Folder Layout

```
.lovable-agent/tests/
├── README.md              # Workspace explanation (template below)
├── (config lives at ../config.json) # Settings + coverage state
├── preview-token.local    # Token only - MUST be gitignored
├── plans/
│   └── TP-[NNN]-[slug].md
├── profiles/
│   └── [name].json
└── results/
    └── [YYYY-MM-DD]-[run-slug].md
```

## `.lovable-agent/config.json` testing section

```json
{
  "version": 1,
  "preview_url": "https://preview--my-app.lovable.app",
  "access_method": "token",
  "token_captured": "2026-06-10",
  "token_expires": "2026-06-17",
  "production_url": "https://my-app.lovable.app",
  "test_after_implementation": true,
  "test_after_deploy": "smoke",
  "last_synced_commit": "abc1234",
  "last_synced_at": "2026-06-10T14:30:00Z",
  "plan_counter": 7,
  "default_profile": "default",
  "sync_wait_seconds": 120
}
```

Field notes:
- `access_method`: `"token"` or `"browser-login"`
- `token_captured` / `token_expires`: dates only - the token itself lives in `preview-token.local`
- `last_synced_commit`: git hash at last `/lovable:test-init` or `/lovable:test-sync` - the baseline for detecting untested features
- `plan_counter`: highest TP number issued (next plan = counter + 1)
- `test_after_deploy`: `"off"`, `"smoke"`, or `"all"`
- `sync_wait_seconds`: how long to wait after git push before testing (GitHub → Lovable sync time)

## Test Plan: plans/TP-NNN-slug.md

One file per plan. ID format `TP-001`, `TP-002`, ... with a kebab-case slug.

```markdown
---
id: TP-001
title: User signup with email
feature: Authentication
priority: high          # high | medium | low
tags: [smoke, auth]     # "smoke" tag = included in smoke runs
profile: default        # profile from profiles/ to use
covers:                 # code this plan covers (used by /test-sync)
  - src/pages/Signup.tsx
  - src/hooks/useAuth.ts
  - supabase/functions/send-welcome
status: active          # active | draft | deprecated
created: 2026-06-10
updated: 2026-06-10
last_run: 2026-06-10
last_result: pass       # pass | fail | blocked | never-run
---

# TP-001: User signup with email

## Objective
Verify a new user can sign up with email/password and lands on the dashboard.

## Preconditions
- Preview app accessible
- Email used must not already exist (use timestamped email from profile pattern)

## Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Navigate to `/signup` | Signup form visible with email, password fields |
| 2 | Fill email with `{profile.email_pattern}` and password `{profile.password}` | Fields accept input, no validation errors |
| 3 | Click "Sign up" button | Loading state, then redirect to `/dashboard` |
| 4 | Check dashboard | Welcome message shows; no console errors |
| 5 | Check network | POST to auth endpoint returned 200 |

## Cleanup
- None required (test accounts are throwaway)

## Notes
- Welcome email sending (send-welcome function) is verified only by absence of errors - actual delivery is out of scope.
```

Conventions:
- **Steps table is the contract**: each row has one Action and one verifiable Expected Result
- `{profile.xxx}` placeholders resolve from the profile JSON at run time
- `covers:` paths let `/test-sync` map code changes → affected plans (`--changed` mode)
- Tag `smoke` for the minimal always-run set (post-deploy verification)
- Destructive/paid actions (real payments, mass emails): mark the step `[MANUAL]` - automation stops there and asks the user, or skips with `blocked` status

## Test Profile: profiles/name.json

Test personas and accounts. **Test credentials only - never real user passwords or production secrets.**

```json
{
  "name": "default",
  "description": "Standard throwaway test user",
  "email_pattern": "test+{timestamp}@example.com",
  "email": "claude-test@example.com",
  "password": "TestPass!2026",
  "role": "user",
  "seed_data": {
    "display_name": "Claude Test",
    "company": "Test Co"
  },
  "notes": "email_pattern with {timestamp} generates unique signup emails; fixed email is for login tests (account must exist in preview DB)."
}
```

- `{timestamp}` in patterns → replace with unix timestamp at run time for uniqueness
- An `admin.json`, `viewer.json`, etc. for role-based testing
- If a profile's fixed account doesn't exist yet, the wizard/run should create it via the signup flow first (and note it)

## Test Result: results/YYYY-MM-DD-run-slug.md

One file per run (a run may cover multiple plans). Slug examples: `2026-06-10-smoke`, `2026-06-10-TP-001`, `2026-06-10-all`.

```markdown
# Test Run: 2026-06-10 - smoke suite

- **Trigger**: post-deploy (yolo) | manual | post-implementation
- **Preview URL**: https://preview--my-app.lovable.app
- **Access**: token (expires 2026-06-17)
- **Commit tested**: abc1234
- **Plans run**: 3 | ✅ 2 pass | ❌ 1 fail | ⏭️ 0 blocked

## TP-001: User signup with email - ✅ PASS
All 5 steps passed. Duration: 38s.

## TP-002: Create project - ✅ PASS
All 4 steps passed. Duration: 22s.

## TP-004: Send invitation - ❌ FAIL
- Failed at step 3: "Click Send invite"
- Expected: success toast appears
- Actual: console error `POST /functions/v1/send-invite 500`
  `{"error":"RESEND_API_KEY is not configured"}`
- Diagnosis: missing secret in Lovable Cloud
- Suggested fix: add RESEND_API_KEY in Cloud → Secrets, then redeploy

## Follow-ups
- [ ] Configure RESEND_API_KEY and re-run TP-004
```

After each run, also update each plan's frontmatter: `last_run`, `last_result`.

## README.md (workspace)

Generated once at scaffold time:

```markdown
# Lovable Preview Test Workspace

Managed by the lovable-claude-code plugin (`/lovable:test-*` commands).

- `.lovable-agent/config.json` - settings, preview URL, coverage state
- `.lovable-agent/preview-token.local` - preview access token (gitignored, valid 7 days)
- `plans/` - test plans (TP-NNN). Edit freely; keep the steps table format.
- `profiles/` - test user personas. Test credentials only - never real secrets.
- `results/` - test run reports (newest = current state)

Commands:
- `/lovable:test-run [TP-NNN | --all | --changed | --smoke]` - run tests in Lovable Preview
- `/lovable:test-sync` - update plans for new/changed features
- `/lovable:test-init` - re-run the setup wizard
```

## ID and Naming Rules

- Plan IDs: `TP-` + zero-padded 3-digit number, never reused (deprecate, don't delete, plans that no longer apply: set `status: deprecated`)
- Slugs: kebab-case, short, from the title
- Result files: ISO date prefix for sorting
- Profile names: lowercase, single word where possible
