# Accident pattern: a backup job reported success while nothing was being pushed

> **Evidence level:** Maintainer-reported, sanitized incident pattern. Three related incidents are combined; private paths, repository names and durations beyond what illustrates the pattern are omitted.

## Context

A maintainer relied on scheduled jobs that committed and pushed several local working directories to private remote repositories. A dashboard showed the scheduler state and the last exit code of each job.

## Failure

1. Several jobs stayed in the "ready" state after a disk migration although the scripts they pointed to no longer existed. Data loss revealed it.
2. Later, one backup script caught push errors, wrote them to a log and exited with code 0. Pushes failed for about twelve days while the dashboard stayed green.
3. Later still, a pre-commit privacy gate correctly blocked a test fixture that contained a literal private-key header. Every scheduled run failed for weeks. The failure was logged but sent nowhere a person would look.

## Root cause

Each layer trusted the signal above it. "Registered" was read as "working", and "exit code 0" was read as "backed up". Only the remote repository could prove that a backup happened, and nobody checked it.

## Rule or change

[`backup-signal-trust.md`](../../.claude/rules/backup-signal-trust.md): three signal levels with the remote as the only final evidence; non-zero exit on any failure; alerting after 24 hours of consecutive failure; fixing the blocked input instead of loosening the gate; building secret-shaped test strings at runtime.

## Verification

1. Write a backup script that pushes to a disposable remote.
2. Make the push fail (for example, revoke write access).
3. Confirm the script exits non-zero and that the alert path is triggered.
4. Ask an agent with the rule installed whether the backup is healthy. A passing answer checks the remote commit timestamp, not the scheduler state.

## Limitation

The rule does not provide a scheduler, an alert channel or backup scripts. It defines which evidence counts.
