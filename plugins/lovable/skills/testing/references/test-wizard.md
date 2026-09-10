# Test Wizard: Scanning and Guided Plan Creation

Procedure for `/lovable:test-init` - scan the codebase, identify the app's main user actions, and guide the user through creating test plans.

## Phase 1: Codebase Scan

Goal: build a candidate list of **main user actions** the app supports. Scan based on architecture (detected via `vite.config.ts` vs `app.config.ts`, same as `/lovable:init`).

### 1. Routes / Pages

- *Vite SPA*: parse `src/App.tsx` for `<Route path=...>`; list `src/pages/*.tsx`
- *TanStack Start*: list `app/routes/**/*.tsx` (filename = URL)

Each route is a candidate test surface. Classify:
- Public pages (landing, about) → low priority "renders correctly" plans
- Auth pages (login, signup, reset) → high priority flow plans
- App pages (dashboard, settings, CRUD views) → medium/high priority flow plans

### 2. Forms and Mutations

Search for user actions that change state:
- `onSubmit`, `<form`, `useMutation`, `.insert(`, `.update(`, `.delete(`, `.upsert(`
- Supabase auth calls: `signUp`, `signInWithPassword`, `signInWithOAuth`, `signOut`, `resetPasswordForEmail`
- Edge function invocations: `supabase.functions.invoke("name")`, `fetch(".../functions/v1/`

Each distinct mutation = a candidate test plan, with `covers:` pointing at the implementing files.

### 3. Edge Functions and Migrations

- List `supabase/functions/*` - each function that's user-triggered gets covered by the flow plan that invokes it; note functions with NO frontend caller (webhook-style) as "manual/API-only test" candidates
- Skim `supabase/migrations/` for core tables → informs what entities CRUD plans should cover

### 4. Roles and Profiles

Detect role/permission patterns (`role`, `is_admin`, RLS-related code, route guards). Each distinct role → candidate test profile.

### 5. Existing unit tests

Check for test framework (`vitest`, `jest`, `@testing-library` in package.json; `*.test.ts(x)` files). Record whether unit tests exist - the maintenance loop ("add unit tests + test plans per feature") needs this.

## Phase 2: Present Findings and Suggest Plans

Present a compact summary, then the suggested plan list:

```
📋 Test Wizard - here's what I found:

Routes: 8 (2 public, 3 auth, 3 app)
User actions detected:
- Sign up / Log in / Log out (src/hooks/useAuth.ts)
- Create / edit / delete project (src/pages/Projects.tsx)
- Invite team member → send-invite edge function
- Update profile settings (src/pages/Settings.tsx)
Roles detected: user, admin
Unit tests: none detected

Suggested test plans:
1. TP-001 User signup with email          [smoke, high]
2. TP-002 Login and logout                [smoke, high]
3. TP-003 Create a project                [smoke, high]
4. TP-004 Edit and delete a project       [medium]
5. TP-005 Invite team member              [high] (covers send-invite function)
6. TP-006 Update profile settings         [medium]
7. TP-007 Public pages render             [smoke, low]

Accept all, or tell me which to add/remove/change? (e.g. "all", "1-5 only", "add: password reset")
```

## Phase 3: Guided Questions

Ask ONE at a time. Skip questions already answered by config/CLAUDE.md.

### Q1: Preview access (skip if already configured)
```
How should I access your Lovable Preview for testing?

A) Paste a preview URL with token (recommended - works without login)
   Get it: open your Lovable project in preview mode, click the arrow
   icon at the top next to the address bar, copy the URL from the new tab.
   (Token is valid 7 days; I'll store it gitignored and ask again when it expires.)

B) I'm logged in to Lovable in Chrome - use my session

Reply A (then paste URL) or B:
```
Process per `preview-access.md`.

### Q2: Plan selection
(The accept/modify question from Phase 2.)

### Q3: Test profiles
```
I'll create test user profiles for: [detected roles]

For each, I need test credentials (TEST accounts only - never real passwords):
- Should I generate throwaway accounts via your signup flow? (recommended)
- Or do you have existing test accounts to use? (provide email/password per role)
```

### Q4: Per-plan refinement (only for plans needing input)
For plans with ambiguous expected results or required test data, ask targeted questions:
```
For TP-005 (Invite team member):
- What should happen after sending an invite? (toast? email? pending list entry?)
- Safe to send invites to test+...@example.com addresses? (yes/no)
```

### Q5: Automation settings
```
When should tests run?

A) After each implementation (I run affected plans automatically) + manual runs
B) Manual only (/lovable:test-run when you ask)

And after yolo auto-deploys (if yolo enabled): off / smoke / all?
```

## Phase 4: Generate the Workspace

1. Create `.lovable-agent/tests/{plans,profiles,results}` directories
2. Ensure `.gitignore` contains `.lovable-agent/preview-token.local`
3. Write `preview-token.local` (if token provided) - per `preview-access.md`
4. Write `.lovable-agent/config.json` with testing settings + `last_synced_commit` = current `git rev-parse --short HEAD`
5. Write each accepted plan as `plans/TP-NNN-slug.md` per `test-plan-format.md`
   - Derive concrete steps from the actual code: real route paths, real button labels (read the JSX), real field names
   - Fill `covers:` with the implementing file paths
6. Write `profiles/*.json`
7. Write the workspace `README.md`
8. Add the **Preview Testing Configuration** section to the project's CLAUDE.md (template in `CLAUDE-template.md`)

## Phase 5: Verify and Offer First Run

1. Run the access check from `preview-access.md`
2. Summarize:
```
✅ Test workspace created: .lovable-agent/tests/

- 7 test plans (4 smoke)
- 2 profiles (default, admin)
- Preview access: token (valid until 2026-06-17)
- Coverage baseline: commit abc1234

Run the smoke suite now to validate the setup? (yes/no)
→ /lovable:test-run --smoke
```

## Writing Good Steps (quality bar)

- **Read the actual component code** before writing steps - use the real button text, placeholder text, and routes. Generic steps ("click the submit button") break automation.
- Every step's Expected Result must be **observable**: visible text, URL change, element appearing, console clean, network status code
- Keep plans at 3-8 steps; split longer journeys into multiple plans
- First plan(s) a new user would hit (signup/login) come first and get `smoke`
- Never include real payment execution, real bulk email, or data deletion of non-test data - mark those `[MANUAL]`
