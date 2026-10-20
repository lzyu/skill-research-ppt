# SkillHub 两页材料：关键能力与生态画像

> 调研快照：2026-10-20（Asia/Shanghai）
> 口径：公开 API + 官方页面 + `Tencent/skillhub` 官方仓库文档；TRACE 抽样沿用 2026-10-19 样本，页面标注“抽样”。
> 用途：支撑 deck 第 3 页「关键能力」、第 4 页「生态画像」。

## 一句话结论

SkillHub 的差异不只是“20 万 Skill”，而是把**供给、安装、云端试跑、TRACE 评测**接成一条链；但生态仍然头部集中，评测覆盖明显偏向企业，ClawHub 镜像基本没有 TRACE。

## A. 关键能力（第 3 页）

### 1. 供给与发布
- 公开 API 总数 **200,462**（2026-10-20 抓取）；页面口径约 **20.0 万**。
- 一级分类 **13 个**（含 Pay Skill）。
- 入驻企业 **1,999** 家；腾讯官方 **155** 个 Skills（企业页实测）。
- 来源三条线：**ClawHub 同步、社区发布、企业/产品团队**；`source` 字段的 community / enterprise / clawhub 总数可重叠，不能直接相加。
- 发布入口：Web、CLI、GitHub、Agent；版本、可见性（public / unlisted / private / org）、团队审核是平台记录。
- 审核与 TRACE 是两条机制：审核决定能否上架，TRACE 是质量参考，不能混为一谈。
- 来源：[公开 API](https://api.skillhub.cn/api/skills?page=1&pageSize=1)、[分类 API](https://api.skillhub.cn/api/v1/categories)、[企业 API](https://api.skillhub.cn/api/v1/enterprises?page=1&pageSize=1)、[腾讯企业页](https://skillhub.cn/enterprise/org-bv6b8qcb)、[官方仓库 README](https://github.com/Tencent/skillhub)。

### 2. 分发与安装
- 入口：Web、CLI、Open API、DSH 插件、ZIP / 版本下载。
- 官方 CLI：
  ```bash
  skillhub search <keyword>
  skillhub install <slug> --dir <skills 目录>
  ```
- 默认目录 `./skills/`；不指定 `--dir` 时可能不被当前 Agent 识别。DSH 默认 `~/.dsh/skills`，可配置。
- 常见宿主目录：Claude Code `~/.claude/skills/`、Cursor `~/.cursor/skills/`、Codex `~/.codex/skills/` 或项目 `.agents/skills/`、Gemini CLI `~/.gemini/skills/` 等。
- 安装器下载、解包、写文件；**不自动执行包内脚本，也不自动安装 pip/npm 依赖**；依赖、账号、网络、权限仍由宿主侧满足。
- 来源：官方 install 文档（`https://skillhub.cn/docs/skills/install`，2026-10-19 抓取）、官方仓库 README。

### 3. 云端试跑
- 官网前端已实现 `createSandboxSession` / `resumeSandboxSession` / `loadSandboxSkills` / `purgeSandboxSession`、会话历史、流式输出、运行案例保存，对应 `/api/v1/sandbox/sessions...`。
- 官方 Open API 文档把“沙箱、会话、流式输出、文件处理”列为能力，但公开 API 目录尚未给出完整运行接口契约；高消耗场景建议联系官方。
- 本次只读核查，**没有登录、创建会话或执行 Skill**；不能把“代码存在”写成“运行成功实测”。隔离效果、成功率、耗时、费用仍需实测。
- 来源：[官方仓库 README](https://github.com/Tencent/skillhub)、[官方 API 文档](https://github.com/Tencent/skillhub/blob/main/docs/README.md)、[API 使用与资源支持](https://github.com/Tencent/skillhub/blob/main/docs/apply.md)。

### 4. TRACE 评测
- 五维、15 子项、5 分制：Trust（scan / domestic）、Reliability（stability / func / errorHandling）、Adaptability（boundary / trigger）、Convention（progressive / structure / docQuality / antiPatternFaq）、Effectiveness（accuracy / completeness / usability / creativity）。
- 展示总分：维度内均分，再五维等权；等级 ≥4 优秀、≥3 良好、≥2 及格，是展示分级，不是上架硬门槛。
- 抽样 **60 条**（Top20 下载、Top20 企业、随机 20），去重 **53**，有效评测 **40**。
- 综合分：均值 **4.54**，中位 **4.56**，最低 4.12，最高 4.84；**72.5% ≥4.5**，**0 条 <4.0**。
- 覆盖：企业 **20/20 = 100%**、社区 **20/27 = 74%**、ClawHub **0/6 = 0%**。
- 五维均值：T 4.87、R 4.35、A 4.48、C 4.38、E 4.61；T 最高、R 最低。
- 评测绑定 `versionId`；旧版本/未评测版本可能为空或 404；分数高且集中，AI 评分有主观性，不能替代真实任务验收。
- 来源：[官方评测 API 文档](https://github.com/Tencent/skillhub/blob/main/docs/api/evaluation.md)、2026-10-19 抽样（40 条有效）、[官方 TRACE evaluator](https://github.com/Tencent/skillhub/tree/main/skills/skillhub-trace-evaluator)。

## B. 生态画像（第 4 页）

### 1. 谁在供给（Top50 头部样本）
- 社区 **22 条 / 44%**、ClawHub **14 条 / 28%**、企业 **14 条 / 28%**（2026-10-20 下载降序 Top50）。
- 全站：20.0 万 Skill、13 个一级类目、1,999 家企业、腾讯官方 155。
- 46/28/26 的旧口径已被本次 44/28/28 取代；差异来自榜单滚动，不是统计错误。
- 来源：[Top50 API](https://api.skillhub.cn/api/skills?page=1&pageSize=50&sortBy=downloads&order=desc)。

### 2. 什么被下载（Top50 下载类别）
- 开发编程 **36.3%**、AI Agent **13.0%**、知识管理 **11.6%**、其余 **39.1%**（其他为剩余类目合计）。
- 开发类 5 条贡献 36.3%，头部集中度高；样本只代表下载头部，不代表全量供给。
- 来源：同上 Top50 API，按 `category` 汇总 `downloads`。

### 3. 消费有多集中
- Top50 下载合计 **54,812,922（约 5,481 万）**。
- 头部：编程大神 521.3 万、编程专家Pro 519.1 万、编程专家 487.6 万、搜索引擎 458.0 万、腾讯文档 182.3 万。
- 前三条编程 Skill 合计约 1,528 万，占 Top50 的 27.9%。
- `downloads` 可能包含 CLI、镜像、脚本拉取，不等于用户数；50 条样本中 29 条 `installs=0`，下载与安装/使用不能直接换算。
- 来源：Top50 API。

### 4. 质量覆盖
- TRACE 覆盖：企业 100%、社区 74%、ClawHub 0%（样本）。
- 均值 4.54，72.5% ≥4.5；最低 4.12，0 条 <4.0；高分集中、区分度有限。
- 企业评测覆盖最完整；ClawHub 镜像基本没有 TRACE；Top20 下载中 11/20 返回 404（旧样本），说明头部社区/同步技能评测并不完整。
- 分数绑定版本，且 AI 自动评分有主观性；不能替代真实任务验收。
- 来源：2026-10-19 抽样、官方 evaluation 文档。

## 数据口径与缺口

- 总数会随同步/发布漂移：2026-10-19 为 199,516，2026-10-20 为 200,462；页面写“20.0 万”，避免过度精确。
- 企业数从 1,993 → 1,999（2026-10-20 API）。
- Top50 来源/类别是**下载头部样本**，不是全量结构；来源字段多标签重叠，不能做全站占比饼图。
- TRACE 为 60 条抽样、去重 53、有效 40；覆盖率是样本口径，不是全站覆盖率。
- 云端试跑只确认前端/官方能力描述，本次未登录实测。
- 官方仓库 README 仍写“13 万+ Skills / 2 万+ 企业”，与当前 API 明显不一致；以 API/页面当前值为准，不引用旧营销数字。

## 来源清单

1. 公开 Skill 列表：https://api.skillhub.cn/api/skills?page=1&pageSize=1
2. Top50 下载榜：https://api.skillhub.cn/api/skills?page=1&pageSize=50&sortBy=downloads&order=desc
3. 分类：https://api.skillhub.cn/api/v1/categories
4. 企业：https://api.skillhub.cn/api/v1/enterprises?page=1&pageSize=1
5. 腾讯企业页：https://skillhub.cn/enterprise/org-bv6b8qcb
6. 官方仓库：https://github.com/Tencent/skillhub
7. TRACE API 文档：https://github.com/Tencent/skillhub/blob/main/docs/api/evaluation.md
8. API 总览：https://github.com/Tencent/skillhub/blob/main/docs/api/README.md
9. 能力/资源说明：https://github.com/Tencent/skillhub/blob/main/docs/README.md
10. 官方 install 文档：https://skillhub.cn/docs/skills/install（2026-10-19 抓取）

## 相对旧 note 的变化

- 总数 199,516 → 200,462；企业 1,993 → 1,999。
- Top50 来源 46/28/26 → 44/28/28。
- Top50 下载类别 36.9/13.2/10.2/39.7 → 36.3/13.0/11.6/39.1。
- Top50 下载合计 5,334 万 → 5,481 万；头部排序变化（编程大神升至第 1）。
- TRACE 结论不变（旧抽样 40 条有效）；页面继续标注“抽样”。
