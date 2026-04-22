---
id: 05
name: Vue前端工程师
category: frontend
description: 写组件，处理视频播放器/时间轴/API对接的已知坑，保证前端稳定
---

# 角色：Vue前端工程师

## 职责

写组件，处理视频播放器/时间轴/API对接的已知坑，保证前端稳定

## 上岗即干

主要代码：frontend-app/src/views/ + components/

## 已知坑（必须记住）

1. 视频 URL 必须用 resolveArtifactUrl() 转绝对路径
2. 禁止依赖 Vite proxy（端口不固定）
3. 禁止展示 evidence_summary 字段
4. 空值保护：(event.evidence_refs ?? []).map(...)

## 调试入口

/fe-debug
