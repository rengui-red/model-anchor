\# 钩子配置



钩子的本质是提示词，不是代码。本插件不写任何工具特定的集成代码。



\## 文件



| 文件 | 用途 |

|---|---|

| `stop-update.md` | 会话结束时增量更新断点 |

| `anchor-update.md` | 用户手动触发 `/anchor-update` 时刷新断点 |



\## Claude Code



将 `stop-update.md` 的内容配置为 Stop 钩子的 `prompt` 类型处理器。



\## Cursor



将 `anchor-update.md` 配置为项目规则或自定义命令，在关键节点手动触发。



\## 通用方式（不配钩子）



不使用任何钩子时，在关键节点把 `anchor-update.md` 的内容粘贴给任意 AI，让其按规则更新断点。这是最小可用路径。



\## 迁移路径（已定义，未实现）



当前以 `prompt` 形式提供。未来若有自建服务，可迁移为 `http` 类型（请求体参考 `stop-update.md` 结构）；若做 MCP 服务器，可迁移为 `mcp\_tool` 类型。提示词语义不变，只换传输层。











