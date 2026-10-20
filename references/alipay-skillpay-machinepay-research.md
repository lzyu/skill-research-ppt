# 支付宝 SkillPay 与 MachinePay：原理、协议与商业化机制

> 调研时间：2026-10-20（Asia/Shanghai）
> 方法：支付宝 AI 付官方文档、SkillPay 官网/博客/FAQ、官方 `alipay/ai` 仓库（买方支付 Skills、A2M 对接文档、示例代码）、公开只读页面；未登录、未实际支付、未创建沙箱会话。
> 口径：【官方文档】= AI 付/开放平台文档；【官网】= SkillPay 官网与 FAQ；【官方仓库】= `github.com/alipay/ai`；【推断】= 基于以上证据的分析，不是官方原话。

---

## 0. 一页速览

| 结论 | 说明 |
|---|---|
| **SkillPay 是“商品层”** | 把 Skill 做成可上架、可定价、可试用、可交付、可退款的产品；一次性买断交源码，周期订阅走云端保护。 |
| **MachinePay 是“协议层”** | 用 HTTP 402 + `Payment-Needed` / `Payment-Proof`，把每一次 API/MCP/算力调用变成一笔可报价、可验单、可履约的交易。 |
| **共同底座是 AI 付钱包** | 用户绑定支付宝、逐笔授权；Agent 通过 `alipay-bot` 拿支付链接/二维码，用户确认后完成支付。 |
| **两者都依赖 402** | 无权益/无凭证 → 402；付款后携带凭证重试；商家/平台验单后交付。 |
| **关键差异** | SkillPay 卖“交付权/使用权”，MachinePay 卖“计量调用”；前者是商品，后者是计费。 |
| **最大边界** | 402 是收费握手，不是支付本身；用户确认/钱包授权仍是信任锚；自主支付要靠“委托支付”（邀测）。 |

---

## 1. 阿里 AI 付的产品矩阵：两条轨道

支付宝 AI 付（aipay.alipay.com）把 Agent 支付拆成多个产品：

| 产品 | 卖什么 | 计费/交付 | 与本主题关系 |
|---|---|---|---|
| Vibe Pay | AI 网页/移动应用的功能、内容、次数、积分、时长 | 一次性/次数包/积分包/时长包 | 应用收款，不是 Skill |
| **Skill Pay** | 可被 Agent 调用的 Skill | 一次性买断 / 周期订阅 / 试用 | **商品层** |
| **Machine Pay** | API、MCP、算力、数字内容 | 每次调用独立定价，按量收费 | **协议层** |
| Token Pay | 模型 Token/额度/持续服务 | 个人订阅/企业席位 | 模型订阅 |
| Agent Pay | Agent 代用户购买商品/服务 | 下单、支付确认、订单回传 | 交易最终购买环节 |

