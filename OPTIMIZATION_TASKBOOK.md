# KealanMemory 全方位优化任务书

生成日期：2026-04-22

目标：把 `D:\KealanMemory` 从“可用的个人记忆中台”升级为“安全、可迁移、可验证、可路由、可长期维护的 AI 记忆操作系统”。

本任务书已按多角色并行审查结果整理，覆盖系统架构、后端自动化、Web 前端、知识库/Skill 体系、安全与发布流程。技能体系优化部分采用系统 `skill-creator` 原则：触发条件明确、输入输出明确、资源按需加载、验收标准可测试。

## 0. 当前结论

当前项目整体分层清楚：`profile` 保存个人画像，`operating_rules` 保存通用规则，`context` 保存当前上下文，`projects` 保存项目记忆，`roles` 保存执行角色，`skills` 保存任务命令，`boot` 保存加载与 hook 脚本，`web` 提供本地管理界面。

主要问题集中在六类：安全配置暴露、路径硬编码与历史路径漂移、加载规则多处重复、hook 自动同步风险、Web API/前端可靠性不足、role 与 skill 缺少显式路由关系。

## 1. 多线程开发总计划

并行原则：P0 安全任务必须先处理；P1 架构与自动化可并行；P2 Web 与知识库标准化可并行；P3 体验增强、CI 和文档收尾。

建议角色池：

| 角色 | 负责方向 | 主要目录 | 调用 skill |
|---|---|---|---|
| 系统架构师 | 加载协议、路径配置、项目索引、历史检索 | `boot/`, `context/`, `projects/` | `skill-creator`, `/memory-update`, `/new-project` |
| 后端/自动化工程师 | Python hooks、CLI、安装脚本、依赖、健康检查 | `boot/`, `install/`, `web/app.py` | `/api-debug`, `/api-new`, `/env-new` |
| 安全/DevOps 工程师 | 密钥治理、git 同步策略、发布前检查 | `install/`, `.gitignore`, `boot/hooks/` | `/env-new`, `/stack-start` |
| 前端体验工程师 | Web UI、响应式、可访问性、错误态 | `web/templates/`, `web/static/` | `/fe-component`, `/fe-debug` |
| 知识库/Skill 体系设计师 | role-skill 路由、模板、去重、项目边界 | `roles/`, `skills/`, `boot/skills/`, `projects/` | `skill-creator`, `/weekly`, `/new-project` |
| 调试专家 | 交叉验证、回归测试、健康检查输出 | 全仓库 | `/api-debug`, `/fe-debug`, `/pipeline-run` |

## 2. 批次安排

| 批次 | 可并行任务 | 阻塞关系 | 目标 |
|---|---|---|---|
| P0 安全止血 | T01, T02 | 必须最先完成 | 移除泄露风险，避免继续污染 git 与用户环境 |
| P1 架构底座 | T03, T04, T05, T06, T07 | T03 是 T04/T05 的基础 | 统一加载、路径、依赖、健康检查 |
| P2 产品化 | T08, T09, T10, T11, T12, T13 | 可与 P1 后半并行 | Web、skill、role、项目记忆体系标准化 |
| P3 质量闭环 | T14, T15, T16, T17, T18 | 依赖 P1/P2 结果 | 测试、CI、文档、发布与日常维护 |

## 3. 任务清单

### T01. 移除密钥并建立安全配置模板

优先级：P0

负责人：安全/DevOps 工程师

调用 skill：`/env-new`

范围：`install/claude_settings.json`, `.gitignore`, `install/*.example.json`

问题：安装配置中出现明文认证 token，必须视为已经泄露；本文不复刻该值。

交付物：移除真实 token；新增 example 配置；新增本地私有配置加载方式；补充 `.gitignore` 防止私密配置入库。

验收标准：仓库全文扫描不再出现真实 token；安装脚本从环境变量或用户本地私有文件读取密钥；已轮换泄露 token；健康检查能阻止疑似密钥提交。

### T02. 降低 hook 自动同步风险

优先级：P0

负责人：安全/DevOps 工程师 + 后端/自动化工程师

调用 skill：`/api-debug`, `/env-new`

范围：`boot/hooks/session_end.py`, `boot/hooks/manual_save.py`

问题：hook 使用类似 `git add . && git commit && git push` 的无差别同步策略，可能提交密钥、临时文件和用户未准备提交的改动。

交付物：改为白名单提交；默认不 push；提供 `KEALAN_MEMORY_AUTO_PUSH=1` 开关；提交前运行敏感信息扫描；失败日志可见。

