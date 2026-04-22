# /focus — 查看或更新当前工作焦点

用法：
- `/focus` — 读取并显示当前焦点
- `/focus <新焦点描述>` — 将当前焦点更新为指定内容

## 执行步骤

### 无参数（`/focus`）

读取 `D:\KealanMemory\context\active_focus.md`，输出：
- 当前阶段
- 本周最重要的 3 件事
- 当前卡点

### 有参数（`/focus <内容>`）

1. 读取 `D:\KealanMemory\context\active_focus.md`
2. 将"本周最重要的 3 件事"中第一条更新为 `$ARGUMENTS`
3. 同时更新"最近一次更新"的日期和描述
4. 写回文件
5. 输出更新后的焦点摘要确认
