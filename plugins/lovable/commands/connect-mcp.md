---
description: Connect Lovable MCP to Claude for faster, more reliable yolo mode deployments without browser automation.
---

# Connect Lovable MCP

Set up the official Lovable MCP server so Claude can send prompts to Lovable directly via API - no browser automation needed.

## What is Lovable MCP?

Lovable exposes an official MCP (Model Context Protocol) server at `https://mcp.lovable.dev`. When connected, Claude can call Lovable's tools directly - including `send_message` to submit deployment prompts to your project.

**Benefits over browser automation:**
- 3-5x faster (API vs browser navigation)
- No Chrome extension required
- Not affected by Lovable UI changes
- More reliable (API is stable, UI is not)
- Works headlessly in any environment

**Requirements:**
- A Lovable account (OAuth sign-in in the browser; Lovable MCP does not accept API keys)
- On Enterprise, a workspace admin or owner must allow third-party MCP clients
- Claude Code (or Claude Desktop / claude.ai)

## Instructions

### 1. Show Introduction

Display this message:

```
## Connect Lovable MCP

This will connect the Lovable MCP server to Claude so yolo mode can
submit deployment prompts via API instead of browser automation.

Benefits:
✅ 3-5x faster deployments
✅ No Chrome extension needed
✅ More reliable (API vs UI automation)
✅ Works in any environment

Requirements:
- A Lovable account (OAuth sign-in; Enterprise admins must allow third-party MCP clients)

Let's get you connected. Choose your setup method:

A) Claude Code (recommended for this plugin)
B) Claude Desktop app
C) claude.ai web interface

Reply A, B, or C:
```

Wait for user selection, then show the appropriate setup instructions.

---

### 2a. Setup for Claude Code (Option A)

**Step 1: Add Lovable as a remote MCP server**

Display these instructions:

```
## Claude Code Setup

Run this command in your terminal:

  claude mcp add --transport http lovable https://mcp.lovable.dev

Then restart Claude Code for the changes to take effect.

After restarting:
1. Claude Code will prompt you to authorize with Lovable
2. Sign in with your Lovable account
3. Grant Claude access to your projects

Done! Come back and I'll verify the connection.

Type "done" when you've completed the setup, or "help" if you ran into issues.
```

Wait for user to type "done" or "help".

**If user types "help":**

```
## Troubleshooting Claude Code MCP Setup

### Error: "claude command not found"
Make sure Claude Code CLI is installed and in your PATH.
Install: https://claude.ai/code

### Error: "transport http not supported"
You may have an older version of Claude Code.
Update: claude update (or reinstall from claude.ai/code)

### OAuth doesn't open / fails
1. Make sure you're logged into Lovable in your browser
2. Try: claude mcp remove lovable
   Then retry: claude mcp add --transport http lovable https://mcp.lovable.dev

### MCP server shows as "offline"
1. Check internet connection
2. Try restarting Claude Code
3. Run: claude mcp list  to verify the server is listed

Still stuck? Check Lovable's docs: https://docs.lovable.dev/integrations/lovable-mcp-server
```

---

### 2b. Setup for Claude Desktop (Option B)

**Display these instructions:**

```
## Claude Desktop Setup

1. Open Claude Desktop
2. Go to: Settings → Connectors
3. Click "Add custom connector"
4. Fill in:
   - Name: Lovable
   - URL: https://mcp.lovable.dev
5. Click "Add"
6. Claude will prompt you to sign in to Lovable via OAuth
7. Authorize the connection

Done! Restart Claude Desktop to activate the connector.

Type "done" when you've completed the setup.
```

Wait for user to type "done".

---

### 2c. Setup for claude.ai (Option C)

**Display these instructions:**

```
## claude.ai Setup

1. Go to claude.ai
2. Click your profile icon → Settings
3. Click "Connectors" in the sidebar
4. Click "Add custom connector"
5. Fill in:
   - Name: Lovable
   - URL: https://mcp.lovable.dev
6. Click "Add"
7. Sign in to Lovable when prompted

Done! The Lovable tools will now be available in Claude.

Type "done" when you've completed the setup.
```

