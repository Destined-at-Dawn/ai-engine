# Codex adapter

Codex reads project instructions from `AGENTS.md`. Keep the ai-engine rules inside the project so their scope is visible and reviewable.

## Minimal setup

1. Copy the rules you want into your project:

```bash
mkdir -p YOUR_PROJECT/.ai-engine/rules
cp ai-engine/.claude/rules/no-blind-overwrite.md YOUR_PROJECT/.ai-engine/rules/
cp ai-engine/.claude/rules/think-before-act.md YOUR_PROJECT/.ai-engine/rules/
cp ai-engine/.claude/rules/anti-illusion-audit.md YOUR_PROJECT/.ai-engine/rules/
```

2. Copy [`adapters/codex/AGENTS.md.example`](codex/AGENTS.md.example) to `YOUR_PROJECT/AGENTS.md` and adjust the rule list to match the files you copied.

3. Start a new Codex session and use the smoke tests in [the installation guide](../docs/agent-install.md).

## Notes

- The example deliberately installs a small set first. Add rules after you have verified their effect in your project.
- A path listed in `AGENTS.md` must exist in the target repository.
- ai-engine provides rules and integration guidance; it does not install backup jobs, branch protections, or schedulers for you.
- See [Capabilities](../docs/capabilities.md) and [Compatibility](../docs/compatibility.md) before claiming an integration is verified.
