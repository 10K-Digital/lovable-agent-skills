# Changelog

All notable changes to the Lovable Claude Code plugin will be documented in this file.

## [2.0.0] - 2026-08-12

### Added

- Provider-neutral Agent Skills for project context, GitHub sync, Lovable deployment, and Preview testing.
- Codex plugin manifest, repository marketplace metadata, official Lovable MCP configuration, and optional Codex hooks.
- Canonical `.lovable-agent/` project contract with `AGENTS.md` instructions and Claude Code compatibility shims.
- Idempotent `migrate-workspace.py` migration from `.claude/lovable-claude/test/`.
- Automated skill, plugin, migration, secret-safety, and packaging validation tests.
- README guidance for Codex installation and Claude Code GitHub Actions PR reviews.

### Changed

- Versioned Claude marketplace and plugin metadata at 2.0.0 while preserving existing Claude commands and hooks.
- Auto-push accepts neutral `.lovable-agent/config.json` settings while retaining CLAUDE.md behavior.

## [1.9.0] - 2026-06-10

### Added

#### Preview Testing (Beta) - Test Your App in Lovable Preview Mode

**Problem**: There was no way to verify that implemented features actually work in the running app. Yolo mode verified *deployments* (logs, console, endpoints), but nobody tested the app's actual user flows - signup, CRUD, invitations - in the live Preview.

**Solution**: A new `testing` skill plus three commands that run standardized test plans against the **Lovable Preview app** via browser automation - after each implementation or as planned end-to-end runs.

**Preview access (two methods):**
1. **Tokenized preview URL** (preferred): the user opens the Lovable project in preview mode, clicks the arrow icon next to the preview address bar, and copies the URL from the new tab (`https://preview--app.lovable.app/?__lovable_token=...`). The token is valid for **7 days**; the plugin decodes the JWT expiry, stores the token gitignored, and re-prompts when it expires.
2. **Logged-in browser session**: the user stays logged in to Lovable in Chrome (Claude in Chrome extension).

**Standardized test workspace** created in the user's project:

```
.claude/lovable-claude/test/
├── README.md              # Workspace guide
├── test-config.json       # Preview URL, settings, coverage baseline (committed)
├── preview-token.local    # Access token ONLY (gitignored, 7-day validity)
├── plans/                 # Test plans (TP-NNN-slug.md, frontmatter + steps table)
├── profiles/              # Test user personas (test credentials only)
└── results/               # Dated test run reports
```

#### New Commands

- **`/lovable:test-init`** - Test wizard: scans the codebase (routes, forms, mutations, auth flows, edge function calls, roles), suggests test plans for the app's main user actions, asks guided questions, captures the preview URL/token, and generates the workspace. `--refresh-token` renews an expired token.
- **`/lovable:test-run`** - Executes test plans in Preview via browser automation. Scopes: `TP-NNN` (one plan), `--smoke`, `--changed` (plans covering recently changed files), `--all` (full end-to-end). Writes dated result reports and offers to fix failures.
- **`/lovable:test-sync`** - Resync: diffs the codebase against the last sync commit, finds new/changed features lacking test plans (and unit tests), suggests new plans, updates stale ones, deprecates orphans. `--apply` and `--dry-run` flags.

#### New Skill: `skills/testing/`

- `SKILL.md` - Orchestration: activation conditions, access priority, workspace structure, configuration, error handling
- `references/preview-access.md` - Token capture/parsing/storage (gitignore enforcement), JWT expiry decoding, access priority, re-prompt flows
- `references/test-plan-format.md` - Standardized formats for plans, profiles, config, results, IDs
- `references/test-wizard.md` - Codebase scanning heuristics and the guided question flow
- `references/test-execution.md` - Browser automation execution, verification (UI/URL/console/network), sync wait after push, manual fallback

#### Integrations

- **`/lovable:init`** - New Question 8.7 asks about preview testing, captures the preview URL/token during setup, and offers to run the wizard afterwards. Generated CLAUDE.md gains a **Preview Testing Configuration** section.
- **Yolo mode** - New optional verification **Level 4**: after auto-deploy, runs the `smoke` (or `all`) test plans per the `Test After Deploy` setting.
- **Continuous maintenance** - When preview testing is enabled, implementing a new feature also adds/updates unit tests and test plans (automatic run if `Test After Implementation: on`, otherwise a `/lovable:test-sync` reminder).

#### Safety

- The preview token is a credential: stored only in `preview-token.local`, gitignored before writing, never echoed in output, CLAUDE.md, or commits
- Tests target Preview, never production; payments/destructive steps are `[MANUAL]` by format rule
- Never blocks: if automation is unavailable, plans double as manual test checklists

### Fixed

- `.claude-plugin/marketplace.json`: `source` field regressed again to the invalid `"plugins/lovable/"` form (causes `plugins.0.source: Invalid input` on install). Restored to `"./plugins/lovable"`.

