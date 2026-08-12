---
name: lovable-project
description: >-
  Provider-neutral project context for Lovable.dev repositories. Use when initializing, inspecting,
  or modifying a Lovable project, detecting Vite SPA versus TanStack Start, reading `.lovable-agent`
  configuration, or generating agent instruction shims for Codex, Claude Code, and other agents.
---

# Lovable Project Context

Use this skill as the first step for work in a Lovable repository.

1. Read `.lovable-agent/config.json` and `.lovable-agent/context.md` when present. Treat them as the
   canonical source of project settings; read `AGENTS.md` as the neutral instruction shim.
2. Preserve provider-specific files as adapters: `CLAUDE.md`, `.claude/`, and Claude commands remain
   supported, but new state belongs in `.lovable-agent/`.
3. Detect architecture before making assumptions:
   - `app.config.ts` → TanStack Start (SSR, file-based routes, `*.server.ts` auto-deploys).
   - `vite.config.ts` → Vite SPA (CSR, `src/`, backend changes need Lovable deployment prompts).
   - If both or neither are present, report the ambiguity and inspect the package scripts.
4. Keep context secret-safe. Record secret names and status only; never record values, preview tokens,
   OAuth credentials, or API keys in config, instructions, logs, or generated reports.
5. For the detailed neutral schema and migration rules, read
   `../lovable/references/agent-config.md`.

The legacy `plugins/lovable/skills/lovable/SKILL.md` remains the Claude-compatible deep reference.
