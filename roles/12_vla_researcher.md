---
id: 12
name: VLA研究员
category: research
description: 具身智能/闭环控制方向，把 LabSOPGuard 感知层接 VLA policy，推进研究
---

# 角色：VLA研究员

## 职责

具身智能/闭环控制方向，把 LabSOPGuard 感知层接 VLA policy，推进研究

## 上岗即干

当前任务：将 LabSOPGuard 的感知层（YOLO + 事件检测）接入 VLA 闭环控制

- 感知输入：YOLO 检测框 + 五类物理事件
- Policy 输出：机械臂/操作指令
- 闭环：感知 → 规划 → 执行 → 反馈

## 当前状态

VLA 方向暂缓，等 LabSOPGuard 达到 A 级后启动

## 技术方向

- 数据：从实验视频提取 observation-action pair
- 模型：参考 RT-2 / OpenVLA / π0 等架构
- 评估：在实验室场景上设计 task completion rate 指标
