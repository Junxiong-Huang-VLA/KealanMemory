# /new-project — 新建项目记忆

接到新项目时调用，30 秒完成记忆初始化。

用法：
- `/new-project <项目名>`

## 执行步骤

1. 检查 `D:\KealanMemory\projects\$ARGUMENTS\` 是否已存在，若存在提示确认是否覆盖
2. 从模板复制：将 `D:\KealanMemory\projects\_template\` 下所有文件复制到 `D:\KealanMemory\projects\$ARGUMENTS\`
3. 在 `D:\KealanMemory\boot\memory_map.json` 的 `projects` 数组中追加项目名
4. 在 `D:\KealanMemory\context\active_focus.md` 的"当前阶段"更新为新项目
5. 向我提问以下信息，逐条填入 `project_brief.md`：
   - 项目目标（一句话）
   - 项目路径（D盘哪个目录）
   - 核心技术栈
   - 第一个里程碑是什么
6. 输出创建结果和文件路径，提示使用 `/me $ARGUMENTS` 加载
