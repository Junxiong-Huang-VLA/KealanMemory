---
id: ppt-outline
name: /ppt-outline
category: 科研与输出
description: 生成答辩或汇报 PPT 大纲，包含页面标题、支撑点、演讲逻辑和评委问题。
triggers:
  - PPT
  - 答辩大纲
  - 汇报
  - 开题
  - 演讲稿
  - 评委问题
roles:
  - ppt-coach
default_files:
  - project_brief.md
  - docs/training_report.md
---

# /ppt-outline - 生成答辩或汇报 PPT 大纲，包含页面标题、支撑点、演讲逻辑和评委问题。

## 适用场景

- 毕业设计、开题、中期或项目汇报需要结构。
- 需要把技术工作压缩成可讲故事线。

## 输入

- 汇报类型
- 时长
- 受众
- 主题

## 输出

- 每页标题
- 三点支撑
- 转场话术
- 预判问题

## 执行流程

1. 确认汇报类型、时长和受众。
2. 按背景、问题、方法、实验、总结组织。
3. 每页标题写结论句。
4. 补充评委可能追问和回答要点。

## 失败处理

- 目标受众不明时先给通用科研答辩结构。
- 实验结果不足时把风险写入备答问题。

## 关联角色

- ppt-coach

## 默认文件

- project_brief.md
- docs/training_report.md
