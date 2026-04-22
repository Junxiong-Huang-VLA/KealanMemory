# 项目规范（Project Rules）

## 项目初始化规范

新项目必须包含：
```
项目名/
├── .env                    # API Key 等敏感配置（不 commit）
├── .gitignore
├── README.md
├── environment.yml         # conda 环境
├── requirements.txt        # pip 补充依赖
├── configs/                # 所有配置文件（yaml）
├── src/<项目名>/           # Python 源码包
├── data/                   # 数据（.gitignore 排除大文件）
│   ├── raw/
│   ├── interim/
│   └── processed/
├── outputs/                # 模型输出、实验结果
├── tests/                  # 测试文件
├── scripts/                # 启动/部署/工具脚本
└── docs/                   # 文档
```

## 配置管理规范

- 所有可变参数走 yaml 配置文件，不硬编码
- 配置文件放 `configs/` 目录下，按功能分文件
- 运行时配置（模型路径、阈值等）单独一个 `*_runtime.yaml`
- `.env` 只放 secrets（API Key、DB 密码等）

## 数据集规范（YOLO）

- 统一格式：YOLOv8 txt（`class cx cy w h`）
- 目录结构：`images/{train,val,test}/` + `labels/{train,val,test}/`
- 划分比例：8:1:1（train:val:test）
- 类别定义：`dataset.yaml`，唯一真实来源
- 标注平台：Roboflow（云端管理，导出 YOLOv8 zip 后合并本地）

## 模型权重规范

- 权重路径统一走配置文件，禁止硬编码
- 当前最佳权重配置在 `configs/model/*_runtime.yaml` 的 `model` 字段
- 每次训练产物存 `outputs/training/<run_name>/`，至少保留 `best.pt` + `results.csv`
- 切换权重只改 yaml，不改代码

## 文档规范

- 每个项目必须有 `LabSOPGuard.md` 或等效的开发约束文档
- 重要决策记录在 `docs/decisions/` 或项目记忆的 `decisions.md`
- 训练结果记录在 `docs/training_report.md`

## 项目记忆规范

新项目启动时，在 `D:/KealanMemory/projects/<项目名>/` 下创建记忆文件：
- `project_brief.md`：目标、背景、核心链路
- `current_status.md`：当前进度、评级、已完成/待完成
- `constraints.md`：硬约束、禁止事项
- `next_actions.md`：下一步优先级队列
- `decisions.md`：关键决策记录
