# 腾讯 SkillHub：资产结构、消费链路、生态与 TRACE 评测

> 调研时间：2026-10-19 22:00–23:55（Asia/Shanghai）
> 方法：官网真实 DOM（Chrome + playwright-core）、公开只读 API、`Tencent/skillhub` 官方仓库与官方文档；辅以 60 条技能抽样（Top20 下载 / Top20 企业 / 随机 20）验证 TRACE 分数与覆盖。
> 口径约定：**【页面】**= 平台页面显示；**【API】**= 公开接口实测；**【抽样】**= 自建样本；**【官方文档】**= 官网/官方仓库。多标签来源与分类不做直接相加。

---

## 0. 一页速览

| 指标 | 数值 | 口径 | 来源 |
|---|---|---|---|
| Skill 总数 | **199,516** | 【API】`/api/skills` 的 `data.total`，2026-10-19 23:40 左右 | https://api.skillhub.cn/api/skills?page=1&pageSize=1 |
| 页面规模 | 20.0 万 | 【页面】技能列表页“共 20.0 万个技能” | https://skillhub.cn/skills |
| 一级分类 | **13**（含 Pay Skill） | 【API】`/api/v1/categories` | https://api.skillhub.cn/api/v1/categories |
| 入驻企业 | **1,993** | 【API】`/api/v1/enterprises` 的 `total` | https://api.skillhub.cn/api/v1/enterprises?page=1&pageSize=1 |
| 腾讯官方 | **155** Skills | 【页面】企业页“腾讯 155 SKILLS” | https://skillhub.cn/enterprise/org-bv6b8qcb |
| TRACE 均分 | **4.54 / 5**（中位 4.56） | 【抽样】40 条有效评测，五维等权 | `/api/v1/skills/{slug}/evaluation` |
| TRACE 覆盖 | 企业 20/20、社区 20/27、ClawHub 0/6 | 【抽样】60 条，去重 53，有效 40 | 同上 |
| 试运行 | 云端沙箱/会话/运行案例已在前端实现，本次未实测 | 【页面/官方文档】 | https://skillhub.cn、`Tencent/skillhub` |

> 数量会随同步/发布漂移：官方页面 20.0 万，API 199,516；同期不同脚本曾看到 199,511/199,514。正文统一以 199,516 为本次快照，并保留“约 20 万”的表达。

---

## 1. 资产定位与结构

### 1.1 四层分析视图（非官方强制依赖）

SkillHub 官网导航与产品对象不只包含单个 Skill。用四层分析视图可以解释“人格、场景、方法、工具”的组合关系：

| 层 | 资产 | 解决什么 | 官方入口/承载 | 与 Skill 的关系 |
|---|---|---|---|---|
| **L4 角色层** | SOUL / Soul.md | 人格、表达与协作方式 | `/soul` | 为 Agent 提供行为与风格配置，可与技能组合 |
| **L3 场景组合层** | 专家包 / 技能包 | 围绕一个工作场景获取多项能力 | `/skillspackage` | 聚合多个 Skills，减少逐项选择成本 |
| **L2 任务方法层** | Skill | 完成具体任务的方法与资源 | `/skills` | 本层主体：`SKILL.md` + 脚本 + 参考 + 模板 |
| **L1 工具服务层** | MCP / 外部 API | 访问真实数据、执行受控动作 | `/mcp` | 提供工具接口、服务与连接，仍需鉴权和运行条件 |

> **声明：四层是本稿的分析视图，不是 SkillHub 官方定义的强制继承/依赖架构。** 官方材料分别提供 Soul、专家包、Skill、MCP 入口，但没有把它们定义成四级分类。

### 1.2 Skill 本体与平台记录

```text
Skill 内容：SKILL.md + 可选脚本、参考资料、模板
平台记录：来源、作者、版本、分类、依赖、热度、质量、安全
安装实例：某个版本在某个宿主中的内容与连接状态
运行案例：某次输入、对话、工具调用与生成结果
```

