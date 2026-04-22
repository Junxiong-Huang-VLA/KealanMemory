# KealanMemory — VS Code AI 规则（Kealan）

## 身份

Kealan，独立全栈研究工程师，研究+工程双轨（VLA/具身智能 + 实验室SOP合规系统）。
核心技术：YOLO系列、Qwen-VL/DashScope、FastAPI、视频事件理解。

## 协作约定

- 直接执行，结论优先，不铺垫，不废话
- 文件找不到先查其他盘（C/D/E）和云端（Roboflow/AutoDL）
- API 只用 Qwen/DashScope，Key 只从 .env 读
- YOLO 权重路径唯一入口：configs/model/detection_runtime.yaml
- PYTHONPATH=src，禁止 sys.path.insert
- 视频 URL 必须用 resolveArtifactUrl() 转绝对路径
- 不用 emoji，简单问题 1-3 句话

## 开工/收工协议

当用户说"开工"：读取 D:\KealanMemory 记忆文件，输出当前焦点+项目状态+下一步，说"开工了，说吧。"

当用户说"收工"：总结本次完成内容，更新 D:\KealanMemory\projects\<项目>\current_status.md 和 next_actions.md 和 context\active_focus.md，说"收工，记忆已保存。"

## 环境

- 项目在 D 盘，conda 在 E:/conda_envs/
- 当前主项目：D:\LabEmbodiedVLA\LabSOPGuard\
- 记忆 Web：http://localhost:7777

## 完整记忆入口

D:\KealanMemory\boot\AI_ONBOARDING.md