验收标准：默认不会执行无差别 `git add .`；只允许提交 `profile/`, `context/`, `projects/`, `roles/`, `skills/` 等明确文件；遇到密钥模式直接中止；hook 失败不影响用户主流程。

### T03. 统一根路径配置并消除历史路径漂移

优先级：P1

负责人：系统架构师 + 后端/自动化工程师

调用 skill：`/env-new`

范围：`boot/load_memory.py`, `boot/load_memory.ps1`, `boot/hooks/`, `web/app.py`, `install/setup.py`, `install/claude_settings.json`

问题：多处硬编码 `D:/KealanMemory`，安装配置仍残留旧路径 `D:/ClaudeMemory`。

交付物：统一 `KEALAN_MEMORY_ROOT` 环境变量；未设置时从脚本所在目录向上推导；安装模板使用占位符渲染。

验收标准：仓库非归档文件不再残留旧根路径；移动仓库到其他盘符后 CLI、Web、hooks 仍能运行；安装后的 hook 指向当前仓库真实路径。

### T04. 建立单一加载协议与共享 loader 模块

优先级：P1

负责人：系统架构师

调用 skill：`skill-creator`, `/memory-update`

范围：`boot/memory_map.json`, `boot/load_memory.py`, `boot/hooks/session_start.py`, `web/app.py`, `boot/load_order.md`, `boot/startup_prompt.md`, `boot/AI_ONBOARDING.md`

问题：CLI、SessionStart、Web、README、启动 prompt 都重复定义核心加载顺序，容易漂移。

交付物：新增共享 loader 模块；所有入口从 `memory_map.json` 派生加载顺序；文档由机器可读配置生成或引用配置。

验收标准：新增一个 `default_load` 文件后 CLI、SessionStart、Web 三条链路输出一致；`AI_ONBOARDING.md` 不漏读协作规则；`load_order.md` 与 `memory_map.json` 不冲突。

### T05. 修复 `--full` 深度加载语义

优先级：P1

负责人：系统架构师

调用 skill：`/memory-update`

范围：`boot/load_memory.py`, `boot/memory_map.json`, `boot/load_order.md`

问题：`memory_map.json` 包含项目级 optional 文件，但当前 `--full` 会过滤项目文件，导致 `decisions.md` 和 `milestones.md` 未加载。

交付物：明确 `--full` 语义；有项目时加载通用 optional 和项目 optional；无项目时只加载通用 optional 并提示。

验收标准：`python boot/load_memory.py --project LabSOPGuard --full --print` 包含 `decisions.md` 和 `milestones.md`；无项目执行 `--full` 不出现 `{project}` 占位路径。

### T06. 修复 PowerShell/BAT 启动脚本

优先级：P1

负责人：后端/自动化工程师

调用 skill：`/env-new`, `/api-debug`

范围：`boot/load_memory.ps1`, `boot/start_memory.bat`, `install/setup.bat`

问题：`boot/load_memory.ps1` 当前存在 PowerShell 解析错误；BAT 参数未完整加引号，项目名含空格会失败。

交付物：修复 PowerShell 语法；统一 UTF-8 输出；BAT 参数加引号；补充脚本级 smoke test。

验收标准：PowerShell Parser 无错误；`.\boot\load_memory.ps1 -List`, `-Project LabSOPGuard`, `-Project LabSOPGuard -Full` 均正常；中文输出不乱码。

### T07. 建立健康检查与发布前检查

优先级：P1

负责人：调试专家 + 后端/自动化工程师

调用 skill：`/api-debug`, `/fe-debug`

范围：新增 `boot/check_memory_consistency.py` 或 `tools/health_check.py`

问题：当前没有一条命令能发现路径漂移、JSON 错误、PowerShell 语法错误、项目索引断链、role-skill 断链、密钥泄露。

交付物：只读健康检查脚本；输出可读报告；失败返回非零退出码；README 中记录验证命令。

验收标准：检查项覆盖 Python compile、PowerShell parse、JSON parse、敏感信息扫描、硬编码旧路径扫描、项目注册完整性、模板占位残留、frontmatter 校验、role-skill 映射断链。

### T08. 统一依赖与环境管理

优先级：P1

负责人：后端/自动化工程师

调用 skill：`/env-new`

范围：`web/requirements.txt`, 新增根级 `requirements.txt` 或 `pyproject.toml`, `install/setup.py`

问题：Web 依赖只声明 Flask，但 hooks 实际使用 OpenAI SDK；安装脚本直接全局 `pip install flask`。

