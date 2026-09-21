---
name: yolo
description: >-
  Compatibility router for legacy Lovable YOLO automation requests, commands, and post-push
  deployment handling. Use lovable-deploy for the maintained deployment workflow.
---

# YOLO Automation Compatibility Router

This retained skill keeps `/yolo`, legacy YOLO configuration, and Claude hooks compatible. The
maintained workflow is [Lovable Deployment](../lovable-deploy/SKILL.md). Do not load the old
automation references unless that workflow specifically needs transport or verification detail.

1. Read policy settings only:

   ```bash
   python3 ~/.codex/skills/lovable-project/scripts/read-context.py --project . --section policies
   ```

   If the neutral `deploy.yolo_mode` field is absent, use the legacy CLAUDE.md status as described
   in [prompt authorization](../lovable/references/prompt-authorization.md). A transport mode never
   grants authorization.
2. For every submission, apply the authorization reference. YOLO authorizes only in-scope Lovable
   prompts; explicit task restrictions remain controlling. `deploy.mode: manual` returns a prompt.
3. Confirm destructive or irreversible database operations. Also confirm a migration whenever
   `deploy.confirm_migrations` is true. Do not enable auto-push or auto-deploy merely because YOLO
   is enabled.
4. Route Edge Functions and migrations to `lovable-deploy`; route Preview checks to
   [lovable-testing](../lovable-testing/SKILL.md). Keep the existing `references/` files for Claude
   command compatibility, reading only the reference that the selected transport needs.

The existing `commands/yolo.md` and Claude hooks remain the command adapters. Report whether a
submission was accepted or verified; an asynchronous acknowledgement alone is not verification.
