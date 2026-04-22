from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("D:/KealanMemory")
ROLES_DIR = ROOT / "roles"
SKILLS_DIR = ROOT / "skills"
BOOT_DIR = ROOT / "boot"


ROLES = [
    {
        "id": "01",
        "slug": "yolo-trainer",
        "name": "YOLO 训练专家",
        "category": "detection",
        "description": "分析 YOLO 训练、验证、推理和困难样本闭环，管理权重切换与模型质量。",
        "triggers": ["训练", "YOLO", "权重", "mAP", "过拟合", "欠拟合", "推理", "验证"],
        "skills": ["train", "val", "infer", "hardcase", "autodl"],
        "default_files": [
            "configs/model/detection_runtime.yaml",
            "data/dataset/dataset.yaml",
            "outputs/training/",
            "outputs/val/",
        ],
        "guardrails": [
            "切换权重前必须先运行验证流程。",
            "只改 detection_runtime.yaml 的 model 字段，不顺手重构业务代码。",
            "训练结论必须引用 results.csv、混淆矩阵或验证指标。",
        ],
    },
    {
        "id": "02",
        "slug": "video-event-engineer",
        "name": "视频事件检测工程师",
        "category": "pipeline",
        "description": "维护视频到事件、clip、材料索引的链路，定位事件漏检、误检和发布断点。",
        "triggers": ["事件", "clip", "materials", "视频处理", "physical_events", "material_stream"],
        "skills": ["event-debug", "pipeline-run", "clip-check"],
        "default_files": [
            "src/labsopguard/event_preprocessing/",
            "outputs/experiments/<id>/physical_events.json",
            "outputs/experiments/<id>/materials/",
        ],
        "guardrails": [
            "先确认视频文件和实验目录存在，再判断算法问题。",
            "事件类型或字段变化必须同步检查下游 step bridge 和前端消费。",
        ],
    },
    {
        "id": "03",
        "slug": "step-bridge-engineer",
        "name": "步骤推理工程师",
        "category": "pipeline",
        "description": "维护 StepBridgeEngine、SOP 图和步骤匹配输出，解释合规判断低置信度原因。",
        "triggers": ["步骤", "SOP", "StepBridge", "合规", "needs_review", "protocol_graph"],
        "skills": ["event-debug", "pipeline-run", "clip-check"],
        "default_files": [
            "src/labsopguard/step_bridge/",
            "outputs/experiments/<id>/steps_bridge_result.json",
        ],
        "guardrails": [
            "StepBridge 内禁止直接调用 Qwen API。",
            "grade 只能是 compliant、needs_review、non_compliant。",
            "新增事件类型必须同步协议图和 schema。",
        ],
    },
    {
        "id": "04",
        "slug": "fastapi-backend-engineer",
        "name": "FastAPI 后端工程师",
        "category": "backend",
        "description": "设计 FastAPI 路由、Pydantic Schema、异步任务和后端错误定位。",
        "triggers": ["API", "FastAPI", "路由", "Schema", "422", "500", "任务队列", "diagnostics"],
        "skills": ["api-new", "api-debug", "stack-start", "pipeline-run"],
        "default_files": [
            "backend/main.py",
            "src/labsopguard/workflow.py",
            "src/labsopguard/tasking.py",
            "backend_start.err.log",
        ],
        "guardrails": [
            "路由统一使用 /api/v1/ 前缀。",
            "耗时超过 1 秒的流程走异步任务。",
            "错误响应保持 {detail, error_code} 结构。",
        ],
    },
    {
        "id": "05",
        "slug": "vue-frontend-engineer",
        "name": "Vue 前端工程师",
        "category": "frontend",
        "description": "维护 Vue 组件、视频播放、API 对接、空值保护和前端调试。",
        "triggers": ["Vue", "前端", "白屏", "组件", "视频播放", "CORS", "resolveArtifactUrl"],
        "skills": ["fe-component", "fe-debug", "stack-start"],
        "default_files": [
            "frontend-app/src/views/",
            "frontend-app/src/components/",
            "frontend-app/src/api/",
        ],
        "guardrails": [
            "视频或材料 URL 必须经过 resolveArtifactUrl。",
            "禁止依赖 Vite proxy 隐式补全生产 API 地址。",
            "渲染列表前对可空字段做默认值保护。",
        ],
    },
    {
        "id": "06",
        "slug": "qwen-vlm-engineer",
        "name": "Qwen VLM 工程师",
        "category": "backend",
        "description": "维护 DashScope/Qwen 文本与多模态调用、prompt 模板、错误处理和降级逻辑。",
        "triggers": ["Qwen", "DashScope", "VLM", "多模态", "prompt", "DASHSCOPE_API_KEY"],
        "skills": ["qwen-call", "api-debug"],
        "default_files": [
            ".env",
            "src/labsopguard/reasoning.py",
            "src/labsopguard/video_analysis.py",
            "tools/check_qwen_integration.py",
        ],
        "guardrails": [
            "唯一供应商是 Qwen/DashScope，不替换为其他模型服务。",
            "Key 只从 .env 的 DASHSCOPE_API_KEY 读取。",
            "调用失败必须降级到 rule_based，不阻断主链路。",
        ],
    },
    {
        "id": "07",
        "slug": "dataset-engineer",
        "name": "数据集工程师",
        "category": "detection",
        "description": "管理 Roboflow/YOLO 数据集、类别分布、标注质量、划分和困难样本回流。",
        "triggers": ["数据集", "Roboflow", "标注", "类别分布", "YOLO txt", "hardcase"],
        "skills": ["dataset", "hardcase", "train", "val"],
        "default_files": [
            "data/dataset/",
            "data/dataset/dataset.yaml",
            "outputs/hardcases/",
        ],
        "guardrails": [
            "合并数据前先统计类别分布和空标签。",
            "保持 train/val/test 划分可复现，固定 seed。",
            "tube、tube-cap、spearhead、pipette 等弱类优先补样。",
        ],
    },
    {
        "id": "08",
        "slug": "autodl-devops",
        "name": "AutoDL 运维工程师",
        "category": "devops",
        "description": "管理 AutoDL 训练环境、数据同步、显存问题、产物下载和全栈启动。",
        "triggers": ["AutoDL", "CUDA", "显存", "scp", "环境", "启动", "训练服务器"],
        "skills": ["autodl", "env-new", "train", "stack-start"],
        "default_files": [
            "scripts/start_full_stack.ps1",
            "outputs/training/",
            "requirements.txt",
            ".env",
        ],
        "guardrails": [
            "关机前必须下载训练产物。",
            "OOM 优先降 batch 或 imgsz，不盲目换代码。",
            "本地 RTX 4050 默认只用于推理或轻量验证。",
        ],
    },
    {
        "id": "09",
        "slug": "debug-expert",
        "name": "调试专家",
        "category": "general",
        "description": "跨检测、事件、API、前端和环境层做最小复现、根因定位和最小修复。",
        "triggers": ["报错", "debug", "traceback", "失败", "异常", "不可用", "复现"],
        "skills": ["api-debug", "fe-debug", "event-debug", "clip-check", "stack-start"],
        "default_files": [
            "backend_start.err.log",
            "frontend-app/",
            "outputs/experiments/",
            "configs/model/detection_runtime.yaml",
        ],
        "guardrails": [
            "先读完整错误，不跳过 traceback 末尾。",
            "先确定发生层级，再扩散排查范围。",
            "修复必须是最小范围，避免引入新抽象。",
        ],
    },
    {
        "id": "10",
        "slug": "experiment-recorder",
        "name": "实验记录员",
        "category": "general",
        "description": "结构化记录训练、验证、对比实验、周报和可复现结论。",
        "triggers": ["实验记录", "周报", "训练报告", "复现", "对比", "结果整理"],
        "skills": ["weekly", "train", "val", "paper-exp"],
        "default_files": [
            "docs/training_report.md",
            "context/history/",
            "outputs/training/",
            "outputs/val/",
        ],
        "guardrails": [
            "每个 run 单独记录参数、数据版本、指标和下一步。",
            "结论必须能追溯到产物路径或指标文件。",
        ],
    },
    {
        "id": "11",
        "slug": "paper-engineer",
        "name": "论文工程师",
        "category": "research",
        "description": "把系统架构和实验结果转成论文方法、实验、图表和学术表达。",
        "triggers": ["论文", "方法章节", "实验章节", "LaTeX", "消融", "baseline"],
        "skills": ["paper-method", "paper-exp", "weekly"],
        "default_files": [
            "project_brief.md",
            "docs/training_report.md",
            "outputs/val/",
        ],
        "guardrails": [
            "方法描述必须与代码实现一致。",
            "实验数字必须与 results.csv 或验证输出一致。",
            "不编造引用、指标或对比实验。",
        ],
    },
    {
        "id": "12",
        "slug": "vla-researcher",
        "name": "VLA 研究员",
        "category": "research",
        "description": "研究 LabSOPGuard 感知层到 VLA policy、闭环控制和 observation-action 数据构建。",
        "triggers": ["VLA", "具身智能", "闭环控制", "policy", "observation-action", "OpenVLA"],
        "skills": ["paper-method", "dataset", "event-debug"],
        "default_files": [
            "project_brief.md",
            "src/labsopguard/event_preprocessing/",
            "data/dataset/",
        ],
        "guardrails": [
            "VLA 方向默认等待 LabSOPGuard 达到稳定 A 级后再工程化。",
            "研究建议要明确感知输入、policy 输出和评估指标。",
        ],
    },
    {
        "id": "13",
        "slug": "system-architect",
        "name": "系统架构师",
        "category": "general",
        "description": "设计新模块、接口契约、目录结构和依赖边界，避免循环依赖。",
        "triggers": ["架构", "新模块", "接口", "目录结构", "依赖", "重构", "新项目"],
        "skills": ["api-new", "env-new", "stack-start", "pipeline-run", "paper-method"],
        "default_files": [
            "README.md",
            "src/labsopguard/",
            "backend/main.py",
            "frontend-app/src/",
        ],
        "guardrails": [
            "先定义输入、输出、schema 和依赖，再写实现。",
            "禁止 lab_preprocessing 到 LabSOPGuard 的循环 import。",
            "保持 detection_runtime.yaml 和 DashScope/Qwen 为唯一入口。",
        ],
    },
    {
        "id": "14",
        "slug": "ppt-coach",
        "name": "PPT 答辩教练",
        "category": "general",
        "description": "拆解汇报逻辑、页面结构、核心卖点、演讲提示和评委问题。",
        "triggers": ["PPT", "答辩", "汇报", "开题", "毕业设计", "演讲", "评委问题"],
        "skills": ["ppt-outline", "weekly", "paper-exp"],
        "default_files": [
            "project_brief.md",
            "docs/training_report.md",
            "context/active_focus.md",
        ],
        "guardrails": [
            "先确认汇报类型、时长和受众。",
            "每页标题优先写结论句。",
            "预判问题必须围绕数据、方法选择和落地可行性。",
        ],
    },
]


