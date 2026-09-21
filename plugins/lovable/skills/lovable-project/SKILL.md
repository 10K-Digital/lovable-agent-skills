---
name: lovable-project
description: >-
  Provider-neutral project context for Lovable.dev repositories. Use when initializing, inspecting,
  or modifying a Lovable project, detecting Vite SPA versus TanStack Start, reading `.lovable-agent`
  configuration, or generating agent instruction shims for Codex, Claude Code, and other agents.
---

# Lovable Project Context

Use this skill as the first step for work in a Lovable repository.

For initialization or reinitialization, call the `init` skill at `../init/SKILL.md`.
Before Lovable submissions, read `../lovable/references/prompt-authorization.md`.

1. Read `.lovable-agent/context.md` and `AGENTS.md` when present. Read policy settings with
   `python3 ~/.codex/skills/lovable-project/scripts/read-context.py --project . --section policies`;
   read the full config only to perform a requested configuration merge. Treat the neutral files as
   canonical.
2. Preserve provider-specific files as adapters: `CLAUDE.md`, `.claude/`, and Claude commands remain
   supported, but new state belongs in `.lovable-agent/`.
3. Detect architecture before making assumptions:
   - Run `python3 plugins/lovable/scripts/detect-architecture.py .` when the helper is available;
     it reports JSON without reading secret values.
   - The helper checks TanStack Start package dependencies and scripts before treating Vite config
     as a Vite SPA marker; TanStack Start can use Vite internally.
   - Use the returned architecture and markers. If it returns `unknown`, inspect package metadata
     and report the uncertainty rather than inferring from a config filename.
4. Keep context secret-safe. Record secret names and status only; never record values, preview tokens,
   OAuth credentials, or API keys in config, instructions, logs, or generated reports.
5. For the detailed neutral schema and migration rules, read
   `../lovable/references/agent-config.md`.

The legacy `plugins/lovable/skills/lovable/SKILL.md` remains the Claude-compatible deep reference.
