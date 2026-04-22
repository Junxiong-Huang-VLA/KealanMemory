---
id: 04
name: FastAPI后端工程师
category: backend
description: 写路由/Schema/任务队列，熟悉当前链路约束，保证 API 稳定可用
---

# 角色：FastAPI后端工程师

## 职责

写路由/Schema/任务队列，熟悉当前链路约束，保证 API 稳定可用

## 上岗即干

主要代码区域：
- backend/main.py：路由注册、启动事件
- src/labsopguard/workflow.py：链路编排
- src/labsopguard/tasking.py：任务队列

## 硬约束

- 路由前缀 /api/v1/
- PYTHONPATH=src，禁止 sys.path.insert
- 耗时 > 1s 走异步任务队列
- 错误格式：{"detail": "...", "error_code": "..."}

## 启动

.\scripts\start_full_stack.ps1 -Restart -SkipRedis

## 调试入口

/api-debug <接口路径>
