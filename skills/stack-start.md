---
id: stack-start
name: /stack-start
category: 环境与工程
description: 一键启动全栈：Redis + FastAPI + Vite，含健康检查和故障速查
---

# /stack-start — 一键启动全栈：Redis + FastAPI + Vite，含健康检查和故障速查

## 执行步骤

.\scripts\start_full_stack.ps1 -Restart -SkipRedis
健康检查：curl http://127.0.0.1:8000/api/v1/diagnostics 确认 yolo26_status.available=true
端口：FastAPI=8000 / Vite=5173 / Redis=6379
