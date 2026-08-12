# 🚀 Lovable Agent Skills: Claude Code + Codex + More

## **Edit Lovable Projects 10x Faster—Without Leaving Your IDE**

Stop copy-pasting between Lovable and Claude. Stop wrestling with two-way sync. Stop burning through API credits for simple changes.

**The Lovable Agent Skills plugin brings the power of your coding agent directly to your Lovable projects.** Codex, Claude Code, and other Agent Skills runtimes share the same provider-neutral workflows; Claude Code commands and hooks remain available for existing projects.

### **What You Get:**

✨ **Edit Lovable projects right in your IDE** with Codex, Claude Code, or another coding agent
🧪 **Preview Testing** - automated test plans run against your live Preview app
🏗️ **Dual-architecture support** - works with both Vite SPA and TanStack Start (SSR) projects (v1.8.1)
🔌 **Lovable MCP integration** - deploy via API instead of browser (NEW in v1.8.0!)
🗺️ **Project Structure Map** - agents navigate your codebase faster
⚡ **Auto-push to GitHub** - automatic commit and push after every task
🚀 **Auto-deploy to Lovable** - no manual commands needed
🤖 **Complete workflow automation** - from code changes to production
💰 **Save credits** by using your Claude subscription for heavy lifting
🔄 **Zero friction syncing** - between your code, GitHub, and Lovable Cloud
🛡️ **Automatic secret detection** - never forget a required API key
⚡ **Instant setup** - generates project context automatically
✅ **Verification built-in** - tests run after every deployment

### Provider-neutral agent contract

New projects use `.lovable-agent/` as the shared source of truth:

```text
.lovable-agent/
├── config.json             # project, sync, deploy, testing, and secret metadata
├── context.md              # provider-neutral project context (no secret values)
├── preview-token.local     # ignored Preview credential, never committed
└── tests/                  # plans, profiles, and results
```

`AGENTS.md` is the canonical instruction file. `CLAUDE.md` and the legacy
`.claude/lovable-claude/test/` workspace remain compatible aliases. Run `/lovable:migrate-agent`
or `python3 plugins/lovable/scripts/migrate-workspace.py` to migrate an existing project.

---

## **The Problem You're Solving**

Working with Lovable is amazing... until it's not:

- 😤 **Context switching pain** - Lovable UI for backend, IDE for frontend, back and forth endlessly
- 💸 **Credit drain** - Lovable charges for what Claude Code can do cheaper (via your subscription)
- 🤷 **Sync confusion** - "What syncs automatically? What needs manual deployment?" Constantly unsure
- ⏱️ **Manual workflows** - Copy prompt → Paste into Lovable → Wait for response → Repeat
- 🔑 **Secret chaos** - Tracking which secrets each function needs, which ones you set up, which ones are missing
- 🐛 **Deploy blind** - No automated tests after deployment. Hope it works!

**This plugin eliminates every single one of these friction points.**

---

## **How It Works (In 90 Seconds)**

### **1️⃣ One-Time Setup**
```bash
/lovable:init
```
Your agent scans the project, asks a few questions, and generates `.lovable-agent/config.json`,
`AGENTS.md`, and a Claude-compatible `CLAUDE.md` shim.

### **2️⃣ Make Your Changes**
Edit code in your IDE like normal. Your coding agent handles the complex Lovable workflow.

### **3️⃣ Automatic Everything**
```bash
/lovable:deploy-edge    # Deploy to Lovable
/lovable:sync           # Keep secrets/config in sync
```

That's it. No manual prompts. No context switching. No forgotten steps.

---

## **Real Workflows**

### **🎯 Manual Mode (Full Control)**
```
You: "Add email notifications to the send-email function"
     ↓
Claude Code: Creates the code
             ↓
Shows you: "Deploy with this prompt: 'Deploy the send-email edge function'"
           Plus: "⚠️ Needs RESEND_API_KEY"
           ↓
You: Copy-paste prompt to Lovable (takes 10 seconds)
Result: ✅ Function deployed, tests pass, you're informed
```

