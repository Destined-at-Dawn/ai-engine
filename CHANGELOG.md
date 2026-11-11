# Changelog

## Unreleased

## v5.2.0 (2026-11-11) — Evidence states and multi-agent coordination

Distilled from three months of daily multi-tool work (Claude Code, Codex and others) across document, research-paper and product workspaces. All material is generalized and sanitized; no project data, names, paths or credentials are included.

### Added — rules (13, total 47)

#### Edit integrity
- `version-baseline-check.md` — list candidates, confirm the newest revision and record the baseline hash before editing a versioned deliverable.
- `metric-family-alignment.md` — realign every value of a metric family from raw evidence; check denominators; finish with a zero-hit residual scan.
- `shell-text-integrity.md` — keep persisted text out of shell-embedded strings (backtick substitution, backslash escapes in paths); read back after writing.

#### Evidence and delivery
- `harness-evidence-states.md` — state ladder (`SOURCE_ONLY` → `LOCAL_ONLY` → `BUILD_VERIFIED` → `DEVICE_VERIFIED` → `PUBLISHED`), blue/red/first-principles roles, fleet conditions, completion gate.
- `delivery-acceptance-layers.md` — document deliverables L1–L4 and software source/build/deploy/real-use layers, each verified separately.
- `agent-autoloop.md` — one verifiable goal per round; end the round instead of waiting when a human decision is needed; hop limits.
- `rule-change-audit.md` — one change at a time, same-condition baseline, recorded adopt/rollback/insufficient-evidence verdict.

#### Agent coordination
- `multi-agent-coordination.md` — lease before editing shared deliverables, allocator for revision numbers, append-only registry, rules every tool must follow live in `AGENTS.md`.
- `subagent-must-return.md` — collect and verify launched sub-agents; write the handoff before a long run; protect active sub-agent directories from cleanup.

#### Continuity and operations
- `session-close-handoff.md` — five-step session close plus `work-logs/HANDOFF-INDEX.md` with final-evidence status.
- `task-state-sync.md` — executed, marked and verified are three separate conditions.
- `backup-signal-trust.md` — scheduler state and exit codes are not evidence; only the remote is; non-zero exit on failure; alert after 24 hours.
- `public-content-hygiene.md` — public / authorized / internal tiers, anonymized references to other people, only publicly reachable links, direct wording without defensive filler.

### Added — tools
- `tools/agent-coord/` — the repository's first executable artifact: a standard-library Python CLI (`init`, `status`, `claim`, `release`, `next-rev`, `log`, `doctor`) with a self-test (`test_coord.py`, 7 tests).

### Added — case studies
- `silent-backup-failure.md`, `half-corrected-metrics.md`, `parallel-agents-duplicate-revision.md`.

### Changed
- Project name in all current documentation aligned with the repository name `ai-engine` (formerly `niuma-engine`; GitHub redirects the old URL). Codex adapter folder renamed from `.niuma-engine/rules` to `.ai-engine/rules`.
- `CLAUDE.md`, both READMEs, `docs/capabilities.md`, `docs/compatibility.md`, Cursor and Gemini CLI adapters updated to v5.2.0 / 47 rule files; Cursor and Gemini adapters no longer claim 29 rules.
- `verify-docs.mjs` now also checks the adapters, `docs/capabilities.md`, the coordination tool files, and stale "34 rules" wording.

## v5.1.0 (2026-08-12) — OSS credibility foundation

### Changed
- Reframed public documentation around shipped rules, documented integrations, and reference architectures.
- Added a reproducible minimal-install path and a current Codex `AGENTS.md` example.
- Added community-health files, Issue Forms, a pull request template, and a local documentation-consistency check.
- Added three sanitized, maintainer-reported incident patterns with verification steps and explicit limitations.
- Enabled GitHub Discussions and Private Vulnerability Reporting for public collaboration and security disclosure.


## v5.0.0 (2026-07-06) -- 从单工具纪律到跨工具生态系统

### 结构性升级
- **知识中枢架构**：从「每个工作区独立管理」升级到「中枢为单一真相源 + 工作区投影」的跨工具治理体系
- **三层文件保护体系 (R21)**：L1 操作前归档 + L2 Git agent/{date} 分支隔离 + L3 每日 Zip 快照
- **Skill 质量对标闭环**：从「有 SKILL.md 就行」到「顶层6文件 + references>=5 + scripts>=1 + 24项门禁」
- **定时任务双冗余**：AI 定时任务 + 操作系统任务计划程序，互不依赖，互为兜底

### 新增规则（4条）
#### 文件保护与安全
- `21-git-archive-ironlaw.md` -- 三层文件保护铁律（修改前必归档 + 禁止直推main + 每日Zip快照）

