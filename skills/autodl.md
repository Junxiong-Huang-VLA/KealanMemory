---
id: autodl
name: /autodl
category: 环境与工程
description: AutoDL 完整工作流：数据上传 → 训练 → 产物下载 → 本地同步
---

# /autodl — AutoDL 完整工作流：数据上传 → 训练 → 产物下载 → 本地同步

## 执行步骤

上传：tar + scp → 训练：ssh + yolo detect train → 下载：scp -r <run_name>/ → 切权重：更新 yaml
注意：RTX 5090 cu128，关机前务必下载产物
