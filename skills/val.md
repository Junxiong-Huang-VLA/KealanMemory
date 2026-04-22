---
id: val
name: /val
category: 检测与训练
description: 对当前或指定权重做测试集评估，产出 mAP/P/R、混淆矩阵和弱类分析。
triggers:
  - 验证
  - 评估
  - mAP
  - confusion_matrix
  - 测试集
  - val
roles:
  - yolo-trainer
  - dataset-engineer
  - experiment-recorder
default_files:
  - configs/model/detection_runtime.yaml
  - data/dataset/dataset.yaml
  - outputs/val/
---

# /val - 对当前或指定权重做测试集评估，产出 mAP/P/R、混淆矩阵和弱类分析。

## 适用场景

- 切换权重前验证质量。
- 论文或报告需要检测指标。

## 输入

- model 路径
- split
- run_name

## 输出

- yolo val 命令
- 指标表
- 混淆矩阵和曲线路径
- 强弱类别结论

## 执行流程

1. 读取当前权重路径。
2. 生成 yolo val 命令并使用 split=test。
3. 检查 confusion_matrix、PR/F1 曲线和 per-class 指标。
4. 标注强类、弱类和下一步补样方向。

## 失败处理

- 权重不可读时停止切换并回退到上一个 best.pt。
- 测试集为空时转入 /dataset 修复划分。

## 关联角色

- yolo-trainer
- dataset-engineer
- experiment-recorder

## 默认文件

- configs/model/detection_runtime.yaml
- data/dataset/dataset.yaml
- outputs/val/
