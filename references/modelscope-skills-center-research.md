# 魔搭 ModelScope Skills 中心：一手来源调研笔记

> 调研时间：2026-10-19 21:28–22:00（Asia/Shanghai）
> 方法：公开 OpenAPI + SPA 真实 DOM（本机 Chrome + playwright-core）+ 官方文档/官方仓库
> 口径约定：**【页面】**= 平台页面直接显示；**【API】**= 我们调用公开 OpenAPI 统计；**【抽样】**= 抽样估算
> 结论性判断均标注来源；凡官方没有的说法，明确标注"本文分析模型"。

---

## 0. 一页速览

| 指标 | 数值 | 口径 | 来源 |
|---|---|---|---|
| Skill 总数 | **83,509** | 【API】`data.total` | https://modelscope.cn/openapi/v1/skills?page_size=1 （21:29） |
| 页面显示总数 | 83,525 | 【页面】搜索框占位符"搜索 Skills（共83,525…）" | https://modelscope.cn/skills （21:44） |
| 一级分类 | **10**（二级 35） | 【API】catalogues | https://modelscope.cn/api/v1/catalogues?Business=skills （21:31） |
| 最大类目 | 开发工具 27,928（33.4%） | 【API】`filter.category` | 同上 |
| 未挂类目 | 1,579（1.9%） | 【API】总数 − 10 类之和 | 计算值 |
| 国际站总数 | **328** | 【API】`www.modelscope.ai` | https://www.modelscope.ai/openapi/v1/skills?page_size=1 （21:44） |
| 中位下载 / 中位浏览 | 158 / 254 | 【抽样】默认排序前 2,400 | 见 §3.3 |
| 头部集中度 | Top 1% 技能占 65.9% 下载 | 【抽样】同上 | 见 §3.3 |
| 在线试运行 | **无技能级沙箱**，仅有"前往实验场试用"跳转 | 【页面】详情页 DOM | https://modelscope.cn/skills/iic/fun-denoise （21:35） |

> 页面 83,525 与 API 83,509 相差 16 条，属两次请求间隔内的正常漂移（也可能前端缓存），记录两个值以备核对。

---

## 1. 资产定位与结构

### 1.1 平台现有资产类型盘点（均为官方入口 + 公开 OpenAPI）

| 资产类型 | 入口 | OpenAPI | 总量 | 承载字段（关键） |
|---|---|---|---|---|
| 模型 Model | https://modelscope.cn/models | `/openapi/v1/models` | **272,995** | `id` `downloads` `likes` `tasks` `license` |
| 数据集 Dataset | https://modelscope.cn/datasets | `/openapi/v1/datasets` | **44,747** | `id` `file_size` `downloads` `tasks` |
| 创空间 Studio | https://modelscope.cn/studios | `/openapi/v1/studios` | **17,313** | `id` `owner` `repo_name` `description` |
| MCP 服务 | https://modelscope.cn/mcp | `PUT /api/v1/dolphin/mcpServers` | **12,690** | `Category[]` `CallVolume` `Abstract/AbstractCN` |
| Skill 技能 | https://modelscope.cn/skills | `/openapi/v1/skills` | **83,509** | `id` `developer` `category` `downloads` `view_count` `source_url` |
| Agent / 实验场 | https://modelscope.cn/agents/playground | 未找到公开聚合 API | 未公开 | 会话式入口，无独立资产 ID |

数据获取时间：2026-10-19 21:29–21:45。命令见 §附录 A。

**要点**
- 六类资产各有独立入口与 OpenAPI，但计数口径不统一：模型/数据集/Studio 用 `total_count`，Skill 用 `total`，MCP 用 `Data.McpServer.TotalCount`——这本身就是"多形态拼装平台"的痕迹。
- MCP 的 `FiledAgg.Category` 直接给出 **100 个**细分行业标签（developer-tools 3,673、scientific-tool 2,043、search 1,511…），说明 **MCP 的分类粒度远细于 Skill**；Skill 只有 10 个一级类目，二级类目几乎空置（见 §3.2）。
- "Agent" 在魔搭没有作为可计数资产暴露，能力被分散在 创空间（Studio）+ 实验场（Playground）+ 智能工坊 三个入口。

### 1.2 四层资产结构（★ 本文分析模型，非 ModelScope 官方定义）

> 声明：ModelScope 官方文档、公告、仓库 README 中**均未出现"四层资产结构"的提法**。以下是我们为资产盘点构建的分析框架，用于对齐 PPT 叙事，不应表述为"官方架构"。

| 层级 | 解决什么问题 | ModelScope 承载物（含规模） | 代表例子 | 与 Skill 的关系 |
|---|---|---|---|---|
| **L1 基础资源层** | 能力从哪来：权重、语料、算力产物 | 模型 272,995 / 数据集 44,747 | `deepseek-ai/DeepSeek-V4.1-Flash-1017`、`Qwen/BlenderWorld` | Skill 不生产模型，只"调用/编排"；一个 Skill 可绑定 0..N 个模型 |
| **L2 工具连接层** | 如何触达外部世界：协议、鉴权、执行 | MCP 服务 12,690、OpenAPI、`ms`/`modelscope` CLI、`install.sh` | `@ModelScope/ms-hub` 通过 `ms` CLI 操作模型/数据集/Studio | Skill 把"工具怎么用"写成可加载的指令；MCP 是 Skill 最常用的被调端 |
| **L3 方法资产层** | 一类任务该怎么做：流程、知识、脚本 | **Skill 83,509** | `@anthropics/skill-creator`、`iic/fun-denoise` | 本层主体；向下引用 L1/L2，向上被 L4 消费 |
| **L4 应用交付层** | 最终谁用、在哪用 | 创空间 17,313、实验场、智能工坊、合集（Collection） | `AlibabaCloud Skills` 合集（302 个 Skill）、`modelscope-studio` 部署 | Agent/应用按需装载多个 Skill；合集是"打包分发"而非新资产类型 |

