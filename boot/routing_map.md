# 意图 -> Role -> Skill -> 文件 路由表

## 路由原则

- 先用用户意图和触发词匹配 role。
- 再加载该 role 的 skills 和 default_files。
- 如果无法判断，回退到 debug-expert，并优先使用 api-debug、fe-debug、event-debug、stack-start。
- routing_map.json 是机器可读版本；本文件是人工检查版本。

## 路由明细

| 意图 | 触发词 | Role | Skills | 默认文件 |
|---|---|---|---|---|
| yolo-trainer | 训练, YOLO, 权重, mAP, 过拟合, 欠拟合, 推理, 验证 | yolo-trainer | train, val, infer, hardcase, autodl | configs/model/detection_runtime.yaml, data/dataset/dataset.yaml, outputs/training/, outputs/val/ |
| video-event-engineer | 事件, clip, materials, 视频处理, physical_events, material_stream | video-event-engineer | event-debug, pipeline-run, clip-check | src/labsopguard/event_preprocessing/, outputs/experiments/<id>/physical_events.json, outputs/experiments/<id>/materials/ |
| step-bridge-engineer | 步骤, SOP, StepBridge, 合规, needs_review, protocol_graph | step-bridge-engineer | event-debug, pipeline-run, clip-check | src/labsopguard/step_bridge/, outputs/experiments/<id>/steps_bridge_result.json |
| fastapi-backend-engineer | API, FastAPI, 路由, Schema, 422, 500, 任务队列, diagnostics | fastapi-backend-engineer | api-new, api-debug, stack-start, pipeline-run | backend/main.py, src/labsopguard/workflow.py, src/labsopguard/tasking.py, backend_start.err.log |
| vue-frontend-engineer | Vue, 前端, 白屏, 组件, 视频播放, CORS, resolveArtifactUrl | vue-frontend-engineer | fe-component, fe-debug, stack-start | frontend-app/src/views/, frontend-app/src/components/, frontend-app/src/api/ |
| qwen-vlm-engineer | Qwen, DashScope, VLM, 多模态, prompt, DASHSCOPE_API_KEY | qwen-vlm-engineer | qwen-call, api-debug | .env, src/labsopguard/reasoning.py, src/labsopguard/video_analysis.py, tools/check_qwen_integration.py |
| dataset-engineer | 数据集, Roboflow, 标注, 类别分布, YOLO txt, hardcase | dataset-engineer | dataset, hardcase, train, val | data/dataset/, data/dataset/dataset.yaml, outputs/hardcases/ |
| autodl-devops | AutoDL, CUDA, 显存, scp, 环境, 启动, 训练服务器 | autodl-devops | autodl, env-new, train, stack-start | scripts/start_full_stack.ps1, outputs/training/, requirements.txt, .env |
| debug-expert | 报错, debug, traceback, 失败, 异常, 不可用, 复现 | debug-expert | api-debug, fe-debug, event-debug, clip-check, stack-start | backend_start.err.log, frontend-app/, outputs/experiments/, configs/model/detection_runtime.yaml |
| experiment-recorder | 实验记录, 周报, 训练报告, 复现, 对比, 结果整理 | experiment-recorder | weekly, train, val, paper-exp | docs/training_report.md, context/history/, outputs/training/, outputs/val/ |
| paper-engineer | 论文, 方法章节, 实验章节, LaTeX, 消融, baseline | paper-engineer | paper-method, paper-exp, weekly | project_brief.md, docs/training_report.md, outputs/val/ |
| vla-researcher | VLA, 具身智能, 闭环控制, policy, observation-action, OpenVLA | vla-researcher | paper-method, dataset, event-debug | project_brief.md, src/labsopguard/event_preprocessing/, data/dataset/ |
| system-architect | 架构, 新模块, 接口, 目录结构, 依赖, 重构, 新项目 | system-architect | api-new, env-new, stack-start, pipeline-run, paper-method | README.md, src/labsopguard/, backend/main.py, frontend-app/src/ |
| ppt-coach | PPT, 答辩, 汇报, 开题, 毕业设计, 演讲, 评委问题 | ppt-coach | ppt-outline, weekly, paper-exp | project_brief.md, docs/training_report.md, context/active_focus.md |

## Skill 索引

| Skill | 关联角色 | 默认文件 |
|---|---|---|
| infer | yolo-trainer | configs/model/detection_runtime.yaml, outputs/inference/ |
| train | yolo-trainer, autodl-devops, dataset-engineer, experiment-recorder | configs/model/detection_runtime.yaml, data/dataset/dataset.yaml, outputs/training/ |
| val | yolo-trainer, dataset-engineer, experiment-recorder | configs/model/detection_runtime.yaml, data/dataset/dataset.yaml, outputs/val/ |
| dataset | dataset-engineer, yolo-trainer, vla-researcher | data/dataset/, data/dataset/dataset.yaml |
| hardcase | dataset-engineer, yolo-trainer | outputs/hardcases/, data/dataset/, outputs/training/ |
| event-debug | video-event-engineer, step-bridge-engineer, debug-expert, vla-researcher | outputs/experiments/<id>/, src/labsopguard/event_preprocessing/ |
| pipeline-run | video-event-engineer, fastapi-backend-engineer, system-architect, step-bridge-engineer | backend/main.py, outputs/experiments/<id>/ |
| clip-check | video-event-engineer, step-bridge-engineer, debug-expert | outputs/experiments/<id>/materials/, tools/rebuild_material_indexes.py |
| api-new | fastapi-backend-engineer, system-architect | backend/main.py, src/labsopguard/tasking.py, src/labsopguard/workflow.py |
| api-debug | fastapi-backend-engineer, qwen-vlm-engineer, debug-expert | backend_start.err.log, backend/main.py, .env |
| qwen-call | qwen-vlm-engineer | .env, src/labsopguard/reasoning.py, src/labsopguard/video_analysis.py |
| fe-component | vue-frontend-engineer | frontend-app/src/views/, frontend-app/src/components/, frontend-app/src/api/ |
| fe-debug | vue-frontend-engineer, debug-expert | frontend-app/src/, .env |
| env-new | autodl-devops, system-architect | requirements.txt, .env, scripts/ |
| autodl | autodl-devops, yolo-trainer | data/dataset/, outputs/training/, configs/model/detection_runtime.yaml |
| stack-start | autodl-devops, fastapi-backend-engineer, vue-frontend-engineer, debug-expert, system-architect | scripts/start_full_stack.ps1, backend_start.err.log, frontend-app/ |
| paper-method | paper-engineer, vla-researcher, system-architect | project_brief.md, src/labsopguard/, docs/ |
| paper-exp | paper-engineer, experiment-recorder, ppt-coach | docs/training_report.md, outputs/val/, outputs/training/ |
| ppt-outline | ppt-coach | project_brief.md, docs/training_report.md |
| weekly | experiment-recorder, paper-engineer, ppt-coach | context/active_focus.md, context/current_status.md, context/next_actions.md, context/history/ |
