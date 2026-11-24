# 上游同步

本 Skill 的方法提炼自 T3 Code。T3 Code 的维护者会持续修订自己的指令文件、lint 规则和验证脚本；跟着上游更新，本 Skill 就能吸收新的经验，同时去掉上游已经放弃的做法。

## 来源

- 上游：[pingdotgg/t3code](https://github.com/pingdotgg/t3code) 的 `main` 分支。只跟踪上游，不跟踪任何 fork；fork 自己加的内容（例如 `docs/agents/`、平台适配）不属于上游方法。
- 已审阅至：`d73e41a3fa379b591d9fb59d722d2569ec05994b`（2026-11-23）。每次同步后，在同一个提交里更新这一行。
- 本 Skill 不复制 T3 Code 的代码，只提炼方法；引用其中的原句和数字仅作示例。

## 关注路径

| 上游路径 | 提炼出的内容 | 对应参考 |
|---|---|---|
| `AGENTS.md`、`CLAUDE.md` | 规范源、章节骨架、高危操作、改动影响面、品味、文档规则 | [指令文件](../skills/agent-ready/references/instructions.md)、[文档体系](../skills/agent-ready/references/docs-system.md)、[文风](../skills/agent-ready/references/style.md) |
| `docs/README.md`、`docs/internals/00_glossary.md` | 文档索引与编号、按区域组织、术语表写法 | [文档体系](../skills/agent-ready/references/docs-system.md) |
| `docs/internals/15_testing.md`、`.macroscope/check-run-agents/test-signal.md`、`evals/test-signal/`、`.github/scripts/test-delta.cjs`、`.github/workflows/pr-size.yml` | 测试规则、测试评审、防回涨护栏 | [测试](../skills/agent-ready/references/testing.md) |
| 测试清理类 PR（来源：[#22557](https://github.com/pingdotgg/t3code/pull/22557)；后续护栏：[#26166](https://github.com/pingdotgg/t3code/pull/26166)、[#34559](https://github.com/pingdotgg/t3code/pull/34559)） | 评分标准、多轮评审、按语法树删除、前后对比 | [冗余测试清理](../skills/agent-ready/references/test-cleanup.md) |
| `CONTRIBUTING.md`、`.github/pull_request_template.md` | 交付证据 | [验证与环境](../skills/agent-ready/references/verification.md) |
| `scripts/check-changed.ts`、`scripts/prove-scenario.ts`、`docs/internals/15_testing.md#scenarios` | 变更检查命令、基准对照证明 | [验证与环境](../skills/agent-ready/references/verification.md) |
| `t3.json`、`scripts/setup-worktree.ts`、`scripts/dev-runner.ts`、`scripts/lib/dev-memory-limit.ts`、`apps/server/scripts/migrate-dev-db.ts`、`docs/operations/00_development.md` | 工作区初始化标记、隔离、资源上限、测试数据 | [验证与环境](../skills/agent-ready/references/verification.md#开发环境) |
| `oxlint-plugin-t3code/`、`vite.config.ts` | 写成 lint 的规则、写给 Agent 的报错消息、绕过须写理由、提交前钩子 | [经验回流](../skills/agent-ready/references/feedback-loop.md#机械规则写成检查)、[文风](../skills/agent-ready/references/style.md#报错与-lint-消息) |
| `.coderabbit.config.ts`、`.macroscope/` | 一份标准多方读取、文档与代码路径的映射、评审范围 | [经验回流](../skills/agent-ready/references/feedback-loop.md#一份标准多方读取) |
| `evals/` | 面向模型的文本按代码对待 | [经验回流](../skills/agent-ready/references/feedback-loop.md#面向模型的文本按代码对待) |
| `.agents/skills/`、`.cursor/rules/`、`scripts/sync-reference-repos.ts`、`.github/workflows/agent-context-budget.yml` | 仓库专属 Skill、harness 专属规则、依赖源码参考、上下文预算 | [指令文件](../skills/agent-ready/references/instructions.md) |
| `docs/user/`、`docs/internals/` 中的其他页面 | 文风样本，只在抽查文风时读 | [文风](../skills/agent-ready/references/style.md) |

## 同步流程

1. **准备上游副本。** 已有 T3 Code checkout 时，执行 `git fetch <上游 remote>`；没有时，执行 `git clone --filter=blob:none https://github.com/pingdotgg/t3code`。在副本目录里设置 `B=<已审阅至的 SHA>`，`U=<上游 remote>/main`。
2. **列出变化。**

   ```sh
   git log --oneline "$B..$U" -- AGENTS.md CLAUDE.md CONTRIBUTING.md docs/README.md \
     docs/internals/15_testing.md docs/internals/00_glossary.md docs/operations/00_development.md \
     oxlint-plugin-t3code vite.config.ts scripts/check-changed.ts \
     scripts/prove-scenario.ts scripts/dev-runner.ts scripts/lib/dev-memory-limit.ts \
     scripts/setup-worktree.ts t3.json apps/server/scripts/migrate-dev-db.ts .agents/skills \
     .cursor/rules .coderabbit.config.ts .macroscope .github/pull_request_template.md \
     .github/workflows/agent-context-budget.yml evals scripts/sync-reference-repos.ts \
     .github/scripts/test-delta.cjs .github/workflows/pr-size.yml
   git diff --name-status --diff-filter=AR "$B" "$U" -- docs/internals docs/operations .agents \
     .github/workflows .macroscope oxlint-plugin-t3code/rules evals
   ```

   第一条列出关注路径上的提交。另外，用 `git log --oneline --diff-filter=D --shortstat "$B..$U" -- '*.test.*'` 查看有没有新的大规模测试删除；有的话，读它的 PR 描述，看清理方法是否有变化。第二条找新增和改名的文件：新的内部文档、仓库专属 Skill、lint 规则、评审检查或评测，往往意味着新方法。上游会给文档改名（例如加编号前缀），关注路径被改名后，第一条命令按旧路径就查不到后续变化，要同步更新上表和命令；命中的新路径如果值得长期关注，也加进去。
3. **逐条判断。** 用 `git show <提交> -- <路径>` 读 diff，把每项变化归入三类之一：
   - **新方法**：多数项目都会遇到，换成通用说法后仍然成立。加进对应参考。
   - **方法变了或被删除**：重写或删除对应段落。上游删掉一条规则，通常说明它没用或有害，这比新增更值得跟进。
   - **T3 专属**：只和它的产品、技术栈有关。跳过。

   要加入的内容还要过 [准入测试](../skills/agent-ready/references/instructions.md#准入测试)：少了它，使用本 Skill 的项目中，Agent 会具体做错什么？
4. **改写。** 按 [文风](../skills/agent-ready/references/style.md) 写成中文，示例保持通用；写 T3 Code 的数字时注明出处。
5. **验证。** 运行 `python3 -m unittest discover -s tests -v`。改动涉及哪个任务分支，就按 [CONTRIBUTING.md](../CONTRIBUTING.md) 中的对应场景，在真实仓库上试用。
6. **记录。** 更新上面“已审阅至”的 SHA 和日期，提交信息写成 `{feat|docs}-Agent就绪技能-同步T3Code上游至<短SHA>`。Skill 行为有变化时，按 CONTRIBUTING 发布新版本。没有值得吸收的变化，也要更新 SHA，免得下次重复审阅同一批提交。

## 何时同步

T3 Code 发布新版本后，或者使用中觉得某条方法过时的时候。在 GitHub 上把 pingdotgg/t3code 设为 Watch → Custom → Releases，就能收到发版通知。
