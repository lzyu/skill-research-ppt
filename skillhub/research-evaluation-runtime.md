# 腾讯 SkillHub：TRACE、可信机制与试运行证据

调研日期：2026-10-19（北京时间）。范围仅包括腾讯 SkillHub 官网、官网当前加载的公开前端资源、`Tencent/skillhub` 官方仓库及公开只读 API。未登录、未安装 Skill、未创建或运行沙箱会话、未发布案例；因此不把文档与代码证据写成运行成功实测。

## 可放入单页的 5 条结论

1. **用四种信号帮助选择：来源认证、安全报告、TRACE 质量、行为热度。** 认证发布者、双路安全状态、TRACE 分数、下载/收藏及榜单分别回答不同问题。列表 `score` 是排序热度，不能直接当作 TRACE 的 5 分制质量得分。[列表字段](https://github.com/Tencent/skillhub/blob/main/docs/api/skills.md)、[插件映射代码](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/src/api.ts)
2. **TRACE 为 5 维、15 子项；展示总分按五维等权。** T 可信任度、R 可靠性、A 适用性、C 规范性、E 有效性；先计算各维子项均值，再取五维均值，保留 1 位小数。不是对 15 子项直接取平均。[评测 API](https://github.com/Tencent/skillhub/blob/main/docs/api/evaluation.md)
3. **安全审核与 AI 质量评测是两条机制。** 官网描述 AI 行为识别、静态检测、动态沙箱交叉验证；而公开的 TRACE evaluator 基于已读包内容给出质量判断，固定跳过安全扫描，对文档型 Skill 明确允许依据流程/模板推断效果。不能宣称开源 evaluator 已把所有技能动态实跑。[官网 TRACE 教程](https://skillhub.cn/tutorials#trace-evaluation)、[开源评测技能](https://github.com/Tencent/skillhub/blob/main/skills/skillhub-trace-evaluator/SKILL.md)、[有效性细则](https://github.com/Tencent/skillhub/blob/main/skills/skillhub-trace-evaluator/references/effectiveness.md)
4. **云端试运行已经有具体产品与前端实现，但本次没有执行验证。** 官网生产代码包含会话创建/恢复、加载 Skill、历史、流式输出、运行案例保存及会话错误恢复流程。公开仓库文档确认沙箱、会话、文件处理能力，但公开 API 目录尚未给出完整运行接口契约。[官网当前前端资源](https://cloudcache.tencent-cloud.com/qcloud/tea/app/skillhub/assets/skill-hub.cpdwg332.js?max_age=31536000)、[能力说明](https://github.com/Tencent/skillhub/blob/main/docs/capabilities.md)、[已整理接口总览](https://github.com/Tencent/skillhub/blob/main/docs/api/README.md)
5. **评测是采用参考，仍须检查结果与目标版本是否对应。** 质量 API 绑定 `versionId`，允许尚无结果；本次单样本发现 `find-skill-skillhub` 的公开评测内容却围绕日志分析，存在描述错配，尚不能确认根因，不宜据此断言全站结果失效。[质量接口约定](https://github.com/Tencent/skillhub/blob/main/docs/api/evaluation.md)、[当前示例详情](https://api.skillhub.cn/api/v1/skills/find-skill-skillhub)、[当前示例评测](https://api.skillhub.cn/api/v1/skills/find-skill-skillhub/evaluation)

## 1. TRACE 评什么

| 维度 | 核心问题 | 子项 |
|---|---|---|
| Trust 可信任度 | 能否放心用、本土环境能否使用 | 安全扫描 `scan`、本土适配 `domestic` |
| Reliability 可靠性 | 是否稳定、完整、有异常处理 | `stability`、`func`、`errorHandling` |
| Adaptability 适用性 | 何时该调用、边界是否清晰 | `boundary`、`trigger` |
| Convention 规范性 | 是否便于理解、维护和复用 | 渐进披露 `progressive`、结构 `structure`、文档 `docQuality`、反模式/FAQ `antiPatternFaq` |
| Effectiveness 有效性 | 最终产出是否可用且有价值 | 准确 `accuracy`、完整 `completeness`、即用 `usability`、增值 `creativity` |

来源：[官方评测 API 的基础维度表](https://github.com/Tencent/skillhub/blob/main/docs/api/evaluation.md)。官网教程以质量观察坐标解释上述维度，并明确结果用于辅助判断，非对行为的保证。[TRACE 教程](https://skillhub.cn/tutorials#trace-evaluation)

### 分数、权重、等级与门槛

- 公开 evaluator 要求普通子项 `0 < score <= 5.0`，缺失方面通常给 1.0–2.0；每项必须同时有开发者理由和普通用户理由，不能未读文件就评分。[SKILL.md](https://github.com/Tencent/skillhub/blob/main/skills/skillhub-trace-evaluator/SKILL.md)
- 质量 API 子项满分 5，未评估可为 `null`；总分不直接返回，由接入方按“维度内均分 → 五维平均”展示。标准口径相当于五维各 20%，但子项的最终贡献随该维有效子项数变化；公开资料未披露额外业务加权。[evaluation.md](https://github.com/Tencent/skillhub/blob/main/docs/api/evaluation.md)
- 当前官网前端 `ScoreOverview` 将 ≥4 显示为优秀，≥3 为良好，≥2 为及格，其余为待改进。这是界面展示等级；没有证据说明它是上架或推荐的硬性准入线。[生产前端代码，查找 `function ScoreOverview`](https://cloudcache.tencent-cloud.com/qcloud/tea/app/skillhub/assets/skill-hub.cpdwg332.js?max_age=31536000)
- 发布审核另有安全门槛：官网团队发布教程描述先自动安全审核，再团队管理员审核（人工，可配置自动）；任一未通过，该版本不会上架。未公开具体风险量化阈值或 TRACE 合格分数线。[官网教程](https://skillhub.cn/tutorials)
- 校验脚本只验证结构、必填项、分数范围等；不验证读包是否真实、结论是否事实正确，也没有统一总分及格阈值。[校验器](https://github.com/Tencent/skillhub/blob/main/skills/skillhub-trace-evaluator/scripts/validate_trace_scores.py)、[输出规则](https://github.com/Tencent/skillhub/blob/main/skills/skillhub-trace-evaluator/references/output-schema.md)

### TRACE 分数与榜单 `score` 必须分开

| 字段/接口 | 明确含义 | 不应推断 |
|---|---|---|
| `/evaluation` 的子项分数 | 版本级质量评价，5 分制，附理由 | 不等于动态执行成功率 |
| `/api/skills` 的 `score` | 供排序使用的综合热门度，值越大越热门 | 不可直接换算为 TRACE 五分制 |
| `/api/skills/top` | 按综合 `score` 取前 50，同分按更新时间倒序 | 不代表质量最高的 50 个 |
| `downloads` / `stars` / `installs` | 下载调用量 / 收藏量 / 安装量 | 不代表真实运行次数、活跃用户或任务成功率 |

官网榜单附近进一步解释综合分参考 TRACE、下载和收藏，但未披露组合公式；因此只能说质量与热度共同参与推荐，不能自行设权重。[列表文档](https://github.com/Tencent/skillhub/blob/main/docs/api/skills.md)、[榜单文档](https://github.com/Tencent/skillhub/blob/main/docs/api/categories.md)、[官网技能列表](https://skillhub.cn/skills?sortBy=score)

## 2. 安全声明、公开实现与实测边界

**平台层安全机制（官方声明）**：官网 TRACE 教程说明以安全实验室交叉扫描作为基础，行为分析、静态分析和动态沙箱用于发现恶意代码、信息泄露及异常联网等；仓库 README 将其描述为双重安全认证。[教程](https://skillhub.cn/tutorials#trace-evaluation)、[README](https://github.com/Tencent/skillhub/blob/main/README.md)

**可观察到的安全元数据（代码及只读 API 证据）**：DSH 插件接收 `securityReports.keen` 和 `.sanbu`，识别 `benign`、`scanning`、`suspicious`、`malicious` 并提供报告入口；实查 `find-skill-skillhub` 详情的两路均为 `benign`。这证明报告状态和查看入口存在，不证明本次已复现扫描过程或审计每份报告。报告 URL 含签名参数，不在本文转录。[映射代码](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/src/api.ts)、[示例详情](https://api.skillhub.cn/api/v1/skills/find-skill-skillhub)

**本地安装防护（开源可核验）**：插件安装 ZIP 时拒绝路径穿越并要求存在 `SKILL.md`；技能 ZIP 仅落盘，不由安装器执行包内脚本。插件市场安装 DSH 插件则会在宿主执行安装命令，是另一种安装边界。[安装器](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/src/install.ts)、[插件 README](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/README.md)

**开源 TRACE evaluator 的边界**：必须定位本地包并读 `SKILL.md`、关键脚本与参考内容；没有包就停止。`trust.scan` 固定标记 skipped，信任维只评本土适配；效果维对文档型技能依据流程和模板作推断。因此它是基于证据的 AI 包质量评审流程，不是平台完整安全扫描服务的开源复刻。[探索细则](https://github.com/Tencent/skillhub/blob/main/skills/skillhub-trace-evaluator/references/explore.md)、[信任维细则](https://github.com/Tencent/skillhub/blob/main/skills/skillhub-trace-evaluator/references/trust.md)、[效果维细则](https://github.com/Tencent/skillhub/blob/main/skills/skillhub-trace-evaluator/references/effectiveness.md)

## 3. 云端试运行：已知流程与未验证内容

| 能力 | 证据 | 本次验证层级 |
|---|---|---|
| 创建、恢复、加载技能、删除工作区 | 生产前端含 `createSandboxSession`、`resumeSandboxSession`、`loadSandboxSkills`、`purgeSandboxSession`，对应 `/api/v1/sandbox/sessions...` | 静态代码读取，未调用 |
| 继续上次会话 | 前端列历史会话、尝试 resume、加载当前 skill，冲突时重试或新建 | 静态代码读取，未恢复真实会话 |
| 流式聊天与运行历史 | 前端包含流式帧解析、`getSessionHistory`、`SandboxCaseChat` | 静态代码读取，未发送提示 |
| 运行案例 | 前端可选消息并保存案例，案例包含对话、工具调用、生成结果；可衔接发布过程 | 代码/官网产品说明，未保存 |
| 文件处理 | 官方 Open API 能力文档明确列出文件处理；运行资源支持还需确认文件上限、并发、时长和 Token | 文档证据，未上传文件或测上限 |
| 沙箱真实隔离、响应速度、成功率、网络权限 | 公开仓库未提供完整运行服务源码；本次不启动线上执行 | 未验证 |

来源：[官网当前资源，检索上述函数名](https://cloudcache.tencent-cloud.com/qcloud/tea/app/skillhub/assets/skill-hub.cpdwg332.js?max_age=31536000)、[能力说明](https://github.com/Tencent/skillhub/blob/main/docs/capabilities.md)、[Open API README](https://github.com/Tencent/skillhub/blob/main/docs/README.md)。高消耗运行能力建议上线前确认容量和资源方案；公开默认采用共享资源，可能限流或降级。[接入说明](https://github.com/Tencent/skillhub/blob/main/docs/apply.md)

这意味着平台体验已经从“下载文件”延伸到“在云端验证一个具体任务并留存案例”。这是根据产品入口和前端流程作出的分析，尚不是对运行效果的实测结论。

## 4. 单样本质量异常记录

在 2026-10-19 只读请求：

- 详情 `/api/v1/skills/find-skill-skillhub` 返回名称 **find skill**，描述为平台技能检索，最新版本 `1.0.2`。
- 对应 `/evaluation` 返回 `skillId=194434`、`versionId=303153`，摘要和多维解释却围绕日志处理、`grep/awk/jq`、堆栈分析等场景。该解释与详情功能不一致；同份解释内部也同时出现“7 个适用场景明确”与“没有使用场景指南”等不一致描述。
- 已将原始评价响应保存为 [evaluation-find-live.json](sources/evaluation-find-live.json)。它是单次只读快照；线上响应可能继续变化。尚未确认是数据映射、评测关联、缓存还是其他原因，不作根因判断，也不以一个样本计算错误率。

此异常说明：若平台建设方把评测用于推荐和发布治理，应把 **Skill 身份、内容哈希、版本、评测任务、报告** 连成可追溯链，并抽检评价与包内容是否对应。此句为建设建议，不是腾讯现状事实。

## 5. 关于“四层资产”的补充

官网当前导航明确区分：Skill（可调用能力）、专家包（按场景组合一组 Skill）、MCP（连接工具和服务）、SOUL（人格与表达）；首页说明专家包用多个 Skills 连续协作推进完整工作交付。仓库 README 也明确 Soul 与行业技能包组合的方向。[官网](https://skillhub.cn)、[README](https://github.com/Tencent/skillhub/blob/main/README.md)

可以用“角色设定 → 能力连接 → 单项技能 → 场景组合”解释资产的组合关系，但应标注为**分析视角**；官方公开材料并未将上述四种产品资产定义为严格继承或依赖的四层架构。不要把专家包、技能包、Soul、Skill 当成同一资产表里已公开的四级分类。
