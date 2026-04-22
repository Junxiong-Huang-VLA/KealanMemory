---
id: val
name: /val
category: 检测与训练
description: 测试集完整评估：各类 mAP/P/R + 混淆矩阵 + 最佳检测样图
---

# /val — 模型评估

## 执行步骤

1. 读取当前权重路径（configs/model/detection_runtime.yaml → model 字段）
2. 跑测试集验证并生成统计图：
   ```bash
   yolo val model=<path> data=data/dataset/dataset.yaml \
     imgsz=640 split=test save=True plots=True \
     project=outputs/val name=<run_name>_test
   ```
3. 生成各类最佳检测样图：python tools/export_best_per_class.py
4. 依次展示：confusion_matrix_normalized.png / BoxPR_curve.png / BoxF1_curve.png / 各类样图
5. 输出各类 P/R/mAP50/mAP50-95 汇总表，标注强/弱类别
