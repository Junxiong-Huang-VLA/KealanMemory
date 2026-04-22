# 记忆加载顺序（Load Order）

## 默认加载（核心记忆，每次必读）

| 顺序 | 文件 | 作用 |
|------|------|------|
| 1 | `profile/identity.md` | 我是谁，做什么方向 |
| 2 | `profile/work_style.md` | 如何和我协作 |
| 3 | `profile/preferences.md` | 路径、命名、工具偏好 |
| 4 | `operating_rules/communication_rules.md` | 回复风格约束 |
| 5 | `context/active_focus.md` | 当前最关心什么 |
| 6 | `context/global_constraints.md` | 跨项目通用约束 |

**以上 6 个文件 = 核心记忆，约 2000 tokens，每次对话必加载。**

## 项目记忆（按需加载，指定项目时追加）

调用 `--project <项目名>` 时额外加载：

| 顺序 | 文件 | 作用 |
|------|------|------|
| 7 | `projects/<项目名>/project_brief.md` | 项目目标和链路 |
| 8 | `projects/<项目名>/current_status.md` | 当前进度和待办 |
| 9 | `projects/<项目名>/constraints.md` | 项目级硬约束 |
| 10 | `projects/<项目名>/next_actions.md` | 下一步行动 |

可选追加（深度开发时）：
- `projects/<项目名>/decisions.md`
- `projects/<项目名>/milestones.md`
- `operating_rules/coding_rules.md`
- `operating_rules/project_rules.md`
- `operating_rules/environment_rules.md`

## 默认不加载（按需检索）

- `context/history/` — 历史决策，需要时通过 `history_index.md` 检索
- `archive/` — 归档内容，正常开发不需要
- `profile/expertise.md` — 技术专长，一般不需要（除非讨论新技术选型）
