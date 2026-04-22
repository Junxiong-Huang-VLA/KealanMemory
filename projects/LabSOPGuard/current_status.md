# LabSOPGuard — 当前状态

**评级：B** — 本地可用，内部 Demo 就绪（2026-04-22）

## 已完成

- YOLO26s 训练（AutoDL RTX 5090，100 epochs，mAP50=0.977）
- 完整处理链路打通（YOLO → 事件 → clip → 步骤推理）
- 前端工作区（时间轴、视频播放、素材搜索）
- Qwen VLM 语义命名集成
- 孤立任务自动恢复机制
- 旧实验补发 clip 接口（/materials/publish）
- steps.json 无 required_event_types 时自动注入
- 跨项目本地记忆系统（D:/KealanMemory/）
- playbook 角色文档（12个）+ skills（7个）
- 记忆系统全自动 hooks（SessionStart/SessionEnd）
- 通用 AI 接入协议（boot/AI_ONBOARDING.md）
- 前端崩溃修复（evidence_refs 空值保护 + ErrorBoundary）
- 关键素材标注升级（PIL 渲染 + 手物交互连线）
- KealanMemory Web 界面（http://localhost:7777）
- 20个通用 Skills + 14个角色文档
- 开工/收工全局协议

## 待完成（按优先级）

| 优先级 | 任务 | 备注 |
|--------|------|------|
| P0 | 重启后端验证关键素材标注效果 | 代码已就绪，publish 后查看 |
| P0 | 补充 tube/tube-cap/spearhead/pipette 标注 | 数据在 Roboflow，未同步本地 |
| P0 | step_bridge 置信度提升（目标 >= 0.5，当前 ~0.18） | 需要真实视频 |
| P1 | goggles 检测类 | 当前依赖 Qwen 语义 |
| P1 | lab_coat mAP50 0.940 -> >= 0.96 | 补充困难样本 |
| P2 | Docker 生产部署 | |
| P3 | 多摄像头同步 | |

## 当前最佳权重

outputs/training/yolo26s_autodl_8_1_1/weights/best.pt
mAP50=0.977 / mAP50-95=0.925（测试集）

## 最近一次更新

- **时间**：2026-04-22 晚
- **做了什么**：
  - 前端崩溃修复（evidence_refs 空值保护 + ErrorBoundary）
  - 关键素材标注重构（track缓存bbox → 实时YOLO逐帧检测 + PIL高质量渲染）
  - 事件类别过滤（clip/keyframe 只显示事件相关类别）
  - 交互触发检测框（手碰到物体才亮框，手离开框消失）
  - clip生成优化（先ffmpeg裁短片段再逐帧标注，避免在大视频上跑推理）
