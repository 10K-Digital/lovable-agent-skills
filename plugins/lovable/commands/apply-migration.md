---
description: Check for pending database migrations and provide Lovable prompts to apply them.
---

# Apply Database Migration

Before submission, read `../skills/lovable/references/prompt-authorization.md` and use
`../skills/lovable-deploy/SKILL.md`. Resolve neutral `deploy.yolo_mode` before legacy status;
explicit false overrides legacy on. Apply migration approval gates and transport selection from
the neutral configuration. The legacy steps below do not override these rules.


Check for pending migrations and generate Lovable deployment prompts.

## Instructions

1. **List migration files**:
   - Show all files in `supabase/migrations/`
   - Sort by timestamp (filename prefix)

2. **Show migration content** for review:
```sql
-- Migration: [filename]
[SQL content]
```

3. **Warn about destructive operations**:
   - Check for: DROP, DELETE, TRUNCATE, ALTER...DROP
   - If found:
```
⚠️ **Destructive operation detected!**
This migration contains: [operation]
Ensure you have a backup before proceeding.
```

4. **Generate deployment prompt**:
```
📋 **LOVABLE PROMPT:**
> "Apply pending Supabase migrations"
```

Or for review first:
```
📋 **LOVABLE PROMPT:**
> "Review and apply the migration [filename]"
```

5. **Suggest verification**:
```
After applying, verify:
> "Show me the [table_name] table structure"
```

6. **Remind about CLAUDE.md**:
   - If new tables created, update database tables section

## Check for Yolo Mode

After generating the prompt, check if yolo mode is enabled:

1. **Read CLAUDE.md:**
   - Look for `## Yolo Mode Configuration (Beta)` section
   - Check `Status` field
   - Extract `Testing` and `Debug Mode` settings

2. **If `Status: on`:**
   - ✅ Yolo mode is enabled
   - Activate yolo skill (see `/skills/yolo/SKILL.md`)
   - Execute browser automation workflow:
     a. Navigate to Lovable project
     b. Submit migration prompt
     c. Monitor for successful application
     d. Run tests if `Testing: on`
     e. Show deployment summary
   - **Exit** (don't show manual prompt)

3. **If `Status: off` or not found:**
   - ⏸️ Yolo mode is disabled
   - Show manual prompt (as shown in examples below)
   - Suggest enabling yolo mode:
     ```
     💡 **Tip:** Automate migrations with yolo mode!
        Run: /lovable:yolo on
        Benefits: No manual copy-paste, automatic testing
     ```

## Example Output

### Example 1: Yolo Mode Disabled (Manual)

```
## Pending Migrations

### 20250101120000_add_profiles_table.sql
```sql
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);
```

✅ No destructive operations detected.

📋 **LOVABLE PROMPT:**
> "Apply pending Supabase migrations"

After applying:
> "Show me the profiles table structure"

💡 Remember to update CLAUDE.md with the new table.

💡 **Tip:** Automate migrations with yolo mode!
   Run: /lovable:yolo on
   Benefits: No manual copy-paste, automatic testing
```

### Example 2: Yolo Mode Enabled (Automated)

```
## Pending Migrations

### 20250101120000_add_profiles_table.sql
✅ No destructive operations detected.
✅ Committed and pushed to main

🤖 Yolo mode: Applying Supabase migrations

⏳ Step 1/8: Navigating to Lovable project...
⏳ Step 2/8: Waiting for GitHub sync...
✅ Step 3/8: Sync verified - Lovable has latest code
✅ Step 4/8: Located chat interface
✅ Step 5/8: Submitted prompt: "Apply pending Supabase migrations"
⏳ Step 6/8: Waiting for Lovable response...
✅ Step 7/8: Migration confirmed
⏳ Step 8/8: Running verification tests...
✅ Step 8/8: All tests passed

## Migration Summary

**Operation:** Database Migration
**Migration:** 20250101120000_add_profiles_table.sql
**Status:** ✅ Success
**Duration:** 42 seconds

**Verification Tests:**
1. ✅ Basic verification: Schema confirmed
2. ✅ Console check: No errors detected
3. ✅ Functional test: Table query succeeded

**Next Steps:**
- Update CLAUDE.md with new table documentation

💡 Yolo mode is enabled. Run `/lovable:yolo off` to disable.
```