---

### 3. Verify the Connection

After the user completes setup, attempt to verify:

```
Verifying Lovable MCP connection...
```

Check if Lovable MCP tools are accessible by looking for `send_message` or similar Lovable tools in the available MCP tools.

**If verification succeeds:**

```
✅ Lovable MCP connected successfully!

Available Lovable tools confirmed. Claude can now send prompts
directly to your Lovable projects.

Next step: Make sure your Lovable project URL is configured.
```

Check CLAUDE.md for `lovable_url`. If missing:

```
Your Lovable project URL is not configured yet.
Please provide it:

What is your Lovable project URL?
(e.g., https://lovable.dev/projects/abc123)
```

If provided, update CLAUDE.md to add/update the Lovable Project URL field.

**If verification cannot be confirmed (tools not yet visible):**

```
⚠️ Could not verify MCP connection yet.

This usually means you need to restart Claude Code / Claude Desktop
for the new connector to take effect.

After restarting:
1. Open this project again
2. Run /lovable:connect-mcp verify  to re-check

Your setup instructions have been saved. Once connected,
yolo mode will automatically use MCP instead of browser automation.
```

---

### 4. Update CLAUDE.md for MCP Mode

Once connection is verified (or user confirms setup is done), update the project's CLAUDE.md:

1. Read current CLAUDE.md
2. If Yolo Mode Configuration section exists:
   - Add or update `Deployment Method: mcp` under the Status line
   - If section doesn't exist yet, skip (will be added when yolo mode is enabled)
3. Confirm the update:

```
✅ CLAUDE.md updated

Yolo mode will now use Lovable MCP for deployments:
- Deployment Method: mcp

If you haven't enabled yolo mode yet:
  Run: /lovable:yolo on

If yolo mode is already enabled, no further action needed.
MCP will be used automatically for the next deployment.
```

---

### 5. Handling `/lovable:connect-mcp verify`

If the user runs the command with `verify` argument:

1. Check if Lovable MCP tools are available
2. If yes:
   ```
   ✅ Lovable MCP is connected and working

   Available tools confirmed. Yolo mode will use MCP for deployments.

   Deployment method in CLAUDE.md: [show current value]
   ```
3. If no:
   ```
   ❌ Lovable MCP tools not detected

   Possible reasons:
   - Setup not completed yet (follow /lovable:connect-mcp steps)
   - Claude needs to be restarted after adding the connector
   - OAuth authorization was not completed

   To retry setup: /lovable:connect-mcp
   ```

---

### 6. Handling `/lovable:connect-mcp status`

Show current MCP connection status:

```
## Lovable MCP Status

Connection: [✅ Connected / ❌ Not connected / ⚠️ Unknown]
Deployment Method: [mcp / browser / auto] (from CLAUDE.md)

[If connected:]
Tools available: send_message, get_message, and others
Yolo mode will use MCP automatically.

[If not connected:]
To connect: /lovable:connect-mcp
```

---

## Example Flows

### First-time setup (Claude Code)

```
$ /lovable:connect-mcp

## Connect Lovable MCP
[... intro ...]

A) Claude Code (recommended for this plugin)
> A

## Claude Code Setup

Run this command in your terminal:

  claude mcp add --transport http lovable https://mcp.lovable.dev

Then restart Claude Code...

> done

Verifying Lovable MCP connection...
✅ Lovable MCP connected successfully!

What is your Lovable project URL?
> https://lovable.dev/projects/abc123

✅ CLAUDE.md updated

Yolo mode will now use Lovable MCP for deployments.
Run: /lovable:yolo on  to enable yolo mode.
```

### Already have yolo mode, adding MCP

```
$ /lovable:connect-mcp

[... setup ...]

✅ CLAUDE.md updated

Yolo mode is already enabled. Deployment Method updated to: mcp
Your next deployment will use Lovable MCP automatically.
```
