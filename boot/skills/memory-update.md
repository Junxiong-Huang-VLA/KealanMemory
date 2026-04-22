# /memory-update — 更新项目记忆

对话结束时调用，自动把本次进展写入记忆系统，下次对话直接延续。

用法：
- `/memory-update <项目名>` — 更新指定项目的状态和下一步

## 执行步骤

1. 回顾本次对话做了什么（不需要我重新描述）
2. 读取 `D:\KealanMemory\projects\$ARGUMENTS\current_status.md`
3. 在"最近一次更新"部分写入：
   - 时间：今天日期
   - 做了什么：本次对话的关键产出（1-3 条）
4. 读取 `D:\KealanMemory\projects\$ARGUMENTS\next_actions.md`
5. 根据本次对话结果，更新"立即要做"列表
6. 同时更新 `D:\KealanMemory\context\active_focus.md` 的"上次工作摘要"
7. 输出更新摘要（更新了哪些文件、改了什么）
