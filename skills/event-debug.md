---
id: event-debug
name: /event-debug
category: 事件与链路
description: 检查视频到事件、clip、步骤推理的全链路，定位断点并给出最小修复方案。
triggers:
  - 事件调试
  - 漏检
  - physical_events
  - steps_bridge_result
  - materials publish
roles:
  - video-event-engineer
  - step-bridge-engineer
  - debug-expert
  - vla-researcher
default_files:
  - outputs/experiments/<id>/
  - src/labsopguard/event_preprocessing/
---

# /event-debug - 检查视频到事件、clip、步骤推理的全链路，定位断点并给出最小修复方案。

## 适用场景

- 实验处理后没有事件、没有 clip 或步骤结果异常。
- 需要解释 needs_review 或低置信度。

## 输入

- experiment_id
- 可选事件类型或视频路径

## 输出

- 链路状态表
- 断点位置
- 修复或重跑命令

## 执行流程

1. 检查 outputs/experiments/<id>/ 是否完整。
2. 确认视频文件、physical_events.json、material_stream.json、steps_bridge_result.json。
3. 统计事件类型分布。
4. 触发或检查 materials publish。
5. 把问题归因到检测、事件、clip、step bridge 或 API 层。

## 失败处理

- 实验目录不存在时转入 /pipeline-run 重新处理。
- 事件为空时先确认检测输出和视频输入，不直接改 step bridge。

## 关联角色

- video-event-engineer
- step-bridge-engineer
- debug-expert
- vla-researcher

## 默认文件

- outputs/experiments/<id>/
- src/labsopguard/event_preprocessing/
