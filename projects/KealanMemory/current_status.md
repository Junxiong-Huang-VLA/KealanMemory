# KealanMemory - 当前状态

## 评级

**当前评级：B** - 本地可用，核心链路已打通，但仍处于快速演进期。

**评级原因**：

- 已具备可用的核心记忆加载、项目注册、历史检索、Web 运维、role/skill 路由和测试基础。
- 已完成一轮安全止血：安装模板不应包含真实密钥，hooks 自动提交默认关闭，敏感信息扫描进入健康检查。
- 仍存在发布整理、snapshot 回归、role/skill schema、hook 可观测性、Web 编辑和 CLI 产品化等后续工作。

## 已完成

- [x] 建立 `profile/`、`operating_rules/`、`context/`、`projects/`、`roles/`、`skills/`、`boot/`、`web/` 的分层目录。
- [x] 建立 `memory_map.json` 作为默认加载、项目加载、可选加载和项目注册的配置中心。
- [x] `load_memory.py` 支持核心记忆、项目记忆、`--full` 可选记忆和 `--history` 历史注入。
- [x] `project_manager.py` 支持 `create/list/archive/validate`。
- [x] `history_search.py` 支持按关键词或文件路径检索历史上下文。
- [x] Web 已具备本地管理入口，并包含 routing、history、health 等 API。
- [x] 建立 `routing_map.md/json`，让意图能够映射到 role、skill 和默认加载文件。
- [x] 14 个 role 与 20 个 skill 已进入标准化方向。
- [x] 建立 schema、测试目录和预提交检查脚本。
- [x] 新增 KealanMemory 自身项目记忆，用于承载本仓库优化计划。
- [x] 建立 hook 脱敏日志，记录项目检测、摘要、写回和 Git 同步状态。
- [x] Web 增加白名单编辑、diff 预览和保存后健康检查。
- [x] 补齐 golden snapshot 与 role/skill frontmatter schema 校验。
- [x] 从 LabSOPGuard 当前状态中移出 KealanMemory 建设条目。

## 进行中

- [ ] 将当前大改动按安全、loader、Web、role/skill、测试、项目 CLI、文档等主题分组整理。
- [ ] 增加文档由配置生成，减少启动 prompt 和安装文档漂移。
- [ ] 增加历史索引自动维护，发现未索引历史文件和断链。
- [ ] 推进统一 `kealan-memory` CLI 产品化。
- [ ] 将高价值 Markdown skill 升级为标准 Codex skill 目录。

## 已知问题

| 问题 | 严重程度 | 状态 |
|---|---|---|
| 当前工作树存在大量未提交修改，主题跨度大 | 高 | 待分组提交或形成发布说明 |
| 终端读取部分中文 Markdown 时显示乱码 | 中 | 待确认编码和终端输出策略 |
| LabSOPGuard 记忆中仍可见 KealanMemory 建设条目 | 中 | 已清理当前状态列表 |
| Web 编辑能力尚未形成白名单、diff、健康检查闭环 | 中 | 已完成基础闭环 |
| hooks 失败排查缺少统一日志 | 中 | 已完成基础日志 |

## 最近一次更新

- **时间**：2026-04-22
- **做了什么**：
  - 新增 `projects/KealanMemory/` 六个项目记忆文件。
  - 将 KealanMemory 注册到 `boot/memory_map.json`。
  - 从 `projects/LabSOPGuard/current_status.md` 移出 KealanMemory 建设条目。
  - 完成 snapshot/schema、hook 日志、Web 编辑和项目记忆拆分的集成验证。
