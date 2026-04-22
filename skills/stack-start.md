---
id: stack-start
name: /stack-start
category: 环境与工程
description: 启动或检查 Redis、FastAPI、Vite 全栈服务，并执行健康检查和端口故障速查。
triggers:
  - 启动全栈
  - FastAPI 启动
  - Vite
  - Redis
  - diagnostics
  - 端口
roles:
  - autodl-devops
  - fastapi-backend-engineer
  - vue-frontend-engineer
  - debug-expert
  - system-architect
default_files:
  - scripts/start_full_stack.ps1
  - backend_start.err.log
  - frontend-app/
---

# /stack-start - 启动或检查 Redis、FastAPI、Vite 全栈服务，并执行健康检查和端口故障速查。

## 适用场景

- 本地开发前启动完整系统。
- 后端或前端不可达时做基础健康检查。

## 输入

- 是否 Restart
- 是否 SkipRedis

## 输出

- 启动命令
- 端口清单
- diagnostics 检查结果

## 执行流程

1. 运行 .\scripts\start_full_stack.ps1 -Restart -SkipRedis。
2. 检查 FastAPI=8000、Vite=5173、Redis=6379。
3. curl /api/v1/diagnostics。
4. 根据日志判断端口占用或依赖不可用。

## 失败处理

- 后端启动失败转入 /api-debug。
- 前端白屏转入 /fe-debug。
- Redis 不需要时允许 SkipRedis。

## 关联角色

- autodl-devops
- fastapi-backend-engineer
- vue-frontend-engineer
- debug-expert
- system-architect

## 默认文件

- scripts/start_full_stack.ps1
- backend_start.err.log
- frontend-app/
