# 腾讯 SkillHub 平台洞察 · 单页规划

## 需求与范围

按用户明确指定的主题、框架、aico-ppt 技能和一页 PPT 制作，用于 AI 资产平台建设讨论。沿用当前项目目录。交付一页 PPTX、同内容单文件 HTML、预览图和详细调研 Markdown。

用户明确要求一页，因此不添加封面、目录或感谢页；采用 work-report 场景的 dense 分层与侧栏页型，保留模板字体、配色和运行外壳。内容不增加动画或 layer，保证导出仍为一页。

## 逐页

| # | label | 核心观点 | 页型 | 排版理由 | 配图与证据 |
| --- | --- | --- | --- | --- | --- |
| 1 | SkillHub洞察 | SkillHub 以多类资产与可信消费组织能力供给 | work-report / layered-platform-ops-rail | 四层资产、消费旅程、生态供需和评测属于耦合维度，在一页以分层主图及分析侧栏组织 | 自绘四层职责图、四步消费链、供需画像、Top50下载占比条形图、TRACE文字维度 |

## 内容权重

- 顶部给出定位与规模，主体展示四层资产、四步消费、三类供需。
- 评测机制作为贯穿消费的控制项，标出质量分与安全/热度的边界。
- 总结落在对应内容区内，不添加独立装饰性口号条。

## 事实与来源

| 主张 | 数值 / 状态 / 口径 | 来源 |
| --- | --- | --- |
| 公开列表规模 | 199511，2026-10-19 列表响应 total | https://api.skillhub.cn/api/skills?sortBy=downloads&order=desc&pageSize=50 |
| 分类 | 13，当前公开一级分类 | https://api.skillhub.cn/api/v1/categories |
| 图表 | 下载榜Top50，条目下载字段之和，不是全平台及活跃用户 | sources/api-downloads.json、statistics.json |
| 图表分组 | 编程36.94%、AI Agent13.23%、知识10.14%、其他39.69% | statistics.json 自行计算 |
| 四层资产 | SOUL、专家包、Skill、MCP，四层关系为分析视图 | 官网当前导航与官方 README |
| 供给样例 | 平台维护技能、腾讯文档、钢联、社区通用技能 | 腾讯官方仓库及具体详情 API |
| 试运行 | 官方文档及当前前端实现存在，未创建会话执行 | research-evaluation-runtime.md |
| TRACE | 五维质量，热度 score 为另一指标；开源 evaluator 非全面动态实测 | 官方 evaluation.md、skills.md 及 evaluator |

详细解释与原始链接见 skillhub-insights.md。PPTX 备注实际写入来源与口径后复核。

## 完成交付与验证

- 单页 PPTX：output/skillhub-insights.pptx，113 个含文字对象，来源与口径已实际写入备注。
- HTML：skillhub-onepage.html，经 aico-ppt edit-bundle 保持单页结构。
- 编辑运行时缺少 @xterm/xterm，已按技能允许的 fallback 走直接编辑流程，未产生编辑器撤销历史。
- 验证：HTML 溢出 0、内部裁切 0；PPTX 结构及布局检查无发现，导入通过；实际 PPTX 渲染已逐项目检。
- 预览：output/skillhub-preview.png，为交付 PPTX 相同字节候选的渲染结果。
- 单页要求优先于技能默认封面、目录和感谢页要求。