### Changed

- `plugins/lovable/plugin.json`: Version 1.8.1 → 1.9.0, description and keywords updated
- `.claude-plugin/marketplace.json`: Version 1.8.1 → 1.9.0
- `plugins/lovable/skills/lovable/references/CLAUDE-template.md`: Added Preview Testing Configuration section
- `plugins/lovable/skills/yolo/SKILL.md`: Added Level 4 (preview test plans) to post-deploy verification

## [1.8.1] - 2026-06-09

### Added

#### TanStack Start (SSR) Architecture Support

**Problem**: Lovable launched TanStack Start as the default for all new projects (post-April 2026), replacing the Vite SPA architecture. New projects use SSR, file-based routing (`app/routes/`), and TanStack server functions — a fundamentally different structure from legacy projects.

**Solution**: Update plugin to detect and support both architectures, while remaining fully backward-compatible with all existing Vite SPA projects.

**Key architectural differences handled:**

| Feature | Vite SPA (legacy) | TanStack Start (new) |
|---------|-------------------|----------------------|
| Config file | `vite.config.ts` | `app.config.ts` |
| Source directory | `src/` | `app/` |
| Routing | React Router in `src/App.tsx` | File-based in `app/routes/` |
| Rendering | Client-side only | Server-side (SSR) |
| Server logic | Only via Supabase Edge Functions | Also via TanStack server functions (`*.server.ts`) |
| Server functions deploy | Via Lovable prompt | Auto via GitHub sync |

**Critical distinction for Claude:** TanStack server functions (`app/**/*.server.ts`) are **not** Supabase Edge Functions. They auto-deploy when pushed to GitHub and never need a Lovable deployment prompt. Only `supabase/functions/` still requires manual deployment via Lovable.

#### Files Updated

- `plugins/lovable/skills/lovable/SKILL.md`
  - Added "Project Architecture Types" section with detection rules
  - Separated "What Syncs Automatically" into Vite SPA and TanStack Start sections
  - Updated "File Structure Reference" to document both architectures
  - Clarified that TanStack server functions auto-deploy (no Lovable prompt needed)

- `plugins/lovable/skills/lovable/references/codebase-map.md`
  - Added Step 0: Architecture detection (`app.config.ts` vs `vite.config.ts`)
  - Added TanStack Start directory scanning (`app/`, `app/routes/`)
  - Added TanStack Start key files table (`__root.tsx`, `*.server.ts`, `app.config.ts`)
  - Updated routing detection to include TanStack file-based routing conventions
  - Added separate map templates for Vite SPA and TanStack Start projects

- `plugins/lovable/skills/lovable/references/CLAUDE-template.md`
  - Added `Architecture` field to Project Overview
  - Added dual-architecture Project Structure Map templates (Vite SPA and TanStack Start)
  - Added architecture-aware Workflow Rules with inline comments for conditional use

- `plugins/lovable/commands/init-lovable.md`
  - Updated scan step (Step 2) to detect architecture type first
  - Made source file scanning conditional on detected architecture
  - Updated Question 8.5 (map generation) to use architecture-specific scanning
  - Updated CLAUDE.md template to include Architecture field and conditional workflow rules

### Changed

- `plugins/lovable/plugin.json`: Version 1.8.0 → 1.8.1
- `.claude-plugin/marketplace.json`: Version 1.8.0 → 1.8.1

### Backward Compatibility

**No action required for existing users.** All Vite SPA projects continue to work exactly as before. The plugin detects the architecture automatically and applies the appropriate rules.

- Old projects (Vite SPA) → plugin behaves identically to v1.8.0
- New projects (TanStack Start) → plugin now correctly understands the structure

## [1.8.0] - 2026-06-09

### Added

#### Lovable MCP Integration (Yolo Mode Upgrade)

**Problem**: Yolo mode required the Claude in Chrome extension and browser automation to submit prompts to Lovable. This was slow, fragile to UI changes, and unavailable in headless environments.

**Solution**: Integrate the official Lovable MCP server (`https://mcp.lovable.dev`) as the preferred deployment method in yolo mode. When connected, Claude sends prompts directly via API instead of navigating the browser.

**Benefits of MCP over browser automation:**
- 3-5x faster deployments (API vs browser navigation)
- No Chrome extension required
- Not affected by Lovable UI changes
- Works in any environment (headless, CI, etc.)

#### New Command: `/lovable:connect-mcp`

Step-by-step setup wizard that guides users through connecting the Lovable MCP server to Claude:

```bash
/lovable:connect-mcp           # Interactive setup (Claude Code, Desktop, or claude.ai)
/lovable:connect-mcp verify    # Verify the connection is working
/lovable:connect-mcp status    # Show current MCP connection status
```

The command covers setup for:
- **Claude Code** - `claude mcp add --transport http lovable https://mcp.lovable.dev`
- **Claude Desktop** - Settings → Connectors → Add custom connector
- **claude.ai** - Settings → Connectors → Add custom connector