- Skill 遵循通用格式；官方说明支持网页、CLI、GitHub、Agent 发布，版本、可见性、团队审核是平台记录的一部分。
- 详情页提供概述、文件、评论、版本历史、评测报告；文件接口返回逐文件 `sha256`。
- 平台为每个版本提供内容指纹与数字签名：`content_hash`、`package_md5`、`publisher_real_name_verified`、`signature`。示例 `dev-expert-pro` v1.1.0：152 个文件、逐文件 SHA-256。

---

## 2. 资产消费：来源、发布、消费、试运行

### 2.1 来源：全球同步、本土共建与企业服务并存

| 来源通道 | 证据 | 说明 |
|---|---|---|
| **ClawHub 同步** | 页面/API 的 `source=clawhub`；官方仓库声明持续同步全球 Skills | 国内加速与中文描述，补齐长尾 |
| **社区发布** | 网页 / CLI / Agent 发布；`source=community` | 个人与社区作者 |
| **企业/产品团队** | 企业专区、认证企业、`source=enterprise` | 腾讯文档、ima、钢联、电子印章等 |
| **官方自营** | 腾讯企业页 155 Skills；平台维护 `find-skill-skillhub` 等 | 平台自服务与产品能力连接 |

**来源口径要小心**：`source=community`、`source=enterprise`、`source=clawhub` 的 `total` 相加大于总数（136k + 69k + 63k > 199k），说明来源可重叠/多标签。**Top50 样本**（下载量降序）来源为社区 23 条（46%）、ClawHub 14 条（28%）、企业 13 条（26%）；这只是头部样本，不是全量结构。

### 2.2 发布：目录、ZIP 与团队库

- 入口：网页 `dashboard/publish`、CLI（`login/init/push/publish`）、GitHub/Agent 发布。
- 平台记录：版本、可见性（public/unlisted/private/org）、分类、团队审核；团队发布场景是“自动安全审核 → 团队管理员审核（可配置自动）”。
- 发布审核与 TRACE 是两条机制：审核决定“能否上架”，TRACE 决定“质量参考”，二者不能混为一谈。
- 官方文档/教程没有公开统一的 TRACE 合格分数线或安全风险量化阈值。

### 2.3 消费：网页发现与 Agent 入口并行

| 入口 | 能力 | 对使用体验的意义 |
|---|---|---|
| Web | 中文搜索、分类、榜单、详情、报告 | 降低发现和选择成本 |
| CLI | `skillhub search/install/update`、`--dir`、`skillhub link` | 在终端完成获取与管理 |
| ZIP / 版本下载 | 指定版本或 tag 下载 | 支持显式版本选择与人工部署 |
| Open API | 列表、详情、文件、版本差异、质量结果 | 可嵌入企业门户、IDE 或自有 Agent |
| DSH 插件 | 对话中搜索、详情、版本选择、本地安装 | 减少离开宿主操作的步骤 |

安装命令（官方 install.md）：

```bash
skillhub search <keyword>
skillhub install <slug> --dir <skills 目录>
```

- **默认目录是 `./skills/`**；不指定 `--dir` 时可能不被当前 Agent 识别。DSH 默认 `~/.dsh/skills`，可配置。
- 常见宿主目录：Claude Code `~/.claude/skills/`、Cursor `~/.cursor/skills/`、Codex `~/.codex/skills/` 或项目 `.agents/skills/`、Gemini CLI `~/.gemini/skills/`、Windsurf、Antigravity、QoderWork、workbuddy 等。
- 安装器下载、解包、写文件；**不自动执行包内脚本，也不自动安装 pip/npm 依赖**。依赖、账号、网络与权限仍需宿主侧满足。

### 2.4 试运行：云端沙箱与运行案例

