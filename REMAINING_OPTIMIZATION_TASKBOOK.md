# KealanMemory 下一阶段优化任务书

生成日期：2026-04-22

说明：本任务书基于当前最新开发状态更新。按你的要求，本版不再跟进外部 token 轮换事项，只记录代码库本身还值得继续优化的工作。

## 0. 当前已完成基线

当前项目已经具备以下能力：

| 能力 | 状态 |
|---|---|
| 安全止血 | 安装模板不再包含真实密钥；hook 自动提交默认关闭；疑似密钥扫描进入健康检查 |
| 统一加载 | Python/PowerShell/BAT 支持统一根路径；`--full` 能加载项目 `decisions.md` 和 `milestones.md` |
| 健康检查 | `python boot/check_memory_consistency.py` 通过，当前结果为 `0 failed, 0 warnings` |
| 测试体系 | `python -m pytest -q` 通过，当前 `9 passed` |
| Schema | 已有 `schemas/memory_map.schema.json` 和 `schemas/routing_map.schema.json` |
| 项目生命周期 | `boot/project_manager.py` 支持 `create/list/archive/validate` |
| 历史检索 | `boot/history_search.py` 支持关键词检索；`load_memory.py --history` 支持历史注入 |
| Web 运维 | Web 已有 `/api/routing`、`/api/history`、`/api/health` 和 Ops 面板 |
| Role/Skill 路由 | 已有 `boot/routing_map.md/json`，14 个 role 与 20 个 skill 已标准化 |
| 提交门禁 | 已有 `scripts/pre_commit_check.ps1` 和 `scripts/install_pre_commit.py` |

## 1. 剩余优化总览

| 优先级 | 任务 | 价值 |
|---|---|---|
| P0 | N01 当前大改动分组提交与发布说明 | 降低 review、回滚和后续维护成本 |
| P0 | N02 行尾与生成物治理 | 消除 CRLF 警告，避免 pycache/生成物污染 |
| P1 | N03 Golden snapshot 测试 | 防止上下文加载顺序和格式悄悄漂移 |
| P1 | N04 Role/Skill frontmatter schema | 让 role/skill 元数据从约定升级为可验证结构 |
| P1 | N05 Hook 日志与可观测性 | hook 失败可追踪，不再只能静默吞错 |
| P2 | N06 KealanMemory 自身项目记忆拆分 | 区分工具项目和 LabSOPGuard 业务项目 |
| P2 | N07 文档由配置生成 | 减少硬编码路径和加载顺序重复 |
| P2 | N08 Web 编辑与 diff 预览 | 让日常维护不用手动打开 Markdown |
| P2 | N09 历史索引自动维护 | 新增历史文件时自动更新/校验索引 |
| P3 | N10 CLI 产品化 | 提供 `kealan-memory` 统一命令 |
| P3 | N11 高价值 skill 升级为标准 Codex skill 目录 | 从 Markdown 命令升级为可复用技能包 |
| P3 | N12 安装流程沙盒测试 | 降低新机器安装破坏用户配置的风险 |
| P3 | N13 Web 体验继续增强 | 增加搜索高亮、状态缓存、快捷键和更清晰的信息架构 |

## 2. 任务详情

### N01. 当前大改动分组提交与发布说明

优先级：P0

负责人：系统架构师 + 调试专家

范围：当前工作区全部改动、`README.md`、可选新增 `CHANGELOG.md`。

问题：当前工作区包含安全、loader、Web、role/skill、测试、schema、项目 CLI、历史检索等多类改动。如果一次性提交，后续定位回归和回滚成本很高。

交付物：

- 按主题拆分提交或至少形成提交分组清单。
- 新增一段发布说明，说明从旧版升级到当前版需要注意的命令。

建议提交组：

1. 安全与安装治理：`.gitignore`, `install/*`, `boot/hooks/*`
2. Loader 与脚本：`boot/memory_loader.py`, `boot/load_memory.py`, `boot/load_memory.ps1`, `boot/start_memory.bat`
3. Role/Skill 路由：`boot/routing_map.*`, `roles/`, `skills/`, `boot/write_skills.py`
4. Web 运维：`web/app.py`, `web/templates/`, `web/static/`
5. 验证体系：`boot/check_memory_consistency.py`, `tests/`, `schemas/`, `scripts/`
6. 项目与历史 CLI：`boot/project_manager.py`, `boot/history_search.py`
7. 任务书与文档：`README.md`, `OPTIMIZATION_TASKBOOK.md`, `REMAINING_OPTIMIZATION_TASKBOOK.md`

验收标准：每组提交前运行 `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/pre_commit_check.ps1` 均通过。

### N02. 行尾与生成物治理

优先级：P0

负责人：后端/自动化工程师

范围：新增 `.gitattributes`，更新 `.gitignore`，检查 `__pycache__` 和生成物。

