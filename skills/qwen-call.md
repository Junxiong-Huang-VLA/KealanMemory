---
id: qwen-call
name: /qwen-call
category: 后端开发
description: 生成 Qwen/DashScope 文本或多模态调用代码，包含 prompt、错误处理和 rule_based 降级。
triggers:
  - Qwen
  - DashScope
  - VLM
  - 多模态调用
  - prompt
  - semantic enhancer
roles:
  - qwen-vlm-engineer
default_files:
  - .env
  - src/labsopguard/reasoning.py
  - src/labsopguard/video_analysis.py
---

# /qwen-call - 生成 Qwen/DashScope 文本或多模态调用代码，包含 prompt、错误处理和 rule_based 降级。

## 适用场景

- 新增 Qwen 文本或图文理解调用。
- 需要修复 DashScope 调用、prompt 或降级逻辑。

## 输入

- 任务目标
- 文本/图片输入
- prompt 草案
- 期望 schema

## 输出

- 调用代码
- prompt 模板
- 异常处理
- 降级路径

## 执行流程

1. 从 .env 读取 DASHSCOPE_API_KEY。
2. 文本接口使用 OpenAI 兼容 DashScope base_url。
3. 多模态接口使用 dashscope.MultiModalConversation.call。
4. 失败时返回 rule_based 结果并记录原因。

## 失败处理

- Key 缺失时不伪造调用结果。
- 接口失败时不阻断主流程，必须降级。

## 关联角色

- qwen-vlm-engineer

## 默认文件

- .env
- src/labsopguard/reasoning.py
- src/labsopguard/video_analysis.py
