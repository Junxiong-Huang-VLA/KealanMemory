# 个人偏好（Preferences）

## 路径与目录

- **所有项目统一放在 D 盘**，不放 C 盘（C 盘只放系统和 conda）
- 主项目根目录：`D:/` 下按项目名建文件夹
- 记忆系统根目录：`D:/KealanMemory/`
- conda 环境：`E:/conda_envs/` 或 `E:/AI_Data/miniconda3/`
- 数据集：`D:/` 下对应项目的 `data/` 子目录

## 命名习惯

- 文件夹：`snake_case` 或 `CamelCase`（保持项目内一致）
- Python 文件：`snake_case.py`
- 配置文件：`xxx_runtime.yaml` / `xxx_config.yaml`
- 训练 run 名：`模型名_数据集描述_版本号`，如 `yolo26s_autodl_8_1_1`
- 不用日期作为主要命名（除非是 history 归档文件）

## 环境管理

- 每个项目独立 conda 环境，环境名与项目名一致
- 依赖文件优先用 `environment.yml`，pip 补充用 `requirements.txt`
- `.env` 文件统一放项目根目录，禁止在子目录单独维护
- API Key 只放 `.env`，禁止硬编码到代码或 commit

## 语言偏好

- 与 Claude 对话：**中文**
- 代码：英文（变量名、函数名、注释默认英文，除非特别说明）
- 文档：中文标题 + 中文内容，技术术语保留英文原词
- commit message：英文
- 对外文档（README 等）：视目标受众决定

## 文档生成偏好

- 优先生成 Markdown
- 不需要目录（TOC）除非文档超过 5 个一级标题
- 表格优于列表
- 代码块必须标注语言
- 不写没有实质内容的占位段落

## 代码生成偏好

- 不写多余注释（逻辑复杂时例外）
- 不过度封装（3 行能解决的不建 class）
- 不写防御性代码（只在系统边界做校验）
- 不引入不必要依赖
- 函数命名要自解释，不需要注释说明 what，只说明 why（如果需要的话）

## 工具偏好

| 场景 | 首选工具 |
|------|---------|
| 标注 | Roboflow |
| 版本管理 | Git + GitHub |
| 远程训练 | AutoDL |
| 本地终端 | PowerShell / bash (Git Bash) |
| 编辑器 | VS Code / Claude Code |
| 画图 | draw.io / Mermaid |
