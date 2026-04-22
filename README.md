# 个人记忆系统（Claude Memory System）

本地跨项目记忆中台，根目录固定在 `D:\KealanMemory`。
任何新项目、新对话，先加载这里，Claude 立即知道你是谁、怎么工作、当前在做什么。

---

## 自动化机制（无需任何操作）

| 时机 | 触发方式 | 效果 |
|------|---------|------|
| 打开任何 Claude Code 对话 | `SessionStart` hook 自动执行 | 核心记忆 + 项目记忆注入 Claude 上下文 |
| 关闭/结束对话 | `SessionEnd` hook 自动执行 | 调 Qwen 总结本次进展，写回记忆文件 |
| 新项目第一次对话 | 说"新项目" / `/new-project 名字` | 30 秒初始化项目记忆 |
| 使用其他 AI（GPT/Gemini/Cursor） | 复制 `boot/AI_ONBOARDING.md` 中的接入 Prompt | 任何 AI 都能读写记忆系统 |

---

## 快速开始

### 方式一：双击 bat（最简单）

```
D:\KealanMemory\boot\start_memory.bat             # 仅核心记忆
D:\KealanMemory\boot\start_memory.bat LabSOPGuard # 核心 + 项目记忆
```
自动生成 `assembled_context.txt`，用记事本打开，复制内容粘贴给 Claude。

### 方式二：Python 脚本

```bash
python D:/KealanMemory/boot/load_memory.py                        # 核心记忆
python D:/KealanMemory/boot/load_memory.py --project LabSOPGuard  # + 项目记忆
python D:/KealanMemory/boot/load_memory.py --project LabSOPGuard --full  # + 完整规范
python D:/KealanMemory/boot/load_memory.py --list                 # 列出所有项目
```

### 方式三：PowerShell

```powershell
.\boot\load_memory.ps1
.\boot\load_memory.ps1 -Project LabSOPGuard
.\boot\load_memory.ps1 -Project LabSOPGuard -Full
.\boot\load_memory.ps1 -List
```

### 方式四：复制启动引导词（手动）

参考 `boot/startup_prompt.md`，复制对应的引导词粘贴给 Claude。

---

## 目录结构

```
D:\KealanMemory\
├── README.md                      ← 你在这里
├── boot\
│   ├── load_order.md              ← 加载顺序规范
│   ├── startup_prompt.md          ← 可复制的 Claude 引导词
│   ├── memory_map.json            ← 机器可读索引
│   ├── load_memory.py             ← Python 拼接脚本
│   ├── load_memory.ps1            ← PowerShell 脚本
│   ├── start_memory.bat           ← 双击启动入口
│   └── assembled_context.txt      ← 自动生成，粘贴给 Claude
├── profile\
│   ├── identity.md                ← 角色定位、技术方向、长期目标
│   ├── work_style.md              ← AI 协作约定、输出偏好
│   ├── expertise.md               ← 技术专长（按需加载）
│   └── preferences.md             ← 路径、命名、工具偏好
├── operating_rules\
│   ├── coding_rules.md            ← 代码规范
│   ├── project_rules.md           ← 项目初始化规范
│   ├── communication_rules.md     ← 沟通规范（默认加载）
│   └── environment_rules.md       ← 环境配置规范
├── projects\
│   ├── _template\                 ← 新项目记忆模板
│   │   ├── project_brief.md
│   │   ├── current_status.md
│   │   ├── constraints.md
│   │   ├── milestones.md
│   │   ├── next_actions.md
│   │   └── decisions.md
│   └── LabSOPGuard\               ← 当前主项目
│       ├── project_brief.md
│       ├── current_status.md
│       ├── constraints.md
│       ├── milestones.md
│       ├── next_actions.md
│       └── decisions.md
├── context\
│   ├── active_focus.md            ← 当前阶段焦点（默认加载）
│   ├── global_constraints.md      ← 跨项目通用约束（默认加载）
│   ├── history_index.md           ← 历史检索入口（按需查）
│   └── history\                   ← 历史决策/踩坑（不自动加载）
└── archive\                       ← 归档（不自动加载）
    ├── old_projects\
    └── deprecated_notes\
```

---

## 维护指南

### 新建项目记忆
```bash
# 复制模板
cp -r D:/KealanMemory/projects/_template D:/KealanMemory/projects/新项目名
# 填写各文件内容
# 在 boot/memory_map.json 的 projects 数组中添加项目名
```

### 更新当前焦点
直接编辑 `context/active_focus.md`，更新"本周最重要的 3 件事"和"当前卡点"。

### 追加历史决策
在 `context/history/` 下新建文件（格式：`YYYY-MM-主题.md`），
然后在 `context/history_index.md` 中添加索引行。

### 更新项目状态
开发结束后更新：
- `projects/<项目名>/current_status.md`（完成了什么、新的待办）
- `projects/<项目名>/next_actions.md`（下次要做什么）
- `context/active_focus.md`（如果焦点变了）
