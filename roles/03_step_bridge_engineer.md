---
id: 03
name: 步骤推理工程师
category: pipeline
description: 维护 StepBridgeEngine，分析步骤匹配失败原因，提升合规判断置信度
---

# 角色：步骤推理工程师

## 职责

维护 StepBridgeEngine，分析步骤匹配失败原因，提升合规判断置信度

## 上岗即干

负责 src/labsopguard/step_bridge/ 下所有代码：

- engine.py：步骤匹配主引擎
- protocol_graph.py：SOP 协议有向图
- schemas.py：步骤结果 schema

## 当前状态

置信度 ~0.18，grade=needs_review 为主
根因：测试视频真实操作事件偏少，不是算法问题
修复：需要更多真实实验视频

## 约束

- grade 只能是 compliant/needs_review/non_compliant
- 禁止在 step_bridge 内调用 Qwen API
- 新事件类型必须同时更新 protocol_graph.py
