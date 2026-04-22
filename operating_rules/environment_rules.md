# 环境配置规范（Environment Rules）

## 本地硬件环境

| 设备 | 规格 | 用途 |
|------|------|------|
| 本地主机 | RTX 4050 Laptop 6GB VRAM, Win10 | 推理、前端开发、调试 |
| AutoDL 服务器 | RTX 5090 32GB VRAM, Ubuntu 22.04 | 模型训练 |

## 磁盘分区约定

| 盘符 | 用途 |
|------|------|
| C:/ | 系统、用户目录（不放项目代码） |
| D:/ | 所有项目代码、数据集、模型权重 |
| E:/ | conda 环境、大型数据备份 |

## conda 环境规范

- 环境统一放 `E:/conda_envs/<项目名>` 或 `E:/AI_Data/miniconda3/envs/`
- 每个项目独立环境，环境名与项目名一致
- Python 版本：3.10+ 优先（3.13 兼容性注意 torch 版本）
- CUDA：本地 cu124，AutoDL cu128

## 环境变量规范

- secrets 统一放项目根目录 `.env`
- 所有服务启动前执行 `load_dotenv('.env')`
- 禁止在子目录单独维护 `.env`
- 关键变量命名约定：
  ```
  <服务名>_API_KEY       # API 密钥
  <服务名>_BASE_URL      # API 地址
  <功能名>_ENABLED       # 功能开关（true/false）
  <功能名>_MODEL         # 模型名称
  ```

## AutoDL 工作流

```bash
# 上传数据
scp -r data/dataset/ user@autodl:/path/
# 下载权重
scp user@autodl:/path/best.pt outputs/training/<run>/weights/
# 下载完整训练产物（含 results.csv、混淆矩阵等）
scp -r user@autodl:/path/run/ outputs/training/<run>/
```

## 端口约定

| 服务 | 端口 |
|------|------|
| FastAPI 后端 | 8000 |
| Vite 前端 | 5173（被占用 +1） |
| Redis | 6379 |

## PYTHONPATH 规范

- 后端启动统一设 `PYTHONPATH=src`
- 禁止在代码中 `sys.path.insert`
- 包名前缀与项目 src 下目录名一致
