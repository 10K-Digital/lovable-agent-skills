# Lovable Agent Context

This repository publishes the Lovable Agent Skills plugin. The reusable behavior lives under
`plugins/lovable/skills/`; Claude-specific commands and hooks are compatibility adapters.

The repository itself is not a Lovable application, so Preview testing is disabled in the checked-in
defaults. User projects initialized by the plugin receive their own `.lovable-agent/config.json`,
`context.md`, `tests/`, and provider shims.
