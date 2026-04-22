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
- 前端崩溃修复（evidence_refs 空值保护 + ErrorBoundary）
- 关键素材标注升级（PIL 渲染 + 手物交互连线）
- 从 D:/cvdemo 合并标注数据（639张，补全 tube/tube-cap/spearhead/pipette/beaker 五类）
- 迁入 RealSense 采集+自动标注+可视化等 8 个工具脚本

## 待完成（按优先级）

| 优先级 | 任务 | 备注 |
|--------|------|------|
| P0 | 重启后端验证关键素材标注效果 | 代码已就绪，publish 后查看 |
| P0 | AutoDL 重训 YOLO（13 类全有标注） | cvdemo 数据已合并，需要重训 |
| P0 | step_bridge 置信度提升（目标 >= 0.5，当前 ~0.18） | 需要真实视频 |
| P1 | goggles 检测类 | 当前依赖 Qwen 语义 |
| P1 | lab_coat mAP50 0.940 -> >= 0.96 | 补充困难样本 |
| P2 | Docker 生产部署 | |
| P3 | 多摄像头同步 | |

## 当前最佳权重

outputs/training/yolo26s_autodl_8_1_1/weights/best.pt
mAP50=0.977 / mAP50-95=0.925（测试集）

## 最近一次更新

- **时间**：2026-04-22
- **做了什么**：
  - 从 D:/cvdemo 合并 639 张标注图片，补全 tube/tube-cap/spearhead/pipette/beaker 五类
  - 迁入 8 个工具脚本（RealSense 采集/实时检测/自动标注/数据合并等）
