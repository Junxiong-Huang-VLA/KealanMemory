# 当前焦点（Active Focus）

> 每次阶段切换时更新此文件。Claude 加载后优先关注这里。

## 当前阶段（2026-04-22）

**主线任务**：LabSOPGuard 检测能力补全 → 升级到 A 级

## 本周最重要的 3 件事

1. **Roboflow 数据导出**：tube/tube-cap/spearhead/pipette 四类标注同步到本地
2. **重训 YOLO**：合并新数据后在 AutoDL 重训，目标全类 mAP50 ≥ 0.98
3. **step_bridge 评估**：用真实实验视频跑一次完整链路，记录步骤推理置信度

## 当前卡点

- tube/pipette 四类标注在 Roboflow 云端，尚未下载到本地
- step_bridge 置信度 ~0.18，需要更多真实操作视频才能提升

## 并行关注

- VLA 方向：暂缓，等 LabSOPGuard 达到 A 级后启动
- 论文：暂缓，等系统稳定后整理实验结果

## 上次工作摘要（2026-04-22）

**项目**：LabSOPGuard + KealanMemory

- cvdemo 数据合并完成（639张，13 类全部有标注）
- 8 个工具脚本迁入 LabSOPGuard/tools/
- 新电脑安装包 + GitHub 自动同步
- 下一步：AutoDL 重训 YOLO
