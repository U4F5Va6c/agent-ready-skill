# Agent Ready Skill

让仓库成为 Claude Code、Codex 等 Agent 能高效、安全工作的环境。方法提炼自 [T3 Code](https://github.com/pingdotgg/t3code) 仓库：它的多数代码由 Agent 写成，指令文件、文档体系、lint 规则和评测都是在这个过程中逐步打磨出来的。

本 Skill 提供方法、清单和模板。各项目自己的事实（路径、命令、账号、数据）仍写在各自仓库里。

## 内容

| 入口 | 用途 |
|---|---|
| [SKILL.md](skills/agent-ready/SKILL.md) | 三条原则、任务路由、与其他 Skills 的分工、完成条件 |
| [审计与接入](skills/agent-ready/references/audit.md) | 逐层核对仓库，报告差距，分批补齐 |
| [指令文件](skills/agent-ready/references/instructions.md) | 规范源、准入测试、章节骨架、篇幅预算、仓库专属 Skill |
| [文档体系](skills/agent-ready/references/docs-system.md) | 按读者分层、写入门槛、索引、术语表、工作产物 |
| [文风](skills/agent-ready/references/style.md) | 句子与结构规则、注释、报错消息、中文写作、改写对照 |
| [验证与环境](skills/agent-ready/references/verification.md) | 变更检查命令、测试规则、交付证据、隔离的开发环境 |
| [经验回流](skills/agent-ready/references/feedback-loop.md) | 经验落在哪一层、规则写成检查、标准共享、评测、上下文预算 |
| [AGENTS 模板](skills/agent-ready/assets/AGENTS.template.md) | 按需取用的指令文件骨架 |

## 安装

```sh
npx -y skills add U4F5Va6c/agent-ready-skill -g -a claude-code codex -s agent-ready -y
```

完整内容会安装到 `~/.agents/skills/agent-ready`，Claude Code 使用安装器建立的软链。在新会话中用 `/agent-ready`（Claude Code）或 `$agent-ready`（Codex）调用；当任务涉及指令文件、项目文档或 Agent 失误复盘时，它也会自动加载。

需要固定版本时，安装已发布的标签：

```sh
npx -y skills add https://github.com/U4F5Va6c/agent-ready-skill/tree/v0.1.0/skills/agent-ready -g -a claude-code codex -s agent-ready -y
```

跟随主分支的用户可运行 `npx skills update -g -y` 更新（该命令也会检查其他已安装的 Skills）。

## 配合使用

- [Matt Pocock Skills](https://github.com/mattpocock/skills)：`writing-for-agents` 提供面向 Agent 的写作手法，`setup-matt-pocock-skills` 生成 tracker 和领域文档的绑定，`domain-modeling` 维护术语表与 ADR，`retro` 负责复盘。本 Skill 补充仓库结构、文风和经验回流，不重复它们的内容。需要另行安装。
- [codeup-skill](https://github.com/U4F5Va6c/codeup-skill)：托管在阿里云云效的仓库，其工作项、合并请求和流水线交给它处理。

使用示例：

> 使用 agent-ready 审计这个仓库，告诉我 Agent 在这里最容易犯什么错，以及最小的改法。

> 这次 Agent 又在测试里用了 sleep，按 agent-ready 的经验回流决定该改哪里。

## 来源与上游同步

方法提炼自 [pingdotgg/t3code](https://github.com/pingdotgg/t3code) 的 `main` 分支。[上游同步](docs/upstream.md) 记录了已审阅到的上游提交、每份参考对应的上游路径，以及从上游更新中吸收、改写或删除方法的流程。

使用示例：

> 按 docs/upstream.md 检查 T3 Code 上游自上次审阅以来的变化，列出值得吸收的方法，再修订 agent-ready。

## 维护

本仓库是唯一的开发源。验证与发布见 [CONTRIBUTING.md](CONTRIBUTING.md)。问题通过 Issues 跟踪，修改通过 PR 审阅。

MIT License。与 T3 Code、Matt Pocock、Anthropic、OpenAI 均无官方隶属关系。
