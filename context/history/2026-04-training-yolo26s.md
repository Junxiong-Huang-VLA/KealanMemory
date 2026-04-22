# YOLO26s 训练记录（2026-04）

## 训练概况

- **Run name**：`yolo26s_autodl_8_1_1`
- **平台**：AutoDL RTX 5090 32GB
- **参数**：epochs=100, imgsz=640, batch=16
- **数据集**：13 类，train/val/test = 8:1:1

## 结果

| 指标 | 验证集 | 测试集 |
|------|--------|--------|
| Precision | 0.958 | 0.961 |
| Recall | 0.945 | 0.950 |
| mAP50 | 0.978 | 0.977 |
| mAP50-95 | 0.921 | 0.925 |

## 各类 mAP50（测试集）

| 类别 | mAP50 |
|------|-------|
| sample_bottle / spatula / sample_bottle_blue | 0.995 |
| reagent_bottle | 0.991 |
| balance | 0.988 |
| paper | 0.968 |
| beaker / gloved_hand | 0.959 |
| lab_coat | 0.940（最弱） |
| tube/tube-cap/spearhead/pipette | 无标注，无法评估 |

## 关键发现

- tube/tube-cap/spearhead/pipette 四类在本地数据集中**无标注**
- 标注数据在 Roboflow 云端，未同步到本地 `D:/LabEmbodiedVLA/LabSOPGuard/data/dataset/`
- AutoDL 上的完整训练产物（results.csv、混淆矩阵等）也未下载到本地（仅有 best.pt）

## 下一步

从 Roboflow 导出四类标注 → 合并数据集 → AutoDL 重训
