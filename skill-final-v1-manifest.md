# skill-final-v1 合并清单

- 输出：`skill-final-v1.pptx`（19 页，16:9，12192000×6858000）
- 原则：按指定顺序合并；不删除重复主题/版本；精确重复的文件不重复入片，源文件全部保留在工作区。
- 说明：为避免不同主题的 notes master 造成跨主题关系异常，合并时未复制演讲者备注；源 PPTX 中的备注仍在原文件。

## 2026-10-20 第二版排版

- 页面标题：微软雅黑 24 pt，RGB 199/0/11（#C7000B），统一上移到距顶 0.045H。
- 删除标题上方 kicker、标题下方红色横线、标题下方一行总结小字；19 页全部校验通过。
- 正文：微软雅黑 10 pt；正文中的章节标题 12 pt；正文采用 -1 pt 字间距、章节标题 -0.5 pt，保证 10/12 号下不溢出。
- 移除右上角日期/来源等元信息、左下角来源/“Huawei Confidential”等小字，以及表格下方的“下载分布”表注。
- 表格统一为 7.5 pt（表头加粗），避免原表格自动增高压住下方内容。
- **Skill 资产生命周期页重做为第 1 页**：生产 / 分发 / 安装 / 使用四段，每段给出可执行动作、检查点与产物，并保留闭环回线；结合智果园示例（AI 资产广场上架分发、CodeArts Agent 安装使用）。原第 5 页删除，总页数 19。
- **第一页按 `skill-lifecycle-summary.md` 的“关键动作”重新核对**：每段只把“动作”放入动作层，检查点与产物另列；生产段把“定任务 / 写方法 / 配资源并验证”拆开，边界放入“定任务”和检查点，样例与评测记录放入产物，不再把“留样例和边界”当作与前两步并列的第三个动作。动作层补入 `$skill-creator`、Git/ZIP、`npx skills add`、`/pdf-processing` 等可执行动作；`$skill-creator` 作为一条起稿路径，不写成唯一方式。
- **最后两页按统一版式重排**：第 18 页先总结阿里/腾讯两条商业化路径（对比表 + 三点判断），第 19 页给出智果园的四条启示、首期路径与验收口径。
- **SkillHub 从 3 页合并为 2 页**：第 3 页“关键能力”（供给与发布 / 分发安装 / 云端试跑 / TRACE）；第 4 页“生态画像”：供给/分类看全站，消费与“谁被下载”中位看 Top10000；改为免费 / Payskill / API Key 三列 Top8 下载榜；移除消费集中度与谁被下载两块；个人/企业为按来源标签折算，Top10000 不等于全站。
- **魔搭合并为一页**：上半部分是“关键能力洞察”（发布 / 使用 / 试运行），下半部分是“生态画像”的 4 项对比：来源结构（GitHub / 其他市场 / 外部网站 / 个人上传）/ 月度上架（集中导入）/ 类目分布 / 四类来源 Top6（24 个，显示名/所有者/下载量）；已按 2026-10-24 全量 source_url 统计更新。
- **标题已回退**：恢复上一版标题；第一页的动作 / 检查 / 产物内容保留。
- 例外：KPI 数字保留展示字号；6.5–9.5 pt 的图注、单位、表注保留原字号，避免密集卡片溢出。若要求所有文字严格 10/12，需要重排或拆页。

## 顺序与来源

