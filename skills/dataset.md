---
id: dataset
name: /dataset
category: 检测与训练
description: 统计类别分布、合并 Roboflow 数据、重新划分、检查标注质量
---

# /dataset — 统计类别分布、合并 Roboflow 数据、重新划分、检查标注质量

## 执行步骤

统计：cat data/dataset/labels/train/*.txt | awk '{print $1}' | sort -n | uniq -c | sort -rn
合并：解压 Roboflow zip → 复制 images/labels → python tools/data_split.py --ratio 0.8 0.1 0.1 --seed 42
检查：bbox 面积异常、类别分布不均、tube/pipette 当前 0 条需要补充
