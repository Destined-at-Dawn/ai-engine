# Accident pattern: fixing one number made the document consistently wrong

> **Evidence level:** Maintainer-reported, sanitized incident pattern from technical writing. The original manuscript, values and reviewers are omitted.

## Context

An AI agent revised a technical manuscript after a review comment pointed out an inconsistent count in one paragraph. The manuscript existed in many numbered revisions, and several sessions had edited it.

## Failure

Two failures happened on the same day:

1. The agent edited an older revision because it was the file already open in its context. The newest revision was elsewhere in the directory.
2. The agent corrected only the number the reviewer pointed to. Related values in the same table and abstract (sample count, success count, ratio, derived totals) were left unchanged. In one place, "99 successes out of 100 attempts" became `99/99`, which silently turned a 99% success rate into 100%.

Before the fix, the error was visible. After the fix, the document was internally consistent and wrong.

## Root cause

The workflow had a "read before write" rule but no rule about *which* file to read, and no rule that a measured value belongs to a family of values derived from the same experiment.

## Rule or change

- [`version-baseline-check.md`](../../.claude/rules/version-baseline-check.md): list and sort candidates, record the baseline file and hash before editing.
- [`metric-family-alignment.md`](../../.claude/rules/metric-family-alignment.md): go back to the raw evidence, update every member of the metric family at once, check the denominator, and finish with a zero-hit scan for old values.

## Verification

1. Create a folder with `report-r3.md` and `report-r5.md`, and a CSV with 100 trials and 99 successes.
2. Put inconsistent counts in several places of `report-r5.md`.
3. Ask the agent to "fix the success count in section 2".
4. A passing run edits `report-r5.md`, reads the CSV, updates every related value, keeps the denominator at 100, and reports a residual scan.

## Limitation

The rules cannot detect an error in the raw evidence itself. They make edits traceable and complete relative to that evidence.
