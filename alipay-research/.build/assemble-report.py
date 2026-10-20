from pathlib import Path
import re,json,hashlib

root=Path('/Users/tpy/workspace/ai_gallery/skill-asset-ppt/alipay-research')
intro='''# 支付宝 SkillPay 与 MachinePay：从商品权益到资源验付的原理剖析

调研日期：2026-10-20，Asia/Shanghai。对应四页可编辑演示文稿 `gpt-alipay-research.pptx`。本研究从用户指定的 SkillPay 博客及 MachinePay 产品页起步，继续核对官方协议文档、官方架构图、当前公开前端、支付宝官方代码和 API 错误码。

## 先回答两者分别解决什么

**SkillPay 商品平台把 Skill 做成可售卖、试用和持续交付的商品。** 买断交完整源文件；订阅交有效期内使用权，完整原文留云端，按任务只输出必要指导，再由本地 Agent 执行。平台需要维护的不只是支付记录，还有商品版本、权益是否可用及资源是否交付。[官方技术博客](https://skillpay.alipay.com/blog/good-world-skills-get-paid)、[更新日志](https://skillpay.alipay.com/changelog)。

**MachinePay 让一笔资源请求具有机器可读的收费和验付流程。** 商户本地签报价，HTTP 402 投递付款要求；付款之后，买家带 Payment-Proof 重试，商户调用支付宝 verify，再对齐自己的订单、金额和资源，控制唯一履约，并提交履约回执。[产品接入指南](https://aipay.alipay.com/docs/ai-receive/MACHINE_PAY.html)、[验付 API](https://aipay.alipay.com/docs/ai-receive/api-list/alipay-aipay-agent-payment-verify.md)。

“商品经营”和“资源调用收费”是解释两者的分析视角，并不是对支付宝内部系统分层的证明。SkillPay 要求相关支付协议并不代表其所有商品按次计费；公开资料也不足以证明所有 SkillPay 请求必定通过某一个 MachinePay 网关或同一段服务代码。

| 问题 | SkillPay 商品平台 | MachinePay |
|---|---|---|
| 购买对象 | Skill 完整文件或期限内使用权 | 某笔 API/MCP/内容/算力资源交易 |
| 付款后还需判断什么 | 权益发放、期限/试用/额度、版本与交付模式 | 凭证有效性、金额/订单/资源一致、幂等执行 |
| 能力在哪里执行 | 买断本地执行；受保护订阅由云端给指导、本地继续执行 | 在实际商户业务后端，具体看服务 |
| 平台承担什么 | 扫描、商品、版本、试用/权益、原文保护、支付后交付与经营 | 报价/支付/验付协议及相关支付能力；业务实现仍在商户 |
| 不能混淆什么 | 已付款、权益可用、已交付、任务已完成 | 签名报价、支付证明、业务结果、履约回执 |

## 四页图解的阅读顺序

1. **Skill 商品与交付**：作者发布后，为什么同一次付费握手会产生“完整文件”与“持续使用权”两种结果。
2. **云端保护与本地执行**：完整原文在哪里，任务数据和指导怎样流动，为什么保护并不等于云端代跑全部任务。
3. **MachinePay 付款协议**：第一次请求只有报价，第二次请求才带支付凭证；商户与支付宝分别做什么。
4. **验付与恢复**：把支付宝交易事实和商户业务订单对齐；资源已生成而回执失败时，怎样恢复同一交易。

以下两部分保留完整研究证据与原理图。事实来自官方；从接口职责推导的工程要求、公开代码观察和未公开实现均单独标明。

'''

def part(path,title):
 s=path.read_text();s=re.sub(r'^# .*?\n','',s,count=1)
 s=re.sub(r'^(#{2,5}) ',lambda m:'#'+m.group(1)+' ',s,flags=re.M)
 return '\n## '+title+'\n\n'+s