#### New Deployment Method Flag in `/lovable:yolo`

```bash
/yolo on --mcp      # Use Lovable MCP only (fastest)
/yolo on --browser  # Use browser automation only (legacy)
/yolo on --auto     # Try MCP first, fall back to browser (default)
```

#### New Reference: `skills/yolo/references/mcp-workflows.md`

Complete implementation reference for MCP-based deployments:
- Project ID extraction from `lovable_url`
- `send_message` tool call patterns
- Async polling with `get_message`
- Error handling (auth errors, credits exhausted, MCP not available)
- Comparison table: MCP vs browser automation

#### Deployment Method in CLAUDE.md

New `Deployment Method` field in yolo mode configuration:
```markdown
- **Deployment Method**: auto   # auto | mcp | browser
```

### Changed

#### Yolo Mode Priority Order

Yolo mode now uses a 3-tier priority system:
1. **Lovable MCP** (preferred) - tries first when `auto` or `mcp`
2. **Browser automation** (fallback) - used when MCP unavailable and `auto`
3. **Manual prompt** (last resort) - always available as copy-paste fallback

#### Yolo Mode Beta Warning

The `/yolo on` command now detects whether MCP is connected and shows context-aware warnings:
- MCP connected: Highlights API speed and no Chrome extension requirement
- MCP not connected: Suggests running `/lovable:connect-mcp` for better experience

#### `/deploy-edge` Yolo Mode Integration

Updated to route through MCP when available, with browser automation fallback.

## [1.7.0] - 2026-01-05

### Added

#### Project Structure Map (Faster Navigation)

**Problem**: Claude Code was slower than Lovable because it needs to search and understand the codebase on its own, while Lovable likely has a pre-built understanding of the project structure.

**Solution**: Generate a "Project Structure Map" in CLAUDE.md that helps Claude navigate user codebases significantly faster.

#### New Command: `/lovable:map`

```bash
/lovable:map              # Generate and display map
/lovable:map --update     # Update CLAUDE.md with new map
/lovable:map --verbose    # Show detailed scanning output
```

**What the map includes** (~60 lines for token efficiency):
- **Directory tree** with purposes and item counts
- **Key files table** (App.tsx, utils.ts, supabase client, etc.)
- **Patterns detected** (component organization, state management)
- **Data flow** overview
- **Quick lookup table** for common searches

#### Integration with Existing Commands

**`/lovable:init`** - New Question 8.5:
```
Would you like me to generate a Project Structure Map?
This helps me navigate your codebase faster.
Generate map? (yes/no)
Default: yes (recommended)
```

**`/lovable:sync`** - New flag:
```bash
/lovable:sync --refresh-map    # Regenerate Project Structure Map
```

### Changed

#### Multi-Plugin Repository Architecture

**Problem**: Repository structure only supported a single plugin, making it impossible to add more plugins to the marketplace.

**Solution**: Restructure repository to support multiple plugins.

**New structure**:
```
.claude-plugin/
└── marketplace.json         # Publisher-level (lists all plugins)

plugins/
└── lovable/                 # Lovable plugin (all files moved here)
    ├── plugin.json
    ├── commands/
    ├── skills/
    ├── hooks/
    └── agents/
```

**Migration notes**:
- **No action required for users** - Installation command unchanged
- Plugin files moved from root to `plugins/lovable/`
- `marketplace.json` updated with new source path
- Future plugins can be added under `plugins/[name]/`

### Files Added

- `plugins/lovable/commands/map-codebase.md` - New command for generating maps
- `plugins/lovable/skills/lovable/references/codebase-map.md` - Map generation patterns and scanning logic

### Files Modified

- `plugins/lovable/skills/lovable/references/CLAUDE-template.md` - Added Project Structure Map section
- `plugins/lovable/commands/init-lovable.md` - Added Question 8.5 for map generation
- `plugins/lovable/commands/sync-lovable.md` - Added `--refresh-map` flag
- `plugins/lovable/agents/sync-agent.md` - Added Phase 2.5 for map refresh
- `.claude-plugin/marketplace.json` - Updated source path to `plugins/lovable/`
- `CLAUDE.md` - Updated with new architecture and file paths
- `README.md` - Added new command and features

---

## [1.6.2] - 2026-01-05

### Improved

#### Major Performance Optimizations for Yolo Automation

**Problem**: Yolo automation was slow (15-45s) and error-prone with issues like clicking wrong places, forgetting to scroll, and mistyping prompts.

**Solution**: Complete overhaul of browser automation approach using modern tools and techniques.

#### Key Optimizations

**1. Ref-Based Element Interaction (Replaces Coordinates)**
- Now uses `find` tool to get element refs (e.g., `ref_42`)
- Click elements using `ref` parameter instead of `(x, y)` coordinates
- **Result**: Eliminates "clicking wrong places" issues entirely

