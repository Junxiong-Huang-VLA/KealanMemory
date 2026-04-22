# 处理链路集成记录（2026-04）

## 主题：LabSOPGuard 端到端链路打通

## 链路现状

完整链路已验证可跑通（基准实验 c404e890）：
- YOLO26 检测 + 多目标跟踪 ✅
- 五类事件检测 ✅
- clip + keyframe 生成 ✅
- 步骤推理（StepBridgeEngine）✅（置信度偏低 ~0.18，属正常，需真实视频）
- Qwen 语义命名 ✅
- 前端展示 ✅

## 踩坑记录

### 视频播放器 URL 问题
- 问题：`<video src>` 用相对路径无法播放
- 原因：Vite proxy 在不同端口（5173/5174）下不可靠
- 解决：用 `resolveArtifactUrl()` 转换为 `http://127.0.0.1:8000` 开头的绝对 URL

### steps.json 缺字段导致步骤推理跳过
- 问题：旧实验 steps.json 没有 `required_event_types`，step_bridge 直接跳过
- 解决：`_enrich_steps_for_bridge` 自动注入 6 个默认步骤

### orphaned tasks 启动挂起
- 问题：上次异常退出后，`running` 状态任务残留，下次启动前端显示一直在跑
- 解决：`_recover_orphaned_tasks()` 在后端启动时自动将残留任务标记为 `failed`

### display_name 含调试信息
- 问题：`evidence_summary` 字段含 `grade=/score=` 等调试文字被误用于显示名称
- 解决：`display_name` 优先级：`event.display_name` > Qwen live > rule_based，禁用 evidence_summary
