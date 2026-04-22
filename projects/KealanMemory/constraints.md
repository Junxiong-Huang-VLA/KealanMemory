# KealanMemory - 项目约束

## 硬约束

- 不回滚他人修改；当前工作树可能包含多条并行任务的未提交变更。
- KealanMemory 自身项目记忆只能写入 `projects/KealanMemory/**`，项目注册写入 `boot/memory_map.json`，必要时才更新 `context/active_focus.md`。
- 不修改 LabSOPGuard，除非用户明确要求；如果只读检查发现 KealanMemory 内容混入 LabSOPGuard，只报告不改。
- `boot/memory_map.json` 是加载顺序和项目注册的单一事实来源。
- `projects/_template` 是模板，不应被当作真实业务项目加载。
- hooks 不得默认执行无差别 `git add .`、自动 push 或提交敏感信息。
- 安装模板、文档、示例配置不得包含真实 token、密钥或私有凭据。

## 路径约束

| 配置项 | 唯一来源 | 当前值 |
|---|---|---|
| 记忆根目录 | `KEALAN_MEMORY_ROOT` 或脚本向上推导 | `D:/KealanMemory` |
| 项目注册 | `boot/memory_map.json.projects` | 包含 `KealanMemory` |
| 默认输出 | `boot/memory_map.json.output_file` | `boot/assembled_context.txt` |
| 项目文件 | `boot/memory_map.json.project_load` / `optional_load` | `projects/{project}/...` |

## Web 约束

- Web API 必须校验项目名和可编辑路径，不能让任意路径写入本地文件。
- 剪贴板、diff、Markdown 渲染和错误展示需要避免注入和命令拼接风险。
- 静态资源应逐步从单体模板拆出，保持移动端可用和键盘可访问。

## Role/Skill 约束

- role frontmatter 需要稳定字段：`id`、`slug`、`category`、`description`、`triggers`、`skills`、`default_files`。
- skill frontmatter 需要可解析到真实 `skills/*.md` 文件，并说明适用场景、输入、步骤、输出和失败处理。
- `routing_map.json` 中引用的 role、skill、default files 必须存在。

## 测试与发布约束

- 每次改动加载协议、项目注册、role/skill 路由或 Web API 后，应运行健康检查和相关测试。
- 发布前至少运行：

```powershell
python boot/project_manager.py validate
python boot/load_memory.py --project KealanMemory --full --output $env:TEMP\kealan_memory_project.txt
```

- 大型重构应按主题拆分提交，避免安全、loader、Web、role/skill、测试和文档混在一个不可审查提交里。