**2. Form Input Instead of Typing (20x Faster)**
- Now uses `form_input(ref=X, value="...")` to set values instantly
- Replaces character-by-character typing (~50ms per char)
- **Result**: Prompt entry reduced from 2-3 seconds to ~100ms

**3. DOM-Based Sync Detection (Faster & More Reliable)**
- Uses `read_page` and text search instead of visual icon scanning
- Polls every 2 seconds instead of 4 seconds
- **Result**: More reliable detection, faster sync verification

**4. Minimal Screenshot Policy (75% Reduction)**
- Screenshots only on errors or final confirmation
- Uses `read_page` for element location and page state
- **Result**: 75% reduction in screenshot-related latency

**5. Hybrid Model Approach**
- **Haiku** for simple operations (clicks, form inputs, waiting)
- **Sonnet** for complex reasoning (error handling, response parsing)
- **Result**: Best of both speed and reliability

#### Performance Improvements

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Time per deployment | 15-45s | 5-12s | 2-3x faster |
| Failed attempts | 2-5 per session | 0-1 | 80%+ reduction |
| Screenshots taken | 5-8 | 1-2 | 75% reduction |
| Typing time | 2-3s | 0.1s | 20x faster |
| Sync detection | 30-80s | 2-20s | 3-4x faster |

### Files Updated

- `skills/yolo/references/automation-workflows.md`
  - Added Performance Principles section
  - Rewrote Steps 1.5, 2, 3, 4 with optimized approaches
  - Added Screenshot Policy section
  - Updated Performance Notes with new timing

- `skills/yolo/SKILL.md`
  - Added Performance Optimization section
  - Added Model Selection guidance (Haiku vs Sonnet)
  - Added Tool Preferences guidance

- `skills/yolo/references/detection-logic.md`
  - Added Step 3 for DOM-based sync verification
  - Referenced automation-workflows.md for implementation

### Migration

**No action required** - These are internal automation improvements. Yolo mode will automatically use the new, faster approach.

---

## [1.6.1] - 2026-01-04

### Fixed

#### Yolo Mode Browser Automation Improvements

**Issue #1: Slow GitHub Sync Detection**
- **Problem**: Waited 30 seconds before checking if Lovable synced from GitHub, causing slow automation
- **Solution**: Navigate immediately, check chat history every 4 seconds
- **Result**: Sync detection now takes ~8 seconds instead of 30+ seconds (4x faster!)

**How it works now**:
1. Navigate to Lovable project immediately after git push (no initial wait)
2. Check LEFT SIDEBAR chat history for GitHub icon + commit message
3. Scroll to bottom of chat history if needed
4. Check every 4 seconds (instead of 30 seconds)
5. Max 20 attempts = 80 seconds total (instead of 2 minutes)

**What to look for**:
- GitHub icon (octocat logo) next to message
- Message starts with commit message just pushed
- Message may be partially truncated
- Located in left sidebar conversation history

**Issue #2: Wrong Chat Input Used**
- **Problem**: Automation was typing in the WRONG input (top preview input instead of main chat)
- **Solution**: Explicitly target LOWER LEFT corner chat input with "Ask Lovable..." placeholder
- **Result**: Prompts now go to the correct Lovable chat interface

**Correct input location**:
- ✅ Lower left corner of page
- ✅ Placeholder: "Ask Lovable..." or similar
- ✅ Main chat interface for Lovable

**Wrong input (no longer used)**:
- ❌ Top of page input (preview/internal page)
- ❌ Any iframe inputs
- ❌ Search/filter inputs

**Files Updated**:
- `skills/yolo/references/automation-workflows.md` - Updated Steps 1.5 and 2
- `skills/yolo/references/post-push-automation.md` - Updated Step 3.5

### Benefits

**Speed improvements**:
- ⚡ **4x faster sync detection**: 8 seconds vs 30+ seconds
- ⚡ **Immediate navigation**: No more 30-second initial wait
- ⚡ **More frequent checks**: Every 4 seconds instead of 30 seconds
- ⚡ **Overall 20-40% faster** auto-deploy workflow

**Reliability improvements**:
- ✅ **Correct chat input**: No more typing in wrong place
- ✅ **Better detection**: Chat history is more reliable than UI indicators
- ✅ **Position-based verification**: Ensures lower-left corner input is used
- ✅ **Placeholder verification**: Confirms "Ask Lovable..." text

### Technical Details

**Sync detection logic** (Step 1.5):
```
OLD: Wait 30s → Check status → Wait 30s → Check → Repeat
NEW: Check immediately → Wait 4s → Check → Wait 4s → Check → Repeat

OLD: Max 2 minutes (4 attempts × 30s each)
NEW: Max 80 seconds (20 attempts × 4s each)

OLD: Looked for sync status indicators
NEW: Looks for commit message in chat history
```

