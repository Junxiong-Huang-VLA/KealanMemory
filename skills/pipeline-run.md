---
id: pipeline-run
name: /pipeline-run
category: 事件与链路
description: 检查后端健康状态，触发实验处理链路并验证关键输出文件完整性。
triggers:
  - 跑链路
  - process experiment
  - diagnostics
  - pipeline
  - 全流程
roles:
  - video-event-engineer
  - fastapi-backend-engineer
  - system-architect
  - step-bridge-engineer
default_files:
  - backend/main.py
  - outputs/experiments/<id>/
---

# /pipeline-run - 检查后端健康状态，触发实验处理链路并验证关键输出文件完整性。

## 适用场景

- 需要从 API 触发一次完整实验处理。
- 需要验证后端、事件、材料和分析产物是否齐全。

## 输入

- experiment_id
- 后端地址

## 输出

- curl 命令
- 健康检查结果
- 产物完整性清单

## 执行流程

1. 请求 /api/v1/diagnostics。
2. POST /api/v1/experiments/<id>/process。
3. 必要时 POST /materials/publish。
4. 验证 physical_events.json、material_stream.json、analysis/annotated.mp4。

## 失败处理

- 后端不可达时转入 /stack-start。
- API 500 时转入 /api-debug。
- 材料缺失时转入 /clip-check。

## 关联角色

- video-event-engineer
- fastapi-backend-engineer
- system-architect
- step-bridge-engineer

## 默认文件

- backend/main.py
- outputs/experiments/<id>/
