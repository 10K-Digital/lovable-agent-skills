---
name: testing
description: >-
  Compatibility alias for legacy Lovable Preview testing activation and Claude `/lovable:test-*`
  commands. Use lovable-testing for the maintained cross-agent workflow.
---

# Legacy Preview Testing Alias

Read [lovable-testing](../lovable-testing/SKILL.md) for the workflow and policy reader. This skill
retains its name and `references/` directory because existing Claude commands link to them.

- `references/test-wizard.md` handles initialization and test-plan synchronization.
- `references/preview-access.md` handles token-safe Preview access.
- `references/test-execution.md` handles smoke, changed, single-plan, and full runs.
- `references/test-plan-format.md` defines stored artifacts.

Do not treat this alias as a separate authorization source or duplicate testing state.