**Input selection logic** (Step 2):
```
OLD: Any textarea matching generic patterns
NEW: Specifically lower-left corner with "Ask Lovable..." placeholder

Verification checklist:
- ✅ Position: Lower left corner (NOT top)
- ✅ Placeholder contains "Ask Lovable"
- ✅ NOT preview/iframe input
- ✅ Visible and enabled
```

### Migration

**No action required** - These are internal automation improvements. Yolo mode will automatically use the new, faster approach.

**Benefits apply to**:
- `/lovable:deploy-edge` with yolo mode
- `/lovable:apply-migration` with yolo mode
- Auto-deploy after git push (when `auto_deploy: on`)

---

## [1.6.0] - 2026-01-04

### Added

#### First Agent Implementation - Sync-Agent
- **New autonomous sync-agent** (`agents/sync-agent.md`) for multi-phase project synchronization
- Completes the plugin's architectural maturity with all four workflow types:
  - ✅ Commands (user interaction)
  - ✅ Skills (knowledge)
  - ✅ Hooks (event automation)
  - ✅ Agents (complex autonomous tasks) **← NEW**

#### Sync-Agent Capabilities
- **5-phase autonomous workflow**:
  1. Git synchronization (fetch, merge, conflict handling)
  2. Secret discovery (codebase scan, .env.example, Lovable Cloud)
  3. State comparison (identify new/removed/changed secrets)
  4. Update proposal (generate diff, preserve user customizations)
  5. Application (write CLAUDE.md if approved)
- **5 operational modes**: interactive, auto-apply, dry-run, manual, debug
- **Independent context window** - doesn't pollute main coding conversation
- **Parallel execution capable** - user can continue working while sync runs
- **Comprehensive error handling** with graceful degradation
- **Preserves all user customizations** in CLAUDE.md

#### Architectural Benefits
- ✅ **Independent context**: Sync operations run in separate 200K token budget
- ✅ **Not related to current code task**: Meta-operations isolated from development work
- ✅ **High complexity justified**: 5 phases, multiple tools, complex decision trees
- ✅ **Parallel workflows enabled**: Background sync while user continues coding
- ✅ **Reference implementation**: Establishes pattern for future agents

### Changed

#### /lovable:sync Command Refactored
- Refactored from procedural to agent-delegation architecture
- Command now focuses on UX (flag parsing, progress display)
- Complex sync logic moved to sync-agent
- **Breaking change**: None - all flags and behavior preserved
- **User experience**: Identical output, more reliable execution

**Before (procedural)**:
- 359 lines of inline logic
- Git, secret detection, comparison, updates all in command
- Difficult to test and maintain
- Clutters main conversation with sync details

**After (agent-delegation)**:
- 342 lines focused on UX and orchestration
- Invokes sync-agent for autonomous execution
- Clean separation of concerns
- Agent runs in separate context

### Fixed

#### Removed Duplication in Lovable Skill
- **Deleted** auto-push explanation section from `skills/lovable/SKILL.md` (lines 154-174)
- Auto-push is now 100% handled by `hooks/auto-push.sh` (added in v1.5.0)
- Skills no longer explain hook implementation details
- Cleaner separation between skills (knowledge) and hooks (automation)

**Why this matters**:
- Skills should provide knowledge Claude needs, not explain implementation
- Hook runs automatically regardless - no need to document internal behavior
- Reduces confusion about what Claude should do vs. what happens automatically

### Architectural Improvements

#### Complete Plugin Architecture
The plugin now demonstrates best practices for all workflow types:

**Commands** (user-invoked, interactive):
- Example: `/lovable:init`, `/lovable:sync`, `/lovable:deploy-edge`
- Use when: User needs to trigger, requires confirmations

**Skills** (contextual knowledge):
- Example: `lovable` (architecture), `yolo` (automation orchestration)
- Use when: Claude needs to understand concepts or patterns

**Hooks** (event-driven automation):
- Example: `auto-sync` (Start), `auto-push` (Stop)
- Use when: Deterministic, no user interaction, background tasks

**Agents** (complex autonomous tasks):
- Example: `sync-agent` (multi-phase synchronization)
- Use when: Independent context needed, parallel-capable, high complexity

#### Decision Guide Updated
- Added clear criteria for when to use each pattern
- Emphasized context isolation and parallel execution for agents
- Documented in plan and architectural review

### Documentation

- New file: `agents/sync-agent.md` - Comprehensive agent documentation
- Updated: `commands/sync-lovable.md` - Simplified with agent delegation
- Updated: `skills/lovable/SKILL.md` - Removed auto-push duplication
- Updated: Architectural review plan saved at `.claude/plans/`

### Benefits of This Release

**For Users**:
- ✅ No breaking changes - all existing workflows work identically
- ✅ More reliable /lovable:sync execution (agent-based)
- ✅ Cleaner skill documentation (no implementation details)
- ✅ Foundation for future autonomous features