问题：当前 `git diff --stat` 显示大量 `LF will be replaced by CRLF` 警告；运行测试和脚本会生成 `__pycache__`，虽然多数已忽略，但还需要统一策略。

交付物：

- 新增 `.gitattributes` 统一文本文件行尾。
- 明确 `.ps1/.bat/.md/.py/.js/.css/.json` 的行尾策略。
- 确认 `boot/assembled_context.txt`、`__pycache__/`、临时 snapshot 输出不入库。

验收标准：新增改动不再产生大量 CRLF 警告；健康检查和 pytest 不受影响。

### N03. Golden snapshot 测试

优先级：P1

负责人：调试专家

范围：`tests/snapshots/`, `tests/test_snapshots.py`, `boot/load_memory.py`。

问题：上下文拼接顺序是核心功能，现在只有行为测试，没有固定输出快照。未来改 `memory_map.json` 或 loader 时，可能无意改变上下文结构。

交付物：

- 核心记忆 snapshot。
- `LabSOPGuard` 标准加载 snapshot。
- `LabSOPGuard --full` snapshot。
- `LabSOPGuard --history architecture` snapshot。
- 一个明确的 snapshot 更新命令。

验收标准：加载顺序、标题格式、来源路径格式发生变化时测试失败；snapshot 不包含密钥或机器绝对临时路径。

### N04. Role/Skill frontmatter schema

优先级：P1

负责人：知识库/Skill 体系设计师

范围：`schemas/`, `boot/check_memory_consistency.py`, `roles/*.md`, `skills/*.md`。

问题：当前只有 `memory_map` 和 `routing_map` schema；role/skill 仍靠健康检查里简单字段判断，无法校验数组类型、slug 格式、role-skill 引用关系。

交付物：

- `schemas/role_frontmatter.schema.json`
- `schemas/skill_frontmatter.schema.json`
- 健康检查按 schema 校验 role/skill frontmatter。

验收标准：缺少 `slug/triggers/skills/default_files` 或字段类型错误时，健康检查能准确指出文件和字段。

### N05. Hook 日志与可观测性

优先级：P1

负责人：后端/自动化工程师

范围：`boot/hooks/session_start.py`, `boot/hooks/session_end.py`, `boot/hooks/manual_save.py`，新增 `boot/hook_logging.py` 或本地日志目录。

问题：hook 需要保护主流程，所以很多异常仍会静默处理。现在虽然安全，但排障成本高。

交付物：

- 统一 hook 日志函数。
- 按天滚动写入本地日志，例如 `%USERPROFILE%/.kealan_memory/logs/`。
- 记录项目检测、加载文件数、Qwen 摘要是否成功、写回文件、Git 同步是否跳过/提交/失败。

验收标准：hook 失败不打断 Claude；日志不记录完整密钥或完整对话敏感内容；Web `/api/health` 或健康检查能提示最近 hook 错误摘要。

### N06. KealanMemory 自身项目记忆拆分

优先级：P2

负责人：知识库/Skill 体系设计师

范围：新增 `projects/KealanMemory/`，更新 `boot/memory_map.json`，清理 `projects/LabSOPGuard/current_status.md`。

问题：KealanMemory 自身优化和 LabSOPGuard 业务进展容易混在一起，导致加载项目记忆时上下文边界不清。

交付物：

- `projects/KealanMemory/project_brief.md`
- `projects/KealanMemory/current_status.md`
- `projects/KealanMemory/constraints.md`
- `projects/KealanMemory/next_actions.md`
- `projects/KealanMemory/decisions.md`
- `projects/KealanMemory/milestones.md`

验收标准：`python boot/project_manager.py validate` 通过；`python boot/load_memory.py --project KealanMemory --full` 可正常输出；LabSOPGuard 只保留业务系统进展。

### N07. 文档由配置生成

优先级：P2

负责人：系统架构师 + 知识库/Skill 体系设计师

范围：新增 `boot/render_docs.py`，更新 `boot/AI_ONBOARDING.md`, `boot/startup_prompt.md`, `install/CLAUDE.md`, `install/claude_commands/`。

问题：多个文档仍手写 `D:\KealanMemory`、核心加载文件和项目加载规则，未来容易与 `memory_map.json` 和 `routing_map.json` 漂移。

交付物：

- 文档模板目录，例如 `boot/doc_templates/`。
- `boot/render_docs.py` 从 `memory_map.json`、`routing_map.json` 渲染 onboarding、startup prompt、Claude commands。
- 文档生成后自动跑健康检查。

验收标准：核心加载文件只改 `memory_map.json` 即可同步到文档；生成后的文档无旧路径、无漏项。

### N08. Web 编辑与 diff 预览

优先级：P2

负责人：前端体验工程师 + 后端工程师

范围：`web/app.py`, `web/static/js/app.js`, `web/static/css/app.css`, `web/templates/index.html`。

