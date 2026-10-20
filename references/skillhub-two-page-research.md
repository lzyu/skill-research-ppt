# SkillHub 两页材料：关键能力与 Top5000 生态画像

> 调研快照：2026-10-20（Asia/Shanghai）
> 口径：公开 API（Top5000 下载降序）+ 官方页面 + `Tencent/skillhub` 官方仓库文档；TRACE 沿用 2026-10-19 的 40 条有效抽样，页面标注“抽样”。
> 用途：支撑 deck 第 3 页「关键能力」、第 4 页「Top5000 生态画像」。

## 一句话结论

SkillHub 的差异不只是“20 万 Skill”，而是把**供给、安装、云端试跑、TRACE 评测**接成一条链；但 Top5000 头部样本显示：**ClawHub 撑数量，社区/企业单条更强；全站付费 10%、API Key 19%，但 Top5000 付费只有 1%。**

## A. 关键能力（第 3 页）

### 1. 供给与发布
- 公开 API 总数 **200,462**（2026-10-20 抓取）；页面口径约 **20.0 万**。
- 一级分类 **13 个**（含 Pay Skill）。
- 入驻企业 **1,999** 家；腾讯官方 **155** 个 Skills（企业页实测）。
- 来源三条线：**ClawHub 同步、社区发布、企业/产品团队**；来源字段可重叠，不能直接相加。
- 发布入口：Web、CLI、GitHub、Agent；版本、可见性（public / unlisted / private / org）、团队审核是平台记录。
- 审核与 TRACE 是两条机制：审核决定能否上架，TRACE 是质量参考，不能混为一谈。
- 来源：[公开 API](https://api.skillhub.cn/api/skills?page=1&pageSize=1)、[分类 API](https://api.skillhub.cn/api/v1/categories)、[企业 API](https://api.skillhub.cn/api/v1/enterprises?page=1&pageSize=1)、[腾讯企业页](https://skillhub.cn/enterprise/org-bv6b8qcb)。

### 2. 分发与安装
- 入口：Web、CLI、Open API、DSH 插件、ZIP / 版本下载。
- 官方 CLI：
  ```bash
  skillhub search <keyword>
  skillhub install <slug> --dir <skills 目录>
  ```
- 默认目录 `./skills/`；不指定 `--dir` 时可能不被当前 Agent 识别。DSH 默认 `~/.dsh/skills`，可配置。
- 安装器下载、解包、写文件；**不自动执行包内脚本，也不自动安装 pip/npm 依赖**。
- 来源：官方 install 文档（`https://skillhub.cn/docs/skills/install`，2026-10-19 抓取）、官方仓库 README。

### 3. 云端试跑
- 官网前端已实现 `createSandboxSession` / `resumeSandboxSession` / `loadSandboxSkills` / `purgeSandboxSession`、会话历史、流式输出、运行案例保存。
- 官方 Open API 文档把“沙箱、会话、流式输出、文件处理”列为能力，但公开 API 目录尚未给出完整运行接口契约；高消耗场景建议联系官方。
- 本次只读核查，**没有登录、创建会话或执行 Skill**；隔离效果、成功率、耗时、费用仍需实测。
- 来源：[官方仓库 README](https://github.com/Tencent/skillhub)、[API 文档](https://github.com/Tencent/skillhub/blob/main/docs/README.md)、[API 使用与资源支持](https://github.com/Tencent/skillhub/blob/main/docs/apply.md)。

### 4. TRACE 评测
- 五维、15 子项、5 分制：Trust（scan / domestic）、Reliability（stability / func / errorHandling）、Adaptability（boundary / trigger）、Convention（progressive / structure / docQuality / antiPatternFaq）、Effectiveness（accuracy / completeness / usability / creativity）。
- 展示总分：维度内均分，再五维等权；等级 ≥4 优秀、≥3 良好、≥2 及格，是展示分级，不是上架硬门槛。
- 抽样 **60 条**（Top20 下载、Top20 企业、随机 20），去重 **53**，有效评测 **40**。
- 综合分：均值 **4.54**，中位 **4.56**，最低 4.12，最高 4.84；**72.5% ≥4.5**，**0 条 <4.0**。
- 覆盖：企业 **20/20 = 100%**、社区 **20/27 = 74%**、ClawHub **0/6 = 0%**。
- 五维均值：T 4.87、R 4.35、A 4.48、C 4.38、E 4.61；T 最高、R 最低。
- 评测绑定 `versionId`；旧版本/未评测版本可能为空或 404；分数高且集中，AI 评分有主观性，不能替代真实任务验收。
- 来源：[官方 TRACE 词条](https://cloud.tencent.cn/developer/techpedia/2618/20639)、[评测 API 文档](https://github.com/Tencent/skillhub/blob/main/docs/api/evaluation.md)、2026-10-19 抽样。

## B. Top5000 生态画像（第 4 页）

### 样本与总量
- 公开 API 按 `sortBy=downloads&order=desc` 取 **Top5000**，2026-10-20 抓取。
- 总下载 **134,768,414（约 1.35 亿）**；均值 26,954，中位 **7,521**。
- Top1 占 **3.9%**，Top10 **24.2%**，Top100 **48.9%**，Top1000 **77.3%**。
- 5000 条中 **1,519 条 `installs=0`**；`downloads` 含 CLI/镜像拉取，不等于安装/使用。

### 1. Top5000 由谁上架（个人 / 企业 / 镜像）
| 类型 | 条数 | 条数占比 | 下载占比 | 中位下载 |
|---|---:|---:|---:|---:|
| 个人 / 社区 | 1,245 | 24.9% | **39.8%** | 8,730 |
| 企业 | 633 | 12.7% | 24.7% | **12,725** |
| 镜像 ClawHub | 3,122 | 62.4% | 35.5% | 6,756 |

- 个人/社区条数少、下载高；企业单条最强；镜像条数最多、单条最弱。
- 个人 = 社区作者直接发布；企业 = 企业/组织账号；镜像 = ClawHub 同步。
- 来源：[Top5000 API](https://api.skillhub.cn/api/skills?pageSize=100&sortBy=downloads&order=desc&page=1)。

### 2. 分类占比（全站，不用 Top5000）
- 全站 **200,403 条**；12 个内容分类合计 200,393 条，另有 10 条未挂类目。
- 条数占比：商业运营 **15.2%**、专业服务 **11.6%**、AI Agent **11.2%**、开发编程 **10.6%**、内容创作 **9.4%**、设计多媒体 **7.4%**；其余 6 类合计 **34.7%**。
- 全站结构比 Top5000 更均衡：Top5000 里 ClawHub 62.4%、社区 24.9%、企业 12.7%；分类不能被头部样本代表。
- **Pay Skill 是多标签分类，20,125 条（10.0%），不计入上述 12 类**，否则会重复计数。
- 分类 API：https://api.skillhub.cn/api/skills?pageSize=1&page=1&category=ai-agent（替换 category 取各分类 total）。

### 3. 消费集中度（Top5000）
- Top1 **3.9%**、Top10 **24.2%**、Top100 **48.9%**、Top1000 **77.3%**。
- 头部 Skill：编程大神 521.3 万、编程专家Pro 519.2 万、编程专家 487.6 万、搜索引擎 463.5 万、dev-expert 417.2 万。
- 前三条均为编程类，合计约 1,528 万，占 Top5000 的 11.3%。
- `installs` 与下载严重脱节：1,519/5,000 条 `installs=0`；腾讯文档 8,107、self-improving agent 86,140、Find Skills 75,956。
- 下载是“发行/拉取”信号，不是用户数或成功运行数。

### 4. 谁被下载（中位）
| 上架方 | 条数 | 单条中位下载 |
|---|---:|---:|
| 企业 | 633 | **12,725** |
| 个人 / 社区 | 1,245 | 8,730 |
| 镜像 ClawHub | 3,122 | 6,756 |
| Top5000 整体 | 5,000 | 7,521 |

- 企业单条最强，个人高于镜像；但企业条数最少，个人/社区条数也远少于镜像。
- 集中度补充：Top5000 共 2,883 个上架方，Top10 占 9.0% 条数、37.9% 下载；Top50 16.0% / 58.7%；Top100 21.8% / 66.5%；Top500 44.8% / 83.4%。
- 这是“单条中位”口径，不是总下载；镜像总下载仍占 35.5%，因为条数多。
- 注意：账号级归并，企业多账号、社区 user_id 不完全等同真实作者。

### 5. PaySkill 与 API Key（全站，不用 Top5000）
| 类型 | 条数 | 全站占比 | Top5000 对照 |
|---|---:|---:|---:|
| Pay Skill 分类 | 20,125 | **10.0%** | 0 条（0%） |
| 付费标签 pricing_type=paid | 17,123 | 8.5% | 50 条（1.0%） |
| 支付宝 pricing_type=alipay | 2,901 | 1.4% | 3 条（0.1%） |
| API Key requires_api_key=true | 38,646 | **19.3%** | 1,441 条（28.8%） |
| Pay Skill 且 API Key | 331 | 1.6%（占 Pay Skill） | 1 条 |

- **全站付费 10.0%，但 Top5000 付费只有 1.0%**：付费供给大量存在，只是没进下载头部。
- **全站 API Key 19.3%，Top5000 反而 28.8%**：API Key 类在头部被高估。
- 付费标签（8.5%）与 Pay Skill 分类（10.0%）不是同一口径，不能混用；Pay Skill 分类还包含支付宝等标签。
- API Key 最集中在商业运营（76.0%），其次数据分析 36.6%、设计多媒体 35.8%、知识管理 33.8%；AI Agent 仅 16.5%，开发编程 13.9%。

## 数据口径与缺口
- 总数会漂移：2026-10-19 为 199,516，2026-10-20 为 200,462；页面写“20.0 万”。
- Top5000 是下载头部样本，不代表全量 20 万；供给/消费/Top5000 上架方看头部，分类与付费/API Key 用全站。
- `pricing_type` 标签可能不完整；Top5000 只有 50 条付费标签，不能据此推断全站付费供给比例。
- API Key 是 `labels.requires_api_key=true`，不代表一定收费或一定需要用户自备 Key。
- TRACE 为 60 条抽样、去重 53、有效 40；覆盖率是样本口径，不是全站覆盖率。
- 云端试跑只确认前端/官方能力描述，本次未登录实测。

## 来源清单
1. 公开 Skill 列表：https://api.skillhub.cn/api/skills?page=1&pageSize=1
2. Top5000 下载榜：https://api.skillhub.cn/api/skills?pageSize=100&sortBy=downloads&order=desc&page=1（翻 50 页）
3. 分类：https://api.skillhub.cn/api/v1/categories
4. 企业：https://api.skillhub.cn/api/v1/enterprises?page=1&pageSize=1
5. 腾讯企业页：https://skillhub.cn/enterprise/org-bv6b8qcb
6. 官方仓库：https://github.com/Tencent/skillhub
7. TRACE 官方词条：https://cloud.tencent.cn/developer/techpedia/2618/20639
8. TRACE API 文档：https://github.com/Tencent/skillhub/blob/main/docs/api/evaluation.md
9. 官方 install 文档：https://skillhub.cn/docs/skills/install（2026-10-19 抓取）
