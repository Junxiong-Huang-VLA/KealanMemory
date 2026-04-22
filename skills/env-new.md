---
id: env-new
name: /env-new
category: 环境与工程
description: 新项目/新机器环境初始化：conda + requirements + .env 模板
---

# /env-new — 新项目/新机器环境初始化：conda + requirements + .env 模板

## 执行步骤

1. conda create -n <项目名> python=3.11 (放 E:/conda_envs/)
2. pip install torch --index-url cu124 + ultralytics + dashscope + openai
3. 生成 .env 模板（DASHSCOPE_API_KEY / CORS_ALLOW_ORIGINS）
4. 验证 torch.cuda.is_available()
