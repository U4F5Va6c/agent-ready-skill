# 维护约定

- 用中文沟通。提交格式为 `{type}-{中文模块}-{中文描述}[-{关联项}]`。
- `skills/agent-ready/` 是唯一的技能源。不要编辑 Dotfiles 快照或 Agent 的安装副本。
- 本 Skill 自己也遵守它的规则：`SKILL.md` 只放原则、路由和完成条件，细节放进 references；修改时按 `references/style.md` 和 `references/instructions.md#准入测试` 自查。
- 示例只用通用场景，不写任何公司、项目、租户、路径或真实数据。
- 运行 `python3 -m unittest discover -s tests -v`。结构检查不能替代在真实仓库上的试用。
- 根据 T3 Code 上游更新修订本 Skill 前，先读 `docs/upstream.md`，从其中记录的已审阅提交开始比对。
- 维护流程见 CONTRIBUTING.md。没有明确请求时，不发布、不打标签、不创建 PR。
