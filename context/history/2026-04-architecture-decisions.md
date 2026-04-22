# 架构决策记录（2026-04）

## 主题：LabSOPGuard 核心架构定型

### 决策1：权重路径唯一入口

- **问题**：权重路径散落在多处，切换时容易遗漏
- **方案**：所有路径读取统一走 `configs/model/detection_runtime.yaml` → `model` 字段
- **解析顺序**：参数 > 环境变量 > yaml model > yaml fallbacks
- **效果**：切换权重只改 yaml，代码零修改

### 决策2：VLM 锁定 Qwen/DashScope

- **原因**：稳定接入、国内网络友好、多模态接口完善
- **约束**：禁止引入其他厂商 SDK，所有 VLM 调用走统一封装

### 决策3：lab_preprocessing 冻结

- **背景**：历史子项目，能力与 LabSOPGuard 重叠
- **结论**：功能全部迁入 `src/labsopguard/`，lab_preprocessing 仅保留历史代码，不新增

### 决策4：steps 自动注入机制

- **问题**：早期 steps.json 缺 required_event_types 导致步骤推理跳过
- **方案**：`_enrich_steps_for_bridge` 自动注入 `_SOP_DEFAULT_STEPS` 六个默认步骤
- **效果**：不再阻断链路，保证端到端可跑通
