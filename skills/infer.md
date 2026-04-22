---
id: infer
name: /infer
category: 检测与训练
description: 在视频或图片上跑推理，输出可视化检测结果和标注视频
---

# /infer — 在视频或图片上跑推理，输出可视化检测结果和标注视频

## 执行步骤

1. 读当前权重路径
2. 图片推理：yolo predict model=<path> source=<路径> conf=0.25 save=True project=outputs/inference
3. 视频推理：同上 source=<视频>
4. 展示推理速度、各类检测数量
5. 输出结果路径
