---
description: Enable/disable yolo mode for automated Lovable deployments via MCP or browser automation. Control deployment method, testing, and debug options.
---

# Yolo Mode Toggle

Enable or disable yolo mode for automated Lovable prompt submission via Lovable MCP (preferred) or browser automation.

## Syntax

```bash
/yolo [on|off] [--mcp|--browser|--auto] [--testing|--no-testing] [--debug]
```

## Arguments

- `on` - Enable yolo mode (default: auto method, with testing, without debug)
- `off` - Disable yolo mode (does not affect auto-push)
- `--mcp` - Use Lovable MCP only (fastest, requires MCP connection)
- `--browser` - Use browser automation only (requires Chrome extension)
- `--auto` - Try MCP first, fall back to browser (default)
- `--testing` - Enable all 3 testing levels after deployment (default when enabling)
- `--no-testing` - Skip testing, only deploy
- `--debug` - Enable verbose logging of automation steps
- (no arguments) - Show current yolo mode status

**Note:** Auto-push is independent. YOLO may deploy after a manual push.

## Instructions

Apply `../skills/lovable/references/prompt-authorization.md` before submission. An explicit
`/yolo on` request already authorizes enabling YOLO; do not ask for confirmation again.
After changing mode, persist `deploy.yolo_mode` as true/false in `.lovable-agent/config.json`
while preserving other fields, and synchronize the legacy CLAUDE.md status. If neutral setup is
missing, use the init skill first. Refresh the conditional authorization section in AGENTS.md
and CLAUDE.md. With no arguments, report effective status without changing settings.


### 1. Parse Command Arguments

Extract the mode (`on`/`off`) and flags from the command:
- If no arguments: proceed to step 7 (show status)
- If `on`: proceed to enable yolo mode
- If `off`: proceed to disable yolo mode
- Parse optional flags: `--auto-deploy`, `--no-auto-deploy`, `--testing`, `--no-testing`, `--debug`

### 2. When Enabling Yolo Mode (`/yolo on`)

**a) Show Beta Warning:**

Check if Lovable MCP tools are available in the current session. Display the appropriate warning:

**If Lovable MCP is available:**
```
⚠️ YOLO MODE (BETA)

Deployment method: Lovable MCP (connected)

Benefits:
✅ Auto-deploy after git push - no manual /deploy-edge command needed
✅ No manual copy-paste of prompts
✅ Automatic deployment verification
✅ Fast API-based deployments (3-5x faster than browser)
✅ No Chrome extension required

Risks:
⚠️ Beta feature - may have bugs
⚠️ Uses Lovable credits for each send_message call
⚠️ Always has manual fallback if automation fails

By saying yes, you authorize me to deploy edge functions and apply
database migrations via Lovable (MCP or browser automation) automatically
after this, subject to your migration approval setting and destructive-operation confirmation.

Continue enabling yolo mode? (yes/no)
```

**If Lovable MCP is NOT available:**
```
⚠️ YOLO MODE (BETA)

Deployment method: Browser automation (MCP not connected)

Benefits:
✅ Auto-deploy after git push - no manual /deploy-edge command needed
✅ No manual copy-paste of prompts
✅ Automatic deployment verification
✅ Saves time on every deployment

Risks:
⚠️ Beta feature - may have bugs
⚠️ Requires Chrome extension and browser session
⚠️ Lovable UI changes may break automation
⚠️ Always has manual fallback if automation fails

💡 Tip: Connect Lovable MCP for faster, more reliable automation:
   Run: /lovable:connect-mcp

By saying yes, you authorize me to deploy edge functions and apply
database migrations via Lovable (MCP or browser automation) automatically
after this, subject to your migration approval setting and destructive-operation confirmation.

Continue enabling yolo mode? (yes/no)
```

Ask whether to enable only if the user has not already requested enabling YOLO.

The explicit enable request (or confirmation when enabling was only proposed) grants standing
authorization for future
automated deployments and migrations while yolo mode stays on — see
`../skills/lovable/references/prompt-authorization.md`.

**b) Validate Prerequisites:**

1. Check if CLAUDE.md exists:
   ```
   ❌ Cannot enable yolo mode - project not initialized
   Run /init-lovable first to set up the project.
   ```

2. Preserve the current auto-push setting. YOLO can deploy code already pushed by the user;
   enabling it does not require or enable auto-push. Verify GitHub sync before deployment.

