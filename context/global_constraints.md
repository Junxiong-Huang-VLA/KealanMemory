# 全局约束（Global Constraints）

> 跨所有项目通用的约束，优先级高于项目级约束。

## API 与服务

- **VLM/LLM 提供商**：优先使用 Qwen / DashScope
- **API Key**：只放 `.env`，禁止硬编码，禁止 commit
- 所有外部 API 调用必须有失败降级处理

## 路径与文件

- 项目代码统一放 D 盘
- 记忆系统根目录：`D:/KealanMemory/`（不移动）
- `.env` 只放项目根目录，不在子目录维护

## 安全规范

- 禁止硬编码任何 credentials
- 禁止把模型权重、数据集、视频文件 commit 进 Git
- 用户输入必须做校验，内部调用不做防御性校验

## 环境规范

- Python 包管理用 conda，每个项目独立环境
- PYTHONPATH 走环境变量，不用 `sys.path.insert`
- Windows 本地开发，Linux 用于 AutoDL 训练

## 代码质量

- commit 前必须通过项目的核心测试
- 禁止 `--no-verify` 跳过 hook
- 不引入不必要的第三方依赖