- 官网当前生产前端包含 `createSandboxSession`、`resumeSandboxSession`、`loadSandboxSkills`、`purgeSandboxSession`、会话历史、流式输出、运行案例保存等流程，对应 `/api/v1/sandbox/sessions...`。
- 官方能力文档列出沙箱、会话、文件处理；公开 API 目录尚未给出完整运行接口契约。
- **本次只读核查，没有登录、创建会话或执行 Skill**；不把“代码存在”写成“运行成功实测”。隔离效果、成功率、耗时、费用仍需实测。
- 这是 SkillHub 相对“只提供下载”的平台的关键差异：从“能装”延伸到“能在云端验证一个具体任务并留存案例”。

---

## 3. 生态画像

### 3.1 规模

| 指标 | 数值 | 口径 |
|---|---|---|
| Skill 总数 | 199,516 | 【API】2026-10-19 23:40 左右 |
| 页面规模 | 20.0 万 | 【页面】技能列表 |
| 一级分类 | 13 | 【API】含 Pay Skill |
| 入驻企业 | 1,993 | 【API】企业列表 `total` |
| 腾讯官方 | 155 Skills | 【页面】腾讯企业页 |
| 来源记录 | community ≈136k、enterprise ≈69k、clawhub ≈63k | 【API】可重叠，不可直接相加 |
| Pay Skill 分类 | 19,940 | 【API】`category=pay-skill`，多标签，非独立总量 |

### 3.2 供给画像：平台官方、垂直/企业、社区泛用

| 供给群体 | 代表资产 | 供给特点 | 对应消费需求 |
|---|---|---|---|
| **平台官方/腾讯产品** | 腾讯文档、ima、腾讯会议 MCP、平台查找技能、TRACE 评测 | 平台自服务与产品能力连接 | 找技能、文档与知识协作、质量检查 |
| **垂直行业/企业** | 钢联 AI 智能问数、全国电子印章互认、国泰海通、携程、36氪、小包公法律 | 行业数据、业务接口、专业服务 | 行情与业务数据、专业流程对接 |
| **社区泛用/全球同步** | Find Skills、Agent Browser、Summarize、Self-Improving Agent、编程专家系列 | 跨任务基础能力与广泛长尾 | Agent 研发、浏览器操作、摘要与通用效率 |

- **Top50 样本来源**：社区 46%、ClawHub 28%、企业 26%。企业供给已进入下载头部，但样本只代表头部，不代表全量。
- **Top50 下载类别**：开发编程 36.9%、AI Agent 13.2%、知识管理 10.2%、其他 39.7%；开发类 5 条贡献 36.9%，头部集中度高。
- **平台官方数量少但单点影响力大**：腾讯 155 个 Skills；腾讯文档、ima 等进入头部。

### 3.3 消费画像

- 下载/安装/收藏/星标是不同信号：`downloads` 可能包含 CLI/镜像/脚本拉取，`installs` 在部分头部记录为 0，不能反推“下载→使用”转化率。
- Top 下载示例（【API】）：编程专家Pro.Skill 518.7 万、编程大神.Skill 505.6 万、编程专家.Skill 486.3 万、搜索引擎 369.6 万、腾讯文档 180.9 万。
- Top50 样本下载记录合计约 5,334 万；这是样本合计，不是全平台总下载。
- 消费需求画像（研发/知识办公/行业业务）依据技能能力推断，不是平台用户调查。

---

## 4. 评测机制：TRACE 深挖

### 4.1 五维、15 子项、5 分制

| 维度 | 核心问题 | 子项 |
|---|---|---|
| **T Trust 可信任度** | 能否放心用、本土环境能否使用 | 安全扫描 `scan`、本土适配 `domestic` |
| **R Reliability 可靠性** | 是否稳定、完整、有异常处理 | `stability`、`func`、`errorHandling` |
| **A Adaptability 适用性** | 何时该调用、边界是否清晰 | `boundary`、`trigger` |
| **C Convention 规范性** | 是否便于理解、维护和复用 | `progressive`、`structure`、`docQuality`、`antiPatternFaq` |
| **E Effectiveness 有效性** | 最终产出是否可用且有价值 | `accuracy`、`completeness`、`usability`、`creativity` |

