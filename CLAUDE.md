# CLAUDE.md

> Compatibility shim: read [`AGENTS.md`](AGENTS.md) first for provider-neutral instructions.
> This file retains Claude Code-specific repository notes and remains supported for existing users.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code plugin** for integrating with Lovable.dev projects. It's distributed as a plugin, not a typical software project with build steps or test suites.

- **Repository**: https://github.com/10K-Digital/lovable-claude-code
- **Current Version**: 2.0.0
- **Type**: Claude Code plugin marketplace (supports multiple plugins)
- **Distribution**: Via Claude Code plugin marketplace (10K-Digital/lovable-claude-code)

## Architecture

### Repository Structure (Multi-Plugin)

This repository is a **plugin marketplace** that can host multiple plugins. Currently contains the `lovable` plugin:

```
.claude-plugin/              # Marketplace metadata (publisher-level)
└── marketplace.json         # Lists all plugins in this marketplace

plugins/                     # Plugin directory (one folder per plugin)
└── lovable/                 # Lovable.dev integration plugin
    ├── .claude-plugin/      # Claude Code plugin manifest (canonical location)
    │   └── plugin.json      # Plugin definition (version, description)
    ├── commands/            # Slash commands (/lovable:* commands)
    │   ├── init-lovable.md  # Initialize project context
    │   ├── map-codebase.md  # Generate Project Structure Map (NEW in v1.7.0)
    │   ├── deploy-edge.md   # Deploy edge functions
    │   ├── apply-migration.md # Apply database migrations
    │   ├── sync-lovable.md  # Sync with Lovable Cloud
    │   ├── yolo.md          # Toggle automation mode
    │   ├── test-init.md     # Preview testing wizard (NEW in v1.9.0)
    │   ├── test-run.md      # Run test plans in Preview (NEW in v1.9.0)
    │   ├── test-sync.md     # Resync test coverage (NEW in v1.9.0)
    │   └── [others].md
    ├── hooks/               # Claude Code hooks
    │   ├── hooks.json       # Hook configuration (Start and Stop events)
    │   ├── auto-sync.sh     # Auto-sync (Start event)
    │   └── auto-push.sh     # Auto-push (Stop event)
    ├── skills/              # Contextual skills
    │   ├── lovable/
    │   │   ├── SKILL.md     # Core Lovable integration patterns
    │   │   └── references/  # Supporting documentation
    │   │       ├── CLAUDE-template.md  # Template for generated CLAUDE.md
    │   │       ├── codebase-map.md     # Project Structure Map patterns (NEW)
    │   │       ├── prompts.md          # Lovable prompt library
    │   │       └── secret-detection.md # Secret scanning patterns
    │   ├── yolo/
    │   │   ├── SKILL.md     # Browser automation orchestration
    │   │   └── references/  # Automation workflows
    │   └── testing/         # Preview testing (NEW in v1.9.0)
    │       ├── SKILL.md     # Preview testing orchestration
    │       └── references/  # preview-access, test-plan-format,
    │                        # test-wizard, test-execution
    └── agents/              # Autonomous agents
        └── sync-agent.md    # Multi-phase sync agent

.claude/                     # Repository-level settings
└── settings.local.json      # Pre-approved git operations

CLAUDE.md                    # This file (repo documentation)
README.md                    # User-facing documentation
CHANGELOG.md                 # Version history
```

**Adding a new plugin**: Create a new folder under `plugins/` with its own `plugin.json` and add it to `marketplace.json`.

### Key Architectural Concepts

#### 1. Two-Tier Documentation System

**Commands** (`/lovable:*`) contain:
- User-facing instructions for Claude to execute
- Step-by-step procedural workflows
- User interaction patterns (questions, confirmations)
- CLAUDE.md generation logic

**Skills** (auto-activate) contain:
- Conceptual knowledge about Lovable integration
- When to use what approach
- Reference materials for complex operations
- Browser automation workflows

**Reference files** (`skills/*/references/`) contain:
- Detailed implementation procedures
- Edge case handling
- UI automation selectors and wait conditions
- Testing procedures

#### 2. CLAUDE.md Generation Pattern

This plugin's core feature is **generating CLAUDE.md files** for user projects (not this repo). The flow:

1. User runs `/lovable:init` in their Lovable project
2. Plugin scans their codebase (edge functions, migrations, secrets)
3. Asks 12-15 questions about their setup
4. Generates `CLAUDE.md` in their project root using `plugins/lovable/skills/lovable/references/CLAUDE-template.md`
5. This CLAUDE.md gives future Claude instances context about their Lovable project

