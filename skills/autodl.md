---
id: autodl
name: /autodl
category: 环境与工程
description: 执行 AutoDL 数据上传、远端训练、产物下载、权重同步和常见故障处理。
triggers:
  - AutoDL
  - 远端训练
  - scp
  - 5090
  - 显存
  - 训练产物
roles:
  - autodl-devops
  - yolo-trainer
default_files:
  - data/dataset/
  - outputs/training/
  - configs/model/detection_runtime.yaml
---

# /autodl - 执行 AutoDL 数据上传、远端训练、产物下载、权重同步和常见故障处理。

## 适用场景

- 本地显存不足，需要在 AutoDL 训练。
- 需要同步训练产物回本地并切权重。

## 输入

- 远端 IP
- 数据集目录
- run_name
- 训练命令

## 输出

- tar/scp 命令
- 远端训练命令
- 下载命令
- 权重同步步骤

## 执行流程

1. 打包并上传 data/dataset。
2. 在远端确认 CUDA/PyTorch 环境。
3. 执行训练命令。
4. 关机前下载 outputs/training/<run>/。
5. 本地运行 /val 后再切换权重。

## 失败处理

- OOM 时降低 batch 或 imgsz。
- 中断时检查 last.pt 续训。
- 下载失败时禁止删除远端产物。

## 关联角色

- autodl-devops
- yolo-trainer

## 默认文件

- data/dataset/
- outputs/training/
- configs/model/detection_runtime.yaml
