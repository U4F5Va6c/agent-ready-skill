# 维护与发布

只在 `skills/agent-ready/` 中修改技能源文件。`SKILL.md` 保持简短，具体方法放进按需加载的 references，骨架放在 assets。

## 验证

```sh
python3 -m unittest discover -s tests -v
npx -y skills add . --list
```

CI 检查以下内容：入口元数据、包内的相对链接和章节锚点、机器路径，以及 references 是否都能从入口到达。`tests/test_matt_contract.py` 只在本机安装了 Matt Skills 时运行，核对本 Skill 引用的 Matt Skill 名称和 `## Agent skills` 标题是否仍然存在；`npx skills update` 之后要先跑一遍。它不验证 Agent 的实际行为。

方法或文风有改动时，至少在一个真实仓库上试用以下场景：

- 审计一个只有 `AGENTS.md`、没有 `CLAUDE.md` 的仓库：指出 Claude Code 读不到规范源，并给出最小改法。
- 审计一个已接入 Matt Skills 的仓库：不重写 `docs/agents/`，也不重复生成 `## Agent skills` 块。
- 仓库有敏感数据目录和 `.env`：审计只记录路径和键名，不读取内容或值。
- 用容器开发，各工作区的 compose 项目名相同：指出新工作区会接管主实例，并给出隔离方法。
- 仓库已有部分机制（例如有回放但没有触发说明）：结论标为“部分”并写明缺口，不报告为缺失。
- Agent 在测试里用了 `sleep`：经验落在 lint 或测试规则，而不是在指令文件里加一句叮嘱。
- 修订一份冗长的指令文件：每次删减都能说出依据的是准入测试的哪一条，并保留真正的高危操作。
- 改写一篇用户文档：去掉界面描述和实现细节，保留任务、设置路径和不直观之处。
- 云效仓库：追踪与交付交给 `codeup` Skill，本 Skill 不写平台命令。

试用时，由一个没有维护上下文的 Agent 加载已安装的 Skill 来执行。只有实际跑过的场景，才能声明通过。

## 发布

1. 检查通过后，按 `{type}-{中文模块}-{中文描述}` 提交，经 PR 审阅后合入 main。
2. 用 `vMAJOR.MINOR.PATCH` 打一个不可移动的标签，并写明行为变化、验证方式和已知限制。小改动和文档修订增加 patch，较大的方法调整增加 minor，不兼容的变更增加 major。
3. 安装标签版本，验证安装目录完整，再更新个人 Dotfiles 快照和来源提交。不要直接编辑 `~/.agents/skills/agent-ready`。

Issues 和 PR 中不要粘贴任何项目的私有代码、数据或凭据。
