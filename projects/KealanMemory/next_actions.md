# KealanMemory - 下一步行动

## 立即要做

1. 运行 `python boot/project_manager.py validate`，确认 `projects/KealanMemory` 已注册且必需文件齐全。
2. 运行 `python boot/load_memory.py --project KealanMemory --full --output $env:TEMP\kealan_memory_project.txt`，确认完整项目记忆可加载。
3. 报告 LabSOPGuard 只读检查中发现的 KealanMemory 内容混入情况，不在本次任务中修改。

## 本周要做

- [ ] 将当前未提交大改动按主题拆分为可审查的提交组。
- [ ] 增加 golden snapshot 测试，覆盖核心记忆、KealanMemory 标准加载、KealanMemory full 加载和历史注入。
- [ ] 为 role/skill frontmatter 增加 schema，并接入健康检查。
- [ ] 给 hooks 增加脱敏日志，记录加载、保存、跳过、提交和失败摘要。
- [ ] 设计 Web 编辑白名单、diff 预览和保存后健康检查流程。

## 下个里程碑前要做

- [ ] 让 README、startup prompt、AI onboarding 等文档由配置生成或显式引用 `memory_map.json`。
- [ ] 建立历史索引自动维护命令，检查断链、未索引历史和重复标题。
- [ ] 提供统一 CLI，例如 `kealan-memory load/check/web/project/history/routing`。
- [ ] 选择高价值 skill 升级为标准 Codex skill 目录结构，优先考虑 `memory-update`、`new-project`、`api-debug`、`fe-debug`、`pipeline-run`、`weekly`。
- [ ] 为安装流程增加 fake home 沙箱测试，避免测试写入真实用户目录。

## 阻塞项

| 阻塞事项 | 等待什么 | 预计解除方式 |
|---|---|---|
| 当前工作树修改范围很大 | 决定提交分组和发布说明格式 | 按主题分批 review |
| LabSOPGuard 混入 KealanMemory 条目 | 用户确认是否允许清理 LabSOPGuard 项目记忆 | 另起任务修改 |
| Web 编辑能力风险较高 | 白名单、diff 和健康检查方案确定 | 先实现只读预览，再开放写入 |
