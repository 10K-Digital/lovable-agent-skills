---
name: init
description: >-
  Initialize or reinitialize a Lovable project for coding agents. Create or refresh
  .lovable-agent configuration and context, AGENTS.md, and the Claude compatibility shim
  while preserving project settings, custom instructions, tests, and local credentials.
---

# Initialize a Lovable Project

Use this skill for “init”, “initialize”, “reinitialize”, or “refresh Lovable project context”.
Resolve helper and reference paths relative to this installed plugin, not the target repository.

1. Read existing `AGENTS.md`, `CLAUDE.md`, `.lovable-agent/config.json`, and
   `.lovable-agent/context.md`. Read [project context](../lovable-project/SKILL.md) and the
   [configuration schema](../lovable/references/agent-config.md).
2. Inspect package metadata, Git remotes, application directories, Edge Functions, and migrations.
   Run `python3 <plugin-root>/scripts/detect-architecture.py <project-root>` when available.
   Resolve ambiguous architecture from actual files; never guess a project URL or backend.
   Record secret names and status only, never values.
3. Reuse existing settings and facts inferable from the repository. Ask only for missing information
   needed to finish setup. Leave optional unknown URLs empty and report them. For new projects,
   default YOLO and auto-push to false; enable them only when requested. Reinitialization preserves
   existing values, including explicit false and custom/unknown configuration fields. Import legacy
   YOLO on/true or off/false only when the neutral field is absent; persist it as a JSON boolean.
4. If a legacy test workspace exists, use `scripts/migrate-workspace.py` from the plugin (inspect
   its usage first). Preserve existing canonical tests and ignored local tokens. Ensure token paths
   are ignored before storing credentials; never place tokenized URLs in generated context.
5. Merge `.lovable-agent/config.json` and refresh factual inventory/context. Do not replace user
   prose, custom instructions, settings, tests, or credentials. If JSON is malformed, report the
   error and preserve the file rather than resetting it. Keep a Claude-compatible `CLAUDE.md` shim
   pointing to the neutral files.
6. Create or update the Lovable-managed section in `AGENTS.md` using the
   [prompt authorization rules](../lovable/references/prompt-authorization.md). Include the explicit
   rule: **YOLO on grants standing authorization for in-scope Lovable prompts; generic prompt
   confirmation requirements apply only when YOLO is off.** Include the retained operation gates
   and task restrictions. Update an existing generic Lovable confirmation sentence to express this
   condition; preserve unrelated instructions. Mirror or reference this policy from `CLAUDE.md`.
7. Validate JSON and review the diff for preserved settings, secret safety, and consistent YOLO
   rules across config and both shims. Repeating init with unchanged inputs should create no
   duplicate sections or reset preferences. Report files updated and effective YOLO status.

Initialization is local setup. It does not itself submit a Lovable prompt, deploy, or publish.
The legacy `/lovable:init-lovable` command delegates here for the same reinitialization behavior.
