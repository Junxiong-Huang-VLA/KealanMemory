---
id: weekly
name: /weekly
category: 科研与输出
description: 读取记忆系统当前状态和历史，生成结构化周报、完成项、问题和下周计划。
triggers:
  - 周报
  - 本周完成
  - 下周计划
  - 进展总结
  - 日报
roles:
  - experiment-recorder
  - paper-engineer
  - ppt-coach
default_files:
  - context/active_focus.md
  - context/current_status.md
  - context/next_actions.md
  - context/history/
---

# /weekly - 读取记忆系统当前状态和历史，生成结构化周报、完成项、问题和下周计划。

## 适用场景

- 需要整理本周项目进展。
- 需要把实验和开发结果转成汇报材料。

## 输入

- 时间范围
- 目标格式
- 可选重点项目

## 输出

- 完成项
- 问题风险
- 下周计划
- 需要支持

## 执行流程

1. 读取 active_focus、current_status、next_actions。
2. 必要时补充 history 中本周记录。
3. 按完成、问题、计划、支持需求输出。
4. 保留关键产物路径和指标。

## 失败处理

- 状态文件缺失时基于可读 history 输出并标注缺口。
- 没有新进展时输出风险和建议动作，不编造完成项。

## 关联角色

- experiment-recorder
- paper-engineer
- ppt-coach

## 默认文件

- context/active_focus.md
- context/current_status.md
- context/next_actions.md
- context/history/
