# ai-engine

> **An engineering-discipline framework for AI coding agents: reusable rules and adapters, not an agent runtime.**

English · [中文](README.md) · [Capabilities](docs/capabilities.md) · [Install](docs/agent-install.md) · [Compatibility](docs/compatibility.md) · [Contributing](CONTRIBUTING.md)

ai-engine turns recurring failure modes in AI-assisted development—blind file overwrites, weak verification, suspicious metrics, multi-agent conflicts, and repeated dead ends—into reviewable Markdown rules and agent-integration guidance.

## What it is / is not

| It is | It is not |
|---|---|
| 47 composable engineering-discipline rules plus a reference tool for multi-agent coordination | An executable agent runtime or background service |
| A Claude Code rules directory plus integration guidance for Codex, Cursor, Aider, and Gemini CLI | A plug-in that automatically creates backups, schedules jobs, or merges branches |
| An open framework for discussing and improving AI engineering workflows | Prompt magic that makes a model smarter |

See [Capabilities](docs/capabilities.md) for the boundary between shipped assets, reference architectures, and automation that you must implement in your own environment.

## Try it in 3 minutes: prevent blind overwrites

For Claude Code, install one minimal rule in a test project:

```bash
git clone https://github.com/Destined-at-Dawn/ai-engine.git
mkdir -p YOUR_PROJECT/.claude/rules
cp ai-engine/.claude/rules/no-blind-overwrite.md YOUR_PROJECT/.claude/rules/
```

Start a new agent session and ask it to modify an existing file. It should read the file first and describe the planned change before writing. The [installation guide](docs/agent-install.md) includes verification steps, Windows commands, and setup instructions for other agents.

> This is a rules framework. Actual behavior depends on the tool, project configuration, and your final review. Test it in a disposable project before adopting it for important work.

## Choose rules by pain point

| Pain point | Start with |
|---|---|
| AI may overwrite or delete existing files | `no-blind-overwrite.md`, `script-safety-check.md` |
| AI reports implausibly good numbers | `anti-illusion-audit.md` |
| AI says “done” without enough verification | `10-engineering-laws.md`, `lifecycle-sop.md` |
| The same failure keeps recurring | `negative-results.md` |
| Multiple agents conflict | `multi-agent-coordination.md` + `tools/agent-coord/`, `agent-prompt-ironclad.md` |
| AI edits an old revision, or fixes only one of several related numbers | `version-baseline-check.md`, `metric-family-alignment.md` |
| “Works locally” gets reported as “released” | `harness-evidence-states.md`, `delivery-acceptance-layers.md` |
| Sub-agents are abandoned halfway, or results live only in a temp folder | `subagent-must-return.md`, `session-close-handoff.md` |
| AI changes the workflow because it “seems better” | `rule-change-audit.md` |
| Backup jobs stay green while nothing reaches the remote | `backup-signal-trust.md` |
| AI-drafted public content leaks internal notes or other people's names | `public-content-hygiene.md` |
| You want the full rule set | `.claude/rules/` (47 rule files) |

## Support status

| Agent | Integration | Status |
|---|---|---|
| Claude Code | `.claude/rules/` | Primary target |
| Codex | `AGENTS.md` plus copied rules | Integration example provided |
| Cursor | `.cursor/rules` | Integration guidance provided |
| Aider | `.aider.conf.yml` | Integration guidance provided |
| Gemini CLI | `GEMINI.md` | Integration guidance provided |

“Integration guidance provided” is not a guarantee of continuous compatibility. Check the [compatibility matrix](docs/compatibility.md) for scope and limitations.

## Repository layout

```text
ai-engine/
├── .claude/rules/       # 47 core Markdown rules
├── tools/agent-coord/   # Multi-agent coordination reference tool (stdlib Python + self-test)
├── adapters/            # Integration examples per agent
├── docs/                # Install, capabilities, compatibility, philosophy, and case studies
├── templates/           # Memory templates in Chinese and English
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE              # MIT
```

## Contributing and feedback

- Usage questions, ideas, and experience reports: GitHub Discussions (once enabled) or a structured Issue.
- Reproducible bugs, documentation problems, and rule proposals: use the Issue templates.
- Security reports: read [SECURITY.md](SECURITY.md); do not disclose details in a public Issue.
- New adapters, reproducible public cases, rule improvements, validation methods, and translations are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Version and evolution

The current public ruleset is **v5.2.0 / 47 rule files**. v5.2.0 adds 13 rules, the `tools/agent-coord/` reference tool, and 3 sanitized incident patterns; see [CHANGELOG.md](CHANGELOG.md). See [CHANGELOG.md](CHANGELOG.md) for history. Release notes are available in GitHub Releases.

## License

[MIT](LICENSE)

> Make AI work like an engineer: understand the boundary before changing, verify the evidence before declaring completion.
