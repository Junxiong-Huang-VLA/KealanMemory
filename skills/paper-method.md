---
id: paper-method
name: /paper-method
category: 科研与输出
description: 把系统架构翻译成论文方法章节，包括模块定义、输入输出、公式框架和图文说明。
triggers:
  - 方法章节
  - 论文方法
  - 系统架构
  - 公式
  - 模块描述
roles:
  - paper-engineer
  - vla-researcher
  - system-architect
default_files:
  - project_brief.md
  - src/labsopguard/
  - docs/
---

# /paper-method - 把系统架构翻译成论文方法章节，包括模块定义、输入输出、公式框架和图文说明。

## 适用场景

- 需要写 LabSOPGuard 方法章节。
- 需要把工程模块转成学术表达。

## 输入

- 模块名称
- 目标会议/格式
- 已有结构或代码路径

## 输出

- 章节大纲
- 模块描述
- 公式占位
- 图注文字

## 执行流程

1. 读取项目简介和相关模块。
2. 按 Overview、Perception、Event Detection、Step Reasoning 组织。
3. 每个模块写输入、输出、核心操作和与 baseline 差异。
4. 保持学术风格，不写口语化实现细节。

## 失败处理

- 没有实验支撑时不夸大效果。
- 代码实现不明时标注待确认而不是编造。

## 关联角色

- paper-engineer
- vla-researcher
- system-architect

## 默认文件

- project_brief.md
- src/labsopguard/
- docs/
