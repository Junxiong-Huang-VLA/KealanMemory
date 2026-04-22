#!/usr/bin/env python3
"""
SessionEnd Hook — 对话结束时自动总结本次工作，写回记忆系统。

流程：
1. 读取当前 session 的对话历史（.claude/projects/.../session.jsonl）
2. 调用 DashScope/Qwen 对话历史做摘要
3. 将摘要写入对应项目的 current_status.md 和 active_focus.md
"""

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime

MEMORY_ROOT = Path("D:/KealanMemory")
CLAUDE_DIR = Path(os.path.expanduser("~/.claude"))
MAP_FILE = MEMORY_ROOT / "boot/memory_map.json"

# DashScope 配置（从 .env 读取，避免硬编码）
def get_api_key() -> str:
    for env_path in [
        Path("D:/LabEmbodiedVLA/LabSOPGuard/.env"),
        Path(os.getcwd()) / ".env",
        Path(os.path.expanduser("~/.env")),
    ]:
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("DASHSCOPE_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("DASHSCOPE_API_KEY", "")


def detect_project(cwd: str) -> str:
    if not cwd:
        return ""
    cwd_lower = cwd.lower().replace("\\", "/")
    try:
        mem_map = json.loads(MAP_FILE.read_text(encoding="utf-8"))
        projects = mem_map.get("projects", [])
    except Exception:
        return ""
    for p in projects:
        if p == "_template":
            continue
        if p.lower() in cwd_lower:
            if (MEMORY_ROOT / f"projects/{p}/current_status.md").exists():
                return p
    return ""


def extract_conversation(session_id: str, cwd: str) -> str:
    """从 session jsonl 提取对话文本（只取 user 问题 + assistant 最后一段回复）"""
    # 查找 session 文件
    project_key = cwd.replace("\\", "-").replace("/", "-").replace(":", "").lstrip("-")
    candidates = list(CLAUDE_DIR.glob(f"projects/**/{session_id}.jsonl"))
    if not candidates:
        # 模糊查找
        candidates = list(CLAUDE_DIR.glob(f"projects/{project_key[:20]}*/{session_id}.jsonl"))
    if not candidates:
        return ""

    session_file = candidates[0]
    lines = session_file.read_text(encoding="utf-8", errors="ignore").splitlines()

    turns = []
    for line in lines:
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") == "user":
            msg = d.get("message", {})
            content = msg.get("content", "")
            if isinstance(content, list):
                text = " ".join(c.get("text", "") for c in content if c.get("type") == "text")
            else:
                text = str(content)
            text = text.strip()
            if text and len(text) > 5:
                turns.append(f"用户：{text[:300]}")
        elif d.get("type") == "assistant":
            msg = d.get("message", {})
            content = msg.get("content", [])
            if isinstance(content, list):
                text = " ".join(c.get("text", "") for c in content if c.get("type") == "text")
            else:
                text = str(content)
            text = text.strip()
            if text and len(text) > 10:
                turns.append(f"Claude：{text[:500]}")

    # 只取最后 30 轮，防止 token 超限
    return "\n\n".join(turns[-30:])


def summarize_with_qwen(conversation: str, project: str) -> dict:
    """调用 DashScope 对对话做结构化摘要"""
    api_key = get_api_key()
    if not api_key:
        return {}

    try:
        import openai
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        prompt = f"""以下是一段 Claude Code 开发对话记录（项目：{project or '未知'}）。
请提取：
1. 本次完成了什么（3条以内，每条一句话）
2. 发现了什么问题或新信息（2条以内）
3. 下一步最重要的事（1-2条）

输出格式为 JSON：
{{
  "completed": ["...", "..."],
  "findings": ["...", "..."],
  "next_actions": ["...", "..."]
}}

对话记录：
{conversation[:3000]}
"""
        resp = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3,
        )
        text = resp.choices[0].message.content.strip()
        # 提取 JSON
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            return json.loads(match.group())
    except Exception as e:
        # 失败时静默，不打断用户
        pass
    return {}


def update_memory(project: str, summary: dict, cwd: str):
    """将摘要写入记忆文件"""
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    completed = summary.get("completed", [])
    findings = summary.get("findings", [])
    next_actions = summary.get("next_actions", [])

    if not completed and not next_actions:
        return  # 摘要为空，跳过

    # 写入 current_status.md
    if project:
        status_file = MEMORY_ROOT / f"projects/{project}/current_status.md"
        if status_file.exists():
            content = status_file.read_text(encoding="utf-8", errors="replace")
            update_block = f"\n\n## 最近一次更新\n\n- **时间**：{today}\n- **做了什么**：\n"
            for item in completed:
                update_block += f"  - {item}\n"
            if findings:
                update_block += "- **发现**：\n"
                for item in findings:
                    update_block += f"  - {item}\n"
            if "## 最近一次更新" in content:
                idx = content.index("## 最近一次更新")
                content = content[:idx].rstrip() + update_block
            else:
                content = content.rstrip() + update_block
            status_file.write_text(content, encoding="utf-8")

    # 写入 next_actions.md
    if project and next_actions:
        actions_file = MEMORY_ROOT / f"projects/{project}/next_actions.md"
        if actions_file.exists():
            content = actions_file.read_text(encoding="utf-8", errors="replace")
            action_block = f"## 立即要做（更新于 {today}）\n\n"
            for i, item in enumerate(next_actions, 1):
                action_block += f"{i}. {item}\n"
            if "## 立即要做" in content:
                idx = content.index("## 立即要做")
                rest = content[idx:]
                next_h2 = re.search(r"\n## ", rest[3:])
                if next_h2:
                    end = idx + 3 + next_h2.start()
                    content = content[:idx] + action_block + "\n" + content[end:]
                else:
                    content = content[:idx] + action_block
            else:
                content = action_block + "\n" + content
            actions_file.write_text(content, encoding="utf-8")

    # 写入 active_focus.md 的"上次工作摘要"
    focus_file = MEMORY_ROOT / "context/active_focus.md"
    if focus_file.exists():
        content = focus_file.read_text(encoding="utf-8")
        summary_block = f"\n\n## 上次工作摘要（{today}）\n\n"
        if project:
            summary_block += f"**项目**：{project}\n\n"
        for item in completed:
            summary_block += f"- {item}\n"
        if "## 上次工作摘要" in content:
            idx = content.index("## 上次工作摘要")
            content = content[:idx].rstrip() + "\n\n" + summary_block
        else:
            content = content.rstrip() + "\n\n" + summary_block
        focus_file.write_text(content, encoding="utf-8")


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except Exception:
        hook_input = {}

    cwd = hook_input.get("cwd", os.getcwd())
    session_id = hook_input.get("session_id", "")
    exit_reason = hook_input.get("exit_reason", "")

    # clear/resume 不触发（用户主动清除或切换，不是真正结束）
    if exit_reason in ("clear",):
        sys.exit(0)

    project = detect_project(cwd)

    # 提取对话历史
    if session_id:
        conversation = extract_conversation(session_id, cwd)
    else:
        conversation = ""

    if not conversation:
        sys.exit(0)

    # 调 Qwen 做摘要
    summary = summarize_with_qwen(conversation, project)

    # 写回记忆
    if summary:
        update_memory(project, summary, cwd)
        # 自动推送到 GitHub
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        os.system(f'cd D:/KealanMemory && git add . && git commit -m "sync: {date_str}" && git push')

    sys.exit(0)


if __name__ == "__main__":
    main()
