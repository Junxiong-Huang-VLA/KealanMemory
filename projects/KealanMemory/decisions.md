# KealanMemory - 决策记录

## D01. KealanMemory 作为独立项目记忆注册

- **日期**：2026-04-22
- **决策**：新增 `projects/KealanMemory/` 并注册到 `boot/memory_map.json`。
- **原因**：本仓库自身优化计划不应继续混入 LabSOPGuard 等业务项目记忆。
- **影响**：后续加载 `--project KealanMemory --full` 时，可直接获得本仓库优化、Web、hooks、skills、roles、测试和计划上下文。

## D02. 不在本次任务中修改 LabSOPGuard

- **日期**：2026-04-22
- **决策**：只读检查 LabSOPGuard，发现 KealanMemory 内容混入时报告，不直接清理。
- **原因**：用户明确限定不要修改 LabSOPGuard，除非只是只读检查后报告明显问题。
- **影响**：LabSOPGuard 的项目记忆边界问题保留为后续可选清理任务。

## D03. `memory_map.json` 保持为加载协议入口

- **日期**：2026-04-22
- **决策**：项目注册通过 `boot/memory_map.json.projects` 完成。
- **原因**：CLI、Web、hooks 和文档应围绕单一加载配置派生，降低漂移风险。
- **影响**：新增项目必须同时具备目录文件和 map 注册，否则校验应失败或告警。

## D04. full load 包含项目决策和里程碑

- **日期**：2026-04-22
- **决策**：KealanMemory 的 `decisions.md` 与 `milestones.md` 放入项目目录，依赖 `optional_load` 在 `--full` 模式加载。
- **原因**：日常加载保持简洁，深度交接时才注入决策背景和阶段记录。
- **影响**：验证必须覆盖 `--project KealanMemory --full`。

## D05. 后续优化按主题拆分

- **日期**：2026-04-22
- **决策**：后续提交按安全与安装、loader 与脚本、Web、role/skill、测试与 schema、项目 CLI 与历史、文档与任务书拆分。
- **原因**：当前工作树跨度大，一次性提交会提高 review、回滚和回归定位成本。
- **影响**：每组提交前应独立运行健康检查和相关测试。