**Critical distinction**: This repo contains the plugin code. User projects get a generated CLAUDE.md.

#### 3. Auto-Sync, Auto-Push, and Yolo Mode Features

**Auto-Sync** (NEW in v1.5.0):
- **Hook-based implementation** - uses Claude Code's Start event hook for 100% reliability
- Automatically pulls latest changes from GitHub when Claude starts working
- **Always-on feature** - runs automatically on every Start event (no configuration needed)
- Implemented in `plugins/lovable/hooks/auto-sync.sh` (triggered by `plugins/lovable/hooks/hooks.json`)
- Safety checks: only on main branch, no uncommitted changes, local is behind remote
- Uses `git pull --rebase` to maintain clean history
- Gracefully handles conflicts - aborts and notifies user if conflicts detected
- **Prevents diverged branch issues** - checks if local/remote have diverged before pulling

**Auto-Push** (v1.4.0, refined in v1.4.1, hook-based in v1.5.0):
- **Hook-based implementation** - uses Claude Code's Stop event hook for 100% reliability
- Automatically commits and pushes to GitHub after Claude finishes responding
- **Independent feature** - can be enabled without yolo mode
- Configured via `Auto-Push to GitHub: on/off` in user's CLAUDE.md (separate section)
- Implemented in `plugins/lovable/hooks/auto-push.sh` (triggered by `plugins/lovable/hooks/hooks.json`)
- Safety checks: auto-push enabled, file changes exist, on main branch
- **More reliable** than skill-based approach (v1.4.x) - hooks guarantee execution

**Yolo Mode / Auto-Deploy** (v1.3.0):
- After git push, automatically deploy backend changes to Lovable via browser automation
- **Requires auto-push to be enabled** (dependency enforced)
- Configured via yolo mode section in user's CLAUDE.md
- Implemented in `plugins/lovable/skills/yolo/` with browser automation
- Detects changes in `supabase/functions/` or `supabase/migrations/`

**Independence vs Dependency**:
- Auto-push can be ON with yolo mode OFF (manual deployment workflow)
- Yolo mode REQUIRES auto-push to be ON (automatic deployment)
- Disabling yolo mode does NOT disable auto-push

**Complete workflow with all features enabled**:
```
User starts conversation
  → Auto-sync: pull latest from GitHub (Start hook)
  → User asks for changes
  → Claude makes changes
  → Auto-push: commit + push to GitHub (Stop hook)
  → Yolo mode: detect backend changes → navigate to Lovable → submit deployment
  → Verification tests run
  → Done (zero manual commands)
```

**Workflow with only auto-push** (yolo mode off):
```
User starts conversation
  → Auto-sync: pull latest from GitHub (Start hook)
  → User asks for changes
  → Claude makes changes
  → Auto-push: commit + push to GitHub (Stop hook)
  → GitHub syncs frontend to Lovable instantly
  → User manually deploys backend via /deploy-edge or copy-paste prompts
```

#### 4. Yolo Mode (Browser Automation)

"Yolo mode" = browser automation for Lovable deployments. Requires Claude in Chrome extension.

**Activation conditions** (in user projects):
- `yolo_mode: on` in user's CLAUDE.md
- Commands: `/deploy-edge`, `/apply-migration`
- Auto-triggers after git push if `auto_deploy: on`

**Implementation**:
- Orchestration logic: `plugins/lovable/skills/yolo/SKILL.md`
- Browser workflows: `plugins/lovable/skills/yolo/references/automation-workflows.md`
- Detection logic: `plugins/lovable/skills/yolo/references/detection-logic.md`
- Testing: `plugins/lovable/skills/yolo/references/testing-procedures.md`

**Graceful degradation**: Always provides manual prompts as fallback if automation fails.

## Working with This Repository

### Versioning

When making changes that affect functionality:

1. Update version in `plugins/lovable/.claude-plugin/plugin.json`
2. Add entry to `CHANGELOG.md` following existing format
3. Update `README.md` if user-facing features changed
4. Update `.claude-plugin/marketplace.json` to match plugin version

**Version scheme**: Semantic versioning
- Patch (1.4.x): Bug fixes, documentation
- Minor (1.x.0): New features, new commands
- Major (x.0.0): Breaking changes to commands/skills

### Making Changes

#### Adding/Modifying Commands

Commands are markdown files in `plugins/lovable/commands/`. Structure:

```markdown
---
description: Short description for command listing
---

# Command Name

Full user-facing instructions that Claude will read and execute.

## Instructions

Step-by-step procedural logic...
```

**Important**: Commands describe what Claude should DO, not what the feature is.