tail='''
## 三、必须分开的四种“成功”

```mermaid
flowchart LR
    W[钱包/支付授权就绪] --> P[某笔交易支付完成]
    P --> E[商品权益已发放且当前可用]
    E --> D[资源或任务指导已交付]
    D --> R[实际业务执行完成，产物合格]
```

这张图表达逻辑检查层次，并不规定所有产品都必须新发一份订阅权益。MachinePay 的一笔资源交易通常直接对齐商户本地订单；SkillPay 则常要维护买断或周期权益。钱包授权不能代替商品权益，支付证明不能代替任务产物。

### 为什么要记住原请求

支付系统记录钱付给谁、哪笔交易；Agent 任务还包含 HTTP 方法、URL、请求体、业务 Header 和上下文。若只保留交易号、丢失原 POST 输入，钱虽然付了，应用也未必知道该恢复哪一次生成或查询。因此恢复机制必须跨过“支付交易”和“业务任务”两类状态。此处是对公开恢复参数与模板接口的工程解释。

### 为什么 Base64URL 不等于加密或验真

Payment-Needed / Payment-Proof 的 Base64URL 是传输封装。可解码并不意味着字段可信或支付完成。报价由商户签名；不透明 payment_proof 交支付宝在线验证；商户再校验自己的业务关联。不能把它们统称为“一段能开所有门的 token”。

### 为什么一次验票不能替代业务幂等

验付和执行业务之间仍有应用层并发、数据库提交和进程故障窗口。即使两次请求拿着同一笔真实支付，商户也要确保只生成一个付费结果，并将结果和回执状态持久保存。下游带副作用的任务还需要可重用的业务幂等键；这些约束不由一个 HTTP 状态码自动完成。

## 四、官方材料中的差异，怎样取舍

| 分歧 | 本次处理 |
|---|---|
| MachinePay 产品页通用 /verify、/settle、交易哈希图，与人民币接入指南不同 | PPT 采用实际人民币 payment.verify / fulfillment.confirm API，不把通用图当作可执行协议 |
| amount 网页写“最小货币单位”，官方专门文档与代码写元 | 讲原理不换算真实账单；示例 0.01 CNY 按当前官方代码为 0.01 元。落地应核对当前通道接口，不把文案矛盾隐去 |
| client_session 参数表可选，但部分错误码要求 | 存在则原样透传，按通道和错误处理；不承诺所有模式必填或都可忽略 |
| 在线指南先交付后异步回执，当前 alipay/ai 模板先确认再返结果 | 时序页采用在线指南并脚注；恢复页明确采用模板的本地状态抽象，不声称是支付宝内部状态机 |
| 首次履约超时策略在 alipay/ai 模板与 antgroup/ACT 集成例中不同 | 作为接入策略差异，不将 pay_before 解释为支付后自动退款或资金失效 |
| SkillPay llms 索引与当前站点不完全对应 | 用当前博客、上架/FAQ/更新日志和公开前端核实商品平台；不把传统生活供给 SkillPay 接入泛化到 Skill 文件商品 |

## 五、证据与交付范围

- 主稿：`../gpt-alipay-research.pptx`
- 离线 HTML：`../gpt-alipay-research.html`
- [SkillPay 专题原始报告](research-skillpay.md)
- [MachinePay 专题原始报告](research-machinepay.md)
- `sources/skillpay/` 保存官方网页、公开 JavaScript、架构 SVG 和官方消费侧规则。
- `sources/machinepay/` 保存产品/接入/API 文档与固定版本官方代码。主代码快照为 `alipay/ai` commit `c4a6d8d58b906bc77e2d88a0adbc0b64e34560a5`；其他示例的来源及版本另列。
- `source-inventory.json` 记录全部源文件的大小与 SHA256；各专题的来源清单记录原 URL。

未登录、安装、签约、授权、创建订单、访问商品购买 CT 或实际付款，也没有以沙箱测试冒充生产验证。闭源钱包扣款内部 API、凭证内部消耗状态、SkillPay 精确权益绑定、后台幂等/崩溃恢复、统一费率和 GMV 没有充分公开证据。报告没有用猜测填补这些环节。
'''

out=root/'alipay-mechanisms.md'
out.write_text(intro+part(root/'research-skillpay.md','一、SkillPay：商品、权益、云端保护与本地执行')+part(root/'research-machinepay.md','二、MachinePay：报价、付款、验付、履约与恢复')+tail)
inventory=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((root/'sources').rglob('*')) if p.is_file()]
(root/'source-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
print('Report characters',len(out.read_text()),'source files',len(inventory),'diagrams',out.read_text().count('```mermaid'))
