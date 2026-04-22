---
id: api-debug
name: /api-debug
category: 后端开发
description: 接口报错定位：读日志 → 复现请求 → 根因分析 → 修复方案
---

# /api-debug — 接口报错定位：读日志 → 复现请求 → 根因分析 → 修复方案

## 执行步骤

1. tail -50 backend_start.err.log
2. curl -v http://127.0.0.1:8000/api/v1/<path>
3. 422=Schema不匹配 / 500=后端异常 / CORS=端口白名单 / YOLO失败=检查yaml
