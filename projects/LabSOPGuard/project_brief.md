# LabSOPGuard — 项目简介

## 基本信息

- **项目路径**：`D:/LabEmbodiedVLA/LabSOPGuard/`
- **项目类型**：工程产品 + 研究基础设施
- **核心目标**：实验室操作视频的自动分析、SOP 合规检测、素材生成与证据链构建

## 核心链路

```
视频上传
  → Qwen VLM 帧分析（语义理解）
  → YOLO26s 检测帧流（目标检测）
    → 多目标跟踪（ByteTrack）
    → 五类物理事件检测（EventProposalBuilder）
    → clip + keyframe 生成（KeyMaterialExtractor）
    → 步骤匹配与合规评分（StepBridgeEngine）
      → 素材命名增强（Qwen VLM display_name）
      → 素材索引写入（SQLite）
→ 前端展示（时间轴 / 步骤视图 / 素材搜索）
```

## 五类核心事件

| 事件类型 | 触发条件 |
|---------|---------|
| `hand_object_interaction` | gloved_hand IoU/距离满足接触阈值 |
| `object_move` | 接触 + 物体中心位移 > 阈值 |
| `liquid_transfer` | 手 + 容器 + 倾倒姿态 |
| `panel_operation` | 手接近 balance/panel |
| `container_state_change` | lid IoU 变化（开盖/关盖） |

## 技术栈

| 层次 | 技术 |
|------|------|
| 检测模型 | YOLO26s（当前 `yolo26s_autodl_8_1_1`） |
| VLM | Qwen-VL / DashScope（唯一，禁止替换） |
| 后端 | FastAPI + Python，PYTHONPATH=src |
| 前端 | Vite + Vue |
| 数据库 | SQLite + 向量检索 |
| 任务队列 | Redis |

## 关键配置文件

| 文件 | 作用 |
|------|------|
| `configs/model/detection_runtime.yaml` | YOLO 权重唯一入口 |
| `.env` | DASHSCOPE_API_KEY 等 secrets |
| `data/dataset/dataset.yaml` | 数据集类别定义 |

## 13 检测类别

`balance` / `beaker` / `gloved_hand` / `lab_coat` / `paper` / `reagent_bottle` / `sample_bottle` / `sample_bottle_blue` / `spatula` / `tube`* / `tube-cap`* / `spearhead`* / `pipette`*

（*标注尚未同步到本地，数据在 Roboflow 云端）

## 启动命令

```powershell
cd D:/LabEmbodiedVLA/LabSOPGuard
.\scripts\start_full_stack.ps1 -Restart -SkipRedis
```
