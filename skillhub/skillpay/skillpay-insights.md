# 腾讯 SkillHub / SkillPay 商业化洞察

调研时间：2026-10-20，北京时间。聚焦 Skill 资产和微信接入。证据来自 SkillHub 当前官网与生产前端、公开 API、腾讯官方商户 Demo、真实上架 Skill 契约及微信支付官方文档。未登录、安装 Skill、创建订单或付款。

## 结论

SkillHub 已提供按次收费的资产发布和交易接入能力，腾讯自营与第三方服务均有真实上架实例。典型模式是免费获取技能文件，再购买技能所调用的远程服务。官网明确平台当前暂不收技术服务费，交易款由用户直接付给创作者。平台目前可确认的作用是组织服务供给、认证身份、展示价格、审核分发和协同支付接入，不能把商户收入记为 SkillHub 平台收入。[SkillPay 介绍与 FAQ](https://skillhub.cn/skillpay)、[当前官网代码](https://cloudcache.tencent-cloud.com/qcloud/tea/app/skillhub/assets/skill-hub.cpdwg332.js?max_age=31536000)。

本次公开条目快照中，两种付费标签合计约 **10.0%**，标记需 API Key 的条目约 **19.3%**。这说明供给结构已包含商业服务，不能说明付费转化或真实收入成熟度。未找到全站 GMV、交易用户、复购或平台净收入的公开可核验数据。

## 商业化程度：统计口径与计算

主统计在北京时间 00:09:45–00:09:51 取得，统一使用 `pageSize=100&sortBy=downloads&order=desc`。每次请求的 URL、服务端响应头、UTC 时间和 total 保存于 [statistics-snapshot.json](statistics-snapshot.json)，原始响应保存于 `sources/snapshot-*.json`。

| 统计维度 | 查询条件 | 返回条目数 | 占全站比例 | 含义 |
|---|---|---:|---:|---|
| 全部公开 Skill | 无标签过滤 | 199,545 | 100% | 本轮分母，按条目而非作者、商户或交易计 |
| 通用付费标签 | `pricing_type:paid` | 17,061 | 8.55% | 官网付费识别的一支，不等于微信已开户或已成交 |
| 支付宝标签 | `pricing_type:alipay` | 2,901 | 1.45% | 官网也按付费资产识别，不能漏算 |
| 两种付费标签合计 | 上两行相加 | 19,962 | **10.00%** | 本报告付费标签口径，两值属于同一标量字段 |
| Pay Skill 目录 | `category=pay-skill` | 19,974 | 10.01% | 目录口径，与付费标签合计相差 12，不再相加 |
| 需要 API Key | `requires_api_key:true` | 38,568 | **19.33%** | 外部凭证依赖，不等于付费 |
| 不需要 API Key | `requires_api_key:false` | 160,951 | 80.66% | 显式 false；不自动代表免费 |
| paid 且需 Key | 两标签 AND | 204 | — | 两个维度可以交叉 |
| alipay 且需 Key | 两标签 AND | 128 | — | 合计约 332，约为付费标签的 1.7% |

数据不是一次数据库事务内取得。全量与子查询可能更新或采用不同索引/缓存，不能用差额构造精确的“未标记”人口，也不能绘制声称严格闭合的付费×Key 四象限。较早参数组出现 all=199,553、paid=17,006、Key=true=38,563，统一参数后采用上表，PPT 只展示一位小数近似占比。Key 的 true/false 两值合计与总量相差 26，也不把这 26 条确认为某个业务类型。

官网 `isPaidSkill` 除 paid/alipay 外，还识别部分对象中的 `billingType=per_call` / `model=pay_per_call`。公开列表 API 没有给出这些分支去重后的独立全集，故 **19,962 是可复算的两标签口径，不宣称穷尽所有可能付费服务**。官网列表“付费”筛选本身只发 `pricing_type:paid`，因此直接读取该筛选会遗漏 alipay 分支。标签 API 的 AND、否定和字段定义见 [官方 API 文档](https://github.com/Tencent/skillhub/blob/main/docs/api/skills.md)。

这里的“API Key 类型占比”指 `requires_api_key=true` 资产占比。公开标签没有可直接汇总的 Key 厂商、OAuth/Token 等认证子类型全集，本次不编造供应商结构或外部订阅收入。Key 依赖可能对应免费额度、付费订阅或按量 API，需逐个读服务条款。

主查询可复算入口：

- [全站列表](https://api.skillhub.cn/api/skills?pageSize=100&sortBy=downloads&order=desc)
- [paid 标签](https://api.skillhub.cn/api/skills?pageSize=100&sortBy=downloads&order=desc&labels=pricing_type%3Apaid)
- [alipay 标签](https://api.skillhub.cn/api/skills?pageSize=100&sortBy=downloads&order=desc&labels=pricing_type%3Aalipay)
- [需 API Key](https://api.skillhub.cn/api/skills?pageSize=100&sortBy=downloads&order=desc&labels=requires_api_key%3Atrue)
- [不需 API Key](https://api.skillhub.cn/api/skills?pageSize=100&sortBy=downloads&order=desc&labels=requires_api_key%3Afalse)
- [Pay Skill 目录](https://api.skillhub.cn/api/skills?pageSize=100&sortBy=downloads&order=desc&category=pay-skill)

## 收费与资金：服务商如何赚钱，平台做什么

| 问题 | 本次核实结果 |
|---|---|
| 收费对象 | 典型模式是远程 API / 专业服务调用；不是通过加密 SKILL.md 收取安装许可 |
| 价格制定 | 商家自主设置按次价格，发布时配置计费与服务说明；实际微信扣款金额由商户传统下单传入 |
| 平台费用 | 官网明确当前暂不收技术服务费，不承诺永久免费，也不代表支付渠道成本为零 |
| 资金归属 | 用户直接付款给创作者；平台详情明确 SkillHub 不是该笔交易收款方或实际服务提供方 |
| 结算 | 按微信/支付宝渠道规则结算到绑定账户，无需在 SkillHub 手动提现；不能泛化为所有银行卡 T+0 |
| 退款 | 用户在对应支付账单发起咨询/退款，平台协助；商户处理服务履约与退款接口，微信沿用传统退款能力 |
| 平台收入与未来抽成 | 未找到可核验的平台收入或未来抽成比例，不能据此声称腾讯正在按每笔交易抽佣 |

来源：[官网 FAQ](https://skillhub.cn/skillpay)、[生产前端责任条款](https://cloudcache.tencent-cloud.com/qcloud/tea/app/skillhub/assets/skill-hub.cpdwg332.js?max_age=31536000)、[微信 FAQ](https://pay.wechatpay.cn/doc/v3/merchant/4035576771)。

SkillHub 的具体工作：

1. **组织与认证供给**：企业/团队注册、企业认证及服务主体展示，个人有支付宝接入路径。微信企业路径绑定微信商户身份。
2. **提供支付身份**：在商户中心管理开发者身份及 RSA 密钥，商户保管私钥，x402 预下单使用 SkillHub 身份签名。
3. **将服务变成可发布资产**：上传包含 SKILL.md 的包，管理 slug、版本、定价、费用/退款/开票说明及效果案例；发布前检查计费与支付链路。
4. **发现与分发**：官网、榜单、CLI/API 和宿主接入把技能送到 Agent；支持支付工具仍是消费端前置条件。
5. **协同售后与责任告知**：展示实际创作者、收款主体和计费单元，按渠道规则协助投诉和退款。

来源：[企业准入](https://skillhub.cn/tutorials#agent-pay-onboard)、[企业改造](https://skillhub.cn/tutorials#enterprise-upgrade)、[发布定价](https://skillhub.cn/tutorials#agent-pay-publish-pricing)、[微信准备指引](https://pay.wechatpay.cn/doc/v3/merchant/4035576711)、[微信 FAQ](https://pay.wechatpay.cn/doc/v3/merchant/4035576771)。

## 真实供给，而非营销示例

| 案例 | 平台认证主体 | 当前展示价 | 用户 API Key | 已核查范围 |
|---|---|---:|---|---|
| WorkRally 图片生成 | 腾讯科技（深圳）有限公司 | ¥0.36 / 次 | 不需要 | 详情、36 分计费配置、调用后端及支付恢复契约、公开 ZIP 下载 |
| 喜鹊标书解读 | 北京喜鹊云智科技有限公司 | ¥1 / 次 | 不需要 | 详情、摘要和三份 Word 的交付约定、支付/查询/人工售后、公开 ZIP 下载 |

来源：[WorkRally 详情](https://api.skillhub.cn/api/v1/skills/workrally-image)、[Skill 契约](https://api.skillhub.cn/api/v1/skills/workrally-image/file?path=SKILL.md)、[喜鹊详情](https://api.skillhub.cn/api/v1/skills/xique-tender-pay)、[Skill 契约](https://api.skillhub.cn/api/v1/skills/xique-tender-pay/file?path=SKILL.md)。只读下载检查见 `sources/business-public-download-check.json`。核实公开文件和调用契约，不代表本次付费调用成功；两例不能泛化全部资产。

官网的“本月调用 12.8 万次”“本月收益 3.19 万”在生产代码里为固定演示值，页面明确标注“示例数据”，因此没有进入商业规模统计。下载量同样不能代替付费调用数。官方仓库的历史公告规模与实时 API 快照没有混用。

## 微信 SkillPay：交易机制与责任边界

支付使用既有微信人民币订单。x402 在这里负责把既有订单转为 Agent 能拉起的支付请求。当前公开产品需要用户逐笔确认，不能概括为 Agent 无需授权自动扣款。[产品介绍](https://pay.wechatpay.cn/doc/v3/merchant/4035576700)、[开发指引](https://pay.wechatpay.cn/doc/v3/merchant/4035576716)。

1. Agent 按 Skill 指令请求商户业务接口。
2. 商户先通过 Native/JSAPI 等传统接口创建微信订单，传入金额、订单号和 notify_url，得到 code_url/prepay_id 等。
3. 商户使用 SkillHub 开发者 RSA 密钥签名，向微信 AI 支付发起 x402 预下单，得到 payment_code。
4. 商户将支付码经 `402 + WeixinPay-Required` 返回给 Agent，支持 HTTP 200 兼容模式。支付码必须保持原文；部分工具链只读 Body，可按微信指引双投递。
5. 宿主支付工具展示卡片，用户扫码到微信 Liteapp 逐笔确认，以 AI 专属卡余额付款；专属卡与用户微信主账户资金隔离。
6. 商户沿用微信 notify_url 或主动查单确认支付状态，回调验签并解密。payment_code 是拉起凭据，不能证明已经付钱。
7. 商户确认订单归属、金额和 SUCCESS 状态后履约。原订单关联的业务结果可以恢复获取；具体重试 Header/字段由服务接口约定。
8. 商户负责订单持久化、业务幂等和失败补偿，退款沿用微信能力。

上述稳定机制依据 [微信 FAQ](https://pay.wechatpay.cn/doc/v3/merchant/4035576771)、[微信 x402 API](https://pay.wechatpay.cn/doc/v3/merchant/4035576740)、[Native 下单](https://pay.wechatpay.cn/doc/v3/merchant/4012791877)、[支付回调](https://pay.wechatpay.cn/doc/v3/merchant/4012791882)。具体 `X-Out-Trade-No` 重试和缓存范式来自 [SkillHub 商户 Demo](https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/mch-demo/mch-demo.zip)，不是所有微信商户必须采用的通用付款证明协议。

### 三类凭证不能混淆

| 凭证 | 用途 | 所在位置 |
|---|---|---|
| 业务 API Key | 访问外部业务服务；资产标签统计所指的凭证依赖 | 依服务要求配置，不能默认等于收费 |
| SkillHub 开发者 RSA 密钥 | 以开发者平台身份签名微信 AI 预下单 | 商户后端保管私钥 |
| 微信商户证书、APIv3 密钥及微信验签公钥 | 传统支付请求签名、回调验签与资源解密 | 商户支付后端 |

### 官方接口存在版本差异

| 项目 | 微信当前 API（2026-09-01 更新） | SkillHub 当前教程 / Demo |
|---|---|---|
| 预下单端点 | `aipay.wxpapp.weixin.qq.com/aipay/preorder` | `payapp.weixin.qq.com/palmpayminiapp/clawagentpay/preorder` |
| 鉴权位置 | Authorization 头 | Body 内身份及签名字段 |
| payment_required | JSON 对象 | Base64 字符串 |
| pay_type | GOODS_PAY | SKILL_PAY |
| 签名覆盖 | 完整 HTTP Body | payment_required 字符串 |

两份均为官方材料，不能将旧端点与新报文拼成可执行请求，也没有证据断言旧端点已停用。PPT采用两方稳定共识机制，详细差异记录在 [微信机制报告](research-wechat-mechanism.md)。当前 product_id 的商品注册/价格绑定机制未被公开文档充分说明，故没有把它画为平台统一计费主键。

### 生产边界

官方 Demo 有微信 SDK 回调验签/解密、主动查单、结果缓存和退款实现，但使用内存状态，不能据此承诺生产并发下绝不重复履约。商户需自建持久化与业务事务保障。未实际验证支付成功、旧网关可用性、到账时效或退款。这限制的是运行验证范围，不影响对公开商业模式与协议职责的梳理。

## 交付与证据索引

- 两页 PPT：`../output/skillhub-skillpay-commercialization-v1.pptx`
- 单文件 HTML：`skillhub-skillpay-commercialization-v1.html`
- [商业模式完整报告](research-business.md)
- [微信协议与 Demo 完整报告](research-wechat-mechanism.md)
- [主统计及请求头](statistics-snapshot.json)
- `sources/business-manifest.json` 记录商业化来源 URL；`sources-manifest.json` 记录全部原始材料的文件大小和 SHA256；微信来源直接链接保存在微信机制报告中。

综合判断：**资产商业化和支付接入已落地，经营规模成熟度尚不能由公开资料证实。** 平台供给比例、商户开户、真实付费调用、平台营收是四个不同层次，应分别衡量。
