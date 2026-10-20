# 华为智果园 AI 资产广场：Skill 资产现状、三平台对照与建设启示

> 调研时间：2026-10-20（Asia/Shanghai）
> 方法：华为云智果园/AI 资产广场公开页面、AgentArts 官方文档、公开 Skill 列表/详情页；结合工作区已完成的魔搭 Skills 中心与腾讯 SkillHub 调研笔记。
> 口径：【页面】= 公开页面实际展示；【官方文档】= 华为云帮助中心；【图片】= 官网价值主张图；【推断】= 基于以上证据的分析，不是官方原话。

---

## 0. 一页速览

| 结论 | 说明 |
|---|---|
| **智果园是入口，AI 资产广场是市场** | 智果园是华为云 Agentic AI 入口；AI 资产广场（pangu.huaweicloud.com/gallery）是模型、数据集、Skills、应用、提示词、合集的统一市场。 |
| **Skills 已是独立资产类型** | 资产广场导航含「Skills」，列表页当前 **239 个 Skills**，按行业/云服务/通用分类。 |
| **沿用 Agent Skills 标准** | 制品包为 ZIP，SKILL.md + scripts/references/assets，遵循 Agent Skills Standard；包 ≤10MB、单文件夹、目录名=name。 |
| **分发走开放 CLI** | 页面直接给 `npx skills add ...` / `skills.sh` 命令；`pangu.huaweicloud.com/skills/{user}/{slug}` 直接返回可安装 ZIP。 |
| **质量有内建评估器** | AgentArts 提供 **Skill 完整度** 评估器（LLM，0/0.25/0.5/0.75/1.0，4 维度），用于上架审核/质量巡检。 |
| **独有：trace 驱动优化** | 轨迹分析 → Skill 优化任务 → 从真实 Agent Trace 生成改进后的 Skill 文档；另有工具/模型优化。 |
| **商业闭环已有骨架** | 官网价值主张：一次发布多渠道触达（CodeArts/ModelArts/AgentArts/CloudRobo）+ 商店上架、调用收益、持续创收。 |
| **当前仍是早期** | 239 个 Skills；AgentArts 文档称 Skill 仅支持导入/管理/浏览、暂不支持智能体调用，且仅贵阳一（文档口径，可能随版本演进）。 |

---

## 1. 智果园与 AI 资产广场

### 1.1 定位

智果园是华为云的 Agentic AI 云入口（2026-06 发布），聚合体验中心、智能体、智能体平台（智果 AgentArts）、百模千态、行业 AI 梦工厂与 AI 资产广场。官方介绍强调：支持 CodeArts 码道、OfficeAce 果办、WorkAgent 等智能体；支持 DeepSeek、Kimi、GLM、Qwen 等模型；提供 Token Plan；覆盖智慧医疗、具身智能、科学计算等行业场景。

