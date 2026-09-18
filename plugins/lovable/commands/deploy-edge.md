---
description: Check for Edge Function changes and provide Lovable deployment prompts.
---

# Deploy Edge Functions

Before submission, read `../skills/lovable/references/prompt-authorization.md` and use
`../skills/lovable-deploy/SKILL.md`. Resolve neutral `deploy.yolo_mode` before legacy status;
explicit false overrides legacy on. Apply migration approval gates and transport selection from
the neutral configuration. The legacy steps below do not override these rules.


Check for Edge Function changes and generate Lovable deployment prompts.

## Instructions

1. **Check for changes** in `supabase/functions/`:
   - List modified files
   - Show which functions have changes

2. **Verify code is pushed**:
   - Check for uncommitted changes
   - Check for unpushed commits to `main`

3. **Detect and validate secrets** (use secret-detection skill):
   - Scan function code for `Deno.env.get("SECRET_NAME")` patterns
   - Read secrets table from CLAUDE.md
   - Cross-reference detected secrets with known status:
     - ✅ In Lovable Cloud → OK
     - ⚠️ Not configured → Warn user
   - Check if any NEW secrets are referenced that aren't in CLAUDE.md
   - Warn about missing secrets before deployment

4. **Generate deployment prompt**:

For specific function:
```
📋 **LOVABLE PROMPT:**
> "Deploy the [function-name] edge function"
```

For multiple functions:
```
📋 **LOVABLE PROMPT:**
> "Deploy all edge functions"
```

5. **If new secrets detected**:
```
⚠️ **New secret required**: `SECRET_NAME`

Before deploying:
1. Go to Cloud → Secrets
2. Add: SECRET_NAME = [your value]
3. Then deploy the edge function
```

6. **Verify without another prompt**: inspect function state/logs in browser Cloud or call the
   endpoint directly. Do not spend a second MCP/chat call merely to request logs.

## Check for Yolo Mode

After generating the prompt, check if yolo mode is enabled:

1. **Read CLAUDE.md:**
   - Look for `## Yolo Mode Configuration (Beta)` section
   - Check `Status` field
   - Extract `Deployment Method`, `Testing`, and `Debug Mode` settings

2. **If `Status: on`:**
   - ✅ Yolo mode is enabled
   - Activate yolo skill (see `/skills/yolo/SKILL.md`)
   - Delegate transport and credit minimization to the yolo skill. In `auto`, use browser first and
     MCP only when browser submission is unavailable; submit one consolidated prompt.
   - Run tests if `Testing: on`
   - Show deployment summary
   - **Exit** (don't show manual prompt)

3. **If `Status: off` or not found:**
   - ⏸️ Yolo mode is disabled
   - Show manual prompt (as shown in examples below)
   - Suggest enabling yolo mode:
     ```
     💡 **Tip:** Automate deployments with yolo mode!
        Run: /lovable:yolo on
        Browser auto mode minimizes charged MCP calls.
     ```

## Example Output

### Example 1: Yolo Mode Disabled (Manual)

```
## Edge Function Changes

Modified functions:
- `send-email` - Updated email template
- `process-payment` - Added refund handling

✅ All changes committed and pushed to main

## Secret Validation

Secrets used by functions:
- RESEND_API_KEY (send-email)
  Status: ✅ In Lovable Cloud
- STRIPE_SECRET_KEY (process-payment)
  Status: ⚠️ Not configured

⚠️ **Missing secret detected:**
Before deploying, add STRIPE_SECRET_KEY to Cloud → Secrets:
1. Go to Cloud → Secrets in Lovable
2. Click "Add secret"
3. Enter: STRIPE_SECRET_KEY = [your value]
4. Then run the prompt below

📋 **LOVABLE PROMPT:**
> "Deploy all edge functions"

After deployment, verify both functions in browser Cloud logs/status or with safe direct calls;
do not submit another Lovable prompt.

💡 **Tip:** Automate deployments with yolo mode!
   Run: /lovable:yolo on
   Browser auto mode minimizes charged MCP calls.
```

### Example 2: Yolo Mode Enabled (Automated)

```
## Edge Function Changes

Modified functions:
- `send-email` - Updated email template

✅ All changes committed and pushed to main

🤖 Yolo mode (MCP): Deploying send-email edge function

⏳ Sending deployment prompt via Lovable MCP...
✅ Deployment confirmed (3.2s)
⏳ Running verification tests...
✅ All tests passed

## Deployment Summary

**Operation:** Edge Function Deployment
**Function:** send-email
**Status:** ✅ Success
**Duration:** 38 seconds

**Verification Tests:**
1. ✅ Basic verification: Deployment logs show no errors
2. ✅ Console check: No errors in browser console
3. ✅ Functional test: Function endpoint responds (200 OK)

**Production Status:**
- Function is live and responding
- No errors detected
- Ready for use

💡 Yolo mode is enabled. Run `/lovable:yolo off` to disable.
```
