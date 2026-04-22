---
id: paper-exp
name: /paper-exp
category: 科研与输出
description: 基于评测指标生成论文实验章节，覆盖数据集、对比、消融、结果表和定性分析。
triggers:
  - 实验章节
  - 消融
  - 对比实验
  - LaTeX 表格
  - 结果分析
roles:
  - paper-engineer
  - experiment-recorder
  - ppt-coach
default_files:
  - docs/training_report.md
  - outputs/val/
  - outputs/training/
---

# /paper-exp - 基于评测指标生成论文实验章节，覆盖数据集、对比、消融、结果表和定性分析。

## 适用场景

- 需要把训练/验证结果写成论文实验。
- 需要生成 LaTeX 指标表或消融表。

## 输入

- 指标文件
- baseline 列表
- 消融设置

## 输出

- 实验章节草稿
- LaTeX 表格
- 结果解读
- 局限性

## 执行流程

1. 读取 mAP50、mAP50-95、P、R 和 per-class AP。
2. 生成数据集、实现细节、对比、消融和定性分析结构。
3. 输出 LaTeX 表格并标注数据来源。
4. 明确弱类和失败案例。

## 失败处理

- 缺少 baseline 时只写当前模型结果，不伪造对比。
- 指标来源不明时要求先运行 /val。

## 关联角色

- paper-engineer
- experiment-recorder
- ppt-coach

## 默认文件

- docs/training_report.md
- outputs/val/
- outputs/training/