### **🚀 Yolo Mode (Full Automation)**
```
You: "Add email notifications"
     ↓
Claude Code: Creates the code, detects needed secrets
        ✅ Automatically commits changes
        ✅ Pushes to GitHub
             ↓
Claude: 🤖 Detects backend changes automatically
        🔌 Submits via Lovable MCP (or browser automation)
        ✅ Confirms deployment
        ✅ Runs verification tests
        ✅ Reports success

Done. Zero manual work. No git commands. No deploy commands!
```

**NEW in v1.8.0:** Lovable MCP integration - deploy via API instead of browser (3-5x faster, no Chrome extension)!
**IMPROVED in v1.5.0:** Hook-based auto-push for 100% reliable automatic commits and pushes!
**NEW in v1.3.0:** With auto-deploy enabled, Claude automatically deploys to Lovable after git push!

---

## **Key Features That Save You Hours**

### ⚡ **Auto-Sync & Auto-Push** (Hook-Based in v1.5.0!)
Using Claude Code hooks for seamless GitHub integration - always in sync, always up-to-date, 100% reliable!

**Auto-Sync (Start Hook):**
```
Claude starts → Hook pulls latest → You work on current code → No conflicts!
```
Automatically pulls latest changes from GitHub when Claude starts working. Only runs on main branch with no uncommitted changes.

**Auto-Push (Stop Hook):**
```
Make changes → Task complete → Hook triggers → Auto-commit → Auto-push → Changes in GitHub!
```
Automatically commits and pushes when Claude finishes any task. No manual git commands!

**Why hooks?** Hooks guarantee execution every time, making sync operations more reliable than skill-based approaches. Auto-sync keeps you current, auto-push keeps GitHub current!

### 🔌 **Lovable MCP Integration** (NEW in v1.8.0!)
Connect the official Lovable MCP server for API-based deployments - no browser required.

```bash
/lovable:connect-mcp    # Set up once (guided wizard)
/lovable:yolo on --mcp  # Enable MCP-powered yolo mode
```

**Benefits:** 3-5x faster, no Chrome extension, works anywhere, not affected by UI changes.

### 🚀 **Auto-Deploy to Lovable** (v1.3.0)
Push backend changes to main, and Claude automatically deploys to Lovable. No commands, no copy-paste, no context switching.

```
Auto-push to GitHub → Claude detects changes → Automatic deployment (MCP or browser) → Tests pass → Done!
```

**Complete automation:** With both features enabled, Claude handles everything from code changes to production deployment!

### 🧪 **Preview Testing** (NEW in v1.9.0!)
Claude tests your app **in Lovable Preview mode** via browser automation - real user flows in the real running app, after each implementation or as planned end-to-end runs.

```bash
/lovable:test-init     # Wizard: scans your app, suggests test plans for its main actions
/lovable:test-run      # Run tests in Preview (--smoke | --changed | --all | TP-001)
/lovable:test-sync     # New features missing tests? Resync coverage
```

**How it accesses your Preview:** either you're logged in to Lovable in Chrome, or you give it a tokenized preview URL - open your Lovable project in preview mode, click the **arrow icon next to the address bar**, and copy the URL from the new tab (`https://preview--your-app.lovable.app/?__lovable_token=...`). The token lasts 7 days; the plugin stores it gitignored and asks for a fresh one when it expires.

**Standardized workspace** at `.lovable-agent/tests/`: test plans (`plans/TP-NNN-*.md`), test user profiles (`profiles/`), and dated run reports (`results/`). The legacy `.claude/lovable-claude/test/` path remains supported and can be migrated with `/lovable:migrate-agent`. As you build new features, your agent keeps unit tests and test plans in sync.

### 🔐 **Smart Secret Detection**
Claude Code automatically finds every secret your functions need—by scanning your code. No more "why is this function failing??"—we tell you upfront: "You need STRIPE_WEBHOOK_SECRET."

### 🔄 **Automatic Sync Command**
Team member added a secret in Lovable Cloud? Run `/lovable:sync` and it updates your project config. No more getting out of sync.

