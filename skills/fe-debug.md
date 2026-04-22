---
id: fe-debug
name: /fe-debug
category: 前端开发
description: 前端白屏/渲染异常调试：定位空值、URL 问题、跨域错误
---

# /fe-debug — 前端白屏/渲染异常调试：定位空值、URL 问题、跨域错误

## 执行步骤

白屏=Console 找 undefined / 视频不播放=resolveArtifactUrl / CORS=更新 .env / evidence_refs 报错=加 ?? []
顺序：Console → Network → URL 检查 → CORS 白名单