3. Read CLAUDE.md and check for `lovable_url` field:
   - If missing, ask user:
     ```
     What is your Lovable project URL?
     (e.g., https://lovable.dev/projects/abc123)
     ```
   - Update CLAUDE.md with provided URL

3. Check current Git branch:
   ```bash
   git branch --show-current
   ```
   - If not `main`, warn:
     ```
     ⚠️ You're on branch '[branch-name]'

     Only the main branch syncs with Lovable.
     Yolo mode will work, but deployments won't sync until you merge to main.
     ```

4. Check for Claude in Chrome extension (optional check):
   ```
   💡 Yolo mode requires the Claude in Chrome extension.

   If you don't have it installed:
   - Install: https://chrome.google.com/webstore/detail/claude/...
   - Read docs: https://docs.claude.com/claude/code-intelligence/browser-automation

   ℹ️ You can enable yolo mode now and install the extension later.
   ```

**c) Update CLAUDE.md:**

1. Read current CLAUDE.md content
2. Ensure auto-push configuration exists (should be separate from yolo mode):

```markdown
## Auto-Push Configuration

- **Auto-Push to GitHub**: on
- **Last Updated**: [current timestamp]

[... rest of auto-push section ...]
```

3. Add or update the yolo mode configuration section:

```markdown
## Yolo Mode Configuration (Beta)

> ⚠️ Beta feature - auto-submits Lovable prompts via MCP or browser automation
> Auto-push is independent; verify GitHub sync before deployment.

- **Status**: on
- **Deployment Method**: [auto if --auto or default; mcp if --mcp; browser if --browser]
- **Deployment Testing**: [on if --testing or default, off if --no-testing]
- **Auto-run Tests**: off
- **Debug Mode**: [on if --debug, off otherwise]
- **Last Updated**: [current timestamp]
- **Operations Covered**:
  - Automatic deployment detection after git push
  - Edge function deployment
  - Migration application
  - Automated testing after code push

**Configure:** Run `/yolo on/off [--mcp|--browser|--auto] [--testing|--no-testing] [--debug]`
```

4. If `lovable_url` was added, update the Project Overview section

**d) Confirm Enablement:**

```
✅ Yolo mode ENABLED

Configuration:
- Deployment Method: [🔌 MCP (auto) / 🌐 Browser (auto) / 🔌 MCP (forced) / 🌐 Browser (forced)]
- Testing: [✅ ON / ⏸️ OFF]
- Debug: [✅ ON / OFF]

Prerequisites:
✅ Existing auto-push preference preserved

[If deployment method is auto and MCP is available:]
⚡ Lovable MCP detected - will use MCP for faster deployments
   Tip: Use /lovable:yolo on --mcp to lock in MCP mode

[If deployment method is auto and MCP is NOT available:]
💡 Lovable MCP not connected - using browser automation
   For faster, more reliable deployments: /lovable:connect-mcp

Workflow:
1. You ask me to make changes
2. I complete the task successfully
3. Auto-push: I automatically commit and push to GitHub
4. Yolo mode: I detect backend changes and auto-deploy to Lovable

[if testing on] - Run 3 levels of verification tests
[if debug on] - Show verbose automation details

Operations automated:
✅ Automatic deployment detection after git push
✅ Edge function deployment
✅ Migration application

To disable yolo mode: /yolo off
To change settings: /yolo on --mcp  or  /yolo on --no-testing  or  /yolo on --debug
```

### 3. When Disabling Yolo Mode (`/yolo off`)

**a) Update CLAUDE.md:**

1. Read current CLAUDE.md
2. Update yolo mode configuration:
   - Set `Status: off`
   - Keep other settings for when user re-enables
   - Update `Last Updated` timestamp
3. **Do NOT change auto-push setting** - auto-push remains independent

**b) Confirm Disablement:**

```
⏸️ Yolo mode DISABLED

I'll still generate Lovable prompts for backend operations,
but you'll need to copy-paste them manually into Lovable.

Your previous settings are saved:
- Testing: [on/off]
- Debug: [on/off]

Note: Auto-push is still enabled and works independently of yolo mode.
To disable auto-push: Edit CLAUDE.md and set "Auto-Push to GitHub: off"

To re-enable yolo mode: /yolo on
```

### 4. When No Arguments (`/yolo`)

**Show Current Status:**