### ⚡ **Auto-Run Tests**
Enable tests to run automatically after every deployment. Catch issues in seconds, not after users report bugs.

### 📊 **Secret Status Dashboard**
CLAUDE.md shows exactly which secrets are configured (✅) and which need setup (⚠️). One glance tells you if you're ready to deploy.

### 🎯 **Context Everything**
Claude Code knows your production URL, database tables, edge functions, secrets, and conventions. Ask it anything about your project—it already knows.

---

## **Installation (2 Minutes)**

### **Option 1: Via Marketplace (Recommended)**

```bash
# In Claude Code, run:
/plugin marketplace add 10K-Digital/lovable-claude-code

# Install the plugin:
/plugin install lovable@10k-digital
```

💡 **Tip:** Enable auto-updates in Claude Code settings so you always get the latest version automatically.

### **Option 2: Codex or another Agent Skills runtime**

Add the repository marketplace, then install the `lovable` plugin:

```bash
codex plugin marketplace add 10K-Digital/lovable-claude-code
```

Restart the Codex/ChatGPT desktop app, open the Plugins Directory, choose the `10K Digital`
marketplace, and install `lovable`. The plugin exposes Agent Skills under `plugins/lovable/skills/`
and the official Lovable MCP server (`https://mcp.lovable.dev`) through `.mcp.json`. Authenticate
with Lovable when the MCP connector prompts you. Deployment always falls back to browser automation
and then a manual prompt.

For any other Agent Skills-compatible agent, point it at the `SKILL.md` files and use
`.lovable-agent/config.json` plus `AGENTS.md` as the project contract.

### **Option 3: Local Claude Code Installation**

Clone or download this repo, then:
```bash
cp -r lovable-plugin/.claude-plugin your-project/.claude-plugin
cp -r lovable-plugin/commands your-project/.claude/commands
cp -r lovable-plugin/skills your-project/.claude/skills
```

### **Option 4: Requirements Check** ✓

