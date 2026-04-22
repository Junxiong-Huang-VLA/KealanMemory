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

## 日常同步

```bash
# 开工前拉最新
git -C D:/KealanMemory pull

# 收工后自动推送（已内置在收工命令里）
收工.bat
```
