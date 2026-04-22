# KealanMemory - 项目简介

## 基本信息

- **项目名称**：KealanMemory
- **项目路径**：`D:/KealanMemory`
- **启动时间**：2026-04-22
- **项目类型**：个人 AI 记忆操作系统 / 本地知识库中台 / 多 AI 协作上下文加载器

## 项目目标

把 `D:/KealanMemory` 建设成安全、可迁移、可验证、可路由、可长期维护的本地 AI 项目记忆系统，为 Claude、Codex 和其他 AI 工具提供一致的个人画像、项目上下文、角色、技能、历史和操作规则。

## 核心链路

```text
memory_map.json -> loader/CLI/Web/hooks -> assembled context -> AI 会话
projects/* -> project_manager.py -> 项目注册/归档/校验
roles + skills + routing_map -> 任务意图路由 -> 专项工作方式
history_index + history_search -> 按需历史注入 -> 长期上下文复用
```

## 技术栈

| 层次 | 技术 |
|---|---|
| 加载协议 | `boot/memory_map.json`, `boot/memory_loader.py`, `boot/load_memory.py` |
| 项目生命周期 | `boot/project_manager.py` |
| 历史检索 | `boot/history_search.py`, `context/history_index.md` |
| Hooks | `boot/hooks/session_start.py`, `boot/hooks/session_end.py`, `boot/hooks/manual_save.py` |
| Web | Flask, `web/app.py`, `web/templates/index.html`, `web/static/` |
| 路由 | `boot/routing_map.json`, `boot/routing_map.md`, `roles/*.md`, `skills/*.md` |
| 验证 | `boot/check_memory_consistency.py`, `tests/`, `schemas/`, `scripts/pre_commit_check.ps1` |

## 关键文件

| 文件 | 作用 |
|---|---|
| `boot/memory_map.json` | 全局加载顺序、项目注册、默认输出位置的单一事实来源 |
| `boot/load_memory.py` | 生成 AI 会话上下文，支持 `--project`、`--full`、`--history` |
| `boot/project_manager.py` | 创建、列出、归档、校验项目记忆 |
| `boot/check_memory_consistency.py` | 健康检查入口，覆盖配置、路径、语法、敏感信息和映射完整性 |
| `boot/routing_map.json` | 意图到 role/skill/default files 的机器可读路由表 |
| `web/app.py` | 本地 Web 运维面板和 API |
| `roles/*.md` | 面向任务的执行角色 |
| `skills/*.md` | 轻量任务命令卡 |
| `tests/` | loader、项目 CLI、Web API、路由和健康检查回归测试 |

## 项目边界

- KealanMemory 只记录记忆系统自身建设、加载协议、Web 管理、hooks、安全、roles、skills、测试和维护计划。
- LabSOPGuard 是业务项目，原则上只记录实验 SOP 检测系统进展，不再承载 KealanMemory 自身优化计划。
- AluminumTubeInspection 是独立业务/实验项目，不作为 KealanMemory 任务载体。
