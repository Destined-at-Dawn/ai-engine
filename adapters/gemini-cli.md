# Gemini CLI Adapter

## Integration Method

Gemini CLI discovers `.md` files in the project root as context.

### Quick Integration

1. Create `GEMINI.md` in project root:

```markdown
> Engineering framework: ai-engine v5.2.0 (47 rule files).
> Rule files are in .claude/rules/.
> See CLAUDE.md for the startup sequence and core principles.

## Key Rules (summary)
- Evidence Layering: every "pass" must carry a calibration label
- Anti-Illusion Audit: high scores first audit how they were produced
- Negative Result Archive: dead ends must be archived
- Agent Prompt Iron Law: specific goal + output format + stop condition
- Agent Concurrency Fallback: 429 rate limit -> immediate sequential mode
```

2. Gemini CLI automatically discovers `GEMINI.md` as context.

### Notes
- Gemini CLI's context discovery is loose — inline the most critical rules in GEMINI.md
- Full rule set: 47 files in `.claude/rules/`