**For Developers**:
- ✅ Clear architectural patterns for all workflow types
- ✅ Reference implementation for future agents
- ✅ Better separation of concerns
- ✅ Easier to test and maintain

**For the Plugin Ecosystem**:
- ✅ Demonstrates agent pattern in production
- ✅ Shows value of context isolation
- ✅ Enables parallel execution capabilities
- ✅ Completes architectural maturity

### Technical Details

**Agent Invocation Pattern**:
```
Command parses flags
   ↓
Configure agent mode
   ↓
Invoke sync-agent
   ↓
Agent executes autonomously (5 phases)
   ↓
Display progress (pass-through)
   ↓
Show results
```

**Files Modified**:
- `.claude-plugin/plugin.json` - Version bump to 1.6.0
- `skills/lovable/SKILL.md` - Removed lines 154-174 (auto-push section)
- `commands/sync-lovable.md` - Refactored to delegate to agent
- `agents/sync-agent.md` - New file (19KB comprehensive documentation)
- `CHANGELOG.md` - This entry

**Lines Changed**:
- Removed: 22 lines (duplication in skill)
- Added: 835 lines (new agent)
- Modified: 342 lines (refactored command)
- **Net**: +1,155 lines of structured, maintainable code

### Migration Guide

**No migration needed** - This is a non-breaking release. All existing workflows continue to work identically.

**Optional**: Review the new sync-agent documentation to understand the improved architecture:
- `agents/sync-agent.md` - Agent capabilities and modes
- `commands/sync-lovable.md` - Updated command documentation

### What's Next

Future agents enabled by this foundation:
1. **deployment-agent** - Autonomous deployment verification and rollback
2. **migration-validator** - SQL analysis and impact assessment
3. **codebase-analyzer** - Project health checks and optimization suggestions

---

## [1.5.0] - 2025-01-04

### Added

#### Auto-Sync Hook (Start Event)
- **New auto-sync hook** keeps local repo synchronized with GitHub
- Automatically pulls latest changes from GitHub when Claude starts working
- Only runs on main branch with no uncommitted changes
- Uses `git pull --rebase` to maintain clean history
- Gracefully handles conflicts - aborts and notifies user if conflicts detected
- Prevents diverged branch issues by checking if local/remote have diverged
- Added `hooks/auto-sync.sh` script that runs on Start event

#### Benefits of Auto-Sync
- ✅ **Always work on latest code** - Pulls changes before Claude starts
- ✅ **Prevents conflicts** - Detects diverged branches and warns user
- ✅ **Safe operation** - Only pulls when no uncommitted changes exist
- ✅ **Seamless workflow** - Happens automatically in the background
- ✅ **Network resilient** - Exits silently if GitHub is unreachable

### Changed

#### Hook-Based Auto-Push Implementation
- **Auto-push now uses Claude Code hooks** instead of skill-based logic
- More reliable and deterministic - hooks always run when Claude finishes responding
- Auto-push logic moved from `skills/lovable/SKILL.md` to `hooks/auto-push.sh`
- New `hooks/hooks.json` configuration file defines Stop event hook
- Hook automatically commits and pushes changes when `Auto-Push to GitHub: on` in CLAUDE.md

#### Benefits of This Change
- ✅ **More reliable** - Hooks guarantee execution vs. Claude sometimes forgetting
- ✅ **Deterministic** - Always runs on Stop event, no conditional logic needed
- ✅ **Cleaner architecture** - Separation of concerns between skills and automation
- ✅ **Better user experience** - Users don't need to remind Claude to push
- ✅ **Maintains all safety checks** - Same conditions apply (main branch, changes exist, enabled in CLAUDE.md)

#### Technical Details
- Added `hooks/` directory with `hooks.json`, `auto-sync.sh`, and `auto-push.sh`
- Updated `.claude-plugin/plugin.json` to reference hooks
- Simplified `skills/lovable/SKILL.md` - removed manual auto-push instructions
- Auto-push hook checks for `Auto-Push to GitHub: on` in user's CLAUDE.md
- Auto-sync hook runs on Start event, auto-push runs on Stop event
- Both hooks exit silently if conditions aren't met
- Smart commit messages based on changed files (edge functions, migrations, frontend)

## [1.4.1] - 2025-01-04

### Fixed

#### Auto-Push Independence
- **Auto-push is now independent of yolo mode** - can be enabled/disabled separately
- Auto-push can be ON while yolo mode is OFF (for manual deployment workflow)
- Yolo mode still REQUIRES auto-push to be ON (enforced when enabling)
- Disabling yolo mode no longer disables auto-push

#### Updated Question Flow in /init-lovable
- Moved auto-push question (Q9) before yolo mode question (Q11)
- Auto-push is now asked independently, not conditionally
- Yolo mode checks for auto-push and prompts to enable if needed
- Clearer separation of concerns in CLAUDE.md template

