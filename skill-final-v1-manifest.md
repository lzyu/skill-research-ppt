# skill-final-v1 合并清单

- 输出：`skill-final-v1.pptx`（20 页，16:9，12192000×6858000）
- 原则：按指定顺序合并；不删除重复主题/版本；精确重复的文件不重复入片，源文件全部保留在工作区。
- 说明：为避免不同主题的 notes master 造成跨主题关系异常，合并时未复制演讲者备注；源 PPTX 中的备注仍在原文件。

## 2026-10-20 排版统一

- 页面标题：微软雅黑 24 pt，RGB 199/0/11（#C7000B）。
- 正文：微软雅黑 10 pt；正文中的章节标题 12 pt；为保住原卡片布局，正文采用 -1 pt 字间距（标题/章节 -0.5 pt）压缩换行。
- 移除右上角日期/来源等元信息、左下角来源/“Huawei Confidential”等小字，以及第 1 页表格下方的“下载分布”表注。
- 表格统一为 7.5 pt（表头加粗），避免原表格自动增高压住下方内容。
- 例外：KPI 数字保留展示字号；6.5–9.5 pt 的图注、单位、表注保留原字号，避免密集卡片溢出。若要求所有文字严格 10/12，需要重排或拆页。

## 顺序与来源

| # | 章节 | 页面标题 | 来源文件（页序） |
|---:|---|---|---|
| 01 | 01 魔搭平台调研 | 魔搭 Skills 中心：8.35 万技能撑起四层框架，验证闭环仍缺一环 | `modelscope-skills-center.pptx`（1/1） |
| 02 | 02 SkillHub 平台调研 | SkillHub 将技能分发扩展到场景组合与云端验证 | `skillhub/output/skillhub-insights.pptx`（1/1） |
| 03 | 02 SkillHub 平台调研 | SkillHub 围绕 Skill 打通生态供给、可信分发与宿主安装 | `skillhub/output/skillhub-insights-v1.pptx`（1/1） |
| 04 | 02 SkillHub 平台调研 | 腾讯 SkillHub：用 TRACE 把 Skill 分发从「能装」推向「可评」 | `skillhub-eval-onepage.pptx`（1/1） |
| 05 | 03 Skill 平台总结 | 一个 Skill 的四段路：写出来 → 发出去 → 装进去 → 用起来 | `skill-asset-lifecycle.pptx`（1/1） |
| 06 | 03 Skill 平台总结 | 从魔搭、SkillHub 到智果园：Skill 资产平台的四个必答题 | `zhiguoyuan-skill-asset-onepage.pptx`（1/1） |
| 07 | 04 腾讯 SkillPay 商业化 | SkillHub 已有按次收费供给，平台暂不收技术服务费 | `skillhub/output/skillhub-skillpay-commercialization-v1.pptx`（1/2） |
| 08 | 04 腾讯 SkillPay 商业化 | 微信 SkillPay 将微信订单接入 Agent，商户验付后履约 | `skillhub/output/skillhub-skillpay-commercialization-v1.pptx`（2/2） |
| 09 | 04 腾讯 SkillPay 商业化 | 两次下单接入 Agent，SkillHub 提供商户验签与分发 | `skillhub/output/skillhub-skillpay-commercialization-v2-final.pptx`（1/2） |
| 10 | 04 腾讯 SkillPay 商业化 | payment_code 发起付款，payment_id 串联任务与交付 | `skillhub/output/skillhub-skillpay-commercialization-v2-final.pptx`（2/2） |
| 11 | 05 阿里 SkillPay 商业化 | SkillPay 经营 Skill 商品，付款后分为源文件与使用权两种交付 | `gpt-alipay-research.pptx`（1/4） |
| 12 | 05 阿里 SkillPay 商业化 | 订阅原文留云端，云端给任务指导，本地 Agent 继续执行 | `gpt-alipay-research.pptx`（2/4） |
| 13 | 05 阿里 SkillPay 商业化 | MachinePay 先签报价，付款后带票重试，商户在线验付 | `gpt-alipay-research.pptx`（3/4） |
| 14 | 05 阿里 SkillPay 商业化 | 支付宝验证支付事实，商户核对业务账并恢复唯一履约 | `gpt-alipay-research.pptx`（4/4） |
| 15 | 05 阿里 SkillPay 商业化 | 阿里把 Agent 支付拆成两层：SkillPay 卖商品，MachinePay 卖调用 | `alipay-skillpay-machinepay.pptx`（1/4） |
| 16 | 05 阿里 SkillPay 商业化 | SkillPay：把 Skill 变成可定价、可交付、可退款的产品 | `alipay-skillpay-machinepay.pptx`（2/4） |
| 17 | 05 阿里 SkillPay 商业化 | MachinePay：用 402 把每次 API 调用变成一笔可验证的交易 | `alipay-skillpay-machinepay.pptx`（3/4） |
| 18 | 05 阿里 SkillPay 商业化 | SkillPay vs MachinePay：商品化与计费化的分工 | `alipay-skillpay-machinepay.pptx`（4/4） |
| 19 | 06 Skill 商业化总结 | 阿里经营 Skill 商品权益，腾讯连接付费服务与生态分发 | `zhiguoyuan-skill-commercialization.pptx`（1/2） |
| 20 | 06 Skill 商业化总结 | 智果园复用资产与云商店底座，重点补齐 Skill 商业编排 | `zhiguoyuan-skill-commercialization.pptx`（2/2） |

## 未重复入片的精确副本

以下文件与已选版本内容一致（同文本/同页数），为避免同一页反复出现，未重复入片；源文件均保留：

- `gpt-alipay-research.pptx` 的重复导出：`alipay-research/output/gpt-alipay-research.pptx`、`alipay-research/output/gpt-alipay-research-native.pptx`、`alipay-research/.build/*`。
- `zhiguoyuan-skill-commercialization.pptx` 的重复导出：`zhiguoyuan-commercialization/output/zhiguoyuan-skill-commercialization-native.pptx`、`zhiguoyuan-commercialization/.build/*`。
- SkillHub 的 `.build/*` 草稿与 `skillhub/output/*` 中的同内容版本。
- 其他 `*.build/*` 为生成过程中的中间稿；如需要可单独加入。

## 版式提醒

- 合并保留每份原稿的字体、字号、文本框与主题；不同来源的标题宽度/字体替换可能造成个别页标题换行或溢出（源 PPTX 同样存在）。
- 建议在 PowerPoint/WPS 中用统一母版、统一字体（如 Noto Sans SC / 微软雅黑）做一次版式整理，再删减重复页。