- 子项满分 5，未评估可为 `null`；展示总分按“维度内均分 → 五维等权”计算。
- 官网前端展示等级：≥4 优秀、≥3 良好、≥2 及格；这是展示分级，不是上架硬门槛。
- TRACE 与列表 `score` 必须分开：`score` 是排序用综合热度，不可直接换算为 5 分制质量分。

### 4.2 官方定位与发布背景

- 官方/技术百科材料称：TRACE 于 **2026-05-21** 由腾讯科技、SkillHub、腾讯玄武实验室联合发布，是国内首个面向 Skill 真实使用场景的严选评测体系。
- 方法：主客观结合——`no-skill` 对照组判断真实增益，旗舰模型盲评；每月一期 TOP10 编辑精选，避免全量评分不可持续和头部效应。
- 平台安全审核为三线并行：内容合规过滤、科恩实验室漏洞扫描、云鼎实验室 AI 模型安全评估；全部通过才上架，报告可在详情页查看。
- **注意**：官网称“评测主要基于 AI 自动化检测，结果供参考”；开源 TRACE evaluator 固定跳过 `trust.scan`，对文档型 Skill 允许依据流程/模板推断有效性——不能把开源 evaluator 当作平台安全扫描器，也不能把每个分数解释为动态实跑。

### 4.3 抽样验证：覆盖、分数、分布

样本：**60 条**（Top20 下载、Top20 企业、随机 20），去重 53，有效评测 40。

| 分段 | 有效/样本 | 覆盖率 | 平均综合分 |
|---|---:|---:|---:|
| 企业 | 20/20 | **100%** | 4.59 |
| 社区 | 20/27 | **74%** | 4.49 |
| ClawHub | 0/6 | **0%** | — |
| 合计（去重） | 40/53 | 75% | **4.54** |

- **企业评测覆盖最完整，ClawHub 镜像基本没有 TRACE**；Top20 下载中 11/20 返回 404，说明头部社区/同步技能的评测并不完整。
- 40 条有效评测的五维均值：**T 4.87、R 4.35、A 4.48、C 4.38、E 4.61**；T 最高（安全与本土可用），R 最低（稳定性/异常处理）。
- 综合分：中位 **4.56**，均值 4.54，最低 4.12，最高 4.84；**72.5% ≥4.5，0 条 <4.0**。分数明显向高分集中，区分度有限。
- 评测按 `versionId` 绑定；旧版本/未评测版本可能返回空或 404，详情页展示的分数需要与目标版本核对。

### 4.4 证据链：安全、指纹、签名、成本

以 `dev-expert-pro` v1.1.0 为例（【API】/【页面】）：

- 页面显示 **4.4 / 5（优秀）**；T 4.3、R 4.2、A 4.3、C 4.6、E 4.6。
- 安全报告：**科恩实验室“安全，无风险”**；**云鼎实验室“可疑，存在潜在风险”**。同一技能两路结论不同，说明“安全”不是单点结论。
- 内容指纹：`content_hash` + `package_md5` + 152 个文件的逐文件 SHA-256。
- 数字签名：`publisher_real_name_verified=true`，签名由 `skillhub.cn` 平台密钥签发。
- 评测成本：**274,519 tokens**（约 27.5 万），DeepSeek V4 Flash 沙箱预估；实际消耗随模型、宿主、环境变化。

### 4.5 评测风险与异常

- **单样本错配**：`find-skill-skillhub` 详情的功能是平台技能检索，但对应评测解释围绕日志处理、`grep/awk/jq` 等场景，存在内容不一致。单样本不能推算全站错误率，但说明“身份—内容哈希—版本—评测”需要可追溯。
- **AI 评分主观性**：评测理由由模型生成，文档结构、示例充分性等指标有主观性；分数高且集中，不能替代真实任务验收。
- **覆盖不均衡**：企业 100%、社区 74%、ClawHub 0%（样本）；对“全站质量信号”不能做无差别推断。
- **版本时效**：评测绑定版本；技能更新后旧分数可能失效，详情页需明确版本。

