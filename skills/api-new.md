---
id: api-new
name: /api-new
category: 后端开发
description: 生成符合项目约束的 FastAPI 路由、Pydantic Schema 和异步任务接入方案。
triggers:
  - 新接口
  - 新增 API
  - FastAPI 路由
  - Pydantic
  - 任务队列
roles:
  - fastapi-backend-engineer
  - system-architect
default_files:
  - backend/main.py
  - src/labsopguard/tasking.py
  - src/labsopguard/workflow.py
---

# /api-new - 生成符合项目约束的 FastAPI 路由、Pydantic Schema 和异步任务接入方案。

## 适用场景

- 新增实验、材料、诊断或任务类 API。
- 需要把耗时流程接入异步队列。

## 输入

- 接口路径
- 请求/响应字段
- 同步或异步需求

## 输出

- 路由草案
- Schema 草案
- 任务队列接入点
- 错误格式

## 执行流程

1. 确认路径统一在 /api/v1/ 下。
2. 定义 Request/Response Schema。
3. 超过 1 秒的处理封装为任务。
4. 保持错误结构 {detail, error_code}。

## 失败处理

- 需求字段不明确时先输出 schema 问题清单。
- 涉及架构边界时转入 system-architect。

## 关联角色

- fastapi-backend-engineer
- system-architect

## 默认文件

- backend/main.py
- src/labsopguard/tasking.py
- src/labsopguard/workflow.py
