# 支付宝 SkillPay × MachinePay · 四页演示规划

## 场景与判断

- 场景：技术机制解读（4 页，不设封面/目录/感谢页；P1 全景，P2 SkillPay，P3 MachinePay，P4 对比）
- 核心判断：SkillPay 是“商品层”，MachinePay 是“协议层”；两者共用支付宝 AI 付钱包与 HTTP 402。
- 听众：做 Skill 商业化、API 计费、Agent 支付与平台治理的人

## 逐页

| # | label | 这页要说啥 | 配图 |
|---:|---|---|---|
| 1 | 全景 | 阿里把 Agent 支付拆成商品层与协议层；同一套钱包与 402，SkillPay 卖交付权、MachinePay 卖计量调用 | 双轨对比 + 同一任务两种收费示例 |
| 2 | SkillPay | Skill 如何上架、定价、试用、交付、退款；一次性源码 vs 周期云端保护 | 5 环节 + 两种交付 + 购买/安装链路 |
| 3 | MachinePay | 402 报价、支付、凭证、验单、履约的完整时序与字段 | 4 角色时序图 + 账单/凭证字段 |
| 4 | 对比 | 两条轨道的分工、边界、对创作者/商家/平台的含义 | 对比表 + 4 条判断 + 3 个原则 |

## 事实与来源

- 主调研笔记：[references/alipay-skillpay-machinepay-research.md](references/alipay-skillpay-machinepay-research.md)
- SkillPay：上架前安全检测；一次性买断交源码；周期订阅云端保护、不交明文、不自动续费；成交即到账开发者支付宝；退款由开发者发起，周期订单整单全额退。
- SkillPay 购买链路：`firsttimebuy` 幂等下单 → 支付待确认 → 原单恢复 → `fulfillment_proof` → 安全下载/解压/安装。
- MachinePay：HTTP 402 + `Payment-Needed`（Base64URL 账单）；商家本地 RSA2 签名；买家回传 `Payment-Proof`；`verify` 校验 active/金额/订单/资源/防重放/pay_before；交付后 `fulfillment.confirm`。
- 钱包：`alipay-bot check-wallet` → `apply-wallet` → 6 位授权码 → `bind-wallet`；支付链接约 5 分钟；逐笔用户确认。
- 自主支付：委托支付（金额/次数/有效期，邀测），不是 402 默认能力。
- 来源：支付宝 AI 付文档、SkillPay 官网/博客、官方 `alipay/ai` 仓库（买方 Skills、A2M 对接文档）。

## 口径与提醒

- 金额单位存在“最小货币单位”与“元”的文档差异；落地以接入文档/接口为准。
- MachinePay 公开文档只暴露 verify + fulfillment，结算/退款/费率以后台协议为准。
- SkillPay 平台抽佣/费率未公开；云端保护不是绝对安全，是提高复制成本。
- 402 是收费握手，不是支付本身；默认逐笔用户确认，自主支付需委托支付。
- 单页无动画；HTML 离线单文件；PPTX 为可编辑对象。
