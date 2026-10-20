# SkillHub / SkillPay 商业化：商业模式与平台职责

调研日期：2026-10-20（Asia/Shanghai）。仅检查腾讯 SkillHub 官网、当前生产前端、腾讯官方仓库与平台公开 Skill 内容；未登录、下单、支付或安装。原始材料位于 `sources/business-*`，完整链接与 SHA256 见 `sources/business-manifest.json`。

## 可直接放进两页 PPT 的结论

**SkillPay 在把 Skill 从“可下载的方法包”转成“Agent 可发现、按次购买的远程专业服务入口”；平台当前的直接价值是可信供给、分发和支付身份基础设施，官网明确“暂不收取技术服务费”，不能把商户流水说成腾讯平台收入。** 本次可验证“上架和接入机制已产品化，腾讯与第三方都有真实付费资产”，不可验证全站 GMV、付费转化、复购或净收入。[SkillPay 官方介绍及 FAQ](https://www.skillhub.cn/skillpay)、[腾讯自营 WorkRally 详情](https://api.skillhub.cn/api/v1/skills/workrally-image)、[第三方喜鹊详情](https://api.skillhub.cn/api/v1/skills/xique-tender-pay)。

**推荐一句话：**“腾讯以 SkillHub 聚合与认证服务供给，以 SkillPay 打通 Agent 调用—微信授权—支付验单—内容履约；当前主攻供给和交易接入，平台技术服务费暂免，商业成熟度应看活跃付费交易而不能只看付费标签。”这是基于上述事实的分析判断。

## 1. 卖的是什么，谁在赚钱

| 层次 | 商业含义 | 可验证证据 |
|---|---|---|
| Skill 包 | SKILL.md、调用脚本与参考资料可公开读取/下载，告诉 Agent 怎样调用服务；不能将付费标签直接解释成购买文件的版权或安装许可 | [WorkRally SKILL.md](https://api.skillhub.cn/api/v1/skills/workrally-image/file?path=SKILL.md)公开可读，真正图像能力在 `workrally.qq.com` 后端 |
| 远程专业服务 | 商家将 API、生成服务、行业数据封装为可调用 Skill；对每次能力调用收费 | [SkillPay 介绍](https://www.skillhub.cn/skillpay)、[企业发布教程](https://skillhub.cn/tutorials#agent-pay-publish-pricing) |
| 支付与履约 | 商户产生订单，微信/支付宝完成授权支付，后端验付后交付资源；用户付给实际创作者/服务商 | 当前生产前端付费详情文案明确交易款直接给创作者，平台不是收款方或实际服务提供方；[当前 bundle](https://cloudcache.tencent-cloud.com/qcloud/tea/app/skillhub/assets/skill-hub.cpdwg332.js?max_age=31536000) |
| 平台商业模式 | 当前支持商家服务变现；官网说技术服务费暂免。未来是否抽成、抽多少、与支付渠道有无收入分成，公开证据不足 | [SkillPay FAQ](https://www.skillhub.cn/skillpay) |

官网 FAQ 的具体口径：按次价格由商家自主设定；支持微信与支付宝；平台暂不收取技术服务费。支付完成后按所选渠道规则结算至绑定账户、无需手动提现。**“实时结算”是官网产品文案，不能据此推出所有商户银行卡 T+0，到账仍以渠道与具体商户协议为准。** 用户在对应支付账单发起咨询或退款，平台按渠道规则协助；发票按对应规则处理。[SkillPay FAQ](https://www.skillhub.cn/skillpay)。

**当前生产前端的责任边界原文位置：**搜索 `本 Skill 为创作者提供的按次收费服务`。其含义是：用户直接付款给创作者，SkillHub 提供展示、投诉处理和其他平台服务，不是该笔交易收款方/实际服务提供方；支付前应核对创作者与收款主体、计费单位、单价、内容和退款规则。[生产 bundle](https://cloudcache.tencent-cloud.com/qcloud/tea/app/skillhub/assets/skill-hub.cpdwg332.js?max_age=31536000)，本地 `sources/business-code-evidence.txt`。

补充只读核验：未登录、未付费，公开下载接口对 WorkRally、喜鹊均返回 HTTP 200、`application/zip`，首字节为 ZIP 文件签名。本次只读取响应头与前四字节，没有安装或执行。因此上述两个实例可以明确表述为“包可免费获取，远程服务按次付费”；不能由两个样本泛化全站所有包。证据见 `sources/business-public-download-check.json`；[WorkRally 下载](https://api.skillhub.cn/api/v1/download?slug=workrally-image)、[喜鹊下载](https://api.skillhub.cn/api/v1/download?slug=xique-tender-pay)。

## 2. SkillHub 平台具体做了哪些事情

| 平台环节 | 当前官方可证实能力 | 与商户/支付渠道的边界 |
|---|---|---|
| 供给组织与可信身份 | 团队/企业注册、企业认证、认证发布主体；企业绑定微信商户号；个人路径提供支付宝接入 | 企业/个人资质和支付签约仍需完成，不能有 Skill 就自动获得收款能力 |
| 商户接入 | 提供 SkillHub 商户号与 Token；微信商户平台绑定后回查已入驻状态 | 绑定支付商户身份，不代表平台成为资金收款主体 |
| 开发者支付身份 | 平台生成 RSA 2048 开发者密钥，私钥交商户持有、公钥留平台验签；管理生成/吊销，最多三对有效密钥 | 这是 AI 预下单的 SkillHub 身份签名；微信 Native 下单/查单另用微信支付 API 证书 |
| 商品化发布 | 上传 SKILL.md 包、slug/版本/分类/费用说明；支持免费与按次计费，商家设置单价；付费前置检查及审核 | 平台展示价不是通用强制扣款引擎；个人教程明确展示价、服务端账单价、支付宝登记价须一致 |
| 信任与质量治理 | 来源认证、内容完整性检查、可信调用入口，文件/格式/计费配置/案例检查；官网还有安全与 TRACE 能力 | 商户仍需实际部署后端并实现付费、验单、幂等和资源交付 |
| 分发与体验 | 官网发现与安装、多渠道分发、Agent 使用引导、云端沙箱与案例 | 买家 Agent 必须具备相应官方支付工具，不能从可下载推断所有 Agent 都能付款 |
| 支付后服务 | 官网承诺账单咨询/退款协助，详情展示交易与责任边界 | 具体服务履约、订单状态与退款操作主要在实际服务商/支付渠道侧；不能虚构平台代收后分账 |

来源：[SkillPay 产品页](https://www.skillhub.cn/skillpay)、[概览](https://skillhub.cn/tutorials#skillpay-overview)、[企业接入](https://skillhub.cn/tutorials#agent-pay-onboard)、[企业最佳实践](https://skillhub.cn/tutorials#enterprise-best-practice)、[个人接入及发布](https://skillhub.cn/tutorials#alipay-pay)、[腾讯官方能力说明](https://github.com/Tencent/skillhub)。上述动态教程的完整内容来自当前生产 bundle，本地截取见 `sources/business-enterprise-tutorial-code.txt` 与 `sources/business-tutorial-extract.txt`。

**订单/交易看板的证据限制：**当前未登录公开前端可确认商户绑定、开发者密钥与发布管理界面及对应接口，但没有证实一个真实运行的“全站交易/收入看板”。首页写着本月调用“12.8 万次”、本月收益“3.19 万”的卡片，在组件 `SkillPayCard` 中为硬编码，并明确标注“示例数据”；不可放入市场规模、GMV 或成熟度数字。本次没有访问私有交易接口。[官网](https://skillhub.cn/)、[生产 bundle](https://cloudcache.tencent-cloud.com/qcloud/tea/app/skillhub/assets/skill-hub.cpdwg332.js?max_age=31536000)。

## 3. 商业化程度统计必须同时看三类指标

1. **供给渗透**：付费资产占全部资产多少。这是标签/目录计数，只表示上架结构，不是收入贡献。
2. **接入摩擦**：需要用户配置 API Key 的资产占比。这表示依赖外部凭证；可能免费、订阅、按量，不能等同付费。
3. **实际交易**：付费调用、交易用户、转化、复购、退款、GMV、净收入。此次公开资料未提供可核验的全站结果；下载量不能代替付费调用。

重要新口径：当前 UI 的 `isPaidSkill` 接受 `pricing_type === "paid"` **和** `pricing_type === "alipay"`，也接受 `billingType === "per_call"` / `model === "pay_per_call"`。而列表页面 `buildLabels` 的“付费”筛选只发送 `pricing_type:paid`，不能将单个筛选结果当付费总量。`requiresApiKey` 只检查 `requires_api_key === "true"`。`pay-skill` 是另一目录筛选，应独立报数并检查交集。[生产 bundle](https://cloudcache.tencent-cloud.com/qcloud/tea/app/skillhub/assets/skill-hub.cpdwg332.js?max_age=31536000)、[列表公开 API](https://api.skillhub.cn/api/skills?category=pay-skill&pageSize=50&sortBy=downloads&order=desc)。

本轮主统计的标准同参数快照由主任务另存：全部 199,545；`paid` 17,061；`alipay` 2,901；两标签合计 19,962，约 10.0%；`pay-skill` 目录 19,974，为另一口径、相差 12，不能再相加。需 API Key 38,568，约 19.3%。这些是非原子元数据快照，不能据此统计真正微信商户开通率或活跃成交率。`paid` 在当前代码中只是通用付费识别之一，没有公开字段定义保证它等于已开通微信商户或发生微信成交。

反例可直接证实两个维度不等价：腾讯 WorkRally、喜鹊付费 Skill 均 `requires_api_key:false`；下载榜样本 `humanizer-zh` 为 `pricing_type:alipay` 且 `requires_api_key:true`，两个维度也会交叉。以原始结果为准，标签可能随版本变动。[WorkRally](https://api.skillhub.cn/api/v1/skills/workrally-image)、[喜鹊](https://api.skillhub.cn/api/v1/skills/xique-tender-pay)、[当前目录样本](https://api.skillhub.cn/api/skills?category=pay-skill&pageSize=50&sortBy=downloads&order=desc)。

官方仓库的“13 万+ Skills、2 万+ 企业 Skills、500+ 商家上架”属于官方公告口径，可作背景；不是当次全站实时计数，更不是“500 家活跃付费商户”，不可直接与当天接口分母拼接算占比。[官方仓库](https://github.com/Tencent/skillhub)。同一次统计亦可能受缓存/实时更新影响，建议用一致参数和时间窗口，注明非原子快照。

## 4. 真实案例：优先用腾讯自营，不用营销动画

### 腾讯 WorkRally 图片生成：最适合一图讲明白

- 平台认证发布者：WorkRally Team；认证主体 **腾讯科技（深圳）有限公司**；当前详情标 `pricing_type:paid`、`requires_api_key:false`；按次展示价 **0.36 元**。这些是平台认证字段，不能被顶层 `skill.verified:false` 误导为企业未认证。[详情 API](https://api.skillhub.cn/api/v1/skills/workrally-image)。
- 公开 SKILL.md 的 frontmatter 同样写 `per_call`、36 分。能力在腾讯 `workrally.qq.com` 后端；买家需要 `weixinpay` extension。文本/参考图→`invoke`→402+支付码→用户微信授权→同一 `payment_id` 取 `content`；生成中轮询、交付后出结果链接、失败可能自动退款；重复取同一结果不再收费。这是可审计的公开调用契约，不代表本次已付款实测。[SKILL.md](https://api.skillhub.cn/api/v1/skills/workrally-image/file?path=SKILL.md)。
- `product_id:image-generation` 是 **WorkRally 业务 API 的产品选择参数**，不要与微信 X402 预下单协议 `pay_items[].product_id` 混为一谈；后者在当前官方教程中是保留字段、格式 `SPxxx`、可任意填写。[WorkRally SKILL.md](https://api.skillhub.cn/api/v1/skills/workrally-image/file?path=SKILL.md)、[企业升级教程](https://skillhub.cn/tutorials#enterprise-upgrade)。

### 第三方喜鹊标书解读：证明专业垂直供给已出现

- 平台认证主体 **北京喜鹊云智科技有限公司**，微信按次付费，展示价 **1 元/次**，用户免注册喜鹊账号、免配置 API Key；交付摘要和三份 Word。[详情](https://api.skillhub.cn/api/v1/skills/xique-tender-pay)。
- SKILL.md 给出真实后端、微信官方支付工具、同任务支付/查询/下载恢复、售后与退款入口。售后通过「喜鹊标书AI」公众号人工服务，退款需用户提供微信订单截图给客服核实，不应画成所有退款都由 SkillHub 自动裁决。[SKILL.md](https://api.skillhub.cn/api/v1/skills/xique-tender-pay/file?path=SKILL.md)。

### 知了标讯：展示价不等于单一付费形态

平台认证主体 **北京百炼智能科技有限公司**。详情展示价 0.1 元，但自身描述是赠送体验积分、高价值联系方式仅付费额度、耗尽后微信购买次数包、按设备保存余额。因此不能仅凭 `per_call` 或列表价格断定所有商户都采用统一一次一付模式，应读真实服务契约。[详情](https://api.skillhub.cn/api/v1/skills/zlbx-bidding-payskill)。

## 5. 两页表达建议与仍需披露的未知项

**第 1 页：SkillHub 商业化的是 Agent 服务调用，平台目前降低交易门槛。** 左边用全站付费/API Key 比例（由同批统计报告提供），中间“Skill 免费获取→远程能力付费”，右边平台六项作用，底部 WorkRally 0.36 元案例；脚注暂不技术服务费、下载不等于付费。

**第 2 页：微信支付机制与各方职责。** 四泳道：Agent/用户、服务商、SkillHub、微信支付；突出两套密钥、SkillHub 验签和来源认证、用户授权、后端查单幂等履约。底部商业成熟度判断：“供给与交易机制已落地；GMV、活跃买家、复购/转化、平台收入仍无公开可核验数据”。

不能确认或不能写死的项目：平台未来费率/抽成、是否与微信支付分成；全站真实交易量与GMV；实际活跃商户数量；统一结算时效/费率；所有 Agent 的支付覆盖率；未登录后台是否有完整交易经营看板。商业化开放 API 的高消耗和正式商用场景仍建议先联系平台确认容量与方案，这不是收费价目表。[正式商用接入说明](https://github.com/Tencent/skillhub/blob/main/docs/README.md)、[接入申请](https://github.com/Tencent/skillhub/blob/main/docs/apply.md)。
