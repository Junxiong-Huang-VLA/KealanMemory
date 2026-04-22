---
id: pipeline-run
name: /pipeline-run
category: 事件与链路
description: 检查后端健康 → 触发实验处理链路 → 验证输出文件完整性
---

# /pipeline-run — 检查后端健康 → 触发实验处理链路 → 验证输出文件完整性

## 执行步骤

1. curl http://127.0.0.1:8000/api/v1/diagnostics
2. curl -X POST http://127.0.0.1:8000/api/v1/experiments/<id>/process
3. 补发 clip：curl -X POST .../materials/publish
4. 验证：physical_events.json / material_stream.json / analysis/annotated.mp4