**为什么这样分层可辩护**
1. 四层各自有**独立入口 + 独立 OpenAPI + 独立计数**（§1.1 表），不是人为切分。
2. 依赖方向单一：L4 → L3 → L2 → L1，反向依赖在平台上找不到（模型不引用 Skill）。
3. 每层的"复用单位"不同：权重（GB 级）、连接（协议级）、方法（目录级，≤5MB）、应用（实例级）。
4. 与官方术语可对齐：官方 README 把 Skill 定义为"equip AI agents with the ability to operate on ModelScope — model/dataset management, Studio deployment, MCP service configuration"，即 **Skill 天然跨 L2 与 L4**，这正是把 Skill 放 L3 的理由——它是"方法"，不是"资源"也不是"应用"。

**四层规模比（同一时点）**：模型 273k : 数据 45k : 工具 12.7k : 技能 83.5k : 应用 17.3k。
→ 技能层已是**第二大资产池**，仅次于模型；但它的"下游承接"（Agent）没有独立计数，这是结构上的断点。

### 1.3 Skill 的内部结构

官方规范（`skills/ms-hub/references/skills-center.md`，https://github.com/modelscope/modelscope-skills/blob/main/skills/ms-hub/references/skills-center.md ，21:36）：

```text
my-skill/
├── SKILL.md          # 必需：YAML frontmatter + Markdown 指令
├── scripts/          # 可选：工具脚本
├── references/       # 可选：参考文档
└── examples/         # 可选：示例代码
```