---

## 5. 总结：5 条判断

1. **SkillHub 的差异化不是“更大”，而是“更可信”。** 19.95 万 Skill 的规模之上，TRACE 五维/15 子项、双路安全报告、内容指纹、数字签名和 token 成本，把“选哪个”从下载量变成多维证据链。
2. **评测与企业供给强绑定。** 企业 100% 覆盖、社区 74%、ClawHub 0%（样本）；企业供给既是专业场景来源，也是评测覆盖最好的部分。
3. **分数高且集中，评测更像“精品标签”而非“全量质量刻度”。** 72.5% ≥4.5、最低 4.12、0 条 <4.0；AI 自动评分有主观性，不能替代任务验收。
4. **消费链路已从“下载”延伸到“宿主 + 云端案例”。** CLI/DSH/API/ZIP 四入口、多宿主目录、云端沙箱与运行案例；但安装不自动装依赖，云端运行本次未实测。
5. **下一关是可信规模化。** 需要全量覆盖、版本一致、评测与包内容对齐、下载/安装口径统一；否则评测只是头部标签，难以成为市场的基础设施。

---

## 6. 可直接上页的关键数字（10 条）

| # | 数字/事实 | 来源 |
|---|---|---|
| 1 | Skill 总数 **199,516**（页面 20.0 万） | https://api.skillhub.cn/api/skills?page=1&pageSize=1 |
| 2 | 一级分类 **13**，入驻企业 **1,993** | https://api.skillhub.cn/api/v1/categories、https://api.skillhub.cn/api/v1/enterprises?page=1&pageSize=1 |
| 3 | 腾讯官方 **155** Skills | https://skillhub.cn/enterprise/org-bv6b8qcb |
| 4 | Top50 来源：社区 46% / ClawHub 28% / 企业 26% | `skillhub/statistics.json`、`download-top50.csv` |
| 5 | Top50 下载类别：开发 36.9% / AI Agent 13.2% / 知识 10.2% / 其他 39.7% | 同上 |
| 6 | TRACE 五维/15 子项、5 分制、维度均分后五维等权 | https://github.com/Tencent/skillhub/blob/main/docs/api/evaluation.md |
| 7 | 抽样 40 条有效：中位 **4.56**，均值 4.54，72.5% ≥4.5，最低 4.12 | 本次抽样（60 条去重 53） |
| 8 | 覆盖：企业 20/20、社区 20/27、ClawHub 0/6 | 本次抽样 |
| 9 | 示例 4.4/5；科恩“安全”/云鼎“可疑”；274,519 tokens；152 文件 SHA-256 | https://api.skillhub.cn/api/v1/skills/dev-expert-pro/evaluation?namespace=indiv-integrator 等 |
| 10 | 云端沙箱/会话/运行案例已在前端实现，本次未实测 | https://skillhub.cn、`Tencent/skillhub` |

---

## 7. 图表建议

| 图表 | 数据 | 为什么 |
|---|---|---|
| **TRACE 五维横向柱** | T 4.87 / R 4.35 / A 4.48 / C 4.38 / E 4.61 | 一页看懂“T 最高、R 最低” |
| **评测覆盖分组柱** | 企业 100%、社区 74%、ClawHub 0% | 直接说明覆盖不均衡 |
| **分数分布条/直方图** | 40 条有效；4.0–4.2 2 条、4.2–4.4 5 条、4.4–4.6 17 条、4.6–4.8 15 条、4.8–5.0 1 条 | 说明高分集中、区分度有限 |
| **Top50 来源堆叠条** | 社区 46 / ClawHub 28 / 企业 26 | 头部供给结构 |
| **Top50 下载类别横向柱** | 开发 36.9 / Agent 13.2 / 知识 10.2 / 其他 39.7 | 消费头部集中 |
| 不建议 | 全站来源占比饼图、增速折线 | 来源多标签重叠；没有可靠时间序列 |

