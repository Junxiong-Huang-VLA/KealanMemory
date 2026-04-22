---
id: fe-debug
name: /fe-debug
category: 前端开发
description: 调试前端白屏、渲染异常、URL、CORS 和空值访问问题。
triggers:
  - 白屏
  - 前端报错
  - undefined
  - CORS
  - 视频不播放
  - Network
roles:
  - vue-frontend-engineer
  - debug-expert
default_files:
  - frontend-app/src/
  - .env
---

# /fe-debug - 调试前端白屏、渲染异常、URL、CORS 和空值访问问题。

## 适用场景

- 页面白屏或控制台报错。
- 视频、材料、接口请求在前端不可用。

## 输入

- 控制台错误
- Network 请求
- 页面路径

## 输出

- 错误层级判断
- 修复点
- 验证步骤

## 执行流程

1. 先看 Console 的 undefined、TypeError 或 CORS。
2. 再看 Network 请求 URL 和响应。
3. 检查 resolveArtifactUrl 与空值保护。
4. 修复后刷新并复测关键页面。

## 失败处理

- API 不通时转入 /api-debug 或 /stack-start。
- 字段缺失时先修前端兼容，不立即要求后端改 schema。

## 关联角色

- vue-frontend-engineer
- debug-expert

## 默认文件

- frontend-app/src/
- .env
