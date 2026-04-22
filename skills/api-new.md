---
id: api-new
name: /api-new
category: 后端开发
description: 生成完整 FastAPI 路由 + Pydantic Schema + 异步任务队列接入代码
---

# /api-new — 生成完整 FastAPI 路由 + Pydantic Schema + 异步任务队列接入代码

## 执行步骤

生成规范：路由前缀 /api/v1/，耗时>1s 走异步队列，错误格式 {detail, error_code}
模板：APIRouter + BaseModel Request/Response + async handler + task_queue.enqueue