来源：[华为云智果园发布报道](https://www.c114.net.cn/industry/88276.html)、[智果园入口](https://agentorchard.huaweicloud.com/)。

智果园下的 **AI 资产广场**（pangu.huaweicloud.com/gallery）定位为“打造 AI 应用，从优质资产开始”，汇聚 **Skills、模型与数据集**，并延伸到应用、提示词、合集。

来源：[AI 资产广场首页](https://pangu.huaweicloud.com/gallery/homepage.html)。

### 1.2 资产结构

AI 资产广场导航：

| 一级入口 | 内容 |
|---|---|
| 概览 | 模型、数据集、Skills 的精选与推荐 |
| 模型库 | 银行、生命科学、医疗等行业模型（如时序预测、AlphaFold_2、HuatuoGPT_o1） |
| 数据集 | 金融、医疗、物流、科学计算等行业数据集 |
| **Skills** | 云服务 Skills、行业 Skills、通用 Skills |
| 应用 | 智能体/应用类资产 |
| 提示词 | 提示词模板 |
| 合集 | 资产合集 |
| 文档 / 我的工作台 | 文档与个人资产管理 |

来源：[AI 资产广场首页](https://pangu.huaweicloud.com/gallery/homepage.html)、[Skills 列表](https://pangu.huaweicloud.com/gallery/asset-list-page.html?type=skills)。

### 1.3 Skills 列表与详情

**规模与分类**（2026-10-20 页面）：

- 共 **239 个 Skills**；
- 标签：**行业 / 云服务 / 通用**；
- 行业细分：智慧金融（银行/保险/证券）、科学计算（生命科学/材料科学/地球科学/决策科学）、智慧政府（政务办公/政务服务/城市治理/产业发展）、智慧医疗（药物研发/临床试验/辅助诊断/健康服务）、其他行业（智能制造/智慧农业）。

**卡片字段**：名称、描述、行业标签、许可证（MIT/Apache/Data files © Original Authors 等）、作者/团队、更新时间、收藏数、下载/使用数。

**详情页字段**：标题、描述、分类、语言、许可证、收藏/下载、更新时间、**申请使用**按钮、`Skill 介绍` / `Skill 文件` 两个页签；介绍页会展示完整 Skill 文档（含环境、工具、执行步骤，部分字段脱敏）。

**安装/获取方式**：

- 开放 Skills：页面直接给 `npx skills add ...` 命令，或通过 `skills.sh` CLI 安装；安装后重启 Agent 客户端即可使用。
- `https://pangu.huaweicloud.com/skills/{user}/{slug}` 返回可安装的 ZIP 包（实际请求返回 ZIP 二进制）。
- 部分行业/企业 Skill 详情页是 **「申请使用」**，不是直接下载；说明平台对高敏感/高价值资产有准入控制。

来源：[Skills 列表](https://pangu.huaweicloud.com/gallery/asset-list-page.html?type=skills)、[Skill 详情示例](https://pangu.huaweicloud.com/gallery/asset-detail-page.html?id=e770278c-9653-4bda-8d81-fb5ede5468e1)、[Skill 制品包示例](https://pangu.huaweicloud.com/skills/ur5217372/dev-design-workflow)。

### 1.4 多渠道分发与商业闭环

官网「为什么选择 AI 资产广场」两张价值主张图给出两条核心能力：

**多渠道触达**：
> 资产一站式创建、发布、上架全流程闭环；支持分发至 CodeArts、ModelArts、AgentArts、CloudRobo 等平台，触达华为云海量用户，扩大资产影响力。
- 一站式发布 / 多平台发布 / 华为云生态 / 影响力放大。

**调用变现**：
> 资产上架平台商店，审核通过后面向最终用户售卖，用户购买使用即产生收益，构建从创造到变现的完整商业闭环。
- 商店上架 / 调用收益 / 持续创收 / 商业变现。

来源：AI 资产广场首页「为什么选择」图片（多渠道触达PC2.jpg、调用变现PC1.jpg）。

> 这意味着 AI 资产广场不是单一仓库，而是 **“一次发布、多平台分发 + 商店变现”** 的资产运营层；Skill 与模型、数据集共享同一套发布/商店/触达机制。

---

## 2. AgentArts 的 Skill 能力：标准、评估与优化

### 2.1 Skill 标准与制品包

AgentArts 将 Skill 定义为“把隐性知识显性化、结构化的任务解决方案”，核心是 **按需加载**：智能体先读 SKILL.md 元数据，判断相关后再加载必要内容，避免上下文过载。

制品包规范：

- ZIP 格式，遵循 **Agent Skills Standard**；
- 内部结构：`SKILL.md`（必需）+ `scripts/` + `references/` + `assets/`；
- `SKILL.md`：YAML frontmatter + Markdown；必填 `name`、`description`；
- 字段：`name`（≤64，小写字母/数字/连字符，不可首尾连字符或连续连字符）、`description`（≤1024，纯文本）、`license`、`allowed-tools`、`metadata`、`compatibility`（≤500 字符串）；
- 上传限制：ZIP 解压后只能有一个文件夹，文件夹名必须与 `name` 完全一致；`SKILL.md` 必须在根目录；包 ≤10MB；frontmatter 字段白名单校验。

来源：[Skill 介绍](https://support.huaweicloud.com/lowcode-agentarts/agentarts_05_01301.html)、[Skill 常见问题](https://support.huaweicloud.com/lowcode-agentarts/agentarts_05_01308.html)。

### 2.2 管理与当前限制

AgentArts「我的资产 > Skill」支持：

- 引用查询：定位使用该 Skill 的智能体；
- 删除：高危操作；
- 导出/导入：ZIP 备份、导入本地/第三方 Skill。

文档同时给出两条重要限制（文档口径，需以最新版本为准）：

- 功能仅在 **贵阳一** 区域提供；
- 当前版本仅支持 Skill 的 **导入、管理和浏览**，暂不支持在智能体中调用；后续版本逐步开放。

来源：[管理 Skill](https://support.huaweicloud.com/lowcode-agentarts/agentarts_05_01307.html)、[Skill 介绍](https://support.huaweicloud.com/lowcode-agentarts/agentarts_05_01301.html)。

> 这与 AI 资产广场页面的 `npx skills add` 形成“市场已可分发、平台内调用仍在演进”的张力：智果园的 Skill 资产能力正在从“可管理”走向“可消费”。

### 2.3 Skill 完整度：内建的质量评估器

AgentArts 提供 **Skill 完整度** 评估器：

| 项 | 内容 |
|---|---|
| 评估方式 | LLM 评估 |
| 评估目标 | Skill |
| 适用场景 | 离线评估；Skill 上架审核、质量巡检 |
| 评分 | 0.0 不可用 / 0.25 较差 / 0.5 一般 / 0.75 良好 / 1.0 优秀 |
| 评估维度 | 步骤完整性、输入输出定义、前置条件、错误处理 |
| 输入 | `skill_package`：skill_name、skill_manifest、instruction_body、task_description |
| 输出 | score + reason（四维度评价与改进建议） |

来源：[Skill 完整度](https://support.huaweicloud.com/ops-agentarts/agentarts_14_0135.html)。

这是智果园相对魔搭/SkillHub 的一个独特资产：**把“Skill 文档质量”做成可配置的评估器**，可嵌入上架审核与质量巡检，而不只是一个榜单分数。

### 2.4 Trace 驱动的 Skill 优化

AgentArts「智能体优化」包含：

- **轨迹分析**：对 Agent 会话 Trace 做失效分析、意图分析、执行摘要，定位到 Session/Span；
- **Skill 优化**：当任务异常根因在 Skill 文档描述不完整/不准确时，从历史执行轨迹提取相关数据，批量分析共性问题，生成优化后的 Skill 文档（补充执行步骤、准入条件、边界处理）；
- **工具优化**：优化工具描述与参数适配；
- **模型优化/部署**：强化学习训练小模型。

来源：[智能体优化介绍](https://support.huaweicloud.com/ops-agentarts/agentarts_14_0143.html)、[创建 Skill 优化任务](https://support.huaweicloud.com/ops-agentarts/agentarts_14_0155.html)。

> 这是“评测 → 反馈 → 生产”的闭环：不是人工拍脑袋改 Skill，而是用真实运行轨迹驱动 Skill 文档迭代。魔搭与 SkillHub 都还没有把这条链路做成平台内建能力。

---

## 3. 三平台对照

### 3.1 规模与供给

| 平台 | 规模 | 供给结构 | 特点 |
|---|---|---|---|
| 魔搭 Skills 中心 | 83,509 Skills / 10 类 | 社区长尾为主；聚合镜像 30.9%；阿里系官方 0.4% | 开放标准 + CLI 多宿主；规模大、官方薄 |
| 腾讯 SkillHub | 199,516 Skills / 13 类 / 1,993 企业 | 社区 + 企业 + ClawHub 镜像；企业供给进入头部 | 本地化镜像 + 企业供给 + 评测/商品化 |
| 华为智果园 AI 资产广场 | 239 Skills / 行业·云服务·通用 | 行业/企业为主，官方与行业团队供给 | 多平台分发 + 商店变现 + 行业深度 |

### 3.2 质量与评测

| 平台 | 质量机制 | 优点 | 缺口 |
|---|---|---|---|
| 魔搭 | 下载/浏览/榜单；无技能级试运行 | 规模与开放 | 质量信号弱、试运行缺位 |
| SkillHub | TRACE 5 维/15 子项 + 双路安全 + 签名 + 云沙箱 | 证据链完整、企业覆盖高 | 覆盖不均、高分集中、评测错配/版本风险 |
| 智果园 | Skill 完整度评估器 + 安全审核 + trace 驱动优化 | 文档质量可评估、优化闭环 | 评测未公开成体系、规模小、调用未完全开放 |

### 3.3 分发与商业化

| 平台 | 分发 | 商业化 |
|---|---|---|
| 魔搭 | `modelscope skills add` / npx / curl / SDK；`~/.agents/skills` | 免费为主，无明确 Skill 付费闭环 |
| SkillHub | `skillhub install` / npx / SDK；多宿主；云端沙箱 | SkillPay：买断/订阅、云端保护、直接到账、退款 |
| 智果园 | `npx skills add` / skills.sh；一发布分发 CodeArts/ModelArts/AgentArts/CloudRobo | 商店上架、调用收益、持续创收（官网价值主张） |

### 3.4 各自做得好的地方

**魔搭值得学**：
- 用 Agent Skills 开放标准 + CLI 多宿主，降低接入门槛；
- 用中文分类/搜索/榜单把长尾组织起来；
- 用公开 API 与 SDK 让开发者可编程接入。

**SkillHub 值得学**：
- 把评测做成产品：TRACE 五维/15 子项 + 双路安全 + 签名 + 云沙箱；
- 企业供给与评测覆盖绑定，形成“可信供给”；
- SkillPay 把“买断/订阅/云端保护/退款”做成商品闭环。

**智果园值得保持/放大**：
- 沿用 Agent Skills 标准与 10MB 包规范，不另造格式；
- 用 Skill 完整度评估器把“文档质量”变成可审核项；
- 用 trace 驱动 Skill 优化，形成“运行 → 诊断 → 改进”的闭环；
- 一次发布、多平台分发（CodeArts/ModelArts/AgentArts/CloudRobo）；
- 商店上架/调用收益，把资产变成可持续供给。

---

## 4. 对智果园的启示：四个必答题

### 4.1 标准与分发：一个包，多平台触达

- 继续沿用 Agent Skills 标准与 ZIP（≤10MB），把 `name/description/license/allowed-tools/metadata/compatibility` 作为上架必填；
- 把 `npx skills add` / `skills.sh` 作为开放分发入口，同时保留“申请使用”用于高敏感行业资产；
- 一次发布分发 CodeArts、ModelArts、AgentArts、CloudRobo，避免每个平台各自维护一套 Skill；
- 版本、可见性（public/unlisted/private/org）、许可证、作者、来源 URL 必须在详情页可追溯。

### 4.2 质量与信任：把证据放在分数前面

- 把 Skill 完整度评估器前置到上架审核：步骤、输入输出、前置条件、错误处理四维打分；
- 增加安全审核（内容合规/漏洞/AI 安全）与内容指纹/签名，形成“可验证”的资产；
- 评测报告绑定版本，公开维度与理由，避免只有一个黑箱总分；
- 控制“高分集中”：SkillHub 样本 72.5% ≥4.5，分数区分度有限；智果园应保留“未评测/待改进”的真实分层。

### 4.3 供给与生态：官方 + 行业 + 社区三层

- 官方做标杆（云服务 Skills、平台能力），行业/企业做深度（政务、医疗、金融、科学计算），社区做长尾；
- 239 个是起点，不是终局：先做 5–10 个垂直行业标杆，再扩品类；
- 分类/搜索/榜单/合集要能表达“行业 × 场景 × 资产类型”，避免只有技术分类；
- 企业供给要有入驻、认证、审核、分成与退出机制。

### 4.4 商业与治理：从能用到能卖

- 商店上架 + 调用收益 + 持续创收，是智果园已有骨架；下一步要补齐定价、计量、结算、退款/争议；
- license/来源/作者/版本/评测/安全报告要能串成一条追溯链；
- 下载 ≠ 用户、调用 ≠ 成功；跨平台分发后要统一口径，避免“一个资产多个数字”；
- 对高敏感 Skill（如政务、医疗）保留“申请使用/授权”而非无门槛下载。

### 4.5 优先级建议（P0/P1/P2）

| 阶段 | 目标 | 关键动作 |
|---|---|---|
| **P0 现在** | 统一入口与证据 | 包规范/导入导出/版本可见性；详情页补安装命令、文件、许可证、作者；接入 skills.sh 分发 |
| **P1 3–6 个月** | 质量与供给运营 | 完整度评测 + 安全审核 + 评测报告；trace 驱动 Skill 优化闭环；企业/行业供给与分类榜单 |
| **P2 6–12 个月** | 商业与生态 | 商店上架/调用计费/分成；跨平台分发数据；生态指标与治理机制 |

### 4.6 不要复制什么

- **不要只追规模**：魔搭 8.35 万、SkillHub 19.95 万，但都出现聚合镜像/长尾稀释；智果园 239 个应先把行业深度做透。
- **不要用单一分数代替证据**：SkillHub 的 TRACE 很有价值，但高分集中、覆盖不均、单样本错配说明“分数 + 报告 + 版本”必须一起给。
- **不要重造格式**：Agent Skills 已是事实标准；智果园应做“标准的最佳实现者”，不是新协议制定者。
- **不要把“上架”当“可调用”**：智果园当前文档仍写“导入/管理/浏览为主”，市场分发与平台内调用要分开推进，避免对外承诺超前。

---

## 5. 风险与缺口

| 问题 | 现状 |
|---|---|
| Skills 规模 | 239 个（2026-10-20 页面），仍在早期 |
| 区域 | AgentArts Skill 文档写“仅贵阳一”，需确认其他区域开放计划 |
| 调用能力 | 文档写“暂不支持在智能体中调用”，但市场已给 npx 安装命令；需统一对外口径 |
| 准入 | 部分 Skill 是“申请使用”，不是直接下载；需明确审批时效与条件 |
| 评测公开度 | Skill 完整度评估器存在，但公开详情页未展示评分/报告；需确认是否对外 |
| 商业化 | “商店上架/调用收益”是官网价值主张；定价、分成、结算、退款细则未公开 |
| 数据口径 | 收藏/下载/使用数含义需定义；跨平台分发后口径要统一 |

---

## 6. 来源

- [AI 资产广场首页](https://pangu.huaweicloud.com/gallery/homepage.html)
- [AI 资产广场 Skills 列表](https://pangu.huaweicloud.com/gallery/asset-list-page.html?type=skills)
- [Skill 详情示例（政务云等保预评估）](https://pangu.huaweicloud.com/gallery/asset-detail-page.html?id=e770278c-9653-4bda-8d81-fb5ede5468e1)
- [Skill 制品包示例](https://pangu.huaweicloud.com/skills/ur5217372/dev-design-workflow)
- [智果园入口](https://agentorchard.huaweicloud.com/)
- [AgentArts 资产广场](https://support.huaweicloud.com/productdesc-agentarts/agentarts_03_0028.html)
- [AgentArts Skill 介绍](https://support.huaweicloud.com/lowcode-agentarts/agentarts_05_01301.html)
- [AgentArts Skill 常见问题](https://support.huaweicloud.com/lowcode-agentarts/agentarts_05_01308.html)
- [AgentArts 管理 Skill](https://support.huaweicloud.com/lowcode-agentarts/agentarts_05_01307.html)
- [Skill 完整度评估器](https://support.huaweicloud.com/ops-agentarts/agentarts_14_0135.html)
- [智能体优化介绍](https://support.huaweicloud.com/ops-agentarts/agentarts_14_0143.html)
- [创建 Skill 优化任务](https://support.huaweicloud.com/ops-agentarts/agentarts_14_0155.html)
- [智果园发布报道（C114）](https://www.c114.net.cn/industry/88276.html)
- [魔搭 Skills 中心调研笔记](modelscope-skills-center-research.md)
- [腾讯 SkillHub 调研笔记](tencent-skillhub-research.md)
