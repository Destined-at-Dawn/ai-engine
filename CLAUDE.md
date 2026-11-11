# Startup Sequence (Every Conversation -- Mandatory)

| Step | Action | When |
|------|--------|------|
| 1 | Read `.claude/rules/` directory | Every conversation (Claude Code auto-loads) |
| 2 | Read `memory/long-term.md` | First conversation / after corrections |
| 3 | Read `memory/{today}.md` | First conversation of the day |
| 4 | Read `EVOLUTION.md` | Match pending tasks -> execute first |
| 5 | **R21 Three-Layer Protection**: verify agent branch + archive ready + pre-modify archive | Every conversation |
| 6 | **Knowledge Hub**: read cross-workspace lessons (last 7 days) | Every conversation |

> **Quick Mode**: If the user message contains a specific trigger word you've defined, skip startup and process directly. High-risk operations still require reading long-term.md.

---

# Project Rules

## R21 -- Three-Layer File Protection (CRITICAL)
**Before any file modification or deletion**: archive -> agent/{date} branch -> daily zip snapshot.
-> See `.claude/rules/21-git-archive-ironlaw.md`

## Think Before Act
New problems require research before action. Never substitute "I think" for best practice.
-> See `.claude/rules/think-before-act.md`

## No Blind Overwrite (CRITICAL)
Read existing files before writing. Use Edit for partial changes, never Write without Read.
-> See `.claude/rules/no-blind-overwrite.md`

## Script Safety Check (CRITICAL)
Pipeline: write script -> safety check -> dry-run -> show -> confirm -> execute -> verify.
Deletions must target specific files, never directories.
-> See `.claude/rules/script-safety-check.md`

## Evidence Layering
Every "pass" claim must carry a calibration label (coarse/medium/full-audit).
-> See `.claude/rules/10-engineering-laws.md` Law 1

## Anti-Illusion Audit
Abnormally good numbers are assumed fake until proven real. Run the five-question check.
-> See `.claude/rules/anti-illusion-audit.md`

## Negative Result Archiving
Dead ends must be archived. An unrecorded dead end will be retried by every subsequent conversation.
-> See `.claude/rules/negative-results.md`

## Agent Prompt Iron Law
Every Agent call must include: specific goal + output format + stop condition.
-> See `.claude/rules/agent-prompt-ironclad.md`

## Agent Concurrency Fallback
When 429 rate limit hits: immediately fall back to sequential direct tool calls. Do not wait. Do not retry.
-> See `.claude/rules/agent-concurrency-fallback.md`

## Sub-Agent Strategy
Use sub-agents for investigation tasks, not decision tasks. Single agent first, scale only when needed.
-> See `.claude/rules/subagent-strategy.md`

## Search Decision Tree
Before searching: is this an immutable fact? A changing state? An unknown entity? Match search depth to question complexity.
-> See `.claude/rules/search-decision-tree.md`

## Lesson Auto-Update
User corrections must trigger workflow updates. Lessons recorded but not applied = wasted.
-> See `.claude/rules/lesson-auto-update.md`

## Boundary Declaration
Every deliverable must include a three-column boundary list: confirmed / reference-only / cannot claim.
-> See `.claude/rules/boundary-declaration.md`

## Git Checkpoint & Recovery
Commit a checkpoint before any file deletion. Recovery must be possible within 30 seconds.
-> See `.claude/rules/git-recovery.md`

## Knowledge Hub Architecture
All workspaces share a single source of truth. Cross-tool lessons must be dual-written.
-> See `.claude/rules/knowledge-hub-architecture.md`

## Scheduled Task Dual Redundancy
Critical periodic tasks run on two independent scheduling systems. Mutual fallback.
-> See `.claude/rules/scheduled-task-dual-redundancy.md`

## Skill Quality Benchmark
New skills must meet the standard: 6 top-level files + 5+ references + 1+ scripts + 24 quality gates.
-> See `.claude/rules/skill-quality-benchmark.md`

## Student Onboarding (v5.0 NEW, self-gating)
Activates only when `STUDENT-GUIDE.md` exists in workspace root. Term bridging, next-step hooks, no overreach tasks, no proactive architecture exposure.
-> See `.claude/rules/student-onboarding.md`, `docs/student-pathway/`

