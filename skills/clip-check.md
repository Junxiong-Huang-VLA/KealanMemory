---
id: clip-check
name: /clip-check
category: 事件与链路
description: 诊断 clip 或 materials 生成问题，检查目录结构、ffmpeg 可用性和材料索引。
triggers:
  - clip
  - materials
  - ffmpeg
  - 素材
  - 索引
  - 视频片段
roles:
  - video-event-engineer
  - step-bridge-engineer
  - debug-expert
default_files:
  - outputs/experiments/<id>/materials/
  - tools/rebuild_material_indexes.py
---

# /clip-check - 诊断 clip 或 materials 生成问题，检查目录结构、ffmpeg 可用性和材料索引。

## 适用场景

- 事件存在但前端没有素材。
- annotated clip 或 material index 缺失。

## 输入

- experiment_id
- materials 目录

## 输出

- 缺失文件清单
- ffmpeg 检查结果
- 重建索引命令

## 执行流程

1. 列出 materials 目录结构。
2. 检查 imageio_ffmpeg 可用性。
3. 确认 events/、clips/、index 文件是否存在。
4. 必要时调用 publish 或 rebuild_material_indexes.py。

## 失败处理

- ffmpeg 不可用时先修环境。
- events 为空时返回 /event-debug。

## 关联角色

- video-event-engineer
- step-bridge-engineer
- debug-expert

## 默认文件

- outputs/experiments/<id>/materials/
- tools/rebuild_material_indexes.py