#### Adding/Modifying Skills

Skills are markdown files in `plugins/lovable/skills/*/SKILL.md`. Structure:

```markdown
---
name: skill-name
description: |
  When this skill activates (conditions).
  What it provides (knowledge, patterns).
---

# Skill Name

Conceptual knowledge, patterns, and guidance...
```

**Important**: Skills describe WHEN to activate and WHAT to know, not step-by-step procedures (those go in references/).

#### Reference Files

Reference files (`plugins/lovable/skills/*/references/*.md`) contain:
- Detailed procedures that skills reference
- Browser automation selectors and workflows
- Edge case handling
- Testing procedures
- Templates (like CLAUDE-template.md)

### Auto-Push Configuration in This Repo

This repository has `.claude/settings.local.json` with pre-approved git operations:

```json
{
  "permissions": {
    "allow": [
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git pull:*)",
      "Bash(git rebase:*)"
    ]
  }
}
```

This allows Claude to commit and push changes when helping develop this plugin.

## Important Patterns

### 1. User Project vs Plugin Repo Context

Always distinguish between:
- **This repo**: The plugin source code (what you're working on now)
- **User projects**: Lovable projects where this plugin is used

Most documentation in this repo describes how to work with **user projects**, not this repo itself.

### 2. Lovable Integration Model

Lovable uses **two-way GitHub sync** on main branch only:
- ✅ Frontend (`src/`) syncs automatically
- ⚠️ Backend (edge functions, migrations) require Lovable prompts to deploy
- ❌ Database operations (tables, RLS, storage) must be done directly in Lovable UI

This plugin bridges the gap by:
1. Detecting when backend operations are needed
2. Generating exact Lovable prompts
3. Optionally automating prompt submission via browser

### 3. Question Flow in /init-lovable

The initialization command asks 13-15 questions in specific order:
1. Backend type (Lovable Cloud vs own Supabase)
2. Production URL
3. GitHub repository
4. Supabase project (if own)
5. Lovable project URL (optional, enables automation)
6. Secret detection method
7. Edge functions context
8. Database tables (optional)
8.5. **Project Structure Map** ← NEW in v1.7.0, helps Claude navigate faster
8.7. **Preview Testing** ← NEW in v1.9.0, captures preview URL/token, offers test wizard
9. **Auto-push toggle** ← NEW in v1.4.0, independent feature
10. Special instructions
11. Yolo mode toggle (checks auto-push requirement)
12. Testing configuration (if yolo enabled)
13. Lovable URL (if skipped in Q5 but yolo enabled)

**Order matters**: Auto-push (Q9) asked before yolo mode (Q11) because yolo requires it.

### 4. Safety and Fallbacks

**Golden rule**: Never block the user. Every automation must have manual fallback.

Examples:
- Browser automation fails → Show manual prompt to copy-paste
- Auto-push fails → Suggest manual git commands
- Auto-deploy fails → Show deployment prompt for manual execution

### 5. Beta Features

Yolo mode (browser automation) and preview testing are marked as **beta**:
- Always show beta warnings when enabling
- Explain risks and requirements
- Provide manual alternatives
- Gracefully handle UI changes

### 6. Preview Testing (v1.9.0)

Tests user projects **in Lovable Preview mode** via browser automation:

- **Test workspace** in user projects: `.claude/lovable-claude/test/` (plans/, profiles/, results/, test-config.json)
- **Preview access**: tokenized preview URL (`https://preview--app.lovable.app/?__lovable_token=...`, captured via the arrow icon next to the preview address bar, **7-day validity**) OR logged-in Chrome session
- **Token is a credential**: stored ONLY in `preview-token.local` (gitignored before writing), never in CLAUDE.md/config/output
- **Commands**: `/lovable:test-init` (wizard), `/lovable:test-run` (execute), `/lovable:test-sync` (coverage resync)
- **Maintenance loop**: implementing a feature in a project with testing enabled should also add/update unit tests + test plans
- **Implementation**: `plugins/lovable/skills/testing/` (SKILL.md + 4 references)

## Common Workflows

### Publishing a New Version

1. Make your changes to `plugins/lovable/` (commands/skills/references)
2. Update `plugins/lovable/.claude-plugin/plugin.json` version
3. Update `.claude-plugin/marketplace.json` version to match
4. Update `CHANGELOG.md` with changes
5. Update `README.md` if needed
6. Commit with message: "Bump version to X.Y.Z" and a brief description of changes
7. Push to GitHub
8. Plugin marketplace auto-updates from GitHub

### Testing Changes Locally

This plugin has no automated tests. To test:

1. Make changes to plugin files
2. Use the plugin in a test Lovable project
3. Run commands like `/lovable:init` to verify behavior
4. Check generated CLAUDE.md files
5. Test automation features if modified

### Adding a New Command

1. Create `plugins/lovable/commands/new-command.md`
2. Add frontmatter with description
3. Write step-by-step instructions for Claude
4. Reference relevant skills if needed
5. Update README.md to mention new command
6. Update version and CHANGELOG.md

### Adding Reference Documentation

1. Create file in appropriate `plugins/lovable/skills/*/references/` directory
2. Write detailed procedures, workflows, or templates
3. Reference from skill's SKILL.md using relative path
4. Keep references focused on implementation details

## Plugin Distribution

- **Installation**: `/plugin marketplace add 10K-Digital/lovable-claude-code`
- **Namespace**: `lovable` (commands are `/lovable:*`)
- **Auto-updates**: Users can enable in Claude Code settings
- **Marketplace**: https://github.com/10K-Digital/lovable-claude-code

## Key Files to Understand

If you need to understand how this plugin works:

1. **README.md** - User-facing documentation and feature explanations
2. **CHANGELOG.md** - Version history and changes
3. **plugins/lovable/commands/init-lovable.md** - Most complex command, orchestrates project setup
4. **plugins/lovable/commands/map-codebase.md** - Project Structure Map generation (NEW in v1.7.0)
5. **plugins/lovable/skills/lovable/SKILL.md** - Core integration patterns
6. **plugins/lovable/skills/yolo/SKILL.md** - Browser automation orchestration
7. **plugins/lovable/skills/lovable/references/CLAUDE-template.md** - Template for generated project files
8. **plugins/lovable/skills/lovable/references/codebase-map.md** - Map generation patterns (NEW in v1.7.0)
9. **plugins/lovable/skills/yolo/references/automation-workflows.md** - Browser automation implementation
10. **plugins/lovable/skills/testing/SKILL.md** - Preview testing orchestration (NEW in v1.9.0)
11. **plugins/lovable/skills/testing/references/test-plan-format.md** - Standardized test workspace formats (NEW in v1.9.0)




Each version builds on previous automation layers to reduce manual work.

### v1.9.0 Architecture Change

v1.9.0 added **Preview Testing** - a third skill (`plugins/lovable/skills/testing/`):
- Tests user apps in Lovable Preview mode via browser automation (after each implementation or planned e2e runs)
- New commands: `/lovable:test-init` (wizard scans codebase, suggests plans), `/lovable:test-run`, `/lovable:test-sync` (coverage resync)
- Standardized test workspace generated in user projects at `.claude/lovable-claude/test/`
- Preview access via tokenized preview URL (7-day JWT, gitignored storage) or logged-in browser
- Integrations: `/lovable:init` Question 8.7, yolo post-deploy verification Level 4
- Also fixed the recurring marketplace.json `source` regression (`"plugins/lovable/"` → `"./plugins/lovable"`)

### v1.7.0 Architecture Change

In v1.7.0, two major changes were made:
1. **Multi-plugin structure** - Repository restructured to support multiple plugins
   - Plugin files moved to `plugins/lovable/`
   - Marketplace.json at root points to plugin directories
   - Enables adding future plugins to same marketplace
2. **Project Structure Map** - New feature to help Claude navigate faster
   - New command: `/lovable:map` for generating/updating maps
   - Integration with `/lovable:init` (Question 8.5)
   - Integration with `/lovable:sync --refresh-map`
   - Generates ~60 line map with directory tree, key files, patterns

### v1.5.0 Architecture Change

In v1.5.0, auto-push was reimplemented using Claude Code hooks for improved reliability:
- **Hook-based implementation** - Auto-push logic moved from skills to hooks
- Uses Stop event hook (`plugins/lovable/hooks/hooks.json` + `plugins/lovable/hooks/auto-push.sh`)
- **100% reliable** - Hooks execute deterministically vs. Claude remembering to check
- Cleaner separation of concerns - Skills provide knowledge, hooks provide automation
- All safety checks preserved (enabled in CLAUDE.md, changes exist, main branch)
- User experience unchanged - Same configuration, same behavior, more reliable execution

### v1.4.1 Architecture Change

Originally in v1.4.0, auto-push was tied to yolo mode. In v1.4.1, this was changed to:
- Auto-push is now a separate, independent feature
- Users can enable auto-push without yolo mode (faster git workflow, manual deploys)
- Yolo mode still requires auto-push (one-way dependency)
- Clearer separation in CLAUDE.md template and `/yolo` command