SKILLS = [
    {
        "id": "infer",
        "name": "/infer",
        "category": "检测与训练",
        "description": "在图片或视频上运行 YOLO 推理，输出可视化检测结果、速度和类别统计。",
        "triggers": ["推理", "预测", "图片检测", "视频检测", "annotated video"],
        "roles": ["yolo-trainer"],
        "default_files": ["configs/model/detection_runtime.yaml", "outputs/inference/"],
        "use_cases": ["用户要快速验证当前权重在图片或视频上的表现。", "需要生成标注视频、检测截图或推理速度摘要。"],
        "inputs": ["source 图片/视频路径", "可选 conf、imgsz、model override"],
        "outputs": ["推理命令", "输出目录", "类别检测数量与速度摘要"],
        "steps": [
            "读取 configs/model/detection_runtime.yaml 获取默认权重。",
            "按输入类型生成 yolo predict 命令。",
            "输出保存到 outputs/inference/<run_name>/。",
            "汇总速度、类别数量和可视化文件路径。",
        ],
        "failure": ["权重不存在时先转入 /val 或提示修正 detection_runtime.yaml。", "source 不存在时停止执行并返回缺失路径。"],
    },
    {
        "id": "train",
        "name": "/train",
        "category": "检测与训练",
        "description": "执行 YOLO 训练准备、命令生成、AutoDL 指引、产物检查和权重切换建议。",
        "triggers": ["训练", "YOLO train", "epoch", "batch", "学习率", "新权重"],
        "roles": ["yolo-trainer", "autodl-devops", "dataset-engineer", "experiment-recorder"],
        "default_files": ["configs/model/detection_runtime.yaml", "data/dataset/dataset.yaml", "outputs/training/"],
        "use_cases": ["需要启动一次新的检测模型训练。", "需要根据数据规模和显存生成训练参数。"],
        "inputs": ["模型规模", "epoch/batch/imgsz", "run_name", "是否使用 AutoDL"],
        "outputs": ["训练命令", "AutoDL 上传/下载步骤", "产物检查清单", "权重切换建议"],
        "steps": [
            "检查 dataset.yaml 和类别分布。",
            "报告样本不足或弱类风险。",
            "生成 yolo detect train 命令。",
            "如使用 AutoDL，补充打包、上传、训练、下载命令。",
            "训练完成后要求保留 best.pt、last.pt、results.csv 和混淆矩阵。",
            "切换权重前触发 /val。",
        ],
        "failure": ["CUDA OOM 时优先降低 batch 或 imgsz。", "数据集路径缺失时转入 /dataset。", "训练中断时检查 last.pt 并给出续训命令。"],
    },
    {
        "id": "val",
        "name": "/val",
        "category": "检测与训练",
        "description": "对当前或指定权重做测试集评估，产出 mAP/P/R、混淆矩阵和弱类分析。",
        "triggers": ["验证", "评估", "mAP", "confusion_matrix", "测试集", "val"],
        "roles": ["yolo-trainer", "dataset-engineer", "experiment-recorder"],
        "default_files": ["configs/model/detection_runtime.yaml", "data/dataset/dataset.yaml", "outputs/val/"],
        "use_cases": ["切换权重前验证质量。", "论文或报告需要检测指标。"],
        "inputs": ["model 路径", "split", "run_name"],
        "outputs": ["yolo val 命令", "指标表", "混淆矩阵和曲线路径", "强弱类别结论"],
        "steps": [
            "读取当前权重路径。",
            "生成 yolo val 命令并使用 split=test。",
            "检查 confusion_matrix、PR/F1 曲线和 per-class 指标。",
            "标注强类、弱类和下一步补样方向。",
        ],
        "failure": ["权重不可读时停止切换并回退到上一个 best.pt。", "测试集为空时转入 /dataset 修复划分。"],
    },
    {
        "id": "dataset",
        "name": "/dataset",
        "category": "检测与训练",
        "description": "统计 YOLO 数据集类别分布、合并 Roboflow 导出、重划分并检查标注质量。",
        "triggers": ["数据集", "Roboflow", "类别统计", "标注质量", "划分", "YOLO txt"],
        "roles": ["dataset-engineer", "yolo-trainer", "vla-researcher"],
        "default_files": ["data/dataset/", "data/dataset/dataset.yaml"],
        "use_cases": ["新增 Roboflow zip 后合并到本地。", "训练前检查类别不均衡或坏标签。"],
        "inputs": ["Roboflow zip 路径", "目标 dataset 目录", "划分比例"],
        "outputs": ["类别分布表", "合并/划分命令", "标注质量问题清单"],
        "steps": [
            "统计 train/val/test label 中的类别分布。",
            "解压 Roboflow zip 并检查 images/labels 对齐。",
            "按固定 seed 重划分数据集。",
            "检查空标签、异常 bbox、类别缺失和弱类。",
        ],
        "failure": ["图片和标签数量不一致时停止合并并列出缺失对。", "类别 id 超出 dataset.yaml 时阻止训练。"],
    },
    {
        "id": "hardcase",
        "name": "/hardcase",
        "category": "检测与训练",
        "description": "挖掘误检/漏检帧，导出困难样本包并推动 Roboflow 复标回流。",
        "triggers": ["困难样本", "误检", "漏检", "hardcase", "复标", "弱类"],
        "roles": ["dataset-engineer", "yolo-trainer"],
        "default_files": ["outputs/hardcases/", "data/dataset/", "outputs/training/"],
        "use_cases": ["某些类别 AP 低，需要针对性补样。", "需要把错误样本打包上传 Roboflow。"],
        "inputs": ["model 路径", "dataset.yaml", "conf 阈值", "输出目录"],
        "outputs": ["困难样本包路径", "错误类型摘要", "复标建议"],
        "steps": [
            "运行检测错误分析脚本。",
            "构建 upload_pack。",
            "按类别和错误类型汇总优先级。",
            "提示上传 Roboflow 复标并回流 /dataset。",
        ],
        "failure": ["分析脚本不存在时给出手动抽样方案。", "输出包为空时降低 conf 或扩大样本来源。"],
    },
    {
        "id": "event-debug",
        "name": "/event-debug",
        "category": "事件与链路",
        "description": "检查视频到事件、clip、步骤推理的全链路，定位断点并给出最小修复方案。",
        "triggers": ["事件调试", "漏检", "physical_events", "steps_bridge_result", "materials publish"],
        "roles": ["video-event-engineer", "step-bridge-engineer", "debug-expert", "vla-researcher"],
        "default_files": ["outputs/experiments/<id>/", "src/labsopguard/event_preprocessing/"],
        "use_cases": ["实验处理后没有事件、没有 clip 或步骤结果异常。", "需要解释 needs_review 或低置信度。"],
        "inputs": ["experiment_id", "可选事件类型或视频路径"],
        "outputs": ["链路状态表", "断点位置", "修复或重跑命令"],
        "steps": [
            "检查 outputs/experiments/<id>/ 是否完整。",
            "确认视频文件、physical_events.json、material_stream.json、steps_bridge_result.json。",
            "统计事件类型分布。",
            "触发或检查 materials publish。",
            "把问题归因到检测、事件、clip、step bridge 或 API 层。",
        ],
        "failure": ["实验目录不存在时转入 /pipeline-run 重新处理。", "事件为空时先确认检测输出和视频输入，不直接改 step bridge。"],
    },
    {
        "id": "pipeline-run",
        "name": "/pipeline-run",
        "category": "事件与链路",
        "description": "检查后端健康状态，触发实验处理链路并验证关键输出文件完整性。",
        "triggers": ["跑链路", "process experiment", "diagnostics", "pipeline", "全流程"],
        "roles": ["video-event-engineer", "fastapi-backend-engineer", "system-architect", "step-bridge-engineer"],
        "default_files": ["backend/main.py", "outputs/experiments/<id>/"],
        "use_cases": ["需要从 API 触发一次完整实验处理。", "需要验证后端、事件、材料和分析产物是否齐全。"],
        "inputs": ["experiment_id", "后端地址"],
        "outputs": ["curl 命令", "健康检查结果", "产物完整性清单"],
        "steps": [
            "请求 /api/v1/diagnostics。",
            "POST /api/v1/experiments/<id>/process。",
            "必要时 POST /materials/publish。",
            "验证 physical_events.json、material_stream.json、analysis/annotated.mp4。",
        ],
        "failure": ["后端不可达时转入 /stack-start。", "API 500 时转入 /api-debug。", "材料缺失时转入 /clip-check。"],
    },
    {
        "id": "clip-check",
        "name": "/clip-check",
        "category": "事件与链路",
        "description": "诊断 clip 或 materials 生成问题，检查目录结构、ffmpeg 可用性和材料索引。",
        "triggers": ["clip", "materials", "ffmpeg", "素材", "索引", "视频片段"],
        "roles": ["video-event-engineer", "step-bridge-engineer", "debug-expert"],
        "default_files": ["outputs/experiments/<id>/materials/", "tools/rebuild_material_indexes.py"],
        "use_cases": ["事件存在但前端没有素材。", "annotated clip 或 material index 缺失。"],
        "inputs": ["experiment_id", "materials 目录"],
        "outputs": ["缺失文件清单", "ffmpeg 检查结果", "重建索引命令"],
        "steps": [
            "列出 materials 目录结构。",
            "检查 imageio_ffmpeg 可用性。",
            "确认 events/、clips/、index 文件是否存在。",
            "必要时调用 publish 或 rebuild_material_indexes.py。",
        ],
        "failure": ["ffmpeg 不可用时先修环境。", "events 为空时返回 /event-debug。"],
    },
    {
        "id": "api-new",
        "name": "/api-new",
        "category": "后端开发",
        "description": "生成符合项目约束的 FastAPI 路由、Pydantic Schema 和异步任务接入方案。",
        "triggers": ["新接口", "新增 API", "FastAPI 路由", "Pydantic", "任务队列"],
        "roles": ["fastapi-backend-engineer", "system-architect"],
        "default_files": ["backend/main.py", "src/labsopguard/tasking.py", "src/labsopguard/workflow.py"],
        "use_cases": ["新增实验、材料、诊断或任务类 API。", "需要把耗时流程接入异步队列。"],
        "inputs": ["接口路径", "请求/响应字段", "同步或异步需求"],
        "outputs": ["路由草案", "Schema 草案", "任务队列接入点", "错误格式"],
        "steps": [
            "确认路径统一在 /api/v1/ 下。",
            "定义 Request/Response Schema。",
            "超过 1 秒的处理封装为任务。",
            "保持错误结构 {detail, error_code}。",
        ],
        "failure": ["需求字段不明确时先输出 schema 问题清单。", "涉及架构边界时转入 system-architect。"],
    },
    {
        "id": "api-debug",
        "name": "/api-debug",
        "category": "后端开发",
        "description": "定位接口报错，读取日志、复现请求、区分 422/500/CORS/业务链路错误。",
        "triggers": ["接口报错", "422", "500", "CORS", "backend_start.err.log", "API debug"],
        "roles": ["fastapi-backend-engineer", "qwen-vlm-engineer", "debug-expert"],
        "default_files": ["backend_start.err.log", "backend/main.py", ".env"],
        "use_cases": ["接口返回 422、500 或前端调用失败。", "Qwen 或 YOLO 后端依赖导致 API 异常。"],
        "inputs": ["接口路径", "请求体", "错误响应", "日志片段"],
        "outputs": ["复现 curl", "根因分类", "最小修复建议"],
        "steps": [
            "读取 backend_start.err.log 最近错误。",
            "用 curl -v 复现请求。",
            "按 422、500、CORS、依赖不可用分类。",
            "定位到 schema、路由、任务队列或模型依赖。",
        ],
        "failure": ["日志不足时要求补充完整响应和请求体。", "后端未启动时转入 /stack-start。"],
    },
    {
        "id": "qwen-call",
        "name": "/qwen-call",
        "category": "后端开发",
        "description": "生成 Qwen/DashScope 文本或多模态调用代码，包含 prompt、错误处理和 rule_based 降级。",
        "triggers": ["Qwen", "DashScope", "VLM", "多模态调用", "prompt", "semantic enhancer"],
        "roles": ["qwen-vlm-engineer"],
        "default_files": [".env", "src/labsopguard/reasoning.py", "src/labsopguard/video_analysis.py"],
        "use_cases": ["新增 Qwen 文本或图文理解调用。", "需要修复 DashScope 调用、prompt 或降级逻辑。"],
        "inputs": ["任务目标", "文本/图片输入", "prompt 草案", "期望 schema"],
        "outputs": ["调用代码", "prompt 模板", "异常处理", "降级路径"],
        "steps": [
            "从 .env 读取 DASHSCOPE_API_KEY。",
            "文本接口使用 OpenAI 兼容 DashScope base_url。",
            "多模态接口使用 dashscope.MultiModalConversation.call。",
            "失败时返回 rule_based 结果并记录原因。",
        ],
        "failure": ["Key 缺失时不伪造调用结果。", "接口失败时不阻断主流程，必须降级。"],
    },
    {
        "id": "fe-component",
        "name": "/fe-component",
        "category": "前端开发",
        "description": "生成符合项目约束的 Vue 组件，覆盖 API 对接、URL 处理、空值保护和展示字段。",
        "triggers": ["Vue 组件", "前端页面", "组件开发", "材料展示", "视频播放器"],
        "roles": ["vue-frontend-engineer"],
        "default_files": ["frontend-app/src/views/", "frontend-app/src/components/", "frontend-app/src/api/"],
        "use_cases": ["新增实验详情、材料列表或结果展示组件。", "需要把后端字段安全渲染到页面。"],
        "inputs": ["组件目标", "API 字段", "交互要求"],
        "outputs": ["Vue 组件代码方案", "API 调用方式", "空值保护点"],
        "steps": [
            "确认 API 地址和字段结构。",
            "视频/材料 URL 统一调用 resolveArtifactUrl。",
            "列表字段使用 ?? [] 做默认值。",
            "只展示 display_name 等稳定字段。",
        ],
        "failure": ["字段不确定时先从 Network 或 API 响应确认。", "视频不播放时转入 /fe-debug。"],
    },
    {
        "id": "fe-debug",
        "name": "/fe-debug",
        "category": "前端开发",
        "description": "调试前端白屏、渲染异常、URL、CORS 和空值访问问题。",
        "triggers": ["白屏", "前端报错", "undefined", "CORS", "视频不播放", "Network"],
        "roles": ["vue-frontend-engineer", "debug-expert"],
        "default_files": ["frontend-app/src/", ".env"],
        "use_cases": ["页面白屏或控制台报错。", "视频、材料、接口请求在前端不可用。"],
        "inputs": ["控制台错误", "Network 请求", "页面路径"],
        "outputs": ["错误层级判断", "修复点", "验证步骤"],
        "steps": [
            "先看 Console 的 undefined、TypeError 或 CORS。",
            "再看 Network 请求 URL 和响应。",
            "检查 resolveArtifactUrl 与空值保护。",
            "修复后刷新并复测关键页面。",
        ],
        "failure": ["API 不通时转入 /api-debug 或 /stack-start。", "字段缺失时先修前端兼容，不立即要求后端改 schema。"],
    },
    {
        "id": "env-new",
        "name": "/env-new",
        "category": "环境与工程",
        "description": "初始化新项目或新机器环境，覆盖 conda、依赖、CUDA、.env 模板和可用性验证。",
        "triggers": ["新环境", "conda", "requirements", ".env", "CUDA", "新机器"],
        "roles": ["autodl-devops", "system-architect"],
        "default_files": ["requirements.txt", ".env", "scripts/"],
        "use_cases": ["新机器首次部署 LabSOPGuard。", "新项目需要标准 Python/CUDA/Qwen 环境。"],
        "inputs": ["环境名", "Python 版本", "CUDA/PyTorch 版本", "是否需要 DashScope"],
        "outputs": ["环境创建命令", "依赖安装命令", ".env 模板", "验证命令"],
        "steps": [
            "创建 Python 3.11 conda 环境。",
            "安装 PyTorch、ultralytics、dashscope、openai 等依赖。",
            "生成 .env 必要键说明。",
            "验证 torch.cuda.is_available 和 Qwen key 读取。",
        ],
        "failure": ["CUDA 不匹配时先确认 torch build 与驱动版本。", "依赖安装失败时锁定失败包，不整体重装。"],
    },
    {
        "id": "autodl",
        "name": "/autodl",
        "category": "环境与工程",
        "description": "执行 AutoDL 数据上传、远端训练、产物下载、权重同步和常见故障处理。",
        "triggers": ["AutoDL", "远端训练", "scp", "5090", "显存", "训练产物"],
        "roles": ["autodl-devops", "yolo-trainer"],
        "default_files": ["data/dataset/", "outputs/training/", "configs/model/detection_runtime.yaml"],
        "use_cases": ["本地显存不足，需要在 AutoDL 训练。", "需要同步训练产物回本地并切权重。"],
        "inputs": ["远端 IP", "数据集目录", "run_name", "训练命令"],
        "outputs": ["tar/scp 命令", "远端训练命令", "下载命令", "权重同步步骤"],
        "steps": [
            "打包并上传 data/dataset。",
            "在远端确认 CUDA/PyTorch 环境。",
            "执行训练命令。",
            "关机前下载 outputs/training/<run>/。",
            "本地运行 /val 后再切换权重。",
        ],
        "failure": ["OOM 时降低 batch 或 imgsz。", "中断时检查 last.pt 续训。", "下载失败时禁止删除远端产物。"],
    },
    {
        "id": "stack-start",
        "name": "/stack-start",
        "category": "环境与工程",
        "description": "启动或检查 Redis、FastAPI、Vite 全栈服务，并执行健康检查和端口故障速查。",
        "triggers": ["启动全栈", "FastAPI 启动", "Vite", "Redis", "diagnostics", "端口"],
        "roles": ["autodl-devops", "fastapi-backend-engineer", "vue-frontend-engineer", "debug-expert", "system-architect"],
        "default_files": ["scripts/start_full_stack.ps1", "backend_start.err.log", "frontend-app/"],
        "use_cases": ["本地开发前启动完整系统。", "后端或前端不可达时做基础健康检查。"],
        "inputs": ["是否 Restart", "是否 SkipRedis"],
        "outputs": ["启动命令", "端口清单", "diagnostics 检查结果"],
        "steps": [
            "运行 .\\scripts\\start_full_stack.ps1 -Restart -SkipRedis。",
            "检查 FastAPI=8000、Vite=5173、Redis=6379。",
            "curl /api/v1/diagnostics。",
            "根据日志判断端口占用或依赖不可用。",
        ],
        "failure": ["后端启动失败转入 /api-debug。", "前端白屏转入 /fe-debug。", "Redis 不需要时允许 SkipRedis。"],
    },
    {
        "id": "paper-method",
        "name": "/paper-method",
        "category": "科研与输出",
        "description": "把系统架构翻译成论文方法章节，包括模块定义、输入输出、公式框架和图文说明。",
        "triggers": ["方法章节", "论文方法", "系统架构", "公式", "模块描述"],
        "roles": ["paper-engineer", "vla-researcher", "system-architect"],
        "default_files": ["project_brief.md", "src/labsopguard/", "docs/"],
        "use_cases": ["需要写 LabSOPGuard 方法章节。", "需要把工程模块转成学术表达。"],
        "inputs": ["模块名称", "目标会议/格式", "已有结构或代码路径"],
        "outputs": ["章节大纲", "模块描述", "公式占位", "图注文字"],
        "steps": [
            "读取项目简介和相关模块。",
            "按 Overview、Perception、Event Detection、Step Reasoning 组织。",
            "每个模块写输入、输出、核心操作和与 baseline 差异。",
            "保持学术风格，不写口语化实现细节。",
        ],
        "failure": ["没有实验支撑时不夸大效果。", "代码实现不明时标注待确认而不是编造。"],
    },
    {
        "id": "paper-exp",
        "name": "/paper-exp",
        "category": "科研与输出",
        "description": "基于评测指标生成论文实验章节，覆盖数据集、对比、消融、结果表和定性分析。",
        "triggers": ["实验章节", "消融", "对比实验", "LaTeX 表格", "结果分析"],
        "roles": ["paper-engineer", "experiment-recorder", "ppt-coach"],
        "default_files": ["docs/training_report.md", "outputs/val/", "outputs/training/"],
        "use_cases": ["需要把训练/验证结果写成论文实验。", "需要生成 LaTeX 指标表或消融表。"],
        "inputs": ["指标文件", "baseline 列表", "消融设置"],
        "outputs": ["实验章节草稿", "LaTeX 表格", "结果解读", "局限性"],
        "steps": [
            "读取 mAP50、mAP50-95、P、R 和 per-class AP。",
            "生成数据集、实现细节、对比、消融和定性分析结构。",
            "输出 LaTeX 表格并标注数据来源。",
            "明确弱类和失败案例。",
        ],
        "failure": ["缺少 baseline 时只写当前模型结果，不伪造对比。", "指标来源不明时要求先运行 /val。"],
    },
    {
        "id": "ppt-outline",
        "name": "/ppt-outline",
        "category": "科研与输出",
        "description": "生成答辩或汇报 PPT 大纲，包含页面标题、支撑点、演讲逻辑和评委问题。",
        "triggers": ["PPT", "答辩大纲", "汇报", "开题", "演讲稿", "评委问题"],
        "roles": ["ppt-coach"],
        "default_files": ["project_brief.md", "docs/training_report.md"],
        "use_cases": ["毕业设计、开题、中期或项目汇报需要结构。", "需要把技术工作压缩成可讲故事线。"],
        "inputs": ["汇报类型", "时长", "受众", "主题"],
        "outputs": ["每页标题", "三点支撑", "转场话术", "预判问题"],
        "steps": [
            "确认汇报类型、时长和受众。",
            "按背景、问题、方法、实验、总结组织。",
            "每页标题写结论句。",
            "补充评委可能追问和回答要点。",
        ],
        "failure": ["目标受众不明时先给通用科研答辩结构。", "实验结果不足时把风险写入备答问题。"],
    },
    {
        "id": "weekly",
        "name": "/weekly",
        "category": "科研与输出",
        "description": "读取记忆系统当前状态和历史，生成结构化周报、完成项、问题和下周计划。",
        "triggers": ["周报", "本周完成", "下周计划", "进展总结", "日报"],
        "roles": ["experiment-recorder", "paper-engineer", "ppt-coach"],
        "default_files": ["context/active_focus.md", "context/current_status.md", "context/next_actions.md", "context/history/"],
        "use_cases": ["需要整理本周项目进展。", "需要把实验和开发结果转成汇报材料。"],
        "inputs": ["时间范围", "目标格式", "可选重点项目"],
        "outputs": ["完成项", "问题风险", "下周计划", "需要支持"],
        "steps": [
            "读取 active_focus、current_status、next_actions。",
            "必要时补充 history 中本周记录。",
            "按完成、问题、计划、支持需求输出。",
            "保留关键产物路径和指标。",
        ],
        "failure": ["状态文件缺失时基于可读 history 输出并标注缺口。", "没有新进展时输出风险和建议动作，不编造完成项。"],
    },
]


