# LabSOPGuard — 下一步行动

## 立即要做（更新于 2026-04-22）

1. AutoDL 重训 YOLO（13 类全有标注，目标 mAP50 >= 0.95）
2. 重启后端验证关键素材标注效果（publish 后查看）
3. D:/cvdemo 确认无遗漏后归档到 KealanMemory/archive/

## 本周要做

- [ ] Roboflow 数据导出并本地合并
- [ ] 新权重训练（AutoDL）
- [ ] 新权重评估（`/val-per-class`）
- [ ] 切换权重（更新 detection_runtime.yaml）

## 下个里程碑（升级到 A 级）

- [ ] tube/tube-cap/spearhead/pipette 四类 mAP50 ≥ 0.95
- [ ] 全类 mAP50 ≥ 0.98
- [ ] step_bridge compliant 步骤 ≥ 70%（需真实实验视频）
- [ ] 后端可用性 7 天连续 ≥ 99.9%

## 阻塞项

| 阻塞事项 | 等待什么 |
|---------|---------|
| tube/pipette 标注数据 | 从 Roboflow 云端导出 |
| step_bridge 置信度提升 | 更多真实实验视频 |
