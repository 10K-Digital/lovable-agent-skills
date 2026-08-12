---
description: Resync tests with your codebase - finds new/changed features that lack test plans or unit tests and creates/updates them.
---

# Resync Tests

Find features added or changed since the last test sync that lack coverage, and update test plans (and unit tests) accordingly.

## Syntax

```
/lovable:test-sync              # Interactive: show gaps, ask before creating
/lovable:test-sync --apply      # Create suggested plans without asking per-plan
/lovable:test-sync --dry-run    # Report coverage gaps only, change nothing
```

## Instructions

1. **Read the testing skill** (`skills/testing/SKILL.md`) and `references/test-plan-format.md` (formats) + `references/test-wizard.md` (how to derive plans from code).

2. **Check workspace** exists - else point to `/lovable:test-init`.

3. **Detect changes since baseline**:
   ```bash
   git diff --name-only [last_synced_commit] HEAD
   ```
   (`testing.last_synced_commit` from `.lovable-agent/config.json`. If missing/invalid, fall back to comparing the full scan against existing plans' `covers:` lists.)

4. **Classify the changed files** into features:
   - New routes/pages → new user-facing surface
   - New/changed forms, mutations, auth calls → new/changed user actions
   - New edge functions → new backend behavior (find their frontend callers)
   - New migrations → data model changes (may affect existing plans' expectations)
   - Pure refactors/styling → usually no plan changes needed (note them as reviewed)

5. **Compute coverage gaps**:
   - For each feature, check whether any active plan's `covers:` includes its files
   - **Gap**: feature with no covering plan → suggest a NEW plan
   - **Stale**: covering plan exists but the covered files changed significantly → suggest UPDATING that plan's steps/expectations
   - **Orphaned**: plan covering deleted files → suggest `status: deprecated`
   - Also check **unit test gaps**: new source files without corresponding `*.test.*` files (if the project has a test framework)

6. **Report**:
   ```
   🔄 Test Sync - changes since [commit] ([date], [N] commits)

   New features without test plans:
   1. Password reset flow (src/pages/ResetPassword.tsx) → suggest TP-008
   2. Export to CSV (src/components/ExportButton.tsx, export-csv function) → suggest TP-009

   Stale plans (covered code changed):
   - TP-003 Create a project - form gained a "category" field → update steps

   Orphaned: none
   Unit test gaps: src/lib/csv.ts has no tests

   Create/update these? (all / pick numbers / skip)
   ```
   With `--dry-run`: stop here.

7. **Apply** (interactive confirmation unless `--apply`):
   - Write new plans per `test-plan-format.md` (read the actual code for real steps; assign next IDs from `plan_counter`)
   - Update stale plans (steps, expectations, `covers:`, `updated:` date)
   - Mark orphaned plans `status: deprecated`
   - Write missing unit tests if the user wants them (use the project's existing test framework and conventions)
   - Update `.lovable-agent/config.json`: `testing.last_synced_commit` = current HEAD, `testing.last_synced_at`, and `testing.plan_counter`
   - Update `Last Test Sync` in CLAUDE.md's Preview Testing section

8. **Offer a run**: "Run the new/updated plans now? → `/lovable:test-run --changed`"

## When to Suggest This Command

Proactively suggest `/lovable:test-sync` when:
- Implementing a feature in a project with a test workspace but `test_after_implementation: off`
- `last_synced_commit` is many commits behind HEAD
- The user mentions tests being out of date
