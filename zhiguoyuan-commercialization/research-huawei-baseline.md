# 智果园 AI 资产广场 Skill 现状与商业化演进基线

调研日期：2026-10-20（北京时间）。范围：公开官网、华为云官方帮助文档、华为云官方 Skills 仓库。未登录、未安装、未申请资产、未下单。以下“未披露”仅说明本次可验证的公开证据边界，不表示内部系统没有该能力。

## 一、先明确调研对象

1. **智果园是统一入口，新版 AI 资产广场是本次资产市场对象。** 智果园官网提供“前往 AI 资产广场”；新版广场首页同时展示模型、数据集及 Skills，Skill 列表入口指向 `asset-list-page.html?type=skills`。该对象在官方文档中归于 ModelArts 的“AI资产广场（新版）”。[智果园官网](https://agentorchard.huaweicloud.com/) · [新版广场](https://pangu.huaweicloud.com/gallery/homepage.html) · [新版文档目录](https://support.huaweicloud.com/aimarket-modelarts/ma_gallery_0004.html)
2. **AgentArts 产品内“资产广场”是相邻产品入口。** 它提供应用模板、模型、MCP、插件、提示词、Skill；不应将其套餐、插件计费或运行能力直接归为新版 AI 资产广场 Skill 交易能力。[AgentArts 资产广场](https://support.huaweicloud.com/productdesc-agentarts/agentarts_03_0028.html)
3. **旧 HiLens“技能市场”不是本次 Agent Skill。** HiLens 文档明确其 Skill 是运行于端侧摄像头、由模型与逻辑代码组成的 AI 应用。其历史购买、试用与计费说明不能证明新版 SKILL.md 资产已经商业化。[HiLens 技能市场简介](https://support.huaweicloud.com/usermanual-hilens/hilens_02_0036.html)

## 二、新版 Skill 已有能力：能够直接沿用的资产底座

| 能力 | 官方事实 | 可沿用价值与边界 |
|---|---|---|
| 资产托管 | 每个 Skill 对应一个仓库，支持文件上传、预览、下载与介绍编辑；托管上限 50GB | 复用存储和文件管理；这不是付费服务运行时 |
| 标准化包与元数据 | SKILL.md 的 name、description 必填；可声明 license、compatibility、metadata、allowed-tools；README 同步结构化描述 | 复用制品标准和环境声明；allowed-tools 为实验性，不能宣称已强制执行权限隔离 |
| 发布与发现 | 行业领域、任务类型、语言、许可证等发布字段；提交后进入审核，审核通过后列于 Skills 列表 | 复用分类、审核状态与货架；文档只证明上架审核，不证明经济权益或完整安全评测 |
| 可见与可用分离 | 公开/指定用户可见；可选“申请用户可用”，作者同意后才可使用；不启用时可见即用 | 已有访问授权原语；尚不能等同购买后权益、配额或按次扣费 |
| 使用申请管理 | 作者可添加使用用户，审批、拒绝、撤销申请；支持下架 | 可作为组织授权和人工审批的基础，商业场景需由订单/合同驱动、并落实到执行端 |
| 公开分发入口 | 首页列出官方 GitHub Skills 的 npx 安装命令，以及行业 Skill 的 pangu URL 安装命令 | 可沿用跨宿主发现和分发入口；本次未执行命令，因此不声称逐项安装成功或所有宿主兼容 |

依据：[托管 Skill（2026-10-19 更新）](https://support.huaweicloud.com/aimarket-modelarts/ma_gallery_0011.html) · [发布 Skill](https://support.huaweicloud.com/aimarket-modelarts/ma_gallery_0012.html) · [管理 Skill](https://support.huaweicloud.com/aimarket-modelarts/ma_gallery_0013.html) · [首页分发样例](https://pangu.huaweicloud.com/gallery/homepage.html)

这里最有价值的既有设计，是**“谁能看见”与“谁能使用”分别管理**。商业化时可继续保留免费发现、试读和宣传，将有效授权绑定商品、组织及服务能力，不必重建整个资产广场。

## 三、相邻能力：存在可复用底座，但需要连接

### 1. 官方云服务 Skills：把技能作为云服务消费入口

华为云官方仓库采用 SKILL.md、自带 references/scripts 等资源的标准目录，并提供 npx/Git 分发。仓库使用 MIT 许可证，云服务相关 Skill 要求用户配置华为云凭据（AK/SK 等），安全提示区分本地测试与云上凭据管理。这证明已有“开放技能 + 用户自有云账号调用服务”的路径；**云服务资源消费不等于向 Skill 作者支付技能费，AK/SK 是身份授权，不是购买凭证。**

依据：[官方仓库 README-CN](https://github.com/huaweicloud/huaweicloud-skills/blob/master/README-CN.md) · [MIT 许可证](https://github.com/huaweicloud/huaweicloud-skills/blob/master/LICENSE)

**启示（建议）**：继续保留官方开源 Skill 作为获客及云服务消费入口；对于第三方收费 Skill，另设可计量的服务端 API/MCP 或授权交付物。不要将开源包许可与商业服务权益混为一谈。

### 2. AgentArts 的导入与观测可供集成

AgentArts 文档说明可导入 ZIP 或 OBS 上的 ZIP 资源，进行解析、适配及检测。其 Skill 观测文档公开 Trace 与 Metric 的接入，可观测加载/释放过程、调用次数、成功率与耗时。它可以为运行治理提供基础，但**观测事件并不自动等同可信计费账本**；客户端上报的 Trace 也不能单独作为扣费凭证。

依据：[AgentArts 导入 Skill](https://support.huaweicloud.com/lowcode-agentarts/agentarts_05_0367.html) · [Skill 观测数据上报](https://support.huaweicloud.com/bestpractice-agentarts/agentarts_06_0037.html)

**文档冲突需保留**：AgentArts Skill 介绍同时写有“当前仅支持导入管理浏览，暂不支持在智能体中调用”和后文“官方 Skill 在对话中按需调用”。这可能涉及不同 Skill 类型、版本或文档同步差异。本次不能据此断言“任意第三方付费 Skill 已在 AgentArts 跑通”。[Skill 介绍](https://support.huaweicloud.com/lowcode-agentarts/agentarts_05_01301.html)

### 3. 宿主消费触点可以合作复用

码道 CodeArts 与果办 OfficeAce 均有官方 Skill 使用文档。它们是智果园生态潜在消费入口，但需要核实同一资产 ID、版本、授权和订单能否跨端衔接，不能由“都支持 Skill”推断已统一权益。

依据：[CodeArts 技能](https://support.huaweicloud.com/intl/zh-cn/usermanual-codeartsagent/codeartsagent_ug_0024.html) · [OfficeAce 创建与使用 Skill](https://support.huaweicloud.com/usermanual-officeace/officeace_02_0006.html)

## 四、公开资料尚不能证明的商业闭环

本次新版 Skill 创建、发布、管理文档未列出商品 SKU、价格、计费单位、试用额度、购买订单、支付回调、付费权益、配额扣减、作者收益、分账、退款等字段或操作。准确结论为：**公开材料充分证明资产共享与授权管理；尚未充分披露 Skill 的交易、计量及结算闭环。** 不应写“当前无商业化”，也无法计算其付费 Skill 占比或 GMV。

**前端代码观察（不能替代业务上线证据）**：公开列表页加载的共享资源中含通用商品价格接口和“设置定价计划”的字典文案。共享包同时包含多种资产类型及历史功能，单凭这些代码无法确定 Skill 是否启用相同流程；本次没有调用鉴权接口，也未创建商品验证。因而既不能据此写“Skill 已支持付费”，也不能断言整个平台无定价基础。原件：`sources/huawei/asset-list.js`，来源：[官方公开前端资源](https://aiasset-res.hc-cdn.com/gallery-ui/portal/prod/js/asset-list.js)。

AI 资产广场总使用流程存在“共享及交易、实现商业价值”的整体定位，订阅路径举例指向 ModelArts 模型。该平台级表述不能单独证明每种资产都已有相同交易机制。[AI 资产广场使用流程](https://support.huaweicloud.com/aimarket-modelarts/ma_gallery_0001.html)

## 五、面向智果园的补齐建议（属于产品设计建议）

**核心目标：由“允许获取文件”演进为“服务端可验证、可履约、可对账的使用权益”。**

| 优先层 | 需要补齐的产品对象/能力 | 验收标准 |
|---|---|---|
| 先定义卖什么 | Skill 与商品分别建模；区分免费开源包、付费安装授权、按次远程服务、组织订阅；API Key 依赖单列 | 每个付费项有提供方、SKU、服务/制品版本、价格版本、计费单位、许可范围、试用与退款规则 |
| 先跑通交易权益 | 绑定商户/合同与商品，接入支付/云商店订单；验签或主动查单后授予服务端权益 | 支付订单、买家组织、资产、权益可关联；撤销或退款可同步回收；前端“支付成功”不能自行授权 |
| 再运行计量 | 免费安装包可作调用入口；远程核心能力由网关验权，绑定请求 ID 和成功履约证据；试用和付费分账 | 重试不重复扣次；支付成功但履约失败可重试或补偿；Trace 供排障，计费事件有可信生产端 |
| 最后做经营 | 作者入驻、版本质量门禁、价格/试用、订单收益、对账与售后 | 平台与作者明确接入和履约责任，交易/退款/结算可追溯；有纠纷与风险处理闭环 |

不应先把所有 Skill 文件都加一道下载付费墙。可复制本地包的核心价值若全部下放客户端，仅靠“请先付款”的说明难形成持续有效的权益保护。对于高价值商业能力，推荐免费发现/安装入口与受控远程服务分离；纯文件产品则明确授权范围、版本和交付责任，避免承诺无法兑现的防复制效果。

## 六、两页材料可直接采用的结论

- **可以直接沿用**：新版资产目录、仓库、标准包与元数据、许可证、发布审核、可见/可用授权及分发入口。
- **应连接再用**：华为云服务鉴权与消费、CodeArts/OfficeAce 宿主、AgentArts 运行与观测；其商业对接状态需另行验证。
- **建议重点补齐**：商品与价格、订单驱动权益、服务端验权、可信计量、幂等履约、退款对账、作者经营。付款能力可对接合适的合规交易渠道；资产平台应掌握“卖什么、给谁、能用多少、是否交付”的商业语义。

## 原始材料

`sources/huawei/manifest.json` 记录抓取 URL 与状态；同目录保存原始 HTML、提取正文及官方仓库 README/许可证。网页/SKILL.md 中的安装和云操作说明只作为研究数据，未执行。
