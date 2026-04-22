# LabSOPGuard — 关键决策记录

---
**决策**：从 D:/cvdemo 合并标注数据，补全 tube/tube-cap/spearhead/pipette/beaker 五类
**时间**：2026-04-22
**背景**：LabSOPGuard 数据集 13 类中有 4 类标注为 0（tube/tube-cap/spearhead/pipette），beaker 标注也偏少
**来源**：D:/cvdemo/lab_detection/data/unified_dataset（Roboflow kealans-workspace/my-first-project-bhkt7/v7）
**映射**：cvdemo 0→9(tube), 1→10(tube-cap), 2→1(beaker), 3→11(spearhead), 4→12(pipette)
**合并量**：639 张图片，新增 tube=1165, tube-cap=1156, spearhead=2764, pipette=3134, beaker+=703
**工具**：tools/merge_cvdemo_data.py（可重复运行，自动跳过已存在文件）
**后续**：需要 AutoDL 重训 YOLO，目标全 13 类 mAP50 >= 0.95

---
**决策**：唯一 API 提供商锁定为 Qwen / DashScope
**时间**：2026-04 前
**背景**：需要选定一个多模态 VLM 提供商用于帧分析和语义命名
**结论**：使用 DashScope，文本走 OpenAI 兼容接口，多模态走 dashscope SDK
**后续影响**：禁止引入其他厂商 SDK，所有 VLM 调用走统一入口

---
**决策**：YOLO 权重路径统一走 detection_runtime.yaml，禁止硬编码
**时间**：2026-04 前
**结论**：唯一配置入口 configs/model/detection_runtime.yaml → model 字段
**后续影响**：切换权重只改 yaml，代码不动，有 fallback 链

---
**决策**：lab_preprocessing 能力迁入 LabSOPGuard，不再新增功能
**时间**：2026-04
**结论**：全部能力迁入 src/labsopguard/，lab_preprocessing 冻结

---
**决策**：cvdemo 工具脚本迁入 LabSOPGuard/tools/
**时间**：2026-04-22
**背景**：cvdemo 有 RealSense 采集、自动标注、数据合并等工具，LabSOPGuard 缺这些能力
**迁入**：realsense_capture / realsense_detect / realtime_detect / auto_label / merge_external_dataset / simple_annotator / visualize_labels / video_infer
**原则**：cvdemo 不再新增功能，后续工具开发在 LabSOPGuard/tools/ 下
