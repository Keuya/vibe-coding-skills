# Requirement: install prompt clarification and Codex surface truth

- Date: 2026-03-22
- Goal: make install prompts and install-facing docs truthful, non-destructive, and community-defensible.

## Required outcomes

1. Claude Code install prompts must stop asking users to paste secrets into AI chat.
2. Claude Code guidance must explain where users should configure values locally, and must preserve existing `~/.claude/settings.json`.
3. Claude Code guidance must explain that `settings.vibe.preview.json` is only a preview scaffold.
4. Codex install guidance must stop implying that unsupported hook/plugin surfaces are part of the supported install path.
5. Codex install guidance must focus on officially evidenced surfaces only, especially local settings and MCP.
6. Installation prompts must stop telling users to install or manually repair `hookify` / `everything-claude-code` / `claude-code-settings` / `ralph-loop` for Codex.
7. AI governance layer configuration must be described as local host configuration, not as chat-supplied credentials.

## Acceptance criteria

- User-facing install prompt docs point users to local config files instead of requesting secrets in chat.
- Claude Code docs describe minimal additive configuration and no destructive overwrite.
- Codex-facing docs no longer recommend unsupported hook/plugin installation as part of the standard path.
- Any remaining Codex integration guidance is limited to officially supportable surfaces.
