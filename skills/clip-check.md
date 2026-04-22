---
id: clip-check
name: /clip-check
category: 事件与链路
description: 诊断 clip 生成问题：目录结构、ffmpeg 可用性、重建索引
---

# /clip-check — 诊断 clip 生成问题：目录结构、ffmpeg 可用性、重建索引

## 执行步骤

1. ls outputs/experiments/<id>/materials/
2. python -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())'
3. 若 events/ 为空：触发 publish 重跑
4. python tools/rebuild_material_indexes.py