1. Read CLAUDE.md
2. Check if yolo mode section exists
3. Check if Lovable MCP tools are available
4. Display current configuration:

If yolo mode is ON:
```
## Yolo Mode Configuration

Status: ✅ ENABLED
Deployment Method: [auto / mcp / browser]
MCP Connection: [✅ Connected / ❌ Not connected]
Auto-Deploy: [✅ ON / ⏸️ OFF] (auto-deploy after git push)
Testing: ✅ ON (runs 3 verification levels)
Debug: OFF
Last updated: 2025-01-03 10:30:00

Active deployment strategy:
[If method=auto and MCP connected]:   ⚡ MCP (with browser fallback)
[If method=auto and MCP not connected]: 🌐 Browser automation
[If method=mcp]:                       🔌 MCP only
[If method=browser]:                   🌐 Browser only

Operations automated:
- Edge function deployment
- Migration application

[if auto-deploy on]
How it works:
- After you push backend changes to main
- I'll automatically detect and deploy them
- No need to run /deploy-edge manually!

To modify:
/yolo off                # Disable
/yolo on --mcp           # Force MCP mode
/yolo on --browser       # Force browser mode
/yolo on --no-testing    # Skip testing
/yolo on --debug         # Enable debug output
/lovable:connect-mcp     # Connect Lovable MCP
```

If yolo mode is OFF or not configured:
```
## Yolo Mode Configuration

Status: ⏸️ DISABLED

Yolo mode automates Lovable prompt submission using MCP or browser automation.

Benefits:
✅ Auto-deploy after git push - no manual commands needed
✅ No manual copy-paste of prompts
✅ Automatic deployment verification
✅ Saves time on every deployment

Deployment options:
⚡ Lovable MCP (recommended) - /lovable:connect-mcp  then  /yolo on --mcp
🌐 Browser automation (fallback) - requires Chrome extension

To enable: /yolo on
To learn more: Check README.md or ask "What is yolo mode?"
```

### 5. Handling Flags

**`--mcp` flag:**
- Set `Deployment Method: mcp` in CLAUDE.md
- Use Lovable MCP only for deployments
- If MCP not available, show manual prompt (skip browser automation)
- Recommended when user has set up Lovable MCP connection

**`--browser` flag:**
- Set `Deployment Method: browser` in CLAUDE.md
- Use browser automation only (legacy behavior)
- Skip MCP even if available
- Useful if user prefers the old behavior

**`--auto` flag (default):**
- Set `Deployment Method: auto` in CLAUDE.md
- Try MCP first, fall back to browser if not available
- Best of both worlds

**`--testing` flag (default):**
- Set `Deployment Testing: on` in CLAUDE.md
- After deployments, run all 3 testing levels:
  - Level 1: Basic verification
  - Level 2: Console error checking
  - Level 3: Functional testing

**`--no-testing` flag:**
- Set `Deployment Testing: off` in CLAUDE.md
- After deployments, skip all testing
- Only deploy and confirm basic success

**`--debug` flag:**
- Set `Debug Mode: on` in CLAUDE.md
- During automation, output verbose logs:
  - MCP: tool calls, parameters, response text
  - Browser: each navigation step, selectors, wait times
  - Full response text from Lovable

### 6. Error Handling

**CLAUDE.md not found:**
```
❌ Cannot configure yolo mode

CLAUDE.md not found. Initialize the project first:
/init-lovable
```

**Invalid arguments:**
```
❌ Invalid syntax

Usage: /yolo [on|off] [--mcp|--browser|--auto] [--testing|--no-testing] [--debug]

Examples:
  /yolo                    # Show status
  /yolo on                 # Enable with auto method and testing
  /yolo on --mcp           # Enable using Lovable MCP
  /yolo on --browser       # Enable using browser automation
  /yolo on --no-testing    # Enable without verification tests
  /yolo on --debug         # Enable with verbose logs
  /yolo off                # Disable
```

**Conflicting flags:**
```
❌ Cannot use --testing and --no-testing together

Choose one:
  /yolo on --testing     # Enable testing (default)
  /yolo on --no-testing  # Skip testing
```

### 7. Integration Notes

**Relationship with auto-push:**
- Auto-push and yolo mode are configured separately in CLAUDE.md
- Auto-push can be on while yolo mode is off (manual deployment workflow)
- Yolo mode works with manual pushes; auto-push is optional
- Disabling yolo mode does NOT disable auto-push

