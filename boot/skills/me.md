# /me — 加载个人记忆

用法：
- `/me` — 加载核心记忆 + 当前焦点
- `/me LabSOPGuard` — 加载核心记忆 + 指定项目记忆

## 执行步骤

### 无参数时（`/me`）

依次读取以下文件：
1. `D:\KealanMemory\profile\identity.md`
2. `D:\KealanMemory\profile\work_style.md`
3. `D:\KealanMemory\profile\preferences.md`
4. `D:\KealanMemory\operating_rules\communication_rules.md`
5. `D:\KealanMemory\context\active_focus.md`
6. `D:\KealanMemory\context\global_constraints.md`

读取完成后输出一段 3-5 行的确认（我的角色 / 当前焦点 / 协作约定），末尾说"记忆已加载，说吧。"

### 有参数时（`/me <项目名>`）

在上述 6 个文件基础上，追加读取：
7. `D:\KealanMemory\projects\$ARGUMENTS\project_brief.md`
8. `D:\KealanMemory\projects\$ARGUMENTS\current_status.md`
9. `D:\KealanMemory\projects\$ARGUMENTS\constraints.md`
10. `D:\KealanMemory\projects\$ARGUMENTS\next_actions.md`

输出 5-8 行确认（角色 / 项目状态 / 核心约束 / 下一步），末尾说"记忆已加载，说吧。"

### 注意
- 不要全量列出文件内容，只输出确认摘要
- 如果某文件不存在，跳过并继续，不要报错中断
