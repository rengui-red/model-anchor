\# Changelog



本文件记录 ModelAnchor 的所有版本变更。格式遵循 Keep a Changelog，版本号遵循语义化版本。



断点格式的字段变更视为破坏性变更，必须在条目中写明兼容说明与迁移方式。



\## \[Unreleased]



\### 计划中

\- v0.2：钩子提示词（`hooks/stop-update.md`、`hooks/anchor-update.md`）

\- v0.2：多模型 profile（claude / deepseek / doubao / generic）

\- v0.2：full 与 task-scoped 打包模式



\## \[0.1.0] - 2026-11-21



\### 新增

\- `templates/断点.md`：四字段断点模板（当前 / 下一步 / 阻塞 / 交接备注）

\- `anchor.md`：通配档案层字段约定（机器可读约定 + 断点层字段定义）

\- `packer/pack.py`：minimal 打包模式、`--init` 模板生成、过期检测

\- `load\_anchor()` 函数边界：未来云端/MCP 版本只替换此函数体



\### 设计约束

\- 仅 Python 标准库，零外部依赖

\- 本地运行，不托管任何用户数据

\- 字段约定从第一天起为全部档案层级设计，v0.1 只实现断点层











