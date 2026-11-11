# agent-coord

A small, dependency-free coordination CLI for workspaces where several AI agents (for example Claude Code and Codex, or several sessions of one tool) edit the same deliverables. It is the reference implementation for [`multi-agent-coordination.md`](../../.claude/rules/multi-agent-coordination.md).

**Status:** Shipped reference tool (v5.2.0). Pure Python standard library, 3.8+. Tested by `test_coord.py` on Windows; the code avoids platform-specific APIs.

## What it solves

| Failure seen in practice | Mechanism |
|---|---|
| Two sessions run the same workflow and both produce `r21` | `claim` takes an exclusive lease; a second claimant gets exit code 1 |
| An agent computes the next revision from stale context | `next-rev` scans deliverables, archives and previous allocations under a lock |
| Concurrent edits to a shared status file silently drop entries | `REGISTRY.jsonl` is append-only |
| Someone edits a deliverable without recording it | `doctor` compares the logged SHA-256 and revision with the disk |
| `AGENTS.md` and `CLAUDE.md` drift apart, so tools follow different rules | `doctor` compares configured mirror pairs |

## Quick start

```bash
cp tools/agent-coord/coord.py YOUR_PROJECT/scripts/
cd YOUR_PROJECT
python scripts/coord.py init          # creates coord.config.json and .coord/
python scripts/coord.py status        # first command of every session
python scripts/coord.py claim --agent claude-code --task "revise section 3"
python scripts/coord.py next-rev --agent claude-code
python scripts/coord.py log --agent claude-code --action "section 3 revised" \
    --artifact deliverables/report-r4.docx --baseline r4
python scripts/coord.py release --agent claude-code
python scripts/coord.py doctor        # last command of every session; exit 1 needs attention
```

Then add the same five commands to your `AGENTS.md` so that every tool, not only Claude Code, sees them.

## Configuration (`coord.config.json`)

| Key | Default | Meaning |
|---|---|---|
| `coord_dir` | `.coord` | Lease, registry and state live here. Never archive or clean it. |
| `deliverables_dir` | `deliverables` | Where current deliverables live |
| `archive_dirs` | `["archive"]` | Scanned (recursively) when allocating revisions |
| `revision_pattern` | `[-_]r(\d+)` | Regex that extracts a revision number from file names |
| `artifact_extensions` | common document types | Which files in `deliverables_dir` count |
| `agents` | `[]` | Optional allow-list of agent names |
| `lease_ttl_minutes` | `90` | Lease lifetime; expired leases can be taken over and the takeover is logged |
| `mirror_pairs` | `[["AGENTS.md","CLAUDE.md"]]` | Files that must stay byte-identical |
| `allowed_top_level` | `[]` | Optional workspace map; `doctor` flags anything else at the root |

## Limits

- The lease is advisory. It protects agents that run `claim`; it does not lock files at the operating-system level.
- `doctor` checks consistency between the registry and the disk. It does not judge whether a deliverable is correct.
- Run the self-test before adapting it: `python tools/agent-coord/test_coord.py`.
