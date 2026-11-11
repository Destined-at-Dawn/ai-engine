# Accident pattern: two agents produced the same revision in parallel

> **Evidence level:** Maintainer-reported, sanitized incident pattern. Tool names are kept because the failure depends on which entry files each tool reads.

## Context

Four AI coding tools worked in the same document workspace, often at the same time. Coordination relied on a hand-written status file in the workspace and on rules written for one tool.

## Failure

- Two sessions independently ran the same revision workflow and both produced the same revision number. The outputs happened to be byte-identical only because the build was deterministic.
- Two sessions edited the shared rules file on the same day; several edits were silently lost.
- One tool archived the hand-written status file as "unrelated to the deliverable", and five revisions lost their records.
- Rules placed in `.claude/rules/` were followed by Claude Code only. The other tools read `AGENTS.md` and never saw them.

## Root cause

Coordination depended on agents remembering conventions. Nothing on disk could refuse a second writer, allocate a revision number, or detect an unrecorded edit.

## Rule or change

- [`multi-agent-coordination.md`](../../.claude/rules/multi-agent-coordination.md)
- Reference tool: [`tools/agent-coord`](../../tools/agent-coord/README.md) with an exclusive lease, an append-only registry, a locked revision allocator and a `doctor` command.

## Verification

1. Run `python tools/agent-coord/test_coord.py`; the tests cover lease exclusivity, revision allocation, unrecorded edits and diverged entry files.
2. In a disposable workspace, start two agent sessions and ask both to produce the next revision. With the protocol in `AGENTS.md`, the second session should stop at `claim` with exit code 1.

## Limitation

The lease is advisory. An agent that ignores the protocol can still write files; `doctor` will report the inconsistency afterwards.
