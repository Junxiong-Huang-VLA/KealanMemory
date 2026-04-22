---
id: hardcase
name: /hardcase
category: 检测与训练
description: 找误检/漏检帧，导出困难样本，生成 Roboflow 上传包
---

# /hardcase — 找误检/漏检帧，导出困难样本，生成 Roboflow 上传包

## 执行步骤

1. python tools/analyze_detection_errors.py --model <path> --data data/dataset/dataset.yaml --conf 0.1
2. python tools/build_ppe_hardcase_pack.py --output outputs/hardcases/upload_pack/
3. 上传 Roboflow 重新标注
重点：lab_coat(0.940) / beaker(0.959) / gloved_hand(0.959)
