# Agent installation guide

ai-engine is modular. Start with one rule in a disposable project, validate the behavior you expect, then add more rules deliberately.

## 1. Choose a rule

| Goal | Start with |
|---|---|
| Prevent blind overwrites | `no-blind-overwrite.md` |
| Check suspicious metrics | `anti-illusion-audit.md` |
| Require evidence before “done” | `10-engineering-laws.md`, `lifecycle-sop.md` |
| Coordinate multiple agents | `agent-prompt-ironclad.md`, `subagent-strategy.md` |

## 2. Install it in a test project

Clone this repository first:

```bash
git clone https://github.com/Destined-at-Dawn/ai-engine.git
```

### Claude Code

```bash
mkdir -p YOUR_PROJECT/.claude/rules
cp ai-engine/.claude/rules/no-blind-overwrite.md YOUR_PROJECT/.claude/rules/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force YOUR_PROJECT\.claude\rules
Copy-Item ai-engine\.claude\rules\no-blind-overwrite.md YOUR_PROJECT\.claude\rules\
```

To adopt the whole ruleset, copy the directory after reviewing its contents:

```bash
cp -r ai-engine/.claude/rules YOUR_PROJECT/.claude/
```

### Codex

Follow [the Codex adapter](../adapters/codex.md). It includes a minimal `AGENTS.md` example and keeps the rules in a visible project-local directory.

### Other agents

- Cursor: [`adapters/cursor.md`](../adapters/cursor.md)
- Aider: [`adapters/aider.md`](../adapters/aider.md)
- Gemini CLI: [`adapters/gemini-cli.md`](../adapters/gemini-cli.md)

## 3. Smoke-test the behavior

Start a fresh agent session and run these checks in a throwaway project:

1. Ask the agent to modify an existing file. With `no-blind-overwrite.md` active, it should inspect the current content before editing.
2. Give the agent an unusually strong metric and ask for a conclusion. With `anti-illusion-audit.md` active, it should ask how the metric was produced.
3. Ask which ai-engine rules are active. The agent should identify only the files you installed.

If the behavior differs, verify that the target tool loads the configured project instructions. Integration mechanics differ by agent and version.

## 4. Expand carefully

Read [Capabilities](capabilities.md) before adopting architecture-oriented rules. The repository ships policies and integration guidance; it does not ship a universal backup, sync, or scheduler service.
