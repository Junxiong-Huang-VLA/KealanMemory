# 新电脑安装说明

## 前提

- Python 已安装（3.10+）
- `D:/KealanMemory/` 已存在（U盘复制或 git clone）

## 一键安装

双击运行：
```
D:\KealanMemory\install\setup.bat
```

或命令行：
```bash
python D:/KealanMemory/install/setup.py
```

安装脚本会按当前仓库位置渲染 Claude hook 路径，并在修改已有 `~/.claude/settings.json` 前自动备份。`install/claude_settings.json` 只包含 hook 模板，不包含任何真实 token。

## 安装内容

| 内容 | 目标位置 |
|------|---------|
| 开工/收工协议 | `~/.claude/CLAUDE.md` |
| `/me` `/focus` 等 Skills | `~/.claude/commands/` |
| SessionStart/End hooks | `~/.claude/settings.json` |
| 收工命令 | `~/bin/收工.bat` |
| Continue 规则 | `~/.continue/config.yaml` |
| Cline 规则 | `~/.cline/rules.md` |
| Copilot 规则 | `~/.github/copilot-instructions.md` |

## 如果从 GitHub 克隆

```bash
git clone https://github.com/Junxiong-Huang-VLA/KealanMemory.git D:/KealanMemory
python D:/KealanMemory/install/setup.py
```

## 安装后验证

```bash
python D:/KealanMemory/boot/check_memory_consistency.py
python D:/KealanMemory/boot/load_memory.py --list
python D:/KealanMemory/web/app.py
```

Web 依赖需要在目标 Python 环境中安装：

```bash
python -m pip install -r D:/KealanMemory/requirements.txt
```

## 日常同步

```bash
# 开工前拉最新
git -C D:/KealanMemory pull

# 收工后写回记忆
收工.bat
```

默认不会自动 `git push`。如需自动提交/推送，显式设置：

```powershell
$env:KEALAN_MEMORY_AUTO_COMMIT="1"
$env:KEALAN_MEMORY_AUTO_PUSH="1"
```
