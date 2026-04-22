---
id: fe-component
name: /fe-component
category: 前端开发
description: 生成符合项目约束的 Vue 组件，覆盖 API 对接、URL 处理、空值保护和展示字段。
triggers:
  - Vue 组件
  - 前端页面
  - 组件开发
  - 材料展示
  - 视频播放器
roles:
  - vue-frontend-engineer
default_files:
  - frontend-app/src/views/
  - frontend-app/src/components/
  - frontend-app/src/api/
---

# /fe-component - 生成符合项目约束的 Vue 组件，覆盖 API 对接、URL 处理、空值保护和展示字段。

## 适用场景

- 新增实验详情、材料列表或结果展示组件。
- 需要把后端字段安全渲染到页面。

## 输入

- 组件目标
- API 字段
- 交互要求

## 输出

- Vue 组件代码方案
- API 调用方式
- 空值保护点

## 执行流程

1. 确认 API 地址和字段结构。
2. 视频/材料 URL 统一调用 resolveArtifactUrl。
3. 列表字段使用 ?? [] 做默认值。
4. 只展示 display_name 等稳定字段。

## 失败处理

- 字段不确定时先从 Network 或 API 响应确认。
- 视频不播放时转入 /fe-debug。

## 关联角色

- vue-frontend-engineer

## 默认文件

- frontend-app/src/views/
- frontend-app/src/components/
- frontend-app/src/api/