Before you start, make sure you have:
- ✅ Your Lovable project with GitHub sync enabled ([docs](https://docs.lovable.dev/integrations/github#about-github))
- ✅ Claude Code configured with your GitHub repo
- ✅ (Optional, recommended) Lovable MCP for yolo mode - run `/lovable:connect-mcp` to set up
- ✅ (Alternative) [Claude in Chrome extension](https://chrome.google.com/webstore/detail/claude/pebppomjfocnoigkeepgbmcifnnlndla) for browser-based yolo mode

---

## **Pro Tip: Enable Claude Code GitHub Actions**

Claude Code can review pull requests in the cloud as soon as they open or receive new commits. Add
the official [Claude Code Action](https://github.com/anthropics/claude-code-action) to your project
and configure the credential described in its current authentication guide:

```yaml
# .github/workflows/claude-review.yml
name: Claude PR review

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write
  id-token: write

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: >-
            Review this pull request for correctness, security, regressions, and missing tests.
            Leave actionable inline comments and summarize only material findings.
```

Store the secret in GitHub Actions secrets, keep pull-request permissions least-privilege, and
follow Anthropic's official action documentation if its supported authentication input changes.

---

## **Your First 5 Minutes**

```bash
# 1. Initialize your project
/lovable:init

# 2. Answer the questions (1 minute)
#    - What's your production URL?
#    - Enable yolo mode? (recommended!)
#    - etc.

# 3. Start coding!
# Claude Code now knows everything about your project

# 4. Push your changes:
git push origin main
# With yolo mode on: Auto-deploys backend changes!
# No /deploy-edge command needed

# 5. Keep in sync:
/lovable:sync
# Updates CLAUDE.md with latest secrets/config
```

---

## **Commands at a Glance**

| Command | What It Does | When To Use |
|---------|-------------|-----------|
| `/lovable:init` | Set up your project | First time setup |
| `/lovable:map` | Generate Project Structure Map | Help Claude navigate faster (NEW!) |
| `/lovable:sync` | Refresh config from Lovable Cloud | After team adds secrets/functions |
| `/lovable:deploy-edge` | Deploy edge functions | After code changes (or auto with yolo) |
| `/lovable:apply-migration` | Apply database migrations | After DB changes (or auto with yolo) |
| `/lovable:yolo on/off` | Toggle automation + auto-deploy | Configure how you work |
| `/lovable:test-init` | Set up preview testing (wizard) | Once, to create test plans (NEW!) |
| `/lovable:test-run` | Run tests in Lovable Preview | After changes or full e2e runs (NEW!) |
| `/lovable:test-sync` | Resync tests with codebase | When new features lack test plans (NEW!) |

**Pro tip:** With yolo mode on, you don't need `/deploy-edge`—just `git push` and it deploys automatically!

---

## **Before & After: Real Time Savings**

### **Without This Plugin:**
```
1. Make changes in Claude Code (5 min)
2. Copy prompt to clipboard (1 min)
3. Switch to browser, open Lovable (1 min)
4. Paste prompt in chat (1 min)
5. Wait for response (2 min)
6. Manually verify (2 min)
7. Switch back to IDE (1 min)
Total: 13 minutes
```

### **With This Plugin (Manual Mode):**
```
1. Make changes in Claude Code (5 min)
2. Copy one-line prompt (30 sec)
3. Paste into Lovable (30 sec)
Total: 6 minutes
= **54% time savings**
```

### **With This Plugin (Yolo Mode + Auto-Push + Auto-Deploy):**
```
1. Make changes in Claude Code (5 min)
   → Auto-commits changes
   → Auto-pushes to GitHub
   → Auto-detects backend changes
   → Auto-deploys to Lovable
   → Auto-runs tests
Total: 5 minutes
= **62% time savings** + **ZERO manual commands needed**
```

---

## **Advanced Features**

### **Yolo Mode (Complete Automation)**
```bash
/lovable:yolo on                    # Enable everything: auto-push, auto-deploy, testing (recommended)
/lovable:yolo on --no-auto-push     # Require manual git commands
/lovable:yolo on --no-auto-deploy   # Require manual /deploy-edge commands
/lovable:yolo on --no-testing       # Skip tests to go faster
/lovable:yolo on --debug            # See automation logs
/lovable:yolo off                   # Disable automation
```

**Auto-Push (Hook-Based in v1.5.0):**
Using a Claude Code hook, after completing each task the plugin automatically:
- Checks for file changes
- Commits with descriptive message
- Pushes to main branch on GitHub
- **More reliable:** Hooks guarantee execution vs. Claude remembering to check

**Auto-Deploy (v1.3.0):**
With auto-deploy enabled, after git push Claude automatically:
- Detects backend file changes (edge functions, migrations)
- Navigates to your Lovable project
- Submits deployment prompts
- Runs verification tests (3 levels)
- Reports success/failure instantly

**Complete automation:** Enable both for a fully automated workflow from code changes to production!

Use `--no-auto-push` or `--no-auto-deploy` if you prefer manual control.

### **Sync Command (Stay In Sync)**
```bash
/lovable:sync                       # Interactive (show changes, ask)
/lovable:sync --apply              # Auto-apply changes
/lovable:sync --dry-run            # Preview changes
/lovable:sync --manual             # Manual entry mode
/lovable:sync --debug              # Show detailed logs
```

Use this when:
- Team members add secrets in Lovable Cloud
- New functions are created
- You want to verify everything is aligned

---

## **The Math: Why This Plugin Pays for Itself**

- **Time saved per deployment:** ~7 minutes
- **Deployments per week (average project):** 5-10
- **Hours saved per week:** 0.6-1.2 hours
- **Hours saved per year:** 30-60 hours

That's **a full week of work back in your pocket every year.**

Plus: No more mistakes from copy-paste errors. No more forgotten secrets. No more "wait, did I deploy that?"

---

## **Troubleshooting**

**Plugin not updating?**
- Make sure marketplace auto-updates are enabled in Claude Code
- Or manually: `/plugin marketplace remove 10K-Digital/lovable-claude-code` then re-add

**Automation timing out?**
- Use manual mode: `/lovable:sync --manual`
- Or try again later (might be network/browser issue)

**Secrets not detected?**
- Run `/lovable:sync` to force a rescan
- Check that secrets use `Deno.env.get("SECRET_NAME")` pattern

---

## **What Gets Synced Automatically**

> **Note:** Lovable now supports two architectures. New projects (post-April 2026) use **TanStack Start (SSR)**; older projects use **Vite SPA**. The plugin detects this automatically.

### Vite SPA projects (`vite.config.ts`)

| What | Auto-Syncs | Next Step |
|------|-----------|-----------|
| React components (`src/`) | ✅ Yes | Just push to GitHub |
| Styling/CSS | ✅ Yes | Just push to GitHub |
| Supabase Edge Function code | ⚠️ Partially | Also run `/lovable:deploy-edge` |
| Database migrations | ⚠️ Partially | Also run `/lovable:apply-migration` |
| New tables | ❌ No | Use Lovable Cloud UI |
| RLS policies | ❌ No | Use Lovable Cloud UI |
| Secrets | ❌ No | Use Lovable Cloud UI |

### TanStack Start projects (`app.config.ts`)

| What | Auto-Syncs | Next Step |
|------|-----------|-----------|
| React components (`app/`) | ✅ Yes | Just push to GitHub |
| TanStack server functions (`*.server.ts`) | ✅ Yes | Just push to GitHub — no deploy prompt needed! |
| Styling/CSS | ✅ Yes | Just push to GitHub |
| Supabase Edge Function code | ⚠️ Partially | Also run `/lovable:deploy-edge` |
| Database migrations | ⚠️ Partially | Also run `/lovable:apply-migration` |
| New tables | ❌ No | Use Lovable Cloud UI |
| RLS policies | ❌ No | Use Lovable Cloud UI |
| Secrets | ❌ No | Use Lovable Cloud UI |

---

## **Technical Details (For The Curious)**

### **How It Works Under the Hood**

This plugin provides:

**🎯 Commands** (`/lovable:*`)
- Interactive setup that scans your codebase
- Deployment helpers for Edge Functions and migrations
- Sync utility to keep config in sync with Lovable Cloud

**🧠 Skills**
- Lovable integration patterns (what syncs, what doesn't)
- Secret detection algorithms (scans code for env vars)
- Yolo mode automation (browser automation workflows)

**📋 Config Generation**
- Creates `CLAUDE.md` with project context
- Tracks secrets and their status
- Stores yolo mode preferences

### **Architecture**

```
Your IDE (Claude Code)
    ↓
lovable-claude-code plugin
    ├─ Scans your codebase
    ├─ Detects secrets & functions
    ├─ Generates exact Lovable prompts
    └─ Optionally auto-executes via browser
    ↓
GitHub (two-way sync)
    ↓
Lovable Cloud (deploys)
```

### **Security & Privacy**

- ✅ No credentials stored in the plugin
- ✅ All automation is transparent (you see what's happening)
- ✅ Manual fallback always available
- ✅ Open source ([github.com/10K-Digital/lovable-claude-code](https://github.com/10K-Digital/lovable-claude-code))

### **Browser Automation Details**

Yolo mode uses the [Claude in Chrome extension](https://chrome.google.com/webstore/detail/claude/pebppomjfocnoigkeepgbmcifnnlndla) to:
- Navigate to your Lovable project
- Interact with the chat interface
- Submit deployment prompts
- Monitor for success

**Note:** Always has manual fallback if anything goes wrong.

---

## **Files Generated**

After running `/lovable:init`, your project gets:

```
your-project/
├── AGENTS.md              # Provider-neutral instructions (canonical)
├── CLAUDE.md              # Claude Code compatibility shim
├── .lovable-agent/
│   ├── config.json        # Project/sync/deploy/testing metadata
│   ├── context.md        # Generated context without secret values
│   ├── preview-token.local # Access token (gitignored, 7-day validity)
│   └── tests/             # Plans, profiles, and results
│       ├── plans/
│       ├── profiles/
│       └── results/
├── .claude/lovable-claude/test/   # Legacy alias, migrated on demand
└── ... your regular code
```

Edit `.lovable-agent/config.json` and `AGENTS.md` to customize the shared workflow. Claude Code also
reads the generated `CLAUDE.md` compatibility shim.

---

## **Version History**

**v2.0.0** (Latest) ⭐
- Provider-neutral Agent Skills for Codex and other coding agents
- Canonical `.lovable-agent/` project configuration and Preview test workspace
- `AGENTS.md` instructions with Claude Code compatibility shims
- Official Lovable MCP packaging plus browser and manual fallbacks
- Idempotent migration from `.claude/lovable-claude/test/`
- Codex marketplace metadata and optional Codex hook definitions

**v1.9.0**
- **Preview Testing (beta)** - test your app in Lovable Preview mode via browser automation
  - New `/lovable:test-init` wizard - scans your codebase, suggests test plans for main user actions
  - New `/lovable:test-run` - run plans in Preview (`--smoke`, `--changed`, `--all`, or one plan)
  - New `/lovable:test-sync` - resync coverage when new features lack test plans
  - Standardized workspace at `.claude/lovable-claude/test/` (plans, profiles, results)
  - Preview access via logged-in browser OR tokenized preview URL (7-day token, stored gitignored)
  - Integrated into `/lovable:init` (Question 8.7) and yolo mode (post-deploy Level 4 tests)
  - Fixed marketplace.json source field (install error regression)

**v1.8.1**
- **TanStack Start (SSR) support** - plugin now understands Lovable's new architecture
  - Auto-detects project type: Vite SPA (`vite.config.ts`) vs TanStack Start (`app.config.ts`)
  - Knows that TanStack server functions (`*.server.ts`) auto-deploy — no Lovable prompt needed
  - Separate structure maps, workflow rules, and scanning for each architecture
  - Fully backward-compatible: Vite SPA projects unaffected

**v1.8.0**
- **Lovable MCP integration** - deploy via API instead of browser (3-5x faster, no Chrome extension)
  - New `/lovable:connect-mcp` command for guided MCP setup
  - 3-tier priority: MCP → browser automation → manual prompt

**v1.7.0**
- **Project Structure Map** - Claude navigates your codebase faster!
  - New `/lovable:map` command for generating/updating maps
  - Integrated into `/lovable:init` (optional question)
  - Use `/lovable:sync --refresh-map` to update
  - ~60 line map with directory tree, key files, patterns
- **Multi-plugin architecture** - repository restructured for future plugins
  - Plugin files now in `plugins/lovable/`
  - Marketplace can host multiple plugins
  - No changes needed for existing users

**v1.4.1**
- **Auto-push independence** - works separately from yolo mode!
- Auto-push can be ON while yolo mode is OFF (manual deployment)
- Yolo mode requires auto-push (enforced when enabling)
- Clearer configuration and mental model

**v1.4.0**
- **Auto-push to GitHub** - automatic commit and push after task completion!
- Complete workflow automation when combined with yolo mode
- Smart commit messages following your project's style

**v1.3.0**
- **Auto-deploy after git push** - no manual commands needed!
- New `--auto-deploy` / `--no-auto-deploy` flags
- Improved graceful fallbacks
- Order-aware deployment (migrations before functions)

**v1.2.0**
- Enhanced secret detection with browser automation
- New `/lovable:sync` command
- Auto-run tests support
- Better init flow

**v1.1.0**
- Yolo mode (automated deployments)
- Initial commands and skills

See [CHANGELOG.md](CHANGELOG.md) for full details.

---

## **License**

MIT—Use it however you want.

## **Contributing**

Found a bug? Have a feature request?
👉 [Open an issue](https://github.com/10K-Digital/lovable-claude-code/issues)

---

## **Made With ❤️ by 10K Digital**

Questions? [GitHub Issues](https://github.com/10K-Digital/lovable-claude-code/issues)
