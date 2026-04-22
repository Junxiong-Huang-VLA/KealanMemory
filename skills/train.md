---
id: train
name: /train
category: 检测与训练
description: YOLO 模型完整训练流程：数据检查 → 训练命令生成 → AutoDL 指引 → 权重切换
---

# /train — YOLO 训练助手

## 执行步骤

1. 读取 `configs/model/detection_runtime.yaml` 确认当前权重和数据集路径
2. 统计各类标注数量，报告样本不足（< 100）的类别
3. 根据用户指定（epoch/batch/模型大小）生成完整训练命令：
   ```bash
   yolo detect train model=yolo26s.pt data=data/dataset/dataset.yaml \
     epochs=100 imgsz=640 batch=16 device=0 \
     name=yolo26s_<run_name> project=outputs/training
   ```
4. 若需要 AutoDL：给出数据打包 + 上传 + 下载产物的完整命令
5. 训练完成后自动更新 `configs/model/detection_runtime.yaml` 的 `model` 字段
6. 触发 `/val` 验证新权重效果
