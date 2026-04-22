# 启动引导词（Startup Prompt）

> 复制以下内容粘贴给 Claude，作为新对话的第一条消息。
> 或使用 load_memory.py 自动生成 assembled_context.txt 后粘贴。

---

## 默认加载（无项目）

```
你现在需要加载我的个人记忆系统，根目录在 D:\KealanMemory。

请按以下顺序依次读取文件，不要跳过，不要全量读取整个目录：
1. D:\KealanMemory\profile\identity.md
2. D:\KealanMemory\profile\work_style.md
3. D:\KealanMemory\profile\preferences.md
4. D:\KealanMemory\operating_rules\communication_rules.md
5. D:\KealanMemory\context\active_focus.md
6. D:\KealanMemory\context\global_constraints.md

读取完成后，输出一段 3-5 行的上下文确认（我的角色、当前焦点、协作约定），
然后说"记忆加载完成，说吧。"，等待我的指令。
不要问我要做什么，不要展开解释。
```

---

## 指定项目加载（以 LabSOPGuard 为例）

```
你现在需要加载我的个人记忆系统，根目录在 D:\KealanMemory。

请按以下顺序依次读取：
1. D:\KealanMemory\profile\identity.md
2. D:\KealanMemory\profile\work_style.md
3. D:\KealanMemory\profile\preferences.md
4. D:\KealanMemory\operating_rules\communication_rules.md
5. D:\KealanMemory\context\active_focus.md
6. D:\KealanMemory\context\global_constraints.md
7. D:\KealanMemory\projects\LabSOPGuard\project_brief.md
8. D:\KealanMemory\projects\LabSOPGuard\current_status.md
9. D:\KealanMemory\projects\LabSOPGuard\constraints.md
10. D:\KealanMemory\projects\LabSOPGuard\next_actions.md

读取完成后，输出一段 5-8 行的上下文确认（我的角色、项目状态、当前约束、下一步），
然后说"记忆加载完成，说吧。"
```

---

## 快速版（纯文本拼接，用 assembled_context.txt）

```
以下是我的个人记忆上下文，请完整读取并按此行事：

[粘贴 assembled_context.txt 的内容]

读取完成后说"记忆加载完成，说吧。"
```