交付物：统一依赖入口；区分 runtime、web、dev 可选依赖；安装脚本不污染全局 Python。

验收标准：新环境按文档安装后 Web、CLI、hooks 全部可运行；`openai` 等真实依赖有声明；版本约束合理；安装失败有明确提示。

### T09. 强化 Web API 输入校验与剪贴板安全

优先级：P2

负责人：后端/自动化工程师

调用 skill：`/api-new`, `/api-debug`

范围：`web/app.py`

问题：`project` 参数未校验；剪贴板写入通过拼接 PowerShell here-string，特殊内容可能破坏命令结构；存在未使用 import。

交付物：合法项目白名单；统一 JSON 错误；安全剪贴板实现；移除未使用 import。

验收标准：非法 project 返回 400 JSON；上下文包含特殊字符时复制不破坏命令；API 错误前端可展示；静态分析无未使用 import。

### T10. 重构 Web 前端资源结构

优先级：P2

负责人：前端体验工程师

调用 skill：`/fe-component`, `/fe-debug`

范围：`web/templates/index.html`, 新增 `web/static/css/`, `web/static/js/`

问题：当前一个模板承载 HTML、CSS、JS、Markdown 渲染和交互逻辑，维护成本高。

交付物：拆分 CSS/JS；移除内联 `onclick`；建立 CSS token；保留 Flask 模板的语义结构。

验收标准：模板文件明显变薄；交互由 JS 事件绑定实现；颜色、字号、间距、圆角使用 CSS 变量；四个 Tab 功能不回退。

### T11. 提升 Web 可访问性、响应式和错误态

优先级：P2

负责人：前端体验工程师

调用 skill：`/fe-component`, `/fe-debug`

范围：`web/templates/index.html`, `web/static/`

问题：导航与卡片用 `div onclick`，缺少键盘操作、ARIA、Escape 关闭、焦点管理；移动端固定布局易溢出；API 失败缺少明确错误态。

交付物：语义化按钮与导航；详情抽屉焦点管理；移动端断点；加载、空状态、错误、重试 UI。

验收标准：Tab/Enter/Space/Escape 可完成主要操作；375px、768px、1440px 无横向溢出；任一 API 失败不会让页面永久停在加载中；低对比文本通过基础可读性检查。

### T12. 建立任务路由表：意图 -> role -> skill -> 文件

优先级：P2

负责人：知识库/Skill 体系设计师

调用 skill：`skill-creator`, `/new-project`, `/weekly`

范围：新增 `boot/routing_map.md`, 可选 `boot/routing_map.json`, `roles/`, `skills/`

问题：用户说“训练”“前端白屏”“接口报错”“写论文”时，没有统一路由说明应该加载哪个 role、skill、项目文件和规则。

交付物：任务路由表；至少覆盖训练、评估、数据集、前端、后端、Qwen、事件链路、论文、PPT、周报、新项目、记忆更新。

验收标准：每类意图都有 role、skill、必读项目文件、必读规则、输出格式；路由中的 skill 均对应真实文件；Web 可读取或展示路由表。

### T13. 标准化 role 元数据

优先级：P2

负责人：知识库/Skill 体系设计师

调用 skill：`skill-creator`

范围：`roles/*.md`

问题：role 文件有 frontmatter，但缺少 `slug`, `triggers`, `skills`, `default_files` 等机器路由字段。

交付物：统一 role frontmatter；建立 role 与 skill 的显式映射；补充默认加载文件。

验收标准：每个 role 都包含 `id`, `slug`, `category`, `description`, `triggers`, `skills`, `default_files`；所有 `skills` 字段能解析到 `skills/*.md`；排序和检索稳定。

### T14. 标准化 skill 模板并同步生成器

优先级：P2

负责人：知识库/Skill 体系设计师

调用 skill：`skill-creator`

范围：`skills/*.md`, `boot/write_skills.py`, `boot/skills/*.md`

问题：当前 skill 多为简短命令说明，缺少输入、输出、失败处理和关联角色；`write_skills.py` 与实际 skill 数量不一致，重新运行可能覆盖新增 skill。

交付物：统一 skill 模板；补齐 20 个 skill 的结构；修复生成器与实际文件同步；必要时把高价值 skill 升级为标准 Codex skill 目录结构。

验收标准：每个 skill 包含适用场景、输入、执行步骤、输出、失败处理、关联角色；生成器运行不会丢失 `/train`、`/val` 等现有文件；健康检查能校验 frontmatter。

