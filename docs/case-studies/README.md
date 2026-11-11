# Case studies

Case studies are the evidence layer of ai-engine. A case should explain a real failure pattern without exposing private data, credentials, proprietary source code, or identifiable third parties.

## Case template

```md
# [Short failure-mode title]

## Context
What kind of task and environment was involved? Keep it anonymous and reproducible.

## Failure
What happened, and what was the observable impact?

## Root cause
Why did the existing workflow fail to catch it?

## Rule or change
Which ai-engine rule was added or changed? Link to the file.

## Verification
How can another maintainer test whether the rule changes the workflow?

## Limitation
What does this rule still not guarantee?
```

Label anecdotal maintainer observations as such. Do not represent them as independently validated results without public evidence.

## Published cases

These are maintainer-reported and sanitized incident patterns. They describe the observed failure mode and a reproducible verification path; they are not independent benchmark results or universal reliability claims.

- [An update erased the surrounding document](blind-overwrite.md)
- [A strong metric survived without an audit trail](unverified-metric.md)
- [A sub-agent returned an unusable investigation](underspecified-subagent.md)
- [A backup job reported success while nothing was being pushed](silent-backup-failure.md)
- [Fixing one number made the document consistently wrong](half-corrected-metrics.md)
- [Two agents produced the same revision in parallel](parallel-agents-duplicate-revision.md)
