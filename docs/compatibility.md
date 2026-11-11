# Agent compatibility

**Document review date:** 2026-11-11  
**Ruleset:** v5.2.0 / 47 Markdown rule files

| Agent | Integration method | Status | Verification scope |
|---|---|---|---|
| Claude Code | `.claude/rules/` and optional `CLAUDE.md` | Primary target | Rule directory and root guide are shipped; verify in a clean project. |
| Codex | `AGENTS.md` that references copied rule files | Documented integration | A minimal example is in `adapters/codex/AGENTS.md.example`. |
| Cursor | `.cursor/rules` | Documented integration | Follow `adapters/cursor.md`; validate against your Cursor version. |
| Aider | `.aider.conf.yml` | Documented integration | Follow `adapters/aider.md`; rule loading is configuration-dependent. |
| Gemini CLI | `GEMINI.md` | Documented integration | Follow `adapters/gemini-cli.md`; validate against your Gemini CLI version. |

## Loading precedence

Agent-specific precedence can change. In general, direct user instructions override project instructions, which override referenced rule files. Treat this table as integration guidance rather than a guarantee of identical behavior across tools.

Entry files differ by tool: Claude Code reads `CLAUDE.md` and auto-loads `.claude/rules/`; Codex and several other tools read `AGENTS.md` and do not auto-load `.claude/rules/`. Rules that every tool in a shared workspace must follow belong in `AGENTS.md` (see `multi-agent-coordination.md`).

## Rule categories

| Category | Examples |
|---|---|
| Engineering discipline | `10-engineering-laws.md`, `lifecycle-sop.md`, `think-before-act.md` |
| File and script safety | `no-blind-overwrite.md`, `script-safety-check.md`, `git-recovery.md` |
| Evidence and quality | `anti-illusion-audit.md`, `boundary-declaration.md`, `negative-results.md`, `harness-evidence-states.md`, `delivery-acceptance-layers.md`, `rule-change-audit.md` |
| Edit integrity | `version-baseline-check.md`, `metric-family-alignment.md`, `shell-text-integrity.md` |
| Agent coordination | `agent-prompt-ironclad.md`, `subagent-strategy.md`, `subagent-must-return.md`, `multi-agent-coordination.md`, `agent-autoloop.md` |
| Continuity and operations | `session-close-handoff.md`, `task-state-sync.md`, `backup-signal-trust.md`, `public-content-hygiene.md` |
| Reference architectures | `21-git-archive-ironlaw.md`, `knowledge-hub-architecture.md`, `scheduled-task-dual-redundancy.md` |

See [Capabilities](capabilities.md) for the distinction between shipped rules, documented integrations, and reference architectures.