#### Updated /yolo Command
- Removed `--auto-push` and `--no-auto-push` flags (auto-push configured separately)
- Added auto-push requirement check when enabling yolo mode
- Prompts user to enable auto-push if it's off
- Disabling yolo mode preserves auto-push setting

#### Benefits of This Change
- ✅ Use auto-push without yolo mode for faster git workflow
- ✅ Clearer mental model - two independent features with one dependency
- ✅ More flexibility in configuration options

## [1.4.0] - 2025-01-04

### Added

#### Auto-Push to GitHub Feature
- **Automatic commit and push after task completion** - Claude automatically commits and pushes your changes to GitHub after successfully completing a task
- **New auto-push question in `/init-lovable`** - During initialization, users are asked if they want auto-push enabled (default: yes, recommended)
- **New `Auto-Push to GitHub` setting** in CLAUDE.md Yolo Mode Configuration
  - Enabled by default when yolo mode is on
  - Disable with `--no-auto-push` flag if you prefer manual git commands
- **Smart commit messages** - Claude creates descriptive commit messages following your project's commit style
- **Safety checks before pushing**:
  - Verifies task completed successfully (no errors)
  - Checks for actual file changes
  - Confirms on main branch
  - Never force pushes without permission

#### Complete Workflow Automation
With auto-push enabled alongside yolo mode, the full workflow is now automated:
```
1. You ask Claude to make changes
2. Claude completes the task successfully
3. Claude automatically commits with descriptive message
4. Claude pushes to main branch on GitHub
5. GitHub syncs to Lovable (frontend changes)
6. Auto-deploy triggers for backend changes (if enabled)
```

#### Enhanced Commands
- Updated `/yolo` command with `--auto-push` and `--no-auto-push` flags
- Updated syntax: `/yolo [on|off] [--auto-push|--no-auto-push] [--auto-deploy|--no-auto-deploy] [--testing|--no-testing] [--debug]`
- Auto-push instructions added to lovable skill

### Benefits
- ✅ **Zero manual git commands** - No more forgetting to commit/push
- ✅ **Instant sync** to GitHub → Lovable
- ✅ **Seamless workflow** from code changes to production
- ✅ **Works perfectly** with existing auto-deploy feature

### How It Works

When auto-push is enabled, after each successful task:
1. Claude checks `git status` for changes
2. If changes exist, stages all files with `git add .`
3. Creates a descriptive commit message
4. Commits with `git commit -m "message"`
5. Pushes to main with `git push origin main`
6. If yolo mode auto-deploy is also on, deployment triggers automatically

## [1.3.0] - 2025-01-03

### Added

#### Automatic Deployment After Git Push (Auto-Deploy)
- **No more manual `/deploy-edge` commands** - Claude automatically detects backend changes after `git push` and deploys them
- **New `auto_deploy` setting** in CLAUDE.md Yolo Mode Configuration
  - Enabled by default when yolo mode is on
  - Disable with `--no-auto-deploy` flag if you prefer manual commands
- **Intelligent detection** - Only triggers for backend file changes:
  - Edge functions: `supabase/functions/**/*`
  - Migrations: `supabase/migrations/*.sql`
- **Order-aware deployment** - Applies migrations before deploying functions when both are changed

#### Enhanced Yolo Mode Commands
- New flag: `--auto-deploy` (default) - Enable automatic deployment after git push
- New flag: `--no-auto-deploy` - Require manual `/deploy-edge` or `/apply-migration` commands
- Updated syntax: `/yolo [on|off] [--auto-deploy|--no-auto-deploy] [--testing|--no-testing] [--debug]`

#### Improved Graceful Fallbacks
- **Never blocks the user** - Every automation failure provides manual prompt as fallback
- **Context-specific error messages** - Clear explanations of what went wrong
- **Actionable troubleshooting** - Suggestions based on error type
- **Recovery options** - Retry, switch modes, or complete manually

### How Auto-Deploy Works

```
1. You push backend changes to main:
   git push origin main

2. Claude automatically detects:
   ✅ Push successful
   ✅ Backend files changed: supabase/functions/send-email/
   ✅ yolo_mode: on, auto_deploy: on

3. Deployment starts automatically:
   🤖 Auto-deploy: Backend changes detected, starting deployment...
   ⏳ Step 1/7: Navigating to Lovable project...
   [... automation runs ...]
   ✅ Complete! Edge function deployed and verified.
```

### New Reference Files
- `skills/yolo/references/post-push-automation.md`
  - Complete auto-deploy implementation details
  - User notification templates
  - Graceful fallback handling
  - Configuration options

### Updated Files
- `skills/yolo/SKILL.md` - Added auto-deploy activation triggers
- `skills/yolo/references/detection-logic.md` - Post-push detection implementation
- `skills/yolo/references/automation-workflows.md` - Graceful fallback strategy section
- `skills/lovable/references/CLAUDE-template.md` - Auto-Deploy configuration option
- `commands/yolo.md` - New `--auto-deploy` and `--no-auto-deploy` flags