| # | 章节 | 页面标题 | 来源文件（页序） |
|---:|---|---|---|
| 01 | 00 Skill 资产生命周期（开篇） | Skill 资产生命周期：生产 → 分发 → 安装 → 使用 | `skill-asset-lifecycle.pptx` 内容重做，结合智果园 / CodeArts Agent 示例 |
| 02 | 01 魔搭平台调研 | 魔搭 Skill 关键能力：发布两步、安装四路，试运行和原创供给都还薄 | `modelscope-skills-center.pptx` 内容重做 + 一手 API/页面核查（1/1） |
| 03 | 02 SkillHub 平台调研 | SkillHub 关键能力：20 万供给、多路安装、云端试跑、TRACE 评分 | `skillhub-insights-v1.pptx` + `skillhub-eval-onepage.pptx`（重做，1/2） |
| 04 | 02 SkillHub 平台调研 | SkillHub 生态画像：全站个人 34.0%、企业 34.4%、镜像 31.6% | `skillhub-insights.pptx` / `skillhub-insights-v1.pptx` + 全站来源拆分/分类/付费与 Top10000 中位复算（重做，2/2） |
| 05 | 03 Skill 平台总结 | 从魔搭、SkillHub 到智果园：Skill 资产平台的四个必答题 | `zhiguoyuan-skill-asset-onepage.pptx`（1/1） |
| 06 | 04 腾讯 SkillPay 商业化 | SkillHub 已有按次收费供给，平台暂不收技术服务费 | `skillhub/output/skillhub-skillpay-commercialization-v1.pptx`（1/2） |
| 07 | 04 腾讯 SkillPay 商业化 | 微信 SkillPay 将微信订单接入 Agent，商户验付后履约 | `skillhub/output/skillhub-skillpay-commercialization-v1.pptx`（2/2） |
| 08 | 04 腾讯 SkillPay 商业化 | 两次下单接入 Agent，SkillHub 提供商户验签与分发 | `skillhub/output/skillhub-skillpay-commercialization-v2-final.pptx`（1/2） |
| 09 | 04 腾讯 SkillPay 商业化 | payment_code 发起付款，payment_id 串联任务与交付 | `skillhub/output/skillhub-skillpay-commercialization-v2-final.pptx`（2/2） |
| 10 | 05 阿里 SkillPay 商业化 | SkillPay 经营 Skill 商品，付款后分为源文件与使用权两种交付；左侧为 402 支付嵌入任务的序列图 | `gpt-alipay-research.pptx`（1/4） |
| 11 | 05 阿里 SkillPay 商业化 | 订阅原文留云端，云端给任务指导，本地 Agent 继续执行 | `gpt-alipay-research.pptx`（2/4） |
| 12 | 05 阿里 SkillPay 商业化 | MachinePay 先签报价，付款后带票重试，商户在线验付 | `gpt-alipay-research.pptx`（3/4） |
| 13 | 05 阿里 SkillPay 商业化 | 支付宝验证支付事实，商户核对业务账并恢复唯一履约 | `gpt-alipay-research.pptx`（4/4） |
| 14 | 05 阿里 SkillPay 商业化 | 阿里把 Agent 支付拆成两层：SkillPay 卖商品，MachinePay 卖调用 | `alipay-skillpay-machinepay.pptx`（1/4） |
| 15 | 05 阿里 SkillPay 商业化 | SkillPay：把 Skill 变成可定价、可交付、可退款的产品 | `alipay-skillpay-machinepay.pptx`（2/4） |
| 16 | 05 阿里 SkillPay 商业化 | MachinePay：用 402 把每次 API 调用变成一笔可验证的交易 | `alipay-skillpay-machinepay.pptx`（3/4） |
| 17 | 05 阿里 SkillPay 商业化 | SkillPay vs MachinePay：商品化与计费化的分工 | `alipay-skillpay-machinepay.pptx`（4/4） |
| 18 | 06 Skill 商业化总结 | 两个平台的商业化：阿里卖商品权益，腾讯连付费服务 | `zhiguoyuan-skill-commercialization.pptx`（1/2，重排） |
| 19 | 06 Skill 商业化总结 | 对智果园的启示：补商业编排，而不是再堆资产 | `zhiguoyuan-skill-commercialization.pptx`（2/2，重排） |

## 未重复入片的精确副本

以下文件与已选版本内容一致（同文本/同页数），为避免同一页反复出现，未重复入片；源文件均保留：

- `gpt-alipay-research.pptx` 的重复导出：`alipay-research/output/gpt-alipay-research.pptx`、`alipay-research/output/gpt-alipay-research-native.pptx`、`alipay-research/.build/*`。
- `zhiguoyuan-skill-commercialization.pptx` 的重复导出：`zhiguoyuan-commercialization/output/zhiguoyuan-skill-commercialization-native.pptx`、`zhiguoyuan-commercialization/.build/*`。
- SkillHub 的 `.build/*` 草稿与 `skillhub/output/*` 中的同内容版本。
- 其他 `*.build/*` 为生成过程中的中间稿；如需要可单独加入。

## 版式提醒

- 合并保留每份原稿的字体、字号、文本框与主题；不同来源的标题宽度/字体替换可能造成个别页标题换行或溢出（源 PPTX 同样存在）。
- 建议在 PowerPoint/WPS 中用统一母版、统一字体（如 Microsoft YaHei / Noto Sans SC）做一次版式整理，再删减重复页。