## Before Editing a Versioned Deliverable (v5.2 NEW)
List candidates, confirm the newest revision, record the baseline hash. When a measured value changes, realign the whole metric family from raw evidence.
-> See `.claude/rules/version-baseline-check.md`, `.claude/rules/metric-family-alignment.md`

## Evidence States and Delivery Layers (v5.2 NEW)
SOURCE_ONLY / LOCAL_ONLY / BUILD_VERIFIED / DEVICE_VERIFIED / PUBLISHED are separate states. Generated, opened, and deployed are separate layers.
-> See `.claude/rules/harness-evidence-states.md`, `.claude/rules/delivery-acceptance-layers.md`, `.claude/rules/agent-autoloop.md`

## Multi-Agent Workspaces (v5.2 NEW)
Status first, claim before editing shared deliverables, allocate revisions with a tool, doctor last. Rules every tool must follow go into AGENTS.md.
-> See `.claude/rules/multi-agent-coordination.md`, `tools/agent-coord/`, `.claude/rules/subagent-must-return.md`

## Session Close (v5.2 NEW)
Write context, state, decisions, negative results and a restart prompt; register it in work-logs/HANDOFF-INDEX.md.
-> See `.claude/rules/session-close-handoff.md`, `.claude/rules/task-state-sync.md`

---

# Compact Instructions

## Protection List (Never Drop During Compression)
1. User's latest request (verbatim)
2. All modified file absolute paths
3. Source: path#line citations
4. Key decisions and rationale
5. Error root causes and fixes
6. Task progress and next steps
7. User correction verbatim
8. **R21 status**: agent branch + last archive + last zip snapshot

## After Compression Recovery
1. Re-read CLAUDE.md + .claude/rules/ (automatic)
2. Actively re-read memory/long-term.md + memory/{today}.md
3. Check for unfinished tasks
4. **Verify R21 protection status** (branch, archive, snapshot)

---

# Rule Categories at a Glance

| Category | Rules | Purpose |
|----------|-------|---------|
| Core Engineering Laws | 10-engineering-laws, lifecycle-sop | Foundation -- always active |
| File Protection (v5.0 NEW) | 21-git-archive-ironlaw | Three-layer: archive + git branch + daily zip |
| Cross-Tool Governance (v5.0 NEW) | knowledge-hub-architecture, scheduled-task-dual-redundancy | Single truth source + dual redundancy |
| Skill Quality (v5.0 NEW) | skill-quality-benchmark | New skills meet benchmark standard |
| Student Onboarding (v5.0 NEW) | student-onboarding | Self-gating layer for AI-course students; see docs/student-pathway/ |
| Agent Management | agent-prompt-ironclad, subagent-strategy, agent-concurrency-fallback, subagent-must-return, multi-agent-coordination | Multi-agent coordination |
| Evidence & Delivery (v5.2 NEW) | harness-evidence-states, delivery-acceptance-layers, agent-autoloop, rule-change-audit | State ladder, layered acceptance, finite loops, audited rule changes |
| Edit Integrity (v5.2 NEW) | version-baseline-check, metric-family-alignment, shell-text-integrity | Right file, whole metric family, no silent shell corruption |
| Continuity & Ops (v5.2 NEW) | session-close-handoff, task-state-sync, backup-signal-trust, public-content-hygiene | Handoffs, real task state, backup evidence, public writing |
| Search & Info | search-decision-tree, lesson-auto-update, anti-info-overload | Information discipline |
| Safety & Ops | script-safety-check, no-blind-overwrite, chinese-path-safety, powershell-safety, pre-action-check, git-recovery, mcp-config-protocol | Prevention of known accidents |
| Memory & Quality | memory-candidate-protocol, memory-confidence, negative-results, anti-illusion-audit, boundary-declaration | Truth maintenance |
| Architecture | competition-workspace-architecture, dual-write-protocol, no-root-rules-dir | Project structure discipline |
| Skill Ecosystem | skill-auto-activation, skill-route-enforcement, skill-execution-discipline, skill-logging-enforcement | If you use skills/plugins |

---

> This framework is alive. Rules grow from real accidents. Each rule blocks one confirmed failure pattern.
> v5.2: 47 rules. From cross-tool ecosystem to evidence states and multi-agent coordination.
> You are looking at a snapshot. The framework updates as new patterns are recognized in production.
