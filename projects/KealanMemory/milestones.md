# KealanMemory - 里程碑

## M1. 本地记忆系统可用

- **状态**：已完成
- **日期**：2026-04-22
- **内容**：
  - 建立核心目录结构。
  - 支持默认记忆和项目记忆加载。
  - 建立 Claude/Codex 可复用的上下文组装方式。

## M2. 安全止血与加载协议统一

- **状态**：已基本完成
- **日期**：2026-04-22
- **内容**：
  - 安装模板不再应包含真实密钥。
  - hooks 自动提交默认关闭。
  - 根路径解析、`--full`、PowerShell/BAT 启动脚本和健康检查进入统一维护范围。

## M3. Web、历史、项目生命周期和路由能力成型

- **状态**：已基本完成
- **日期**：2026-04-22
- **内容**：
  - Web 本地运维面板具备 routing、history、health 等能力。
  - `project_manager.py` 支持项目创建、列出、归档和校验。
  - `history_search.py` 支持按需历史注入。
  - `routing_map.md/json` 建立意图到 role/skill/files 的映射。

## M4. KealanMemory 自身项目记忆拆分

- **状态**：本次完成
- **日期**：2026-04-22
- **内容**：
  - 新增 `projects/KealanMemory/project_brief.md`。
  - 新增 `projects/KealanMemory/current_status.md`。
  - 新增 `projects/KealanMemory/constraints.md`。
  - 新增 `projects/KealanMemory/next_actions.md`。
  - 新增 `projects/KealanMemory/decisions.md`。
  - 新增 `projects/KealanMemory/milestones.md`。
  - 在 `boot/memory_map.json` 注册 `KealanMemory`。

## M5. 下一阶段质量闭环

- **状态**：待开始
- **目标**：
  - 当前大改动按主题拆分并形成发布说明。
  - 补齐 golden snapshot。
  - role/skill frontmatter schema 化。
  - hooks 增加脱敏日志。
  - Web 支持安全编辑、diff 预览和保存后健康检查。
  - 历史索引自动维护。
  - 统一 CLI 产品化。
