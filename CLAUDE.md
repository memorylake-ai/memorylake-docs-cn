# CLAUDE.md

本文件为 Claude Code 在此仓库工作时提供指引。

## 项目概述

**MemoryLake 中国站文档**（Mintlify），发布到 `https://docs.memorylake.cn`。

内容起源于国际站文档仓库 `memorylake-docs` 的中文树（`zh/`），但**已按中国站实况差异化**，两者不是简单的翻译关系，不要直接互相覆盖。

## 与国际站的关系

| | 国际站 | 中国站（本仓库） |
|---|---|---|
| 文档 | `docs.memorylake.ai`（英文 + `/zh` 中文） | `docs.memorylake.cn`（仅中文） |
| 控制台 | `app.memorylake.ai` | `app.memorylake.cn` |
| 仓库 | `memorylake-docs` | `memorylake-docs-cn` |
| docs.json | `navigation.languages`（en + zh） | 单语，直接 `navigation.tabs` |
| 页面路径 | 中文页在 `zh/` 前缀下 | 中文页在仓库根目录，内链**不带** `/zh` 前缀 |

**两侧部署相互独立**：账号、工作空间、记忆数据、API Key、配额都不互通。文档里凡涉及服务地址，一律用 `app.memorylake.cn`。

## 开发命令

```bash
mint dev              # 本地预览（需 npm i -g mint）
mint broken-links     # 链接检查（注意：不检查锚点，见下）
```

## 产品事实的唯一准绳

写内容前，**用线上实测确认功能开关，不要读 helm 配置**：

```bash
curl -s https://app.memorylake.cn/api/status | python3 -m json.tool
```

`data.features` 里是该部署的真实开关。helm 里的值会误导——连接器、集成等开关是数据库持久化的，admin 可覆盖 helm 的初始值（例如 helm 写 `avaliable_connectors: null`，线上实际开着 5 个连接器）。

### 中国站当前状态（2026-07-27 实测，会变，以线上为准）

- **可用**：MemoryLake 记忆平台、Model Router（含 Playground，Claude/Gemini 供应商）、OAuth2 MCP（`/memorylake/mcp/v2`）、Agent 插件（OpenClaw/QClaw/Hermes）、REST API、Claude/ChatGPT/Gemini/Chrome 扩展集成、Open Data、连接器（WPS/飞书/OneDrive/SharePoint/Dropbox）
- **未开放**：Memory Router（网关未注册）、Memory Arena、NL2SQL/数据库查询、Actor UI、聊天记录导入、连接器中的 Google Drive/钉钉/百度网盘
- 登录仅邮箱密码（无第三方登录），注册开启且当前无需邮箱验证
- 计费按人民币显示；**不要写具体支付方式**，未经确认一律引导到控制台 Billing 或商务

## 写作约定

- 每个 `.mdx` 必须有 frontmatter 的 `title` 与 `description`
- 用「您」，简洁的技术中文
- 术语：工作空间 / 项目 / 会话 / 事实 / 记忆 / 文件库 / **条目**（drive item，绝不用「项目」）/ 来源溯源 / 冲突 / 遗忘 / 配额
- 保留英文：MemoryLake、Memory Router、Model Router、Actor、Agent、MCP、Boundary、Playground、Open Data、OpenClaw、QClaw、Hermes、BYOK
- API 参考章节里 resolve 译「解决」；概念叙述页译「消解」
- 控制台 UI 中是英文的状态字面量（`pending`/`okay`/`error`）保持英文
- 新增页面**必须**注册到 `docs.json`，否则站点上看不到

## 锚点（重要）

Mintlify 的标题锚点由标题文本生成，**保留 `：`、`’`、`&` 等标点，只去掉括号**，空格转 `-`，中文原样保留。

`mint broken-links` **不检查锚点**，所以坏锚点会长期潜伏。改动标题或新增带锚点的链接后，用 `mint dev` 起服务、抓页面 HTML 里 `<h2..h4 id="...">` 作为基准来核对，不要凭推断拼 slug。

## 合规

- 页脚必须保留 ICP 备案号 **浙ICP备2023036353号** 及工信部备案查询链接（配置在 `docs.json` 的 `footer`）
- 数据存储地域、是否跨境、等保等资质：文档只写「需与商务书面确认」，**不做合规承诺**（见 `deployment.mdx`）
