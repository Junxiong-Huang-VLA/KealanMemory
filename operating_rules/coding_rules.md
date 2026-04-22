# 代码规范（Coding Rules）

## 通用原则

- 代码写给人读，其次才是机器执行
- 不为假想的未来需求预留接口
- 三行相似代码才考虑抽象，不提前抽象
- 遇到安全漏洞（SQL 注入 / 命令注入 / XSS）主动指出并修复

## Python 规范

### 结构
- 包名前缀与项目名一致（如 `labsopguard.*`）
- 禁止在入口文件中 `sys.path.insert`，用 `PYTHONPATH` 环境变量
- 配置读取统一走 yaml 或 `.env`，禁止硬编码
- 类型注解：函数签名必须有，函数体内部可选

### 命名
- 变量/函数：`snake_case`
- 类：`PascalCase`
- 常量：`UPPER_SNAKE_CASE`
- 私有方法：`_single_underscore`

### 注释
- 默认不写注释
- 只在以下情况写：隐含约束、绕过 bug 的 workaround、会让读者意外的行为
- 禁止写多行 docstring（一行描述即可，或不写）
- 禁止写"这个函数做了 X"式注释（函数名已经说了）

### 错误处理
- 只在系统边界（用户输入、外部 API、文件 IO）做校验
- 不对内部函数做防御性校验
- 异常要有足够信息定位问题，不要 `except Exception: pass`

## FastAPI 规范

- 路由统一前缀 `/api/v1/`
- 请求/响应 schema 用 Pydantic model 定义
- 耗时操作走异步任务队列，不同步阻塞
- 错误响应格式：`{"detail": "...", "error_code": "..."}`

## 前端规范

- API 请求统一封装，不在组件里直接 fetch
- 硬编码 URL 统一走配置（如 `resolveArtifactUrl()`）
- 禁止在页面展示内部调试字段（如 `evidence_summary`）

## Git 规范

- commit message 用英文，格式：`type: brief description`
  - type: `feat` / `fix` / `refactor` / `docs` / `test` / `chore`
- 禁止 `--no-verify` 跳过 hook
- 禁止把 `.env` / API Key / 权重文件 commit 进仓库
- 大文件（模型权重、视频）用 `.gitignore` 排除
