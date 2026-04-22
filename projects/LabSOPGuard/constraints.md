# LabSOPGuard — 硬约束

## 唯一真实来源

| 配置项 | 唯一来源 | 当前值 |
|--------|---------|--------|
| YOLO 权重路径 | `configs/model/detection_runtime.yaml` → `model` 字段 | `outputs/training/yolo26s_autodl_8_1_1/weights/best.pt` |
| API 提供商 | DashScope / Qwen（唯一） | `DASHSCOPE_API_KEY` in `.env` |
| 环境变量 | `D:/LabEmbodiedVLA/LabSOPGuard/.env` | — |

## 禁止事项

- 禁止硬编码权重路径（只改 yaml）
- 禁止引入 `anthropic` / `openai`（非兼容模式）/ `cohere` 等其他厂商 SDK
- 禁止在 `lab_preprocessing/` 新增功能（历史遗留，能力已迁入 LabSOPGuard）
- 禁止从 `LabSOPGuard` 代码 import `lab_preprocessing` 包
- 禁止在 `backend/main.py` 中 `sys.path.insert`
- 禁止 `display_name` 使用 `evidence_summary` 字段（含调试信息）
- 禁止在前端直接硬编码 `http://127.0.0.1:8000`（用 `resolveArtifactUrl()`）

## 事件类型约束

- 只有五类事件：`hand_object_interaction` / `object_move` / `liquid_transfer` / `panel_operation` / `container_state_change`
- 新增事件必须同时更新：`semantic_events.py` + `_SOP_DEFAULT_STEPS` + `protocol_graph.py`

## 测试约束

每次 commit 前必须通过：
```bash
pytest -q tests/test_model_data_enhancements.py tests/test_material_production_features.py
```