问题：Web 目前已经能查看 memory、routing、history、health，但日常维护仍要手动编辑 Markdown。

交付物：

- 只允许编辑白名单文件：`context/active_focus.md`、项目 `current_status.md`、项目 `next_actions.md`。
- 保存前展示 diff。
- 保存后自动触发健康检查。
- 失败时不覆盖原文件。

验收标准：非法路径返回 400；保存前能看到 diff；写入后健康检查通过；移动端仍可操作。

### N09. 历史索引自动维护

优先级：P2

负责人：系统架构师

范围：`context/history_index.md`, `context/history/`, `boot/history_search.py`, 可选新增 `boot/history_manager.py`。

问题：历史文件能搜索，但索引仍靠手工维护。长期会出现历史文件存在但未索引、索引指向不存在文件的情况。

交付物：

- `history_manager.py add <file>` 自动追加索引。
- `history_manager.py validate` 检查索引断链、未索引历史文件、重复标题。
- 健康检查接入历史索引校验。

验收标准：新增历史文件后能一条命令注册；索引断链时健康检查失败。

### N10. CLI 产品化

优先级：P3

负责人：系统架构师

范围：新增 `pyproject.toml`，可选新增 `kealan_memory/` 包目录。

问题：当前功能分散在多个脚本中，长期使用需要记住 `boot/load_memory.py`、`boot/project_manager.py`、`boot/history_search.py` 等路径。

交付物：提供统一命令 `kealan-memory`。

建议子命令：

- `kealan-memory load`
- `kealan-memory check`
- `kealan-memory web`
- `kealan-memory project create/list/archive/validate`
- `kealan-memory history search/show`
- `kealan-memory routing list`

验收标准：安装后可在任意目录运行；旧脚本仍兼容；README 以统一 CLI 为主。

### N11. 高价值 skill 升级为标准 Codex skill 目录

优先级：P3

负责人：Skill 体系设计师

范围：新建 `skills_codex/` 或迁移部分 `skills/*.md` 到标准目录结构。

问题：当前 `skills/*.md` 是项目内轻量命令卡，不是完整 Codex skill 目录。对于高频复杂任务，可以进一步升级为带脚本和 references 的标准 skill。

建议优先升级：

- `memory-update`
- `new-project`
- `api-debug`
- `fe-debug`
- `pipeline-run`
- `weekly`

验收标准：每个标准 skill 有 `SKILL.md`，必要时带 `scripts/` 或 `references/`；内容遵循 `skill-creator` 的精简、渐进披露原则。

### N12. 安装流程沙盒测试

优先级：P3

负责人：后端/自动化工程师

范围：`install/setup.py`, `tests/`, 可选新增 `tests/fixtures/fake_home/`。

问题：安装脚本会写入用户目录下的 Claude/Continue/Cline/Copilot 配置。虽然已备份，但还缺少针对“假 HOME”的自动测试。

交付物：安装脚本支持传入 `--home` 或环境变量 `KEALAN_MEMORY_TEST_HOME`，测试在临时目录中运行。

验收标准：测试不会改真实用户目录；能验证备份、hook 渲染、命令复制、重复安装幂等。

### N13. Web 体验继续增强

优先级：P3

负责人：前端体验工程师

范围：`web/static/`, `web/templates/index.html`。

问题：Web 已具备基础 Ops 面板，但还可以更像真正的本地控制台。

交付物：

- 全局搜索高亮。
- Routing 详情按 role/skill 反向跳转。
- 健康检查结果缓存与刷新时间。
- 键盘快捷键，例如 `/` 聚焦搜索、`Esc` 关闭面板。
- 空状态和错误态进一步统一。

验收标准：现有功能不回退；`node --check` 和 Web smoke 通过；移动端布局不溢出。

## 3. 建议执行顺序

第一轮：N01, N02。先把当前大改动整理成可发布状态，并消除行尾/生成物噪音。

第二轮：N03, N04, N05。增强回归测试、schema 和 hook 可观测性。

第三轮：N06, N07, N08, N09。补齐记忆系统自身项目、文档生成、Web 编辑和历史索引。

第四轮：N10, N11, N12, N13。做 CLI 产品化、标准 skill 包、安装沙盒测试和 Web 体验增强。

## 4. 下一阶段 Definition of Done

| 维度 | 标准 |
|---|---|
| 发布 | 当前大改动按主题可 review、可回滚；无 CRLF 噪音 |
| 测试 | pytest 覆盖 snapshot、schema、Web API、项目 CLI、历史检索 |
| 可观测 | hook 有脱敏日志；Web/健康检查能提示最近 hook 失败 |
| 可维护 | 文档由配置生成；历史索引和项目生命周期自动校验 |
| 可用性 | Web 可安全编辑核心记忆文件并展示 diff |
| 产品化 | 提供统一 `kealan-memory` CLI，旧脚本保持兼容 |