---

## 8. 数据快照与复现命令

```bash
# 总数
curl -s 'https://api.skillhub.cn/api/skills?page=1&pageSize=1' | jq '.data.total'
# 分类
curl -s 'https://api.skillhub.cn/api/v1/categories' | jq '.count'
# 企业
curl -s 'https://api.skillhub.cn/api/v1/enterprises?page=1&pageSize=1' | jq '.total'
# 评测（示例）
curl -s 'https://api.skillhub.cn/api/v1/skills/dev-expert-pro/evaluation?namespace=indiv-integrator' | jq '.dimensions | keys'
# 文件与签名
curl -s 'https://api.skillhub.cn/api/v1/skills/dev-expert-pro/files?version=1.1.0&namespace=indiv-integrator' | jq '.count'
curl -s 'https://api.skillhub.cn/api/v1/open/skills/dev-expert-pro/versions/1.1.0/signature?namespace=indiv-integrator' | jq '.payload'
# token
curl -s 'https://api.skillhub.cn/api/v1/skills/dev-expert-pro/token-usage?namespace=indiv-integrator' | jq '.usage'
```

**抽样说明**：Top20 下载（`sortBy=downloads&order=desc`）、Top20 企业（`source=enterprise&sortBy=downloads`）、随机 20（默认列表第 5 页）；去重后 53 条，40 条有效。TRACE 覆盖率是样本估计，不是全站精确值。

---

## 9. 已知缺口

| 缺口 | 尝试 | 结论 |
|---|---|---|
| 全量 TRACE 覆盖率 | 抽样 60 条 + 公开 API | 只能给样本估计；全站精确值未公开 |
| 全站来源精确占比 | `source` 过滤 total 相加 > 总数 | 多标签/重叠，不能直接相加 |
| 审核规则/TRACE 合格线 | 官网教程、官方仓库、发布流程 | 未公开统一阈值/时效 |
| 云端沙箱实测 | 未登录/未创建会话 | 只确认前端实现，未验证成功率/隔离/费用 |
| SkillPay 真实收入 | 官网/公告 | 首页“本月调用/收益”标注示例数据，不能当真实 |
| 评测错配根因 | 单样本 `find-skill-skillhub` | 只记录现象，不推断全站错误率 |

---

## 10. 主要来源

- [SkillHub 官网](https://skillhub.cn)
- [Tencent/skillhub 官方仓库](https://github.com/Tencent/skillhub)
- [评测 API 文档](https://github.com/Tencent/skillhub/blob/main/docs/api/evaluation.md)
- [TRACE 教程](https://skillhub.cn/tutorials#trace-evaluation)
- [TRACE evaluator](https://github.com/Tencent/skillhub/blob/main/skills/skillhub-trace-evaluator/SKILL.md)
- [安装文档](https://skillhub.cn/install/skillhub.md)
- [公开列表 API](https://api.skillhub.cn/api/skills?page=1&pageSize=1)
- [分类 API](https://api.skillhub.cn/api/v1/categories)
- [企业 API](https://api.skillhub.cn/api/v1/enterprises?page=1&pageSize=1)
- [示例技能详情](https://skillhub.cn/skills/indiv-integrator/dev-expert-pro)
- [腾讯云技术百科 SkillHub](https://cloud.tencent.com/developer/techpedia/2618)
- [TRACE 评测体系文章](https://cloud.tencent.cn/developer/article/2698657)
- [SkillPay 报道](https://tech.cnr.cn/techgd/20260717/t20260717_527715580.shtml)
- 本地子调研：[skillhub-insights.md](../skillhub/skillhub-insights.md)、[research-evaluation-runtime.md](../skillhub/research-evaluation-runtime.md)、[research-supply-distribution-install-v1.md](../skillhub/research-supply-distribution-install-v1.md)
