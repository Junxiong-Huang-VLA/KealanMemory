---
id: event-debug
name: /event-debug
category: 事件与链路
description: 检查视频→事件→clip→步骤全链路，定位断点，给出修复方案
---

# /event-debug — 检查视频→事件→clip→步骤全链路，定位断点，给出修复方案

## 执行步骤

1. ls outputs/experiments/<id>/
2. 统计事件类型：Counter(e['event_type'] for e in events)
3. 确认视频文件存在
4. 读 steps_bridge_result.json 看置信度
5. curl -X POST http://127.0.0.1:8000/api/v1/experiments/<id>/materials/publish
