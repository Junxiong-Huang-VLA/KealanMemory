---
id: fe-component
name: /fe-component
category: 前端开发
description: 生成符合项目规范的 Vue 组件代码，含 API 对接和 URL 处理
---

# /fe-component — 生成符合项目规范的 Vue 组件代码，含 API 对接和 URL 处理

## 执行步骤

关键约束：视频 URL 用 resolveArtifactUrl()，API 地址 http://127.0.0.1:8000，只显示 display_name
resolveArtifactUrl(url) { return url.startsWith('http') ? url : 'http://127.0.0.1:8000' + url }
