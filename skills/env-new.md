---
id: env-new
name: /env-new
category: 环境与工程
description: 初始化新项目或新机器环境，覆盖 conda、依赖、CUDA、.env 模板和可用性验证。
triggers:
  - 新环境
  - conda
  - requirements
  - .env
  - CUDA
  - 新机器
roles:
  - autodl-devops
  - system-architect
default_files:
  - requirements.txt
  - .env
  - scripts/
---

# /env-new - 初始化新项目或新机器环境，覆盖 conda、依赖、CUDA、.env 模板和可用性验证。

## 适用场景

- 新机器首次部署 LabSOPGuard。
- 新项目需要标准 Python/CUDA/Qwen 环境。

## 输入

- 环境名
- Python 版本
- CUDA/PyTorch 版本
- 是否需要 DashScope

## 输出

- 环境创建命令
- 依赖安装命令
- .env 模板
- 验证命令

## 执行流程

1. 创建 Python 3.11 conda 环境。
2. 安装 PyTorch、ultralytics、dashscope、openai 等依赖。
3. 生成 .env 必要键说明。
4. 验证 torch.cuda.is_available 和 Qwen key 读取。

## 失败处理

- CUDA 不匹配时先确认 torch build 与驱动版本。
- 依赖安装失败时锁定失败包，不整体重装。

## 关联角色

- autodl-devops
- system-architect

## 默认文件

- requirements.txt
- .env
- scripts/