### T15. 清理项目记忆边界与模板语义

优先级：P2

负责人：知识库/Skill 体系设计师 + 系统架构师

调用 skill：`/new-project`, `/memory-update`

范围：`projects/LabSOPGuard/`, `projects/AluminumTubeInspection/`, `projects/_template/`, `boot/memory_map.json`

问题：LabSOPGuard 项目状态混入 KealanMemory 自身建设记录；`AluminumTubeInspection` 可能存在模板占位但已列为可用项目；`_template` 被放在 `projects` 数组中语义不清。

交付物：新增或补齐 `projects/KealanMemory`；拆分业务项目与记忆系统项目；清理占位项目；把 `_template` 移到独立 `templates` 字段。

验收标准：`--list` 只显示真实可加载项目；未初始化项目不会被误加载；LabSOPGuard 只保留业务系统进展；KealanMemory 自身优化记录有独立项目记忆。

### T16. 增加历史上下文检索入口

优先级：P3

负责人：系统架构师

调用 skill：`/memory-update`

范围：`context/history_index.md`, `context/history/`, `boot/load_memory.py`, `web/app.py`

问题：历史上下文默认不加载是对的，但目前只有索引，没有 CLI/Web 的受控检索入口。

交付物：CLI 参数 `--history <keyword-or-file>`；Web 历史检索 API；加载结果带来源路径。

验收标准：按关键词能列出匹配历史；指定文件能注入上下文；默认加载仍不包含历史全文；不存在的关键词有清晰提示。

### T17. 建立测试与 golden snapshot

优先级：P3

负责人：调试专家

调用 skill：`/api-debug`, `/fe-debug`

范围：新增 `tests/`, `boot/`, `web/`

问题：加载结果、Web API、项目索引没有自动回归测试，后续重构容易破坏行为。

交付物：Python 单元测试；CLI golden snapshot；Web API 测试；前端基础 smoke test。

验收标准：`pytest` 可验证核心 loader、项目加载、`--full`、非法 project、frontmatter 解析；snapshot 变更必须人工确认；测试不依赖真实密钥。

### T18. 更新 README、安装说明与日常工作流

优先级：P3

负责人：实验记录员 + 知识库/Skill 体系设计师

调用 skill：`/weekly`, `/memory-update`

范围：`README.md`, `install/README.md`, `boot/AI_ONBOARDING.md`, `boot/startup_prompt.md`

问题：文档与实际机制存在重复和漂移；安装、验证、故障处理、日常维护流程不够闭环。

交付物：重写快速开始；新增安装后验证；新增健康检查命令；新增故障速查；说明多 AI 接入方式。

验收标准：新机器按 README 能完成安装、启动 Web、加载项目、运行健康检查；文档不包含真实密钥；加载顺序引用单一配置源。

## 4. Definition of Done

全项目优化完成必须同时满足：

| 维度 | 完成标准 |
|---|---|
| 安全 | 无真实 token 入库；hook 不再无差别提交；敏感扫描进入健康检查 |
| 可迁移 | 根路径可配置；无非归档旧路径；换盘符后核心链路可跑 |
| 一致性 | CLI、hook、Web 使用同一加载协议；role-skill-project 路由可机器读取 |
| 可维护 | Web 拆分静态资源；依赖统一声明；安装脚本幂等且可回滚 |
| 可验证 | 一条健康检查命令覆盖语法、配置、路径、索引、密钥、映射；测试可重复 |
| 可用性 | Web 支持错误态、空状态、移动端、键盘操作；README 可带新人完成安装 |

## 5. 建议并行执行顺序

第一轮并行：T01 安全配置、T02 hook 同步风险、T03 路径统一。

第二轮并行：T04 共享 loader、T06 PowerShell/BAT 修复、T08 依赖管理、T09 Web API 校验。

第三轮并行：T10/T11 Web 前端体验、T12/T13/T14 role-skill 路由标准化、T15 项目边界清理。

第四轮收敛：T07 健康检查、T16 历史检索、T17 测试、T18 文档。

## 6. 立即开工建议

如果要马上进入开发，先开 3 条并行线程：

| 线程 | 任务 | 原因 |
|---|---|---|
| 安全线程 | T01 + T02 | 防止密钥和误提交继续扩散 |
| 架构线程 | T03 + T04 + T05 | 后续 Web、hook、CLI 都依赖统一 loader |
| 体验线程 | T09 + T10 + T11 | Web 当前是用户可见入口，收益明显且可独立推进 |

