\# 项目指令



\## 技术栈

Python 3.11 + FastAPI，不使用 ORM，数据库访问统一走 `db/query.py`。



\## 目录约定

\- `api/` 放路由，`service/` 放业务逻辑，`utils/` 放工具函数

\- 新增文件必须在 `docs/index.md` 登记一行



\## 红线

\- 不引入新依赖，除非用户明确同意

\- API 路径一旦上线不可变更