#### 跨工具治理
- `knowledge-hub-architecture.md` -- 知识中枢架构规则（单一真相源 + 一改全改 + li-zhongshu 守护者）
- `scheduled-task-dual-redundancy.md` -- 定时任务双冗余规则（AI+OS 双调度，故障时互相兜底）

#### Skill 质量
- `skill-quality-benchmark.md` -- Skill 质量对标规则（24项创建门禁 + 防退化机制 + 三阶段学习闭环）

#### 学员成长（2026-07-09 补充）
- `student-onboarding.md` -- 学员引导铁律，自门控（检测 `STUDENT-GUIDE.md` 存在即激活，不影响非学员用户）
- `docs/student-pathway/` -- 六层学员成长路线图（L0 快速上手 → L5 技能生态），配套 `career-compass.md`（5 个 AI 能力方向自评）+ `self-check.md`（30秒定位当前层级）
- 新增下载包 `niuma-engine-v5.0.0-student-pack.zip`：合并版 CLAUDE.md（含学员模式段）+ 34 条规则 + 六层路线图，解压即用

### 优化
- `README.md` -- 全面重写：从「10条法则故事」升级到「多Agent生态 + 知识中枢 + 三层保护」完整介绍
- `CLAUDE.md` -- 启动序列更新：增加知识中枢感知 + R21 三层保护 + 工作区协议
- `EVOLUTION.md` -- 进化日志更新：v5.0 升级路径和事故来源
- `docs/philosophy.md` -- 设计哲学更新：从「纪律框架」到「生态系统」的范式升级
- `skill-route-enforcement.md` -- 合并 v4.0 的铁律 0 和铁律 0.5 为单一铁律 0（创建+迭代统一入口）

### 规则总数
- v4.0: 29 条规则
- v5.0: **34 条规则**（新增 5 条：4 条核心 + 1 条学员引导）

---


## v4.0.0 (2026-06-22) — 从单体纪律到多Agent协作生态

### 结构性修复
- **修复 .gitignore 阻止规则分发**：`.claude/` 整目录排除 → `.claude/*` + `!.claude/rules/`
- **全量规则入库**：从实际工作区同步全部 29 条规则（v1.0 仅含 10 条）

### 新增规则（19条，自v1.0以来）
#### Agent管理与故障恢复
- `agent-concurrency-fallback.md` — Agent 并发降级协议（429限流零等待切换）
- `agent-prompt-ironclad.md` — Agent Prompt 三要素铁律（目标/格式/停止条件）
- `subagent-strategy.md` — Sub-Agent 策略（何时用/不用/模型选择/故障恢复）

#### 信息搜索与纪律
- `search-decision-tree.md` — 搜索决策树（何时搜/搜多深/用什么工具）
- `lesson-auto-update.md` — 教训闭环自动更新（用户纠正→工作流自动修改）

#### Skill管理与路由
- `skill-auto-activation.md` v2.0 — 技能自动激活（三层路由+联动链+自我学习闭环）
- `skill-execution-discipline.md` — Skill 执行纪律（必读执行协议，不可跳过）
- `skill-logging-enforcement.md` — Skill 调用日志强制记录
- `skill-route-enforcement.md` — Skill 路由注册强制规则

#### 安全与运维深化
- `chinese-path-safety.md` — Windows 中文路径安全（禁Bash heredoc）
- `powershell-safety.md` — PowerShell 安全规则
- `pre-action-check.md` — 动手前检查门禁
- `git-recovery.md` — Git 检查点与恢复（删前commit+30秒恢复）
- `mcp-config-protocol.md` — MCP 配置协议四铁律

#### 架构与治理
- `competition-workspace-architecture.md` — 竞赛项目工作区架构
- `dual-write-protocol.md` — 双写协议（经验教训根级+模块级同步）
- `no-root-rules-dir.md` — 禁止根目录 rules/（防回退）
- `_MIGRATED-TO-RULES.md` — 规则迁移说明

### 优化
- `anti-info-overload.md` — 补充数据筛选和折叠技巧
- `no-blind-overwrite.md` — 补充 .gitignore 安全策略
- `script-safety-check.md` — 细化路径白名单

### 移除（太个人化/信息密度低）
- `identity-consistency.md` — 太泛泛，具体规则已覆盖
- `preference-memory.md` — 信息密度不足
- `voice-dna-auto-inject.md` — 个人文风，不适合通用框架

---

## v1.0.0 (2026-05-26)

### Added
- 10 cross-cutting engineering laws
- 6-stage project lifecycle SOP
- 3-layer memory architecture (with confidence labels)
- Anti-illusion audit (five-question check)
- Negative result archiving mechanism
- Memory candidate confirmation protocol
- Script safety check protocol
- Anti-information overload rules
- Boundary declaration rules
- Claude Code / Codex / Cursor / Aider / Gemini CLI adapters
- Chinese and English memory templates

