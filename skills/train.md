---
id: train
name: /train
category: 检测与训练
description: 执行 YOLO 训练准备、命令生成、AutoDL 指引、产物检查和权重切换建议。
triggers:
  - 训练
  - YOLO train
  - epoch
  - batch
  - 学习率
  - 新权重
roles:
  - yolo-trainer
  - autodl-devops
  - dataset-engineer
  - experiment-recorder
default_files:
  - configs/model/detection_runtime.yaml
  - data/dataset/dataset.yaml
  - outputs/training/
---

# /train - 执行 YOLO 训练准备、命令生成、AutoDL 指引、产物检查和权重切换建议。

## 适用场景

- 需要启动一次新的检测模型训练。
- 需要根据数据规模和显存生成训练参数。

## 输入

- 模型规模
- epoch/batch/imgsz
- run_name
- 是否使用 AutoDL

## 输出

- 训练命令
- AutoDL 上传/下载步骤
- 产物检查清单
- 权重切换建议

## 执行流程

1. 检查 dataset.yaml 和类别分布。
2. 报告样本不足或弱类风险。
3. 生成 yolo detect train 命令。
4. 如使用 AutoDL，补充打包、上传、训练、下载命令。
5. 训练完成后要求保留 best.pt、last.pt、results.csv 和混淆矩阵。
6. 切换权重前触发 /val。

## 失败处理

- CUDA OOM 时优先降低 batch 或 imgsz。
- 数据集路径缺失时转入 /dataset。
- 训练中断时检查 last.pt 并给出续训命令。

## 关联角色

- yolo-trainer
- autodl-devops
- dataset-engineer
- experiment-recorder

## 默认文件

- configs/model/detection_runtime.yaml
- data/dataset/dataset.yaml
- outputs/training/