> 来源：[AI 付产品总览](https://aipay.alipay.com/docs/overview.md)、[Machine Pay](https://aipay.alipay.com/products/machine-pay)、[SkillPay](https://skillpay.alipay.com/)。

**一句话**：SkillPay 回答“卖什么、怎么交付、怎么退款”；MachinePay 回答“每次调用怎么报价、怎么验单、怎么履约”。两者共享 AI 付钱包与 402 协议。

---

## 2. SkillPay：把 Skill 变成商品

### 2.1 定位与角色

SkillPay 是支付宝面向 Skill 创作者/消费者的商品化平台。官方定位：

- 面向 Skill 服务商提供使用收费能力；
- 把支付嵌入 Skill 的调用与交付流程；
- 适合专业工具、内容生成、数据查询、行业服务等 Skill。

来源：[AI 付产品总览 · Skill Pay](https://aipay.alipay.com/docs/overview.md)、[SkillPay 官网](https://skillpay.alipay.com/)。

角色：

| 角色 | 做什么 |
|---|---|
| 创作者 | 上传 Skill、定价、选择交付方式、处理退款、持续更新 |
| 消费者/买家 Agent | 在任务中发现并购买 Skill，获得源码或云端使用权 |
| SkillPay 平台 | 安全检测、商品页、支付/交付编排、云端保护、协议与合规 |
| 支付宝 | 支付、风控、资金流转、退款通道 |

### 2.2 上架：安全检测 + 商品化

官网 FAQ 与博客给出的流程：

1. 创作者提交 Skill；
2. 平台做安全检测与风险扫描（识别恶意行为、安全风险）；
3. 检测通过后上架为商品；
4. 上架前须完成 **SkillPay 协议** 与 **AI 按量付费协议** 的签署。

来源：[SkillPay 官网 FAQ](https://skillpay.alipay.com/)、[《好的世界，技有所得》](https://skillpay.alipay.com/blog/good-world-skills-get-paid)。

> 推断：要求签署 AI 按量付费协议，说明 SkillPay 的云端调用/计量与 MachinePay 的按量能力共用底座；但 SkillPay 对消费者卖的是“买断/订阅”，不是逐次 API 计费，二者在商品层与计费层分工。

### 2.3 定价与两种交付

SkillPay 支持三种商业形态：

| 形态 | 交付什么 | 关键规则 |
|---|---|---|
| **免费试用** | 真实任务试用 | 先验证价值，再购买/订阅 |
| **一次性买断** | 完整 Skill 源码（明文） | 永久使用；适合不需要持续更新的 Skill |
| **周期订阅** | 当期使用权，不交付明文 | 云端保护调用；不自动续费；到期失效 |

来源：[SkillPay 官网 FAQ](https://skillpay.alipay.com/)、[《好的世界，技有所得》](https://skillpay.alipay.com/blog/good-world-skills-get-paid)。

**为什么订阅不交源码**：Skill 的核心价值常在系统指令、专业知识和执行方法；交付明文等于把可复制资产交出去。订阅制用云端保护把“能力”交付，把“原文”留在云上。

### 2.4 购买/安装链路（官方执行器）

`https://aipayapi.alipay.com/skillpay/ct?c=...` 返回一份“Skill 购买、履约与安装执行器”，核心步骤：

1. **首次履约请求**：`alipay-bot curl-proxy` POST 到卖家 proxy：
   `https://agentpay.alipay.com/ai-pay/proxy/{seller_id}/{service_id}`  
   body `{"prompt":"firsttimebuy"}`；`firsttimebuy` 是幂等的“购买或履约”请求。
2. **支付待确认**：输出包含“支付待确认”、订单号、支付方式链接；保存订单号与原始请求，展示给用户一次，停止本轮。
3. **用户支付**：用户在支付宝完成支付。
4. **恢复履约**：不要重新下第二单；用原订单号与**完全相同的 URL/方法/请求体/业务 Header** 查询支付状态并恢复资源。
5. **拿到 `fulfillment_proof`**：响应 200 且含 `fulfillment_proof` 才视为 FULFILLED；不能把 `success:true` 或 HTTP 200 直接当安装成功。
6. **安全下载/解压/安装**：只接受本次响应的唯一 HTTPS 地址；拒绝绝对路径、`..`、越界符号链接、设备文件；只解压到临时目录；不执行包内脚本；最后验证安装。

来源：SkillPay 购买/履约执行器（`aipayapi.alipay.com/skillpay/ct`，2026-10-20 读取）。

> 这条链路说明：SkillPay 的商品购买不是“扫码付款后给个下载链接”这么简单，而是 **幂等下单 → 支付待确认 → 原单恢复 → 履约凭证 → 安全安装 → 验证** 的状态机。支付成功不等于交付成功。

### 2.5 运行期 402：没有权益就付费

博客给出的运行期流程：

1. Agent 在执行任务中触发付费 Skill；
2. 没有有效权益 → 返回 **HTTP 402 + 支付要求**；
3. Agent 向用户说明能力与价格，用户付款；
4. Agent 携带凭证重试原请求；
5. 平台按收费方式履约：一次性购买交付完整 Skill；订阅制开放云端保护调用；
6. 原任务继续，不丢上下文。

来源：[《好的世界，技有所得》](https://skillpay.alipay.com/blog/good-world-skills-get-paid)。

**关键设计**：402 不是“弹一个付款页”，而是让原任务有明确的恢复点：无权益 → 支付要求 → 权益建立 → 继续交付。

### 2.6 云端保护：保护“方法”，不是答案

博客明确描述了云端保护的机制与边界：

- 完整原文隔离保管，不下载到用户本地；
- 每次调用只返回当前任务所需的执行文本；
- 脚本、公开数据、最终答案仍在本地处理；
- 防止角色扮演、指令覆盖、编码转换、多轮提问等套取；
- 先理解请求，再把受保护能力收敛为当前任务专用执行文本；
- 正常任务获得可执行指导，明显套取被拒绝，边界请求最小披露；
- **不是绝对不可破解**，而是“原文隔离 + 按任务拆分 + 权限控制 + 本地校验 + 审计 + 回归评测”的持续防御，提高批量复制成本。

来源：同上。

### 2.7 资金、退款与安全

官网 FAQ 的明确表述：

- 消费者付款成功后，款项**实时进入开发者的支付宝账户**，无需经过 SkillPay 中转，也无需等待结算；
- 消费者退款需先联系开发者协商；确认后开发者可在产品页面**手动发起实时退款**；
- **周期付费订单整单全额退还**；
- 平台提供 Skill 安全检测、云端保护、支付宝支付安全；
- 支持宿主：WorkBuddy、豆包工作、千问办公、Cursor、Codex、Claude Code；支付流程需要在本地沙盒写入文件，建议开启文件写入权限并允许操作批准。

来源：[SkillPay 官网 FAQ](https://skillpay.alipay.com/)。

> 未公开：平台是否抽佣/费率、结算周期、发票/税务、争议处理细则。官网只说“成交即到账、无需 SkillPay 中转”。

### 2.8 SkillPay 的四层能力（官方博客）

| 层级 | 核心问题 | 开发者价值 | 用户价值 |
|---|---|---|---|
| 402 支付 | 识别付费、恢复任务 | 标准化收费入口 | 原任务内完成购买 |
| 云端交付 | 提供能力、不交原文 | 保留核心 Skill | 获得结果即可 |
| 安全保护 | 降低套取风险 | 提高复制成本 | 正常任务可用 |
| 商业经营 | 试用、订阅与履约 | 获得持续收入 | 先试用再购买 |

来源：[《好的世界，技有所得》](https://skillpay.alipay.com/blog/good-world-skills-get-paid)。

---

## 3. MachinePay：把每次调用变成交易

### 3.1 定位：A402 / A2M

MachinePay 是支付宝 AI 付推出的、基于 **HTTP 402 Payment Required** 的 A2M 方案：让 API、数字内容、算力资源直接向访问它们的 AI Agent 发起自动收款。

- 按量收费：每次调用独立定价，不必依赖包月；
- 原生适配 Agent：402 告诉 Agent “这个资源需要先付款”；
- 链路短：用户不需要在商家侧注册/登录/跳转；
- 用户授权后，Agent 完成请求、支付、交付。

来源：[Machine Pay 产品页](https://aipay.alipay.com/products/machine-pay)、[产品接入指南](https://aipay.alipay.com/docs/ai-receive/MACHINE_PAY.html)。

> “A2M”与“A2A”在文档中混用：产品页称 A2M；`payment.verify` 文档称 A2A 场景下商户验证买家 Agent 的支付凭证。可理解为：Agent 面向商家资源的付费调用（A2M），以及商家向支付宝验证 Agent 凭证（A2A）。

### 3.2 完整时序（官方）

```text
用户 → 买家 Agent：下达任务
买家 Agent → 商家 API：GET /resource（无 Payment-Proof）
商家 API → 买家 Agent：402 + Payment-Needed（Base64URL 账单）
买家 Agent → 用户：展示价格/商户/过期时间
用户 → 支付宝：确认并支付
支付宝 → 买家 Agent：Payment-Proof（payment_proof / trade_no / client_session）
买家 Agent → 商家 API：重试原请求 + Payment-Proof
商家 API → 支付宝：alipay.aipay.agent.payment.verify(trade_no, payment_proof, client_session)
支付宝 → 商家 API：active / amount / out_trade_no / resource_id
商家 API → 买家 Agent：200 + 资源
商家 API → 支付宝：alipay.aipay.agent.fulfillment.confirm(trade_no)
```

来源：[Machine Pay 产品接入指南](https://aipay.alipay.com/docs/ai-receive/MACHINE_PAY.html)、[verify API](https://aipay.alipay.com/docs/ai-receive/api-list/alipay-aipay-agent-payment-verify.md)、[fulfillment API](https://aipay.alipay.com/docs/ai-receive/api-list/alipay-aipay-agent-fulfillment-confirm.md)。

### 3.3 Payment-Needed：商家报价单

402 响应的核心是 `Payment-Needed` Header（Base64URL 编码的 JSON）；响应体只用于调试，Agent 以 Header 为准。

```json
{
  "protocol": {
    "out_trade_no": "ORDER_...",
    "amount": "0.01",
    "currency": "CNY",
    "resource_id": "RES_...",
    "pay_before": "2026-03-25T12:00:00+08:00",
    "seller_signature": "YYYYxxxx=",
    "seller_sign_type": "RSA2",
    "seller_unique_id": "2088xxxxxxxx"
  },
  "method": {
    "seller_name": "测试商家",
    "seller_id": "2088xxxxxxxx",
    "seller_app_id": "app_123456",
    "goods_name": "测试商品",
    "seller_unique_id_key": "seller_id",
    "service_id": "xxxx_12344"
  }
}
```

字段要点：

- `out_trade_no`：商户订单号，全局唯一，用于幂等/防重复支付；
- `amount`：应付金额字符串；`currency` 默认 CNY；
- `resource_id`：资源唯一标识，用于“资源防串”；
- `pay_before`：支付截止时间（ISO8601），过期不可支付；
- `seller_signature` / `seller_sign_type`：商家签名（RSA2）；
- `seller_unique_id`：卖家唯一标识（此处是 seller_id）；
- `service_id`：商户服务 ID，用于平台识别服务。

### 3.4 商家签名：本地完成，不请求支付宝

商家用自己的应用私钥，对账单关键字段按 **key 字典序** 拼接后 RSA2 签名：

```text
amount=0.01&currency=CNY&goods_name=测试商品&out_trade_no=ORDER_...&pay_before=...&resource_id=RES_...&seller_id=2088xxxxxxxx&service_id=xxxx_12344
```

签名只在商家本地完成，不请求支付宝服务端；这样 402 账单可以离线生成，响应快，且支付宝无法被“签名请求”打爆。

来源：[Machine Pay 产品接入指南](https://aipay.alipay.com/docs/ai-receive/MACHINE_PAY.html)、[A2M 对接文档](https://github.com/alipay/ai/blob/main/code_example/aipay-402-example/A2M智能收产品对接文档.md)。

> 金额单位有一处不一致：官方接入文档写“最小货币单位”，A2M 示例文档写“元”。落地时应以接入文档/实际接口为准，并在账单与验单中保持同一口径。

### 3.5 Payment-Proof：买家凭证

买家付款后，重试原请求并携带 `Payment-Proof` Header（Base64URL 编码）：

```json
{
  "protocol": {
    "payment_proof": "7cf8...",
    "trade_no": "2026040900828111317760000001xxxx"
  },
  "method": {
    "client_session": "ImNsaWVudFNlc3Npb24..."
  }
}
```

- `payment_proof`：支付凭证；
- `trade_no`：支付宝交易号；
- `client_session`：买家客户端会话标识，由 C 端 Agent 通过支付宝 CLI 生成，用于校验买家身份/真实性；商家必须原样透传，不得修改、缓存或自行构造。

来源：[A2M 对接文档](https://github.com/alipay/ai/blob/main/code_example/aipay-402-example/A2M智能收产品对接文档.md)、[verify API](https://aipay.alipay.com/docs/ai-receive/api-list/alipay-aipay-agent-payment-verify.md)。

### 3.6 验单：不是“接口成功”就交付

商家调用 `alipay.aipay.agent.payment.verify`，入参 `trade_no`、`payment_proof`、可选 `client_session`；返回包含 `active`、`amount`、`out_trade_no`、`resource_id`。

**必须同时通过**：

- `active=true`；
- `amount` 等于本地订单金额；
- `out_trade_no` 等于商家订单号；
- `resource_id` 等于当前请求资源；
- `trade_no` 未被重复履约（防重放/重复使用）；
- 本地订单处于允许的支付/履约状态；首次履约前仍在 `pay_before` 内且未取消。

任一失败 → 返回 402，让 Agent 重新支付；**不得返回资源**。

来源：[Machine Pay 产品接入指南](https://aipay.alipay.com/docs/ai-receive/MACHINE_PAY.html)、[verify API](https://aipay.alipay.com/docs/ai-receive/api-list/alipay-aipay-agent-payment-verify.md)。

### 3.7 履约回执：把“交付”告诉支付宝

资源生成后，商家异步调用 `alipay.aipay.agent.fulfillment.confirm`，入参只有 `trade_no`；必须在回执成功后再把订单标记最终完成。

- 履约确认失败时，允许同一 `Payment-Proof` 重试确认，避免“资源已生成但平台未记录履约”；
- 已原子进入待确认/已完成状态的同一订单，只能重试确认或返回已保存结果，不得因支付截止时间已过而重复生成资源。

来源：[fulfillment API](https://aipay.alipay.com/docs/ai-receive/api-list/alipay-aipay-agent-fulfillment-confirm.md)、[Machine Pay 产品接入指南](https://aipay.alipay.com/docs/ai-receive/MACHINE_PAY.html)。

### 3.8 买家侧：alipay-bot 与钱包授权

官方买方 Skill `alipay-pay-for-402-service` 给出的流程：

1. `alipay-bot check-wallet` 检查钱包状态；
   - 已开通已授权 → 继续；
   - 已申请未授权 → 调用 `alipay-authenticate-wallet` 完成授权；
   - 未开通 → 申请开通。
2. 保存 402 的 `Payment-Needed` 原文到文件（不解码、不篡改）；
3. `alipay-bot 402-buyer-pay -f <file>` 提交支付，CLI 返回支付链接/二维码；**等用户支付完成通知**；
4. `alipay-bot 402-query-payment-status -t <tradeNo> -r <resource-url> ...` 查询支付并重试原请求；
5. 把支付信息与资源透传给用户；
6. 发送履约回执。

来源：[官方买方 Skill](https://github.com/alipay/ai/blob/main/skills/alipay-pay-for-402-service/SKILL.md)。

钱包授权：

- 用户扫码申请开通 AI 付，获得 6 位授权码；
- `alipay-bot bind-wallet -c <code>` 绑定；
- 支付链接通常 5 分钟内有效，一次性、用户绑定；
- 逐笔支付由用户授权（不是静默扣款）。

来源：[钱包授权 Skill](https://github.com/alipay/ai/blob/main/skills/alipay-authenticate-wallet/SKILL.md)。

### 3.9 自主支付：委托支付（Delegation）

如果希望 Agent 在用户不在场时自动扣款，支付宝另有一个 **委托支付** 产品：

- 用户预先授权，含 **金额、次数、有效期** 限制；
- 后续 Agent 在授权范围内自动执行支付；
- 适用代买、抢票、监控购买等；
- 产品为 **邀测**，需联系 BD 开通；委托场景另需开通 App 支付；
- 流程：委托代买申请 → 用户授权签约 → 查询委托 → 商户预下单 → 执行委托支付 → 取消委托。

来源：[委托支付 Skill](https://github.com/alipay/ai/blob/main/skills/alipay-delegation-pay/SKILL.md)。

> **重要边界**：MachinePay 的 402 流程本身是“逐笔用户确认”的；它不是无授权的静默扣款。真正让 Agent 自主花钱的是委托支付，且必须预设金额/次数/有效期。把 402 说成“机器自动付款、无需人”是不准确的。

### 3.10 结算、退款与边界

- 产品页称“自动结算”，但公开文档只暴露 `verify` + `fulfillment.confirm`，没有独立结算/退款接口；
- 资金走支付宝收单/结算体系，具体账期、费率、发票、退款/争议规则以后台签约协议为准（未公开）；
- 商家自行定价（402 账单里的 amount），平台不代商家定价；
- 金额、资源、订单、凭证必须绑定；防重放/重复履约是商家责任；
- `Payment-Validation` Header 在 A2M 示例中出现（trade_no/out_trade_no/validated/resource_id），但官方接入指南未把它列为核心字段；落地时以实际接口为准。

---

## 4. SkillPay vs MachinePay：商品层与协议层

| 维度 | SkillPay | MachinePay |
|---|---|---|
| 卖什么 | Skill 商品/权益（源码或云端使用权） | API/MCP/算力等按次调用的资源 |
| 计费单位 | 一次性买断 / 周期订阅 / 免费试用 | 每次调用独立定价（商家在 402 账单报价） |
| 触发 | 无有效权益 → 402/支付要求 | 无 `Payment-Proof` → 402 + `Payment-Needed` |
| 交付 | 源码 zip / 云端执行文本 | API 结果 |
| 资金 | 直接到开发者支付宝；退款开发者发起 | 支付宝收单/结算到商家账户 |
| 信任 | 安全检测 + 云端保护 + 支付宝 | RSA2 签名 + verify + 防重放 + 履约回执 |
| 角色 | 创作者/消费者/平台 | 商家/买家 Agent/支付宝 |
| 关键风险 | 云端保护非绝对；退款靠协商；订阅不自动续费 | 金额/资源校验；结算退款规则未公开；逐笔授权 |

**关系**：

- SkillPay 是“商品化层”：解决 Skill 的上架、定价、试用、交付、退款；
- MachinePay 是“计量协议层”：解决每次调用的报价、支付、验单、履约；
- 两者共用 AI 付钱包与 402，但 SkillPay 的商品购买走卖家 proxy + `fulfillment_proof`，MachinePay 走资源级 402 + `Payment-Proof`；
- SkillPay 订阅的云端调用需要签署 AI 按量付费协议（官网 FAQ），说明云端交付与按量计费能力共用底座（推断）。

---

## 5. 第一性原理：支付协议的五步与三本账

### 5.1 五步

1. **报价（Quote）**：商家把价格、资源、过期时间、收款方写进 402 账单，并签名；
2. **授权（Authorize）**：用户通过 AI 付钱包确认支付（逐笔），或委托支付在限额内自动授权；
3. **证明（Prove）**：支付宝给买家一个与 trade_no/client_session 绑定的支付凭证；
4. **验证（Verify）**：商家向支付宝验单，确认 active/金额/订单/资源/未重放；
5. **履约（Fulfill）**：商家交付资源并发履约回执；资金按支付宝结算体系流转。

### 5.2 三本账

| 账本 | 谁维护 | 关键键 | 作用 |
|---|---|---|---|
| 订单/账单账 | 商家 | `out_trade_no` | 幂等、防重复下单、金额/资源 |
| 支付账 | 支付宝 | `trade_no` | 支付事实、凭证、结算 |
| 履约/权益账 | 商家或 SkillPay | `trade_no` + `resource_id` / `version` | 防重复履约、交付、退款、审计 |

**核心不变量**：

- 无凭证 → 不交付；
- 一凭证 → 一次履约（防重放）；
- 金额/订单/资源三者一致；
- 支付成功 ≠ 交付成功（还要 fulfillment）；
- 账单/凭证/履约都要能追溯到同一个订单与资源。

### 5.3 为什么是 402

- **机器可读**：Agent 能直接解析价格，不需要理解页面；
- **任务可恢复**：付款后重试原请求，不丢上下文；
- **链路短**：不用注册/登录/跳转；
- **通用**：API、MCP、Skill、数字内容、算力都能用；
- **边界**：需要 Alipay 钱包/用户确认；不是所有 Agent 宿主都支持；不是无授权的自动扣款。

---

## 6. 风险与未公开项

| 问题 | 现状 |
|---|---|
| SkillPay 平台佣金/费率 | 官网只说“成交即到账、无需中转”；抽佣/费率未公开 |
| MachinePay 结算周期/费率/发票 | 文档只暴露 verify + fulfillment；具体以后台协议为准 |
| MachinePay 退款/争议 | 公开文档未给退款接口；需走商家/支付宝协议 |
| 自主支付限额 | 402 逐笔确认；委托支付需邀测，含金额/次数/有效期 |
| 云端保护强度 | 官方明确“不是绝对不可破解”，是提高复制成本 |
| 金额单位 | 接入文档“最小货币单位” vs A2M 示例“元”，落地需核对 |
| 版本/权益绑定 | SkillPay 订阅需绑定版本；MachinePay 账单绑定 resource_id |
| 跨境/税务/责任 | 未公开；涉及外汇、税务、Agent 责任边界 |

---

## 7. 可直接上页的关键事实

1. SkillPay 两种交付：一次性买断交源码；周期订阅云端保护、不交明文、不自动续费。
2. SkillPay 购买链路是幂等状态机：`firsttimebuy` → 支付待确认 → 原单恢复 → `fulfillment_proof` → 安全安装。
3. SkillPay 成交即到账开发者支付宝；退款由开发者发起，周期订单整单全额退。
4. MachinePay 用 402 + `Payment-Needed` 报价；Agent 付款后带 `Payment-Proof` 重试。
5. 商家本地 RSA2 签名账单；`verify` 必须校验 active/金额/订单/资源/防重放/pay_before。
6. 交付后异步 `fulfillment.confirm`；失败可重试，资源不重复生成。
7. 402 是逐笔用户确认；自主支付靠委托支付（金额/次数/有效期，邀测）。
8. 两者共用 AI 付钱包与 402；SkillPay 是商品层，MachinePay 是计量层。

---

## 8. 主要来源

- [AI 付产品总览](https://aipay.alipay.com/docs/overview.md)
- [Machine Pay 产品页](https://aipay.alipay.com/products/machine-pay)
- [Machine Pay 产品接入指南](https://aipay.alipay.com/docs/ai-receive/MACHINE_PAY.html)
- [payment.verify API](https://aipay.alipay.com/docs/ai-receive/api-list/alipay-aipay-agent-payment-verify.md)
- [fulfillment.confirm API](https://aipay.alipay.com/docs/ai-receive/api-list/alipay-aipay-agent-fulfillment-confirm.md)
- [A2M 对接文档（官方仓库）](https://github.com/alipay/ai/blob/main/code_example/aipay-402-example/A2M智能收产品对接文档.md)
- [买方 402 Skill](https://github.com/alipay/ai/blob/main/skills/alipay-pay-for-402-service/SKILL.md)
- [钱包授权 Skill](https://github.com/alipay/ai/blob/main/skills/alipay-authenticate-wallet/SKILL.md)
- [委托支付 Skill](https://github.com/alipay/ai/blob/main/skills/alipay-delegation-pay/SKILL.md)
- [SkillPay 官网](https://skillpay.alipay.com/)
- [SkillPay 博客《好的世界，技有所得》](https://skillpay.alipay.com/blog/good-world-skills-get-paid)
- [SkillPay 购买/履约执行器](https://aipayapi.alipay.com/skillpay/ct?c=BHa9h1KetgSC3Q2LqYsw)
- [支付宝 AI 付服务协议](https://render.alipay.com/p/c/180021120000001082/index.html?agreementId=AG01001505)
