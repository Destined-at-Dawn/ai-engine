# ai-engine

> **给 AI 编程代理的工程纪律框架：可复用的规则与适配器，而不是 agent runtime。**

[English](README.en.md) · [能力边界](docs/capabilities.md) · [安装指南](docs/agent-install.md) · [兼容性](docs/compatibility.md) · [贡献](CONTRIBUTING.md)

ai-engine 把 AI 辅助开发中反复出现的失败模式——例如盲目覆盖文件、验证不足、异常指标、多人/多 Agent 冲突和重复踩坑——整理成可审阅的 Markdown 规则与 Agent 适配说明。

## 它是什么 / 不是什么

| 是什么 | 不是什么 |
|---|---|
| 47 个可组合的工程纪律规则，外加一个多 Agent 协作参考工具 | 一个可执行的 agent runtime 或后台服务 |
| Claude Code 的规则目录，以及 Codex、Cursor、Aider、Gemini CLI 的集成说明 | 安装后自动替你创建备份、定时任务或合并分支的插件 |
| 用于讨论、改进和复用 AI 工程工作流的开源框架 | 让模型“变聪明”的提示词魔法 |

仓库实际交付的内容、参考架构与需要自行实现的自动化，见 [能力边界](docs/capabilities.md)。

## 3 分钟试用：防止盲目覆盖

以 Claude Code 为例，在一个测试项目中安装一条最小规则：

```bash
git clone https://github.com/Destined-at-Dawn/ai-engine.git
mkdir -p YOUR_PROJECT/.claude/rules
cp ai-engine/.claude/rules/no-blind-overwrite.md YOUR_PROJECT/.claude/rules/
```

重新打开你的代理会话后，要求它修改一个已有文件。它应先读取现有内容、说明计划修改的位置，再进行变更。更多验证步骤、Windows 命令和其他代理的接入方式见 [安装指南](docs/agent-install.md)。

> 这是一个规则框架：代理是否遵守规则，取决于所用工具、项目配置和你的最终审阅。请先在测试项目验证，再推广到重要仓库。

## 从痛点选择规则

| 痛点 | 建议先读 |
|---|---|
| 担心 AI 覆盖或删除已有文件 | `no-blind-overwrite.md`、`script-safety-check.md` |
| AI 报出的数字过于漂亮 | `anti-illusion-audit.md` |
| AI 声称完成但验证不足 | `10-engineering-laws.md`、`lifecycle-sop.md` |
| 同一种失败反复发生 | `negative-results.md` |
| 多 Agent 改动冲突 | `multi-agent-coordination.md` + `tools/agent-coord/`、`agent-prompt-ironclad.md` |
| AI 改了旧版文件，或只改了一处数字 | `version-baseline-check.md`、`metric-family-alignment.md` |
| 本地跑通就说“已发布” | `harness-evidence-states.md`、`delivery-acceptance-layers.md` |
| subagent 跑了一半被放弃，或结果丢在临时目录 | `subagent-must-return.md`、`session-close-handoff.md` |
| AI 觉得“这样更好”就改了工作流 | `rule-change-audit.md` |
| 备份任务一路绿灯，其实早就没推上去 | `backup-signal-trust.md` |
| AI 代写的对外内容混进内部信息或他人姓名 | `public-content-hygiene.md` |
| 想使用完整规则集 | `.claude/rules/`（47 个规则文件） |

## 支持状态

| Agent | 接入方式 | 状态 |
|---|---|---|
| Claude Code | `.claude/rules/` | 主要目标 |
| Codex | `AGENTS.md` + 规则副本 | 已提供接入示例 |
| Cursor | `.cursor/rules` | 已提供接入说明 |
| Aider | `.aider.conf.yml` | 已提供接入说明 |
| Gemini CLI | `GEMINI.md` | 已提供接入说明 |

“已提供接入说明”不等于持续自动兼容；请查看 [兼容性矩阵](docs/compatibility.md) 中的验证范围与限制。

## 仓库结构

```text
ai-engine/
├── .claude/rules/       # 47 个核心 Markdown 规则
├── tools/agent-coord/   # 多 Agent 协作参考工具（纯标准库 Python + 自测）
├── adapters/            # 各 Agent 的集成示例
├── docs/                # 安装、能力边界、兼容性、设计哲学与事故案例
├── templates/           # 中英文记忆模板
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE              # MIT
```

## 贡献与反馈

- 用法问题、想法与经验：请使用 GitHub Discussions（启用后）或先开一个结构化 Issue。
- 可复现的错误、文档问题和规则提案：请使用 Issue 模板。
- 安全问题：请阅读 [SECURITY.md](SECURITY.md)，不要在公开 Issue 中披露细节。
- 欢迎提交新适配器、公开可复现案例、规则改进、验证方法和翻译；详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 版本与演进

当前公开规则集为 **v5.2.0 / 47 个规则文件**。v5.2.0 新增 13 条规则、`tools/agent-coord/` 参考工具和 3 个脱敏事故案例，见 [CHANGELOG.md](CHANGELOG.md)。版本历史见 [CHANGELOG.md](CHANGELOG.md)；发布说明见 GitHub Releases。

## 许可证

[MIT](LICENSE)

> 让 AI 像工程师一样工作：先理解边界，再修改；先验证证据，再宣布完成。
