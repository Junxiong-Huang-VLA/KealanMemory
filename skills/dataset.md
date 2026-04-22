---
id: dataset
name: /dataset
category: 检测与训练
description: 统计 YOLO 数据集类别分布、合并 Roboflow 导出、重划分并检查标注质量。
triggers:
  - 数据集
  - Roboflow
  - 类别统计
  - 标注质量
  - 划分
  - YOLO txt
roles:
  - dataset-engineer
  - yolo-trainer
  - vla-researcher
default_files:
  - data/dataset/
  - data/dataset/dataset.yaml
---

# /dataset - 统计 YOLO 数据集类别分布、合并 Roboflow 导出、重划分并检查标注质量。

## 适用场景

- 新增 Roboflow zip 后合并到本地。
- 训练前检查类别不均衡或坏标签。

## 输入

- Roboflow zip 路径
- 目标 dataset 目录
- 划分比例

## 输出

- 类别分布表
- 合并/划分命令
- 标注质量问题清单

## 执行流程

1. 统计 train/val/test label 中的类别分布。
2. 解压 Roboflow zip 并检查 images/labels 对齐。
3. 按固定 seed 重划分数据集。
4. 检查空标签、异常 bbox、类别缺失和弱类。

## 失败处理

- 图片和标签数量不一致时停止合并并列出缺失对。
- 类别 id 超出 dataset.yaml 时阻止训练。

## 关联角色

- dataset-engineer
- yolo-trainer
- vla-researcher

## 默认文件

- data/dataset/
- data/dataset/dataset.yaml