def yaml_list(values: list[str]) -> str:
    return "\n".join(f"  - {value}" for value in values)


def bullet_list(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def numbered_list(values: list[str]) -> str:
    return "\n".join(f"{idx}. {value}" for idx, value in enumerate(values, 1))


def write_role(role: dict) -> None:
    path = ROLES_DIR / f"{role['id']}_{role['slug'].replace('-', '_')}.md"
    content = f"""---
id: "{role['id']}"
slug: {role['slug']}
name: {role['name']}
category: {role['category']}
description: {role['description']}
triggers:
{yaml_list(role['triggers'])}
skills:
{yaml_list(role['skills'])}
default_files:
{yaml_list(role['default_files'])}
---

# 角色：{role['name']}

## 职责

{role['description']}

## 触发意图

{bullet_list(role['triggers'])}

## 默认加载文件

{bullet_list(role['default_files'])}

## 可调用 Skills

{bullet_list(role['skills'])}

## 工作约束

{bullet_list(role['guardrails'])}
"""
    path.write_text(content, encoding="utf-8", newline="\n")


def write_skill(skill: dict) -> None:
    path = SKILLS_DIR / f"{skill['id']}.md"
    content = f"""---
id: {skill['id']}
name: {skill['name']}
category: {skill['category']}
description: {skill['description']}
triggers:
{yaml_list(skill['triggers'])}
roles:
{yaml_list(skill['roles'])}
default_files:
{yaml_list(skill['default_files'])}
---

# {skill['name']} - {skill['description']}

## 适用场景

{bullet_list(skill['use_cases'])}

## 输入

{bullet_list(skill['inputs'])}

## 输出

{bullet_list(skill['outputs'])}

## 执行流程

{numbered_list(skill['steps'])}

## 失败处理

{bullet_list(skill['failure'])}

## 关联角色

{bullet_list(skill['roles'])}

## 默认文件

{bullet_list(skill['default_files'])}
"""
    path.write_text(content, encoding="utf-8", newline="\n")


def build_routing() -> dict:
    roles_by_slug = {role["slug"]: role for role in ROLES}
    skills_by_id = {skill["id"]: skill for skill in SKILLS}
    intents = []
    for role in ROLES:
        intents.append(
            {
                "intent": role["slug"],
                "description": role["description"],
                "triggers": role["triggers"],
                "role": role["slug"],
                "skills": role["skills"],
                "default_files": role["default_files"],
            }
        )

    return {
        "version": 1,
        "generated_by": "boot/write_skills.py",
        "policy": {
            "selection_order": ["intent triggers", "role triggers", "skill triggers", "default files"],
            "fallback_role": "debug-expert",
            "fallback_skills": ["api-debug", "fe-debug", "event-debug", "stack-start"],
        },
        "intents": intents,
        "roles": {
            slug: {
                "id": role["id"],
                "name": role["name"],
                "category": role["category"],
                "description": role["description"],
                "triggers": role["triggers"],
                "skills": role["skills"],
                "default_files": role["default_files"],
            }
            for slug, role in roles_by_slug.items()
        },
        "skills": {
            sid: {
                "name": skill["name"],
                "category": skill["category"],
                "description": skill["description"],
                "triggers": skill["triggers"],
                "roles": skill["roles"],
                "default_files": skill["default_files"],
            }
            for sid, skill in skills_by_id.items()
        },
    }


def write_routing_files() -> None:
    routing = build_routing()
    (BOOT_DIR / "routing_map.json").write_text(
        json.dumps(routing, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    lines = [
        "# 意图 -> Role -> Skill -> 文件 路由表",
        "",
        "## 路由原则",
        "",
        "- 先用用户意图和触发词匹配 role。",
        "- 再加载该 role 的 skills 和 default_files。",
        "- 如果无法判断，回退到 debug-expert，并优先使用 api-debug、fe-debug、event-debug、stack-start。",
        "- routing_map.json 是机器可读版本；本文件是人工检查版本。",
        "",
        "## 路由明细",
        "",
        "| 意图 | 触发词 | Role | Skills | 默认文件 |",
        "|---|---|---|---|---|",
    ]
    for role in ROLES:
        lines.append(
            "| {intent} | {triggers} | {role} | {skills} | {files} |".format(
                intent=role["slug"],
                triggers=", ".join(role["triggers"]),
                role=role["slug"],
                skills=", ".join(role["skills"]),
                files=", ".join(role["default_files"]),
            )
        )

    lines.extend(
        [
            "",
            "## Skill 索引",
            "",
            "| Skill | 关联角色 | 默认文件 |",
            "|---|---|---|",
        ]
    )
    for skill in SKILLS:
        lines.append(
            "| {skill} | {roles} | {files} |".format(
                skill=skill["id"],
                roles=", ".join(skill["roles"]),
                files=", ".join(skill["default_files"]),
            )
        )

    (BOOT_DIR / "routing_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def validate() -> None:
    skill_ids = {skill["id"] for skill in SKILLS}
    missing = []
    for role in ROLES:
        for skill_id in role["skills"]:
            if skill_id not in skill_ids:
                missing.append(f"role:{role['slug']} -> {skill_id}")
    if missing:
        raise SystemExit("Missing skill definitions:\n" + "\n".join(missing))


def main() -> None:
    ROLES_DIR.mkdir(exist_ok=True)
    SKILLS_DIR.mkdir(exist_ok=True)
    validate()
    for role in ROLES:
        write_role(role)
    for skill in SKILLS:
        write_skill(skill)
    write_routing_files()
    print(f"Wrote {len(ROLES)} roles, {len(SKILLS)} skills, and routing maps.")


if __name__ == "__main__":
    main()
