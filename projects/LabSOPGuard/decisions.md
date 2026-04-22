# LabSOPGuard — 关键决策记录

---
**决策**：唯一 API 提供商锁定为 Qwen / DashScope
**时间**：2026-04 前
**背景**：需要选定一个多模态 VLM 提供商用于帧分析和语义命名
**结论**：使用 DashScope，文本走 OpenAI 兼容接口，多模态走 dashscope SDK
**后续影响**：禁止引入其他厂商 SDK，所有 VLM 调用走统一入口

---
**决策**：YOLO 权重路径统一走 detection_runtime.yaml，禁止硬编码
**时间**：2026-04 前
**背景**：早期开发中权重路径散落在多个 Python 文件，切换困难
**结论**：唯一配置入口 `configs/model/detection_runtime.yaml` → `model` 字段
**后续影响**：切换权重只改 yaml，代码不动，有 fallback 链

---
**决策**：lab_preprocessing 能力迁入 LabSOPGuard，不再新增功能
**时间**：2026-04
**背景**：lab_preprocessing 是早期独立子项目，功能与 LabSOPGuard 重叠
**结论**：全部能力迁入 `src/labsopguard/`，lab_preprocessing 冻结
**后续影响**：禁止从 LabSOPGuard import lab_preprocessing，禁止在其中新增功能

---
**决策**：steps.json 无 required_event_types 时自动注入 SOP 默认步骤
**时间**：2026-04
**背景**：早期 steps.json 缺少 required_event_types 会导致 step_bridge 跳过
**结论**：_enrich_steps_for_bridge 自动注入 _SOP_DEFAULT_STEPS，不阻断链路
**后续影响**：不再需要手动为每个实验配置 required_event_types

---
**决策**：AutoDL RTX 5090 作为训练平台，本地 RTX 4050 只做推理
**时间**：2026-04
**背景**：本地 6GB VRAM 不足以跑大 batch 训练
**结论**：所有正式训练在 AutoDL，训练产物下载回本地
**后续影响**：训练产物（results.csv/混淆矩阵等）需要手动从 AutoDL 同步
