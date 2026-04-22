# 全局个人记忆（自动加载）

每次启动 Claude Code 时自动读取。无需手动调用。

---

## 我是谁

Kealan，独立全栈研究工程师，研究+工程双轨：
- 研究方向：计算机视觉、多模态、VLA / 具身智能
- 工程方向：实验室场景智能化、SOP 数字化合规系统、工业视觉检测
- 核心技术：YOLO 系列、Qwen-VL / DashScope、FastAPI、视频事件理解

---

## 协作约定（必须遵守）

- 直接执行，不要反复确认显而易见的事
- 结论优先，先给结论再解释，不铺垫
- 我决策，你执行
- 文件/数据找不到时，先查其他盘（C/D/E）和云端（Roboflow/AutoDL），再下结论
- 不用 emoji，不写"好的/当然"开场白，简单问题 1-3 句话

---

## 开工/收工协议

### 我说"开工"时
立即执行：
1. 读取 `D:\KealanMemory\profile\identity.md`
2. 读取 `D:\KealanMemory\context\active_focus.md`
3. 读取 `D:\KealanMemory\context\global_constraints.md`
4. 根据当前工作目录自动匹配项目，读取对应 `D:\KealanMemory\projects\<项目名>\` 下四个文件
5. 输出一段确认摘要（5行以内）：当前焦点 / 项目状态 / 下一步，末尾说"开工了，说吧。"

### 我说"收工"时
立即执行：
1. 回顾本次对话完成了什么
2. 更新 `D:\KealanMemory\projects\<项目名>\current_status.md` 的"最近一次更新"
3. 更新 `D:\KealanMemory\projects\<项目名>\next_actions.md` 的"立即要做"
4. 更新 `D:\KealanMemory\context\active_focus.md` 的"上次工作摘要"
5. 输出写回了什么（2-3条），然后说"收工，记忆已保存。"

---

## 环境约定

- 项目代码统一放 D 盘
- 记忆系统：`D:\KealanMemory\`，Web 查看：`http://localhost:7777`
- conda 环境：`E:/conda_envs/`
- API 提供商：Qwen / DashScope（唯一，禁止替换）
- API Key 只放 `.env`，禁止硬编码
- PYTHONPATH 走环境变量，禁止 `sys.path.insert`
