# Evolution Calendar

> Rules grow from accidents. This file tracks what to evolve next.

## How It Works

Each time a new failure pattern is discovered in your projects:
1. Add an entry below with status `[pending]`
2. After the corresponding rule is created/updated, mark it `[done]`
3. Rules that prove unnecessary get `[cancelled]`

## Evolution Log

| Date | Incident | Rule Created/Updated | Status |
|------|----------|---------------------|--------|
| — | (Your first incident goes here) | — | — |

## How to Contribute Back

If you discover a failure pattern and create a rule that isn't in this repo:
1. Sanitize it (remove personal paths/info)
2. Open a PR to `ai-engine`
3. Add it to the evolution log above

## Rule Upgrade Path

```
Single incident -> Write it in memory/{date}.md
Same incident 2+ times -> Create/update a rule in .claude/rules/
Incident pattern across projects -> Propose addition to ai-engine
```

---

> The framework is alive. Your accidents are its next rules.