**Workflow when yolo mode is enabled:**
After a successful `git push origin main` (triggered by auto-push) that includes backend changes:
- Claude automatically detects edge function or migration changes
- Triggers browser automation without manual command
- Deploys to Lovable and runs verification tests

**Manual deployment with yolo mode:**
Even with yolo mode on, you can still manually trigger deployments:
- `/deploy-edge` - Deploys edge functions to Lovable
- `/apply-migration` - Applies database migrations

The automation workflow is defined in `/skills/yolo/SKILL.md` and references.
See `/skills/yolo/references/post-push-automation.md` for auto-deploy implementation.

## Example Outputs

### Example 1: First-time Enable (MCP connected)

```
$ /yolo on

⚠️ YOLO MODE (BETA)

Deployment method: Lovable MCP (connected)

Benefits:
✅ Auto-deploy after git push - no manual /deploy-edge command needed
✅ No manual copy-paste of prompts
✅ Fast API-based deployments (3-5x faster than browser)
✅ No Chrome extension required

Risks:
⚠️ Beta feature - may have bugs
⚠️ Uses Lovable credits for each send_message call

Continue enabling yolo mode? yes

✅ Yolo mode ENABLED

Configuration:
- Deployment Method: auto (MCP detected)
- Testing: ✅ ON
- Debug: OFF

⚡ Lovable MCP detected - will use MCP for faster deployments

From now on, after you push backend changes to main:
- I'll automatically detect edge function or migration changes
- Submit deployment prompts via Lovable MCP
- No need to run /deploy-edge manually!
- Run 3 levels of verification tests

Operations automated:
✅ Edge function deployment
✅ Migration application

To disable: /yolo off
```

### Example 2: First-time Enable (no MCP)

```
$ /yolo on

⚠️ YOLO MODE (BETA)

Deployment method: Browser automation (MCP not connected)
...
💡 Tip: Connect Lovable MCP for faster, more reliable automation:
   Run: /lovable:connect-mcp

Continue enabling yolo mode? yes

✅ Yolo mode ENABLED

Configuration:
- Deployment Method: auto (browser fallback)
- Testing: ✅ ON
- Debug: OFF

Operations automated:
✅ Edge function deployment
✅ Migration application

To enable MCP: /lovable:connect-mcp
To disable: /yolo off
```

### Example 3: Enable Without Testing

```
$ /yolo on --no-testing

⚠️ YOLO MODE (BETA)
[... beta warning ...]

Continue enabling yolo mode? yes

✅ Yolo mode ENABLED

Configuration:
- Auto-Deploy: ✅ ON
- Testing: ⏸️ OFF (deployments only, no verification tests)
- Debug: OFF

Operations automated:
✅ Edge function deployment (no testing)
✅ Migration application (no testing)

To enable testing: /yolo on --testing
```

### Example 4: Enable with Debug

```
$ /yolo on --debug

⚠️ YOLO MODE (BETA)
[... beta warning ...]

Continue enabling yolo mode? yes

✅ Yolo mode ENABLED

Configuration:
- Auto-Deploy: ✅ ON
- Testing: ✅ ON
- Debug: ✅ ON (verbose browser automation logs)

You'll see detailed output during deployments:
- Navigation steps
- Element selectors
- Response text
- Timing information

To disable debug: /yolo on
```

### Example 5: Check Status

```
$ /yolo

## Yolo Mode Configuration

Status: ✅ ENABLED
Auto-Deploy: ✅ ON (auto-deploy after git push)
Testing: ✅ ON (runs 3 verification levels)
Debug: ✅ ON
Last updated: 2025-01-03 10:30:00

Operations automated:
- Edge function deployment
- Migration application

How it works:
- After you push backend changes to main
- I'll automatically detect and deploy them
- No need to run /deploy-edge manually!

To modify:
/yolo off                 # Disable
/yolo on --no-auto-deploy # Require manual deploy commands
/yolo on --no-testing     # Skip testing
/yolo on                  # Disable debug (keeps auto-deploy and testing)
```

### Example 6: Disable

```
$ /yolo off

⏸️ Yolo mode DISABLED

I'll still generate Lovable prompts for backend operations,
but you'll need to copy-paste them manually into Lovable.

Your previous settings are saved:
- Auto-Deploy: on
- Testing: on
- Debug: on

To re-enable: /yolo on
```