- **frontmatter 必填**：`name`、`description`（同文档"Skill Directory Structure"节）。
- **发布时额外要求**：经 CLI（`ms create --repo-type skill --skill-file <zip>`）发布时，frontmatter 必须含 `name`/`version`/`description`，zip ≤ 5 MB（同文档"Publishing a Skill"注）。
- **与 Agent Skills 开放标准的关系**：官方 README 明确 "This repository follows the [Agent Skills](https://agentskills.io/home) standard format"；官方文档 `https://modelscope.cn/docs/skills/intro` 表述为"其规范源于 Anthropic Agent Skills 协议"。即**魔搭是标准的实现者/托管方，不是标准制定方**。
- **assets/ 与 examples/**：官方仓库文档只列 `scripts/ references/ examples/`，**未提 `assets/`**；`assets/` 出现在社区通行写法中。本文脚注区分，避免把社区惯例说成官方规范。

**规范 vs 落地的落差（实测）**
以 `iic/fun-denoise` 为例，详情页"Skill 文件"标签页实际文件树（https://modelscope.cn/skills/iic/fun-denoise/files ，21:35）：

| 文件 | 大小 | 是否符合目录约定 |
|---|---|---|
| `SKILL.md` | 7.38 KB | ✅ 必需 |
| `denoise_cli.py` | 9.71 KB | ⚠️ 脚本放在根目录，未进 `scripts/` |
| `skill-card.md` | 2.26 KB | ⚠️ 约定外文件（疑似展示卡片） |

→ 结论：**目录约定是"推荐"而非"校验"**，平台没有对 `scripts/` 等结构做强制。这对"Skill 资产质量分级"是机会点。

另：详情页文件浏览支持逐文件下载，直链形如
`https://modelscope.cn/skills/iic/fun-denoise/resolve/master/SKILL.md?view=false`；仓库分支为 `master`（与 `ms-hub` 文档"Default branch master"一致）。

---

## 2. 资产消费链路

### 2.1 来源：Skill 从哪里来

| 来源通道 | 证据 | 说明 |
|---|---|---|
| **GitHub 导入托管** | 【页面】"新建 Skill → 快速创建：从 Github 导入并托管您的 Skills"（https://modelscope.cn/skills ，21:44 截图） | 官方称"快速创建"，对应仓库的自动同步机制 |
| **本地 zip 上传** | 【页面】"新建 Skill → 自定义创建：从本地文件上传并提交您的 Skills" | 对应 §2.2 两步 API |
| **外部 registry 搬运** | 【抽样】`source_url` 出现 `clawhub.ai`、`beatra.ai`、`cuecue.cn`、`gitee.com` | 说明存在第三方 Skill 市场的镜像式导入 |
| **官方仓库** | https://github.com/modelscope/modelscope-skills （`ms-hub`、`ms-studio-deploy`） | 官方自营 Skill 源码，Apache-2.0 |

**`source_url` 字段怎么用**
- 【API】列表/详情返回 `source_url`，可为空字符串（如 `iic/fun-denoise` 为空）。
- 【抽样】默认排序前 2,400 条中 **74.3%（1,782/2,400）指向 `github.com`**，空值 328 条（13.7%），`beatra.ai` 182 条（7.6%）为单一站点第二大来源。
- 该字段是**自由文本，不做校验**：抽样中出现 `"1111"` 这类明显无效值（`zhangyiyi12/zhangyiyi111`）。→  provenance 不可作为可信度依据。

**同步状态字段**：`auto_sync_enabled`（布尔）与 `sync_status`，抽样中仅 **7.2%** 开启自动同步。说明"GitHub 导入"更多是一次性快照，而非持续同步。

### 2.2 发布：完整步骤与约束

官方 API 流程（`skills-center.md` "Publishing a Skill (Two Steps)"）：

| 步骤 | 请求 | 关键点 |
|---|---|---|
| ① 上传 zip | `POST /openapi/v1/files/upload`，`-F file=@my-skill.zip -F type=skill` | 返回 `data.id`（注意 key 是 `id`，不是 `file_id`） |
| ② 创建 Skill | `POST /openapi/v1/skills`，body 含 `owner` `skill_name` `display_name` `description` `skill_file` `category` `license` `tags[]` `source_url` | `skill_file` 用①的 `data.id` |
| ③ 更新 | `PATCH /openapi/v1/skills/{owner}/{skill_name}/settings` | 只传要改的字段 |

**字段约束（官方原文归纳）**

| 约束 | 内容 |
|---|---|
| zip 根目录 | 必须**恰好含 1 个 `SKILL.md`**，且别无他物（"exactly 1 SKILL.md file and nothing else"） |
| 大小 | CLI 发布路径 ≤ **5 MB** |
| 命名 | `skill_name` 仅允许小写字母、数字、连字符；**创建后不可改** |
| owner | **创建后不可改** |
| 可更新字段 | `display_name` `description` `skill_file` `tags` `source_url` `category` `license` |
| 私有 | 存在 `private` 字段；私有 Skill 安装需 `--token`（官方 install 文档） |
| 审核 | **未公开**。官方文档、SKILL.md、OpenAPI 响应中均无审核状态字段；抽样 2,400 条 `private` 全为 `false`，未见"审核中/已驳回"状态。尝试过：详情页、发布入口（需登录）、`/api/v1/console/config/list/business/skill`，均未获得审核规则 |

**版本**：API 无 `version` 字段，版本实际由 git 提交承载（详情页显示 `master` 分支、`Init Skill 1个月前`）。CLI 要求 frontmatter 有 `version`，但平台侧不落库为独立版本号 → **"版本"在魔搭是弱概念**。

**namespace 规则（实测）**：URL 有两种形态——
- `owner/name`：`iic/fun-denoise`、`modelscope/ModelScope-Studio`、`alibabacloud-skills/...`
- `@developer/name`：`@anthropics/skill-creator`、`@MiniMax-AI/h3-prompt-writing`
抽样中 **43.8%** 的 id 带 `@` 前缀，即"开发者命名空间"已成主流；这与组织 owner 体系并行，是历史双轨。

### 2.3 消费：搜索、详情、安装

**搜索参数**（`skills-center.md` "Search Parameters"，并在 OpenAPI 实测生效）

| 参数 | 实测 | 示例 |
|---|---|---|
| `search` | ⚠️ 实测**未生效**（`search=pdf` 仍返回 83,509，且结果不变） | 文档写作 keyword |
| `filter.category` | ✅ 生效，精确匹配类目 ID | `developer-tools` → 27,928 |
| `filter.developer` | ✅ 生效 | `anthropics` → 119 |
| `filter.owner` | ✅ 生效 | `alibabacloud-skills` → 302 |
| `filter.custom_tag` | ✅ 生效 | `skill-creation` → 3,707 |
| `filter.license` | 未验证 | — |
| `page_number` × `page_size` | ⚠️ 文档称 ≤3000；**实测 `page_size=100` 时第 25 页起持续 403**（重试仍 403） | 有效可抓 ≈2,400 条 |

> `search` 未生效是重要发现：**公开 OpenAPI 目前只能"筛类目/作者"，不能"搜关键词"**。站内搜索走的是内部接口 `PUT /api/v1/dolphin/skills`（body 含 `Query`/`Criterion`/`Sort`），未在 OpenAPI 暴露。这直接影响"Skill 可发现性"的评估。

**详情页字段与真实文案**（https://modelscope.cn/skills/iic/fun-denoise ，21:35 抓取 DOM）

| 区域 | 实际文案/内容 |
|---|---|
| 头部 | `Fun Denoise`、`@iic`、`/fun-denoise`、浏览 `5.3k`、下载 `774`、日期 `2026.09.11`、点赞 `32` |
| 标签页 | `Skill 介绍` / `Skill 文件` / `交流反馈2` |
| 主按钮 | **`前往实验场试用`** → `/agents/playground` |
| 安装区（页面底部） | `/下载`（`fun-denoise.zip`）、`/通过npx安装`、`/通过ModelScope SDK安装`、`/通过bash安装` |
| 安装命令原文 | `npx skills add https://modelscope.cn/skills/ iic/fun-denoise`（页面在 `skills/` 后多一个空格，疑为排版缺陷；API `install_command` 为 `https://modelscope.cn/skills/iic/fun-denoise`，无空格） |

**API `install_command` 三条**（【API】`GET /openapi/v1/skills/iic/fun-denoise`，21:33）：
```text
npx skills add https://modelscope.cn/skills/iic/fun-denoise
curl -fsSL https://modelscope.cn/skills/install.sh | bash -s -- iic/fun-denoise
pip install --upgrade modelscope && modelscope skills add iic/fun-denoise
```

**四种安装方式对照**（官方 install 文档：https://modelscope.cn/docs/skills/install ，21:47；原文 markdown 见 `https://resouces.modelscope.cn/document/docdata/2026-10-9_16-57-CN/dist/skills/install/install_CN.md`，注意官方域名拼写为 `resouces`）

| 方式 | 命令 | 适用 | 限制 |
|---|---|---|---|
| npx | `npx skills add <url>`，合集用 `/collections/{id}` | Node 环境快速试用 | **不支持私有 Skill/合集** |
| SDK | `modelscope skills add <id>` / `ms skills add` | 日常使用，支持批量、`--local_dir`、`--token`、`--max-workers`(默认8) | `ms`(modelscope_hub) 无 `skills` 子命令，入口冲突需改用 curl |
| Bash | `curl -fsSL .../install.sh \| bash -s -- <id>` | CI/CD、批量 | 需 shell 环境 |
| 手动 | 详情页"下载"zip 解压 | 离线/审计 | 无 |

**默认安装目录**：`~/.agents/skills/`（README "Installation" 与 skills-center.md 一致），"where major agent tools auto-discover them"。

**宿主兼容性（官方声明）**：Cursor、Claude Code、Codex、Gemini CLI；README 给出各自路径：
- Cursor：项目内 `.cursor/skills/`
- Codex：`$HOME/.agents/skills` 或 `$REPO_ROOT/.agents/skills`
- Claude Code：`/plugin marketplace add modelscope/modelscope-skills`
- Gemini CLI：`gemini extensions install <repo> --consent`
另 install.sh 支持 `--agent cursor` 选择目标宿主。

**私有技能 token**：`modelscope skills add <id> --token <token>` / `bash -s -- <id> --token <token>`；token 页面 `https://modelscope.cn/my/myaccesstoken`，且 **token 按站点隔离**（国内/国际站账号、目录独立）。

**站点**：国内 `modelscope.cn`（83,509）与 `www.modelscope.ai`（328）为两套独立目录，`MODELSCOPE_ENDPOINT` 切换。

### 2.4 试运行：有没有"在线跑一下"

**结论：没有技能级在线试运行/沙箱。**

实测证据（2026-10-19 21:35，`https://modelscope.cn/skills/iic/fun-denoise`）：
1. 详情页唯一可点击的行动按钮是 **`前往实验场试用`**，`href=/agents/playground`；
2. 页面内无"运行""示例输入""执行结果"面板；`Skill 介绍` 只是渲染 README（含代码块，纯文本）；
3. `Skill 文件` 仅文件浏览 + 逐文件下载；
4. 点击安装命令只有复制，无"一键安装到云端"；
5. 未登录点击 `新建 Skill` 即弹登录框（截图确认），说明**发布与试跑都需要登录态**；
6. `PUT /api/v1/dolphin/skills` 返回字段中无 `sandbox`/`run_url`/`demo_url` 一类字段。

**最接近的替代路径（按可用性排序）**

| 替代方式 | 怎么做 | 缺口 |
|---|---|---|
| ① 实验场（Playground） | 详情页点 `前往实验场试用` → `/agents/playground`，在通用 Agent 会话里手动提需求 | 不是"带输入输出的技能级沙箱"，无预置示例参数，无结果回放；需登录 |
| ② 本地安装后跑 | `npx/curl/sdk` 安装到 `~/.agents/skills`，在 Cursor/Claude Code/Codex 中触发 | 需要本地 Agent 宿主 + 依赖环境（如 DashScope Key） |
| ③ 看示例文件 | 读 README/`examples/` 里的命令与参数表（如 `python denoise_cli.py input.mp3 output.wav`） | 纯静态，无执行验证 |
| ④ MS-Agent 集成 | 官方文档给 `create_agent_skill(skills_dir=...)`、`agent.test_skill(...)` 代码 | 要自己搭 Python 环境 |

→ **生态缺口 #1**：Skill 是"可执行资产"，却缺"执行入口"。对比 MCP 广场有"MCP 实验场"（页面文案实见 `MCP 实验场 🔥新增对话记忆🔥`），Skill 侧没有对等设施。

---

## 3. 生态画像

### 3.1 规模

| 口径 | 数值 | 来源 |
|---|---|---|
| 技能总数【API】 | 83,509 | 21:29 |
| 技能总数【页面】 | 83,525 | 21:44 |
| 国际站【API】 | 328（= 国内 0.39%） | 21:44 |
| 一级分类数 | 10 | 21:31 |
| 二级分类数 | 35（其中 24 个为 0 条） | 21:31 + 21:38 |
| 合集（Collection） | 未获取总数；首页合集轮播仅有 9 个分页点 | 页面 |

**增长信号（弱证据，仅作参考）**：抽样 2,400 条的 `last_modified` 月份分布为 2026-06: 1,150 / 07: 182 / 08: 284 / 09: 337 / 10: 447。6 月峰值对应一次**批量导入**（`file_last_modified` 中 1,432 条落在 2026-06，896 条为 `1970-01-01` 即从未同步），不能解读为真实创作高峰。**平台未公开时间序列，无法计算真实增速。**

### 3.2 供给画像

#### 3.2.1 十个一级分类的精确总量【API】

| # | 分类（中文） | CatalogID | 技能数 | 占比 | 二级类目数 |
|---|---|---|---|---|---|
| 1 | 开发工具 | `developer-tools` | **27,928** | 33.44% | 4 |
| 2 | 代码质检 | `code-quality-testing` | **16,854** | 20.18% | 5 |
| 3 | 媒体处理 | `ai-media` | **10,569** | 12.66% | 4 |
| 4 | 前端开发 | `frontend-development` | 6,686 | 8.01% | 4 |
| 5 | 云效工具 | `cloud-devops` | 5,544 | 6.64% | 5 |
| 6 | 市场推广 | `marketing-seo` | 5,409 | 6.48% | 5 |
| 7 | Skills管理 | `skill-management` | 4,192 | 5.02% | 3 |
| 8 | 其他 | `other` | 2,669 | 3.20% | 1 |
| 9 | 移动开发 | `mobile-development` | 1,233 | 1.48% | 4 |
| 10 | 科研工具 | `scientific-tool` | 846 | 1.01% | 0 |
| — | **未挂类目** | — | **1,579** | 1.89% | — |
| — | 合计 | — | 83,509 | 100% | 35 |

**Top 3 类目合计 66.3%**（27,928+16,854+10,569 = 55,351）。

**两个分类治理事实**
1. **官方文档列了 12 个类目，线上只有 10 个**。`skills-center.md` 的表格含 `ai-automation`、`analytics`、`doc-processing`，但 catalogues API 中这三者是**二级类目**（分别挂在 ai-media / marketing-seo / developer-tools 下，实际条数 1,202 / 59 / 23）。→ 文档与实现不同步，PPT 引用时须以 API 为准。
2. **二级分类基本失效**：35 个二级类目合计仅约 1,547 条，其中 24 个为 0；只有 `ai-automation`(1,202) 有实际量。→ 平台的分类治理是"一级可用、二级荒废"。

#### 3.2.2 头部 owner / developer【API 精确值 vs 抽样】

| 账号 | 命名空间 | 技能数 | 口径 | 性质 |
|---|---|---|---|---|
| `majiayu000` | developer | **16,093** | 【API】`filter.developer` | 聚合/镜像（source 指向 `github.com/majiayu000/claude-skill-registry`） |
| `diegosouzapw` | developer | **9,315** | 【API】 | 聚合/镜像 |
| `alibabacloud-skills` | owner | **302** | 【API】`filter.owner` | 阿里云官方精选（首页合集文案"7月28日新增至205个skills"） |
| `beatra01` | owner | **189** | 【API】 | 批量导入（source `beatra.ai`） |
| `smyx-sunjinhui` | developer | **211** | 【API】 | 批量导入 |
| `anthropics` | developer | **119** | 【API】 | 品牌官方（Anthropic） |
| `aliyun` | developer | **32** | 【API】 | 阿里云 |
| `MiniMax-AI` | developer | **28** | 【API】 | 品牌官方 |
| `inference-sh` | developer | 21 | 【API】 | 品牌 |
| `modelscope` | owner | **2** | 【API】 | 平台官方 |
| `iic` | owner | **1** | 【API】 | 平台官方（通义实验室） |

> 注意：`modelscope` 只有 2 个、`iic` 只有 1 个，但它们在首页卡片上的浏览/下载并不低（`modelscope-studio` 34.1k 浏览 / 3.7k 下载）。**官方账号数量极少、单条影响力大**。

#### 3.2.3 三段画像（平台官方 / 垂直领域 / 社区泛用）

**判定规则（本文自定，可复核）**
1. **平台官方**：账号 ∈ {`modelscope`, `iic`, `aliyun`, `alibabacloud-skills`, `damo`, `qwen`}——可通过组织页/官方公告核对。
2. **垂直领域（企业/机构）**：可核验的品牌/机构账号，如 `anthropics`、`MiniMax-AI`、`AMap-Web`、`Gaodekaifangpingtai`、`BaiduDrive`、`vercel-labs`、`OneScience`、`inference-sh`、`Alipay`。
3. **社区泛用（含聚合/镜像）**：其余个人或工具型账号；其中 `majiayu000`/`diegosouzapw`/`beatra01`/`smyx-sunjinhui` 单列为"聚合/镜像"子类，因为其供给是搬运而非原创。

**精确计数（平台官方，全站）**：302 + 32 + 2 + 1 = **337 条，占 0.40%**。
**聚合/镜像（全站，已逐账号核实 4 个）**：16,093 + 9,315 + 211 + 189 = **25,808 条，占 30.9%**（`majiayu000` + `diegosouzapw` + `smyx-sunjinhui` + `beatra01`；均为 `filter.developer`/`filter.owner` 精确值，非抽样外推）。
**垂直领域**：可枚举品牌合计约 **500–600 条**（anthropics 119 + MiniMax 28 + inference-sh 21 + 其余品牌各 1–6，另有 OneScience/AMap 等未逐一定量），**量级 <1%**。
**剩余 ≈67%**：社区个人长尾（无法全量枚举，按抽样比例外推）。

**抽样结构（前 2,400 条，仅代表"头部曝光区"，不代表全站）**

| 段落 | 样本数 | 占比 | 中位下载 | 中位浏览 | 下载份额 |
|---|---|---|---|---|---|
| 平台官方 | 64 | 2.7% | 374 | 348 | 2.3% |
| 聚合/镜像 | 652 | 27.2% | 145 | 269 | 6.8% |
| 品牌/垂直 | 78 | 3.2% | **516** | **663** | 7.3% |
| 社区个人/长尾 | 1,606 | 66.9% | 148 | 230 | **83.7%** |

**读法**：数量上社区长尾占 2/3，但**品牌/垂直机构的中位下载是长尾的 3.5 倍**（516 vs 148）——"少而精"；聚合账号"多而不精"（中位 145，低于长尾）。**平台官方数量几乎可忽略（0.4%），却是流量与信任的锚点。**

**头部集中度**：样本前 15 个账号占 40.0% 的条目；前 3 个账号（smyx-sunjinhui 211 / majiayu000 185 / beatra01 182）占 24.1%。

### 3.3 消费画像

**抽样说明**
- 样本 A：默认排序（`Sort=Default`，即首页推荐序）前 **2,400** 条，`page_size=100`，第 25 页起因 403 停止；去重后 2,400。
- 样本 B：10 个一级类目各取前 300 条，共 **3,000** 条（每类 3 页×100），用于校验 A 的偏置。
- 合并去重 **3,610** 条（A∪B），占全站 4.3%。
- 局限：默认排序本身是推荐序，**样本偏向"已被推荐/较热"的技能**，真实全站中位数只会更低。B 的分层样本可作对照。

#### 3.3.1 分布【抽样】

| 指标 | 样本 A（n=2,400） | 样本 B（n=3,000） |
|---|---|---|
| 下载 中位数 | **158** | 117 |
| 下载 P90 | **673** | 620 |
| 下载 均值 | 903 | 738 |
| 下载 最大值 | 1,156,294 | 1,156,294 |
| 浏览 中位数 | **254** | 123 |
| 浏览 P90 | **1,190** | 870 |
| 浏览 均值 | 753 | 570 |
| Top 1% 技能占下载总量 | **65.9%** | 65.4% |
| Top 10% 技能占下载总量 | 80.8% | 81.2% |

→ **极端帕累托**：1% 的技能拿走 2/3 的下载，90% 的技能合计只占 19%。中位下载仅 158，意味着"上架即沉默"是常态。

#### 3.3.2 Top 10（按 downloads，取自 A∪B 3,610 条）

| # | Skill ID | 下载 | 浏览 | 分类 | 备注 |
|---|---|---|---|---|---|
| 1 | `ebandao/dev-expert` | **1,156,294** | **592** | developer-tools | ⚠️ 下载/浏览 = 1,953:1，异常值 |
| 2 | `@wyb92/mysteel-pricesearch` | 31,470 | 6,232 | developer-tools | source 为 `clawhub.ai` |
| 3 | `xbgai123/xiaobaogongai-law` | 26,643 | 28,381 | cloud-devops | 法律垂直，source 为企业官网 |
| 4 | `xbgai123/xiaobaogongai-contract-drafting` | 25,695 | 26,115 | cloud-devops | 同主体第 2 个 |
| 5 | `@anthropics/skill-creator` | 20,473 | **70,032** | skill-management | 浏览全站第一 |
| 6 | `@anthropics/frontend-design` | 16,165 | 34,925 | frontend-development | |
| 7 | `OneScience/oneskills` | 12,755 | 6,129 | developer-tools | 科研 |
| 8 | `tingting0980/baobiao-API` | 11,300 | 13,515 | marketing-seo | 无 source_url |
| 9 | `@anthropics/docx` | 10,454 | 13,453 | developer-tools | |
| 10 | `zhangyiyi12/zhangyiyi111` | 9,620 | **33** | skill-management | ⚠️ source_url 为 `"1111"`，疑测试/刷量 |

Top 10 按浏览（对照）：`@anthropics/skill-creator` 70,032 → `@pskoett/self-improving-agent` 40,258 → `@anthropics/frontend-design` 34,925 → `modelscope/modelscope-studio` 34,118 → `@AMap-Web/amap-lbs-skill` 32,996。

#### 3.3.3 view_count 与 downloads 的口径差异（不能混用）

| 现象 | 数据 | 解释 |
|---|---|---|
| 正常条目 | `skill-creator`：70,032 浏览 / 20,473 下载 ≈ **3.4:1** | 浏览是漏斗上层，下载是转化 |
| 极端异常 | `ebandao/dev-expert`：592 浏览 / 1,156,294 下载 ≈ **1:1,953** | 下载量不可能来自页面点击；疑为 CI/脚本拉取、或 `downloads` 计数含 API/CLI 拉包与重复计数 |
| 反向异常 | `zhangyiyi12/zhangyiyi111`：33 浏览 / 9,620 下载 | 同上，且 source_url 为 `"1111"` |

**结论**：`downloads` 更像"发行/拉取次数"（含 CLI、镜像、自动同步），`view_count` 才是"人类注意力"。**PPT 上一律标注口径**，且不建议用 downloads 直接代表"用户数"。Top 1 的 115 万下载应作为"数据质量案例"而非"标杆案例"。

#### 3.3.4 段落间的消费差异

| 段落 | 中位下载 | 中位浏览 | 相对长尾 |
|---|---|---|---|
| 品牌/垂直 | 516 | 663 | 下载 ×3.5，浏览 ×2.9 |
| 平台官方 | 374 | 348 | 下载 ×2.5 |
| 社区长尾 | 148 | 230 | 基准 |
| 聚合/镜像 | 145 | 269 | 下载 ×0.98（几乎无转化增益） |

→ **"官方/品牌"带来信任溢价，"聚合"只带来数量不带来消费**。这直接支持"资产分级 + 品牌位"的产品设计。

---

## 4. 总结

### 4.1 五到七条洞察

1. **核心框架是"资源—工具—方法—应用"的四层漏斗，但漏斗在第三层断裂。**
   模型 273k、技能 83.5k、应用 17.3k，数量上技能已成第二大池；但技能到应用之间没有可计数的 Agent 资产，也没有技能级运行环境，导致"方法资产"无法被验证、只能被下载。

2. **这是一座"索引型"市场，不是"创作型"市场。**
   两个聚合账号（majiayu000 16,093 + diegosouzapw 9,315）合计 30.4%，前 3 个批量账号占头部曝光的 24.1%；74.3% 的 `source_url` 指向 GitHub。平台的核心能力是**收录与分发**，原创供给高度集中在少数品牌（Anthropic 119、阿里云 302+32）。

3. **分类体系"头重脚轻"：10 个一级类目承载全部，35 个二级类目 24 个为空。**
   Top 3 类目占 66.3%，科研工具仅 846（1.0%）。官方文档还停留在"12 类目"的旧描述，与线上不一致——分类治理是当前最容易被忽视、也最容易补的短板。

4. **最弱的一层是"试运行 + 治理"。**
   没有沙箱、没有在线执行、没有审核状态字段、没有版本号、`search` 参数在公开 OpenAPI 失效。一个"可执行资产"却只能"下载后自行验证"，这解释了为什么中位下载只有 158——**转化断点在"看到"与"跑通"之间**。

5. **最强的一层是"分发通道"。**
   4 种安装方式（npx / SDK / bash / zip）+ `~/.agents/skills` 默认目录 + Cursor/Claude Code/Codex/Gemini 四宿主兼容 + 合集打包。**分发做得比验证好**，这是魔搭相对其他 Skill 市场的真实优势。

6. **数据口径本身是风险。**
   单条技能 115.6 万下载对 592 浏览；页面总数 83,525 与 API 83,509 不一致；`source_url` 可填 `"1111"`。**做对外汇报时，任何"下载量"都必须带口径与异常剔除说明**，否则会被一个异常值带偏。

7. **生命周期启示：Skill 资产需要"三段治理"——入库（provenance 校验）、在架（分级/版本/审核）、出库（可运行验证）。**
   魔搭目前只完成了"入库 + 分发"，在架治理与出库验证是空白，也正好是第三方工具/服务的机会窗口。

### 4.2 可直接上 PPT 的关键数字（8–12 条，逐条带来源）

| # | 数字/事实 | 来源（访问时间 2026-10-19） |
|---|---|---|
| 1 | Skills 总数 **83,509**（页面显示 83,525） | https://modelscope.cn/openapi/v1/skills?page_size=1 （21:29）；https://modelscope.cn/skills （21:44） |
| 2 | 一级类目 **10 个**、二级 35 个（24 个为空），Top3 占 **66.3%** | https://modelscope.cn/api/v1/catalogues?Business=skills （21:31）+ `filter.category` 逐类统计（21:38） |
| 3 | 最大类目「开发工具」**27,928**（33.4%）；最小「科研工具」846（1.0%） | 同上 |
| 4 | 平台官方账号合计仅 **337 条 = 0.40%**（alibabacloud-skills 302 / aliyun 32 / modelscope 2 / iic 1） | `filter.owner`、`filter.developer` （21:46） |
| 5 | 两个聚合账号占 **30.4%**（majiayu000 16,093 + diegosouzapw 9,315） | `filter.developer` （21:52） |
| 6 | 中位下载 **158**、P90 **673**；中位浏览 254、P90 1,190（n=2,400 默认序） | 抽样，见 §3.3.1 |
| 7 | Top **1%** 技能拿走 **65.9%** 下载 | 抽样，n=2,400 |
| 8 | **74.3%** 的 `source_url` 指向 github.com；**34.1%** 无 license | 抽样，n=2,400 |
| 9 | 单条最高下载 **1,156,294**，但浏览仅 **592**（口径异常样本） | 抽样 + `ebandao/dev-expert` |
| 10 | 国际站 **328** 条 = 国内 **0.39%** | https://www.modelscope.ai/openapi/v1/skills?page_size=1 （21:44） |
| 11 | 安装：4 条通道，默认装到 `~/.agents/skills/`，兼容 4 类宿主 | https://github.com/modelscope/modelscope-skills （21:36）；https://modelscope.cn/docs/skills/install （21:47） |
| 12 | 发布：**2 步**（upload → create）、zip **≤5 MB**、`skill_name`/`owner` **不可改** | https://github.com/modelscope/modelscope-skills/blob/main/skills/ms-hub/references/skills-center.md （21:36） |
| 13 | 试运行：**无技能级沙箱**，只有"前往实验场试用"→ `/agents/playground` | https://modelscope.cn/skills/iic/fun-denoise DOM（21:35） |

### 4.3 图表建议

| 图表 | 数据 | 为什么 |
|---|---|---|
| **横向柱状图**（降序） | §3.2.1 十个类目技能数 | 类目量级差 33 倍，柱状最直观；标注 Top3=66.3% 的括号 |
| **环形图** | 平台官方 0.4% / 聚合 30.9% / 品牌垂直 <1% / 社区长尾 ≈67% | 展示"数量结构"的极端不均；环心写 83,509 |
| **帕累托图**（柱+累计线） | 下载分布分位数（Top1%=65.9%，Top10%=80.8%） | 一眼说明"少数技能吃掉多数下载"，支撑"长尾沉默"论点 |
| **漏斗图** | 曝光（浏览）→ 详情 → 安装（下载）→ 运行（无数据/断点） | 第四段直接画成虚线/空白，正是"试运行缺口"的视觉表达 |
| **矩阵/气泡图** | X=技能数（供给），Y=中位下载（需求），气泡=类目 | 找"供大于求"的类目（开发工具）与"供不应求"的类目（科研/移动） |
| **四层堆叠示意** | 273k / 45k / 12.7k / 83.5k / 17.3k | 唯一能同时表达"层级 + 规模"的图；务必标注"本文分析模型，非官方" |
| 不建议 | 折线/增速图 | 平台不公开时间序列，6 月峰值是批量导入，画增长曲线会失真 |

---

## 附录 A：数据快照与复现命令

**快照（2026-10-19，Asia/Shanghai）**

| 项 | 值 | 时刻 |
|---|---|---|
| skills total（国内） | 83,509 | 21:29 |
| skills total（页面） | 83,525 | 21:44 |
| skills total（国际） | 328 | 21:44 |
| models / datasets / studios | 272,995 / 44,747 / 17,313 | 21:45 |
| MCP servers | 12,690 | 21:43 |
| 类目树 | 10 一级 / 35 二级 | 21:31 |
| 样本 A / B | 2,400 / 3,000（并集 3,610） | 21:46 |

```bash
# 1) 总数
curl -s 'https://modelscope.cn/openapi/v1/skills?page_size=1' | jq '.data.total'
curl -s 'https://www.modelscope.ai/openapi/v1/skills?page_size=1' | jq '.data.total'

# 2) 官方类目树（一级 10 + 二级 35）
curl -s 'https://modelscope.cn/api/v1/catalogues?Business=skills' \
  | jq '.Data.Catalogues[] | {id:.CatalogID, zh:.ChineseName, children:(.Children|length)}'

# 3) 按类目/作者精确计数
curl -s -G 'https://modelscope.cn/openapi/v1/skills' \
  --data-urlencode 'filter.category=developer-tools' --data-urlencode 'page_size=1' | jq '.data.total'
curl -s -G 'https://modelscope.cn/openapi/v1/skills' \
  --data-urlencode 'filter.developer=majiayu000' --data-urlencode 'page_size=1' | jq '.data.total'

# 4) 详情（含 install_command）
curl -s 'https://modelscope.cn/openapi/v1/skills/iic/fun-denoise' | jq '.data.install_command'

# 5) 其它资产规模
for t in models datasets studios; do
  printf '%s ' $t; curl -s "https://modelscope.cn/openapi/v1/$t?page_size=1" | jq '.data.total_count'
done
curl -s -X PUT 'https://modelscope.cn/api/v1/dolphin/mcpServers' \
  -H 'Content-Type: application/json' \
  -d '{"PageSize":1,"PageNumber":1,"Query":"","Criterion":[]}' | jq '.Data.McpServer.TotalCount'
```

**抽样脚本要点（可复现）**
- 样本 A：`page_number=1..30`、`page_size=100`，第 25 页起 HTTP 403（实测上限），实际得 2,400。
- 样本 B：10 个 `filter.category` × `page_number=1..3` × `page_size=100`，得 3,000。
- 统计字段：`downloads`、`view_count`、`license`、`source_url`、`last_modified`、`developer`、`owner`。
- 分位数用线性插值（numpy 默认 percentile 口径）。

**已知缺口（未获取，及尝试路径）**
| 缺口 | 尝试过 | 结论 |
|---|---|---|
| 审核规则/时长 | 详情页、发布入口、`console/config`、官方文档、`ms-hub` | 未公开 |
| 关键词 `search` 语义 | OpenAPI `search=pdf` 返回全量不变 | 公开 API 未实现，站内走内部 `dolphin/skills` |
| 每日新增/增速 | `last_modified` 分布、无时间序列 API | 不可得（6 月为批量导入） |
| 私有 Skill 数量 | `private` 字段全为 false | 不公开 |
| 合集总数 | 首页轮播只有 9 个，无公开合集 API | 未获取 |
| Agent 资产计数 | `/agents/playground` 无聚合列表 | 未公开 |
