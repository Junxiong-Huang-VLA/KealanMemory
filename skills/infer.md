---
id: infer
name: /infer
category: 检测与训练
description: 在图片或视频上运行 YOLO 推理，输出可视化检测结果、速度和类别统计。
triggers:
  - 推理
  - 预测
  - 图片检测
  - 视频检测
  - annotated video
roles:
  - yolo-trainer
default_files:
  - configs/model/detection_runtime.yaml
  - outputs/inference/
---

# /infer - 在图片或视频上运行 YOLO 推理，输出可视化检测结果、速度和类别统计。

## 适用场景

- 用户要快速验证当前权重在图片或视频上的表现。
- 需要生成标注视频、检测截图或推理速度摘要。

## 输入

- source 图片/视频路径
- 可选 conf、imgsz、model override

## 输出

- 推理命令
- 输出目录
- 类别检测数量与速度摘要

## 执行流程

1. 读取 configs/model/detection_runtime.yaml 获取默认权重。
2. 按输入类型生成 yolo predict 命令。
3. 输出保存到 outputs/inference/<run_name>/。
4. 汇总速度、类别数量和可视化文件路径。

## 失败处理

- 权重不存在时先转入 /val 或提示修正 detection_runtime.yaml。
- source 不存在时停止执行并返回缺失路径。

## 关联角色

- yolo-trainer

## 默认文件

- configs/model/detection_runtime.yaml
- outputs/inference/
