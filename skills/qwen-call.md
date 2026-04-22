---
id: qwen-call
name: /qwen-call
category: 后端开发
description: 生成 Qwen 文本/多模态调用代码，含 prompt 模板、错误处理和降级逻辑
---

# /qwen-call — 生成 Qwen 文本/多模态调用代码，含 prompt 模板、错误处理和降级逻辑

## 执行步骤

文本：openai.OpenAI(api_key=DASHSCOPE_API_KEY, base_url=dashscope兼容地址).chat.completions.create
多模态：dashscope.MultiModalConversation.call(model=qwen-vl-plus, content=[image+text])
约束：Key 只从 .env 读，失败降级 rule_based
