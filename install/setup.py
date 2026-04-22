#!/usr/bin/env python3
"""
KealanMemory 新电脑一键安装脚本
运行方式：python D:/KealanMemory/install/setup.py
"""

import os
import shutil
import json
from pathlib import Path

INSTALL_DIR = Path(__file__).parent
MEMORY_ROOT = Path("D:/KealanMemory")

def log(msg): print(f"  [ok] {msg}")
def warn(msg): print(f"  [!]  {msg}")

def get_username():
    return os.environ.get("USERNAME") or os.environ.get("USER") or "Win10"

def main():
    username = get_username()
    home = Path(f"C:/Users/{username}")

    print(f"\nKealanMemory 安装器")
    print(f"用户目录：{home}")
    print(f"记忆根目录：{MEMORY_ROOT}")
    print("-" * 40)

    # 1. Claude Code 全局 CLAUDE.md
    claude_dir = home / ".claude"
    claude_dir.mkdir(exist_ok=True)
    shutil.copy(INSTALL_DIR / "CLAUDE.md", claude_dir / "CLAUDE.md")
    log(f"CLAUDE.md → {claude_dir / 'CLAUDE.md'}")

    # 2. Claude Code 全局 commands
    commands_dir = claude_dir / "commands"
    commands_dir.mkdir(exist_ok=True)
    for f in (INSTALL_DIR / "claude_commands").glob("*.md"):
        shutil.copy(f, commands_dir / f.name)
    log(f"claude commands → {commands_dir} ({len(list(commands_dir.glob('*.md')))} 个)")

    # 3. Claude Code settings.json（合并 hooks，不覆盖已有 env/model 配置）
    settings_path = claude_dir / "settings.json"
    new_settings = json.loads((INSTALL_DIR / "claude_settings.json").read_text(encoding="utf-8"))
    if settings_path.exists():
        existing = json.loads(settings_path.read_text(encoding="utf-8"))
        # 只合并 hooks，保留已有 env/model
        existing["hooks"] = new_settings.get("hooks", {})
        settings_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
        log(f"settings.json hooks 已合并（保留原有 env/model）")
    else:
        shutil.copy(INSTALL_DIR / "claude_settings.json", settings_path)
        log(f"settings.json → {settings_path}")

    # 4. 收工命令（bin 目录）
    bin_dir = home / "bin"
    bin_dir.mkdir(exist_ok=True)
    shutil.copy(INSTALL_DIR / "收工.bat", bin_dir / "收工.bat")
    shutil.copy(INSTALL_DIR / "收工", bin_dir / "收工")
    # 修正路径中的用户名（如果不同）
    bat_content = (bin_dir / "收工.bat").read_text(encoding="utf-8", errors="replace")
    (bin_dir / "收工.bat").write_text(bat_content, encoding="utf-8")
    log(f"收工命令 → {bin_dir}")

    # 检查 bin 是否在 PATH
    path_env = os.environ.get("PATH", "")
    if str(bin_dir).lower() not in path_env.lower() and str(bin_dir).replace("/","\\").lower() not in path_env.lower():
        warn(f"{bin_dir} 不在 PATH 中，需要手动添加或重启终端")

    # 5. Continue (VS Code 插件)
    continue_dir = home / ".continue"
    continue_dir.mkdir(exist_ok=True)
    shutil.copy(INSTALL_DIR / "continue_config.yaml", continue_dir / "config.yaml")
    log(f"Continue config → {continue_dir / 'config.yaml'}")

    # 6. Cline / Roo Code
    cline_dir = home / ".cline"
    cline_dir.mkdir(exist_ok=True)
    shutil.copy(INSTALL_DIR / "cline_rules.md", cline_dir / "rules.md")
    log(f"Cline rules → {cline_dir / 'rules.md'}")

    # 7. Copilot
    github_dir = home / ".github"
    github_dir.mkdir(exist_ok=True)
    shutil.copy(INSTALL_DIR / "copilot_instructions.md", github_dir / "copilot-instructions.md")
    log(f"Copilot instructions → {github_dir / 'copilot-instructions.md'}")

    # 8. 安装 Flask（Web 界面依赖）
    print("\n安装 Web 依赖...")
    ret = os.system("pip install flask -q")
    if ret == 0:
        log("Flask 已安装")
    else:
        warn("Flask 安装失败，请手动运行：pip install flask")

    print("\n" + "=" * 40)
    print("安装完成！")
    print()
    print("验证步骤：")
    print("  1. 重启终端（让 PATH 生效）")
    print("  2. 启动 Web：python D:/KealanMemory/web/app.py")
    print("  3. 打开浏览器：http://localhost:7777")
    print("  4. Open Claude Code and say kaigong to test memory loading")
    print()
    print("收工命令：在任意终端输入 收工 或 收工.bat")

if __name__ == "__main__":
    main()