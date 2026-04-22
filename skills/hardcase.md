---
id: hardcase
name: /hardcase
category: 检测与训练
description: 挖掘误检/漏检帧，导出困难样本包并推动 Roboflow 复标回流。
triggers:
  - 困难样本
  - 误检
  - 漏检
  - hardcase
  - 复标
  - 弱类
roles:
  - dataset-engineer
  - yolo-trainer
default_files:
  - outputs/hardcases/
  - data/dataset/
  - outputs/training/
---

# /hardcase - 挖掘误检/漏检帧，导出困难样本包并推动 Roboflow 复标回流。

## 适用场景

- 某些类别 AP 低，需要针对性补样。
- 需要把错误样本打包上传 Roboflow。

## 输入

- model 路径
- dataset.yaml
- conf 阈值
- 输出目录

## 输出

- 困难样本包路径
- 错误类型摘要
- 复标建议

## 执行流程

1. 运行检测错误分析脚本。
2. 构建 upload_pack。
3. 按类别和错误类型汇总优先级。
4. 提示上传 Roboflow 复标并回流 /dataset。

## 失败处理

- 分析脚本不存在时给出手动抽样方案。
- 输出包为空时降低 conf 或扩大样本来源。

## 关联角色

- dataset-engineer
- yolo-trainer

## 默认文件

- outputs/hardcases/
- data/dataset/
- outputs/training/