### Example Configurations

**Full automation (recommended):**
```
/lovable:yolo on
# Auto-deploy after git push, with testing
```

**Manual deploy commands only:**
```
/lovable:yolo on --no-auto-deploy
# Browser automation for /deploy-edge, but not automatic
```

---

## [1.2.0] - 2024-01-15

### Added

#### Enhanced Secret Management
- **Automated secret detection** during `/lovable:init` - Scans codebase for environment variables
  - Detects `Deno.env.get("SECRET")` patterns in Edge Functions
  - Parses `.env.example` files for configuration templates
  - Context-based inference for common services (OpenAI, Stripe, Resend, Twilio, SendGrid, AWS)
- **Browser automation for secret extraction** - Automatically fetch existing secrets from Lovable Cloud
  - Navigate to Cloud → Secrets page
  - Extract secret names with graceful fallback to manual entry
  - 30-second timeout, never blocks workflow
- **Enhanced CLAUDE.md template** - Better tracking of secret status
  - Added Status column (✅ In Lovable Cloud / ⚠️ Not configured)
  - Added "Used In" column showing which functions use each secret
  - Legend explaining status indicators
  - Clear setup instructions

#### New `/lovable:sync` Command
- Re-synchronize CLAUDE.md with current Lovable Cloud state
- Refresh secrets, functions, and project settings
- Detects new secrets added by team members
- Updates configuration while preserving user notes and conventions
- Command flags: `--apply`, `--dry-run`, `--manual`, `--debug`, `--force-rescan`

#### Improved Init Flow
- **Reorganized questions** - Better logical grouping
  - Q5: Lovable Project URL (now asks all users, enables secret extraction)
  - Q6: Secret Detection Method (auto-detect or manual)
  - Questions 7-12: Reordered for clarity
- **Auto-run tests configuration** - Part of yolo mode setup
  - Detect test framework automatically (jest, vitest, npm test)
  - Run tests after every git push to main branch
  - Configuration stored in CLAUDE.md Yolo section
  - Independent of backend deployments

#### Better Secret Validation
- Enhanced `/lovable:deploy-edge` to validate secrets before deployment
- Cross-reference detected secrets with CLAUDE.md status
- Warn about missing secrets to prevent deployment failures
- Show which secrets are already configured in Lovable Cloud

### Improved

- Secret detection algorithm now detects purpose/usage context
- Error handling reuses proven patterns from existing automation
- Browser automation timeout strategies refined (45 seconds max, never blocks)
- CLAUDE.md updates preserve all user customizations (conventions, notes, custom prompts)

### Documentation

- New reference file: `skills/lovable/references/secret-detection.md`
  - Complete secret detection patterns and algorithms
  - Context-based inference logic for services
  - Merge and deduplication strategies
  - Edge case handling
- New reference file: `skills/yolo/references/secrets-extraction.md`
  - Browser automation workflow for Cloud → Secrets
  - Element selectors and extraction patterns
  - Error handling and timeout strategies
  - Integration with init flow
- Updated `skills/lovable/references/CLAUDE-template.md`
  - Enhanced Secrets table with Status and Used In columns
  - Enhanced Edge Functions table with Status indicators
  - New legend and setup instructions
- Updated `commands/deploy-edge.md`
  - Improved secret validation workflow
  - Better error messages for missing secrets
- Updated README.md
  - Added `/lovable:sync` command documentation

### Technical

- Reuses existing automation patterns - No duplicated logic
- Graceful fallback for all browser automation operations
- Smart caching to reduce repeated automation runs
- Debug mode for troubleshooting automation workflows

## [1.1.0] - Previous Release

- Added yolo mode (v1.1.0) - automated browser-based Lovable deployments
- Initial version with basic commands and skill integration

---

## Upgrading from 1.1.0 to 1.2.0

### For Users in Claude Code

1. Open Claude Code
2. Run: `/plugin install lovable@10k-digital --scope project --force`
3. Or: `/plugin install lovable@10k-digital --force` (for user-level installation)
4. Restart Claude Code

### What's New for Your Existing Projects

- Run `/lovable:sync` to refresh your CLAUDE.md with latest secrets and settings
- Consider re-running `/lovable:init` to set up auto-run tests (optional)
- Existing CLAUDE.md files are fully compatible (no breaking changes)

### Benefits

- ✅ Automatic secret detection saves time
- ✅ `/lovable:sync` keeps your config in sync with team changes
- ✅ Better secret status tracking prevents deployment failures
- ✅ Auto-run tests catch issues early
- ✅ Improved init flow for new projects

---

## Version Format

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes
- MINOR: New features, backwards compatible
- PATCH: Bug fixes, backwards compatible
