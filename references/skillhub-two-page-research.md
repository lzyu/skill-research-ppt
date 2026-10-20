# SkillHub 两页材料：关键能力与 Top1000 生态画像

> 调研快照：2026-10-20（Asia/Shanghai）
> 口径：公开 API（Top1000 下载降序）+ 官方页面 + `Tencent/skillhub` 官方仓库文档；TRACE 沿用 2026-10-19 的 40 条有效抽样，页面标注“抽样”。
> 用途：支撑 deck 第 3 页「关键能力」、第 4 页「Top1000 生态画像」。

## 一句话结论

SkillHub 的差异不只是“20 万 Skill”，而是把**供给、安装、云端试跑、TRACE 评测**接成一条链；但 Top1000 头部样本显示：**ClawHub 撑数量、社区撑下载、开发类最重、付费标签仍在边缘，API Key 已是三成供给。**

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

## B. Top1000 生态画像（第 4 页）

### 样本与总量
- 公开 API 按 `sortBy=downloads&order=desc` 取 **Top1000**，2026-10-20 抓取。
- 总下载 **104,071,496（约 1.04 亿）**；均值 104,071，中位 **32,907**。
- Top1 占下载 **5.0%**，Top3 **14.7%**，Top10 **31.3%**，Top50 **52.7%**，Top100 **63.3%**。
- 1000 条中 **443 条 `installs=0`**；`downloads` 含 CLI/镜像拉取，不等于安装/使用。

### 1. 谁在供给
| 来源 | 条数 | 条数占比 | 下载占比 | 中位下载 |
|---|---:|---:|---:|---:|
| ClawHub | 447 | 44.7% | 27.0% | 29,655 |
| 社区 community | 305 | 30.5% | **44.2%** | 39,902 |
| 企业 enterprise | 248 | 24.8% | 28.8% | 33,547 |

- **ClawHub 条数最多，但下载份额最低**；社区条数三成，却拿走 44.2% 下载。
- 社区 = 个人/社区作者直接发布；企业 = 企业/组织账号；ClawHub = 外部同步/镜像。
- 来源：[Top1000 API](https://api.skillhub.cn/api/skills?pageSize=100&sortBy=downloads&order=desc&page=1)。

### 2. 分类占比
| 分类 | 条数占比 | 下载占比 |
|---|---:|---:|
| 开发编程 | 7.2% | **21.8%** |
| AI Agent | **15.8%** | 15.4% |
| 办公效率 | 12.7% | 10.4% |
| 知识管理 | 6.8% | 9.5% |
| 内容创作 | 11.8% | 9.2% |
| 设计多媒体 | 12.3% | 8.1% |
| 其余 6 类 | 33.4% | 25.6% |

- **开发类只占 7.2% 供给，却拿走 21.8% 下载**；AI Agent 供给最多（15.8%），下载占比 15.4%，略低于供给。
- 12 个实际分类中 Pay Skill 在 Top1000 为 **0 条**（付费 Skill 下载量未进入头部）。
- 分类口径来自每条 Skill 的 `category` 字段；下载为 `downloads` 字段汇总。

### 3. PaySkill 与 API Key
| 类型 | 条数 | 占比 | 下载占比 |
|---|---:|---:|---:|
| PaySkill（pricing_type=paid/alipay） | 9 | **0.9%** | 0.8% |
| API Key（requires_api_key=true） | 307 | **30.7%** | 21.6% |
| 付费且 API Key | 1 | 0.1% | 0.05% |
| Pay Skill 分类 | 0 | 0% | 0% |

- **付费在 Top1000 几乎不可见**：9 条、0.9%；大部分付费 Skill 不在下载头部。
- **API Key 已是三成供给**：307 条、30.7%，但下载占比 21.6%，低于条数占比。
- API Key 最集中在商业运营（73/96 = 76.0%），其次数据分析（36.6%）、设计多媒体（35.8%）、知识管理（33.8%）；AI Agent 仅 16.5%，开发编程 13.9%。
- 付费标签按 `pricing_type=paid/alipay` 统计；Pay Skill 分类单独统计，二者不混用。

### 4. 头部 Skill
- 编程大神 521.3 万、编程专家Pro 519.2 万、编程专家 487.6 万、搜索引擎 463.5 万、dev-expert 417.2 万。
- 前三条均为编程类，合计约 1,528 万，占 Top1000 的 14.7%。
- `installs` 与下载严重脱节：Top20 中多数 `installs=0`，腾讯文档 8,107、self-improving agent 86,140、Find Skills 75,956。
- 下载是“发行/拉取”信号，不是用户数或成功运行数。

## 数据口径与缺口
- 总数会漂移：2026-10-19 为 199,516，2026-10-20 为 200,462；页面写“20.0 万”。
- Top1000 是下载头部样本，不代表全量 20 万；来源/分类占比不能外推全站。
- `pricing_type` 标签可能不完整：Top1000 只有 9 条付费标签，Pay Skill 分类 0 条；不能据此推断全站付费供给比例。
- API Key 是 `labels.requires_api_key=true`，不代表一定收费或一定需要用户自备 Key。
- TRACE 为 60 条抽样、去重 53、有效 40；覆盖率是样本口径，不是全站覆盖率。
- 云端试跑只确认前端/官方能力描述，本次未登录实测。

## 来源清单
1. 公开 Skill 列表：https://api.skillhub.cn/api/skills?page=1&pageSize=1
2. Top1000 下载榜：https://api.skillhub.cn/api/skills?pageSize=100&sortBy=downloads&order=desc&page=1
3. 分类：https://api.skillhub.cn/api/v1/categories
4. 企业：https://api.skillhub.cn/api/v1/enterprises?page=1&pageSize=1
5. 腾讯企业页：https://skillhub.cn/enterprise/org-bv6b8qcb
6. 官方仓库：https://github.com/Tencent/skillhub
7. TRACE 官方词条：https://cloud.tencent.cn/developer/techpedia/2618/20639
8. TRACE API 文档：https://github.com/Tencent/skillhub/blob/main/docs/api/evaluation.md
9. 官方 install 文档：https://skillhub.cn/docs/skills/install（2026-10-19 抓取）
