---
id: api-debug
name: /api-debug
category: 后端开发
description: 定位接口报错，读取日志、复现请求、区分 422/500/CORS/业务链路错误。
triggers:
  - 接口报错
  - 422
  - 500
  - CORS
  - backend_start.err.log
  - API debug
roles:
  - fastapi-backend-engineer
  - qwen-vlm-engineer
  - debug-expert
default_files:
  - backend_start.err.log
  - backend/main.py
  - .env
---

# /api-debug - 定位接口报错，读取日志、复现请求、区分 422/500/CORS/业务链路错误。

## 适用场景

- 接口返回 422、500 或前端调用失败。
- Qwen 或 YOLO 后端依赖导致 API 异常。

## 输入

- 接口路径
- 请求体
- 错误响应
- 日志片段

## 输出

- 复现 curl
- 根因分类
- 最小修复建议

## 执行流程

1. 读取 backend_start.err.log 最近错误。
2. 用 curl -v 复现请求。
3. 按 422、500、CORS、依赖不可用分类。
4. 定位到 schema、路由、任务队列或模型依赖。

## 失败处理

- 日志不足时要求补充完整响应和请求体。
- 后端未启动时转入 /stack-start。

## 关联角色

- fastapi-backend-engineer
- qwen-vlm-engineer
- debug-expert

## 默认文件

- backend_start.err.log
- backend/main.py
- .env
