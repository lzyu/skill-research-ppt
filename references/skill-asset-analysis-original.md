# Skills 资产形态分析：生产、安装、使用与分发

从 AI 资产平台建设的视角，Skills 已经成为 Agent 生态中非常重要的一种资产形态。

与传统的模型、数据集、MCP Server、Agent 应用不同，Skill 的核心价值是**将某一类任务的专业知识、操作流程、工具使用方法和配套资源封装成可复用的能力包，使 Agent 能够按需加载并执行。**

结合 Agent Skills 开放标准，以及 Claude Code、OpenAI Codex、Skills.sh 等生态的发展，可以从以下几个方面理解。

## 一、Skills 是什么？资产形态长什么样？

### 1.1 核心定义

按照 [Agent Skills 开放标准](https://agentskills.io/specification)，一个 Skill 本质上是一个文件目录，至少包含一个 `SKILL.md` 文件。

它可以包含：

- **Instructions**：任务说明、执行步骤、约束条件。
- **Scripts**：Python、Shell、JavaScript 等可执行脚本。
- **References**：领域知识、规范文档、API 说明。
- **Assets**：模板、图片、配置、数据等资源。
- **Tool Instructions**：如何使用 MCP、CLI、API 等外部工具的说明。

一个典型的 Skill 资产：

```text
pdf-processing/
│
├── SKILL.md                  # 必选：技能定义
│
├── scripts/                  # 可选：可执行脚本
│   ├── extract_text.py
│   └── convert_pdf.py
│
├── references/               # 可选：参考知识
│   └── pdf_specification.md
│
├── assets/                   # 可选：资源文件
│   └── report_template.pdf
│
└── examples/                 # 可选：示例
    └── example.md
```

其中 `scripts/`、`references/` 和 `assets/` 是规范推荐的目录约定，并非全部必选。

### 1.2 SKILL.md 的内容

例如：

```markdown
---
name: pdf-processing
description: 用于 PDF 文件提取、转换、合并和分析。
---

# PDF Processing Skill

## When to use

当用户提出以下需求时使用：

- 提取 PDF 中的文字
- 将 PDF 转换为其他格式
- 合并多个 PDF 文件

## Workflow

1. 分析用户任务。
2. 检查输入文件。
3. 选择对应的处理脚本。
4. 执行脚本。
5. 检查结果。
6. 返回生成文件。

## Resources

- scripts/extract_text.py
- scripts/convert_pdf.py
```

`SKILL.md` 由两部分组成：

| 组成 | 作用 | 是否必选 |
|---|---|---|
| name | Skill 唯一名称（在相应命名空间内） | 是 |
| description | 能力描述及触发条件 | 是 |
| Markdown 指令 | 告诉 Agent 如何完成任务 | 是 |
| license | 授权信息 | 否 |
| compatibility | 环境兼容性说明 | 否 |
| metadata | 扩展元数据 | 否 |

需要特别注意：

**Skill 不是一种新的模型，也不是独立的 Agent 运行时，而是一种面向 Agent 的可加载能力资产。**

它可以只有 Markdown 指令，也可以同时包含代码、知识库、模板，以及对外部工具的调用约定。[GitHub](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx?utm_source=chatgpt.com)

---

## 二、Skills 资产有哪些类型？

这里需要区分两个维度：**文件组织格式**和**能力实现方式**。

文件组织格式相对统一，主要遵循 `SKILL.md + 可选资源目录` 的结构。

但不同 Skill 的能力实现方式差异很大。

从 AI 资产平台的角度，建议划分为以下五类。

| Skill 类型 | 核心组成 | 典型用途 | 是否依赖外部工具 |
|---|---|---|---|
| ① Prompt 型 | SKILL.md | 文案编写、代码评审规范 | 不一定 |
| ② Knowledge 型 | SKILL.md + References | 法律知识、行业知识、企业规范 | 不一定 |
| ③ Script 型 | SKILL.md + Scripts | PDF 处理、数据分析、文件转换 | 通常需要执行环境 |
| ④ Tool/MCP 型 | SKILL.md + 工具使用说明 | 操作 GitHub、云资源管理、数据库查询 | 通常需要 |
| ⑤ Composite 型 | Instructions + Scripts + References + Tools | 自动化研发、复杂数据分析、业务流程 | 通常需要 |

这五类是**建议的资产平台分类方式，并非 Agent Skills 官方定义的五种标准类型**。

它们也不是互斥关系，一个 Skill 完全可以同时具备多种特征。

例如，一个“云资源成本分析 Skill”可以：

1. 使用 MCP 查询云资源账单。
2. 使用 References 读取企业成本核算规则。
3. 使用 Python Scripts 计算成本。
4. 按照 SKILL.md 的流程生成优化报告。

从资产治理角度，还建议给每个 Skill 标记能力特征，如 `prompt`、`knowledge`、`script`、`mcp`，这样比强制归入单一类型更合理。

---

## 三、Skills 类型的资产如何生产？

当前主流生产模式可以归纳为四种。

### 3.1 方式一：人工编写

开发者直接创建 Skill 目录，编写 `SKILL.md`，按需添加脚本、文档和资源。

基本流程：

```text
开发者
   │
   ▼
创建 Skill 目录
   │
   ▼
编写 SKILL.md
   │
   ├── 定义使用场景
   ├── 定义执行步骤
   ├── 定义输入输出
   └── 定义工具调用方式
   │
   ▼
添加 Scripts / References / Assets
   │
   ▼
测试验证
   │
   ▼
发布到 Git 仓库或资产平台
```

**特点：**

适用于需要严格控制行为、具备明确执行规范的企业级 Skill。

### 3.2 方式二：使用 AI 自动生成

这是目前非常典型的 Skill 生产方式。

开发者无需直接编写完整的 `SKILL.md`，而是通过自然语言描述需求，让 AI 辅助生成。

例如，在 Codex 中调用：

```text
$skill-creator

创建一个华为云 ECS 运维 Skill。

要求：
1. 能够查询 ECS 实例。
2. 能够分析实例监控指标。
3. 能够诊断常见故障。
4. 使用华为云 MCP 工具进行操作。
5. 输出结构化运维报告。
```

AI 可以协助生成：

```text
huawei-cloud-ecs/
├── SKILL.md
├── references/
│   └── ecs_troubleshooting.md
└── scripts/
    └── analyze_metrics.py
```

OpenAI 官方文档明确支持使用 `skill-creator` 创建技能，同时支持手工创建。[OpenAI Developers](https://developers.openai.com/plugins/build/skills?utm_source=chatgpt.com)

**特点：**

降低生产门槛，适合企业内部业务专家、运营人员和低代码开发者。

但自动生成的 Skill 仍需要测试，尤其是脚本执行安全性、工具权限和输出准确性。

### 3.3 方式三：从现有能力或工具封装

这类生产方式对 AI 资产平台尤其有价值。

企业通常已经积累了大量：

- MCP Server
- OpenAPI
- CLI 工具
- Python 脚本
- 业务 SOP
- 企业知识文档

这些资产可以被封装、组合为 Skill。

例如：

```text
已有 MCP Server
    │
    ├── list_ecs
    ├── get_ecs_monitor
    └── restart_ecs
    │
    ▼
定义运维流程
    │
    ▼
生成 SKILL.md
    │
    ▼
ECS 运维 Skill
```

需要明确的是：

**MCP Server 并不直接等于 Skill。**

MCP 主要负责提供数据访问、认证授权和工具执行能力。

Skill 则负责规定什么时候调用工具、以什么顺序调用，以及如何处理结果。

OpenAI 当前的 Plugins 架构也明确采用这种分层：MCP 提供工具能力，Skill 提供工作流编排和操作指导。[OpenAI Developers](https://developers.openai.com/plugins/concepts/skills?utm_source=chatgpt.com)

另外，OpenAI 也支持在插件提交过程中，从符合相应能力声明要求的 MCP Server 导入 Skill 文件。这里是导入 Skill 资源，而不是把普通 MCP Tool 自动转换成完整 Skill。[OpenAI Developers](https://developers.openai.com/plugins/build/skills?utm_source=chatgpt.com)

### 3.4 方式四：复用现有 Skill 二次开发

开发者也可以直接从 GitHub、Skills.sh 等平台获取现有 Skill。

然后通过以下方式生产企业自己的版本：

```text
公共 Skill
    │
    ▼
Fork / Clone
    │
    ▼
修改 SKILL.md
    │
    ├── 增加企业规范
    ├── 替换内部工具
    ├── 添加企业知识
    └── 调整执行流程
    │
    ▼
测试与安全检查
    │
    ▼
企业 Skill
```

这种模式适合 AI 资产平台沉淀公共生态能力，并推动企业内部复用。

需要遵循原始资产的许可证以及再分发限制。

### 3.5 生产模式总结

| 生产模式 | 生产入口 | 典型用户 | 资产平台可以提供的能力 |
|---|---|---|---|
| 人工开发 | IDE / Git / 文件编辑器 | 专业开发者 | Skill 模板、校验工具、Git 导入 |
| AI 生成 | skill-creator / 对话界面 | 开发者、业务专家 | AI Skill Builder |
| 现有资产封装 | MCP / API / Script / 文档 | 平台开发者 | 资产转 Skill、自动生成描述 |
| 二次开发 | GitHub / Skills.sh | 开发者、企业用户 | Fork、版本管理、二次发布 |

**对于 AI 资产平台，最值得优先建设的是 Skill 导入、AI 辅助生成和现有 MCP 能力封装三条生产链路。**

---

## 四、Skills 资产如何安装？

Skill 的安装有一个很重要的特点：

**大多数基于 Agent Skills 文件规范的 Skill，并不需要像传统软件一样进行编译和部署。安装主要是把 Skill 文件放入 Agent 能够发现和读取的位置。**

但如果 Skill 依赖 Python 包、Node.js、MCP Server 或其他外部环境，还需要额外完成依赖配置。

### 4.1 当前主要有四种安装方式

| 安装方式 | 具体实现 | 典型生态 |
|---|---|---|
| ① 手工安装 | 下载 Skill 目录，复制到指定位置 | Claude Code、Codex |
| ② CLI 安装 | 通过 `npx skills add` 等命令安装 | Skills.sh |
| ③ Agent 内安装 | 通过 AI 指令或内置安装器安装 | Codex、Claude Code 及其扩展 |
| ④ 平台/API 安装 | 在插件市场安装、上传 ZIP 或通过 API 注册 | ChatGPT、OpenAI API |

### 4.2 方式一：手工安装

以 Claude Code 为例。

假设已经下载了一个 `pdf-processing` Skill：

```text
pdf-processing/
├── SKILL.md
├── scripts/
└── references/
```

可以将其复制到：

```text
# 用户级
~/.claude/skills/pdf-processing/

# 项目级
<project>/.claude/skills/pdf-processing/
```

Codex 也支持类似的项目级、用户级 Skill 发现机制，例如：

```text
# 用户级
~/.agents/skills/pdf-processing/

# 项目级
<project>/.agents/skills/pdf-processing/
```

不同版本的 Codex 以及旧安装工具还可能使用 `~/.codex/skills/`，所以具体目录需要以使用的客户端版本为准。

这类安装的本质是：

```text
Skill 资产包
     │
     ▼
复制到指定目录
     │
     ▼
Agent 扫描 Skill
     │
     ▼
解析 SKILL.md
     │
     ▼
注册到可用 Skills 列表
```

注意：这里的“注册”一般是客户端运行时维护可用 Skill 列表，不代表注册到中心化服务器。

### 4.3 方式二：通过 Skills CLI 安装

目前比较有代表性的是 [Skills.sh](https://skills.sh)。

Vercel 于 2026 年 1 月推出了 Skills CLI 与 Skills.sh 目录服务，支持在多个 Agent 客户端中安装和管理 Skill。[Vercel](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem?utm_source=chatgpt.com)

例如：

**安装整个仓库中的 Skills：**

```bash
npx skills add vercel-labs/agent-skills
```

**安装指定 Skill：**

```bash
npx skills add vercel-labs/agent-skills \
  --skill react-best-practices
```

**全局安装：**

```bash
npx skills add vercel-labs/agent-skills -g
```

这里需要区分：

- 项目级安装：Skill 主要对当前项目生效。
- 用户级安装：Skill 可以被当前用户的相关项目复用。
- 具体复制位置及支持的 Agent，由安装工具与客户端共同决定。

Skills CLI 会发现来源中的 Skills，并协助安装到受支持的 Agent 环境，而不是让 Skill 自己提供一个统一的运行时。

官方文档：[Skills CLI](https://www.skills.sh/docs/cli)。

### 4.4 方式三：通过 Agent 内置能力安装

例如，Codex 的经典 Skill 机制提供过 `$skill-installer`：

```text
$skill-installer

Install a skill from:
https://github.com/owner/repo/tree/main/skills/pdf-processing
```

Agent 根据 Skill Installer 的说明，调用下载脚本，获取文件并安装到本地。

需要关注一个新的变化：

**截至 2026 年 10 月，OpenAI 已经将 Plugins 作为 ChatGPT 和 Codex 统一的能力分发体系。**

当前公开文档支持把一个或多个 Skills，以及可选的 MCP Server，封装为 Plugin。

用户可以通过插件目录安装，而不必直接操作 Skill 文件。[OpenAI Developers](https://developers.openai.com/plugins/build/plugins?utm_source=chatgpt.com)

因此，Codex 生态正在同时存在两类值得关注的路径：

1. 传统的独立 Skill 安装、加载机制。
2. 以 Plugin 为分发单元，安装包含一个或多个 Skills 的能力包。

对于 AI 资产平台，这个变化很有参考价值：**Skill 是能力资产，Plugin 可以是更高一层的交付与分发载体。**

### 4.5 方式四：通过 API 上传并使用

OpenAI 的 API 已经提供了 Skills 资源接口。

例如，可以通过 `POST /v1/skills` 上传一个 Skill ZIP：

```bash
curl -X POST https://api.openai.com/v1/skills \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "files=@./pdf-processing.zip;type=application/zip"
```

接口返回 Skill ID、名称、版本等信息。

这说明 Skill 不局限于存储在 Agent 客户端的本地文件系统，也可以由平台统一托管、管理版本，并在支持的运行环境中供 Agent 使用。

但要注意，上传成功不意味着 Skill 已经被任何一个 Agent 自动激活，还需要通过对应 API 或运行环境关联它。[OpenAI Developers](https://developers.openai.com/api/docs/guides/tools-skills?utm_source=chatgpt.com)

---

## 五、Skills 安装后如何使用？

### 5.1 两种核心使用方式

**第一种：Agent 自动发现并触发 Skill。**

例如用户输入：

> 帮我把这三个 PDF 合并成一个文件。

Agent 发现当前可用的 Skills 中存在：

```yaml
name: pdf-processing
description: 用于 PDF 合并、拆分、转换和内容提取。
```

模型判断当前任务与 Skill 的描述匹配，读取完整的 `SKILL.md`，再按照其中的步骤执行。

整个过程一般不需要用户明确指定 Skill。

**第二种：用户显式调用 Skill。**

以 Claude Code 为例：

```text
/pdf-processing
```

也可以带上任务描述：

```text
/pdf-processing 帮我合并这三个 PDF
```

在支持相应语法的 Codex 场景中，也可以通过 Skill 名称显式引用：

```text
$pdf-processing
```

不过显式调用的具体语法并不是 Agent Skills 开放标准的一部分，而是不同宿主 Agent 的实现机制。

### 5.2 Skills 的完整运行流程

这是理解 Skill 与传统工具之间区别的关键。

```text
                  用户提出任务
                       │
                       ▼
                Agent 接收任务
                       │
                       ▼
               Skill Discovery
                       │
           扫描可用 Skill 元数据
             name + description
                       │
                       ▼
                Skill Matching
                       │
              判断是否需要 Skill
                       │
                       ▼
                Skill Activation
                       │
                加载 SKILL.md
                       │
                       ▼
                Skill Execution
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       读取知识      执行脚本       调用工具
       References    Scripts       MCP/API
          │            │            │
          └────────────┼────────────┘
                       │
                       ▼
                Agent 汇总结果
                       │
                       ▼
                  返回用户
```

Agent Skills 规范将这种加载机制称为 **Progressive Disclosure（渐进式披露）**。

具体可以分成三个层次：

| 阶段 | 加载内容 | 目的 |
|---|---|---|
| Level 1：发现 | name、description | 让 Agent 知道有哪些 Skill |
| Level 2：激活 | 完整 SKILL.md | 让 Agent 知道如何执行 |
| Level 3：执行 | Scripts、References、Assets 等 | 按需获取实际执行资源 |

其核心价值在于：

**不需要在每次对话时，把所有 Skills 的完整内容都放入模型上下文。**

只有真正用到某个 Skill 时，才加载详细指令和资源。

因此，Skill 既是一种资产封装格式，也是一种面向 LLM 上下文管理的能力组织方式。[GitHub](https://github.com/agentskills/agentskills?utm_source=chatgpt.com)

### 5.3 Skill 是否需要独立运行？

这是 AI 资产平台需要明确的一个问题。

通常情况下，**Skill 自己不运行，而是由宿主 Agent 解释和执行。**

例如：

```text
                   Codex Agent
                        │
                 加载 PDF Skill
                        │
                 阅读 SKILL.md
                        │
                 决定执行脚本
                        │
                 调用 Python 环境
                        │
                   生成 PDF
```

真正负责执行的是 Codex 所处的工具或沙箱环境。

Skill 则负责描述工作流程，以及提供所需资源。

因此，一个 Skill 从平台下载后，能否正常使用，需要同时满足：

- 宿主 Agent 支持相应 Skill 格式。
- 宿主具有 Skill 所要求的工具能力。
- 必要的运行环境和依赖已经配置。
- 用户具备执行所需的权限。

这也意味着：**文件格式兼容不等于运行能力完全兼容。**

例如，同一个 Skill 可能在 Claude Code 和 Codex 中都能够被识别，但因为某些工具或权限机制不同，实际效果并不完全一致。

---

## 六、Skills 资产如何分发？

目前 Skill 资产的分发方式，可以总结为四类。

| 分发方式 | 资产存储形态 | 代表平台 | 特点 |
|---|---|---|---|
| Git 仓库 | Skill 文件目录 | GitHub | 版本管理、源码可见、便于协作 |
| Skill Marketplace | Git 仓库索引或平台托管资源 | Skills.sh | 搜索、发现、安装、更新 |
| 文件包分发 | ZIP / 目录 | Claude Code、Codex | 易于导入、离线交付 |
| 托管 API / Plugin | 平台管理的版本化资产或插件包 | OpenAI | 统一管理、部署、权限和版本 |

特别需要关注 GitHub 与 Skills.sh 之间的关系。

### Skills.sh 本质上扮演什么角色？

以 GitHub 上的 Skill 为例：

```text
        Skill 开发者
             │
             ▼
       GitHub Repository
             │
             │ 存放 SKILL.md
             │ Scripts / Assets
             │
             ▼
          Skills.sh
             │
       ┌─────┼─────┐
       ▼     ▼     ▼
      搜索   排行   详情
       │
       ▼
    CLI 安装
       │
       ▼
   用户本地 Agent
       │
       ▼
      使用 Skill
```

Skills.sh 提供 Skill 搜索、目录展示、安装指令及相关生态服务。对于 GitHub 来源的 Skill，实际资产主要存放在来源仓库中。

因此它不仅仅是一个文件下载网站，更接近于：

**Skill 发现目录 + 资产索引 + 安装工具生态。**

另外，它的 Packs 机制支持将多个 Skills 组织为一个可安装集合。[Skills](https://www.skills.sh/docs?utm_source=chatgpt.com)

这里还要区分两个概念：

- **Skill**：一项具体能力的定义及资源。
- **Skill Pack / Plugin**：一个或多个 Skills 的交付集合，可能附带 MCP、配置和其他扩展。

对于华为云 AI 资产平台，建议同时支持独立 Skill 资产与组合资产包，而不是把两者混为同一种资产格式。

---

## 七、Skills 与 MCP、Agent 之间是什么关系？

结合之前讨论过的 Agent 资产形态，我建议这样定位：

| 资产类型 | 解决的问题 | 核心交付内容 | 主要消费方式 |
|---|---|---|---|
| Model | 智能从哪里来 | 模型权重或推理服务 | 推理 API / SDK |
| MCP Server | Agent 能调用什么工具 | 工具服务及协议接口 | MCP Client |
| Skill | Agent 如何完成特定任务 | 指令、流程、脚本、资源 | Agent 按需加载 |
| Agent | 谁来自主完成任务 | 模型、工具、记忆、工作流及配置 | API / A2A / 工作台 / SDK |
| Plugin | 如何组合并分发扩展能力 | Skills、MCP 配置及其他扩展 | 插件市场 / Agent 宿主 |

它们之间可以形成下面的关系：

```text
                    用户
                     │
                     ▼
                 Agent
                     │
       ┌─────────────┼──────────────┐
       │             │              │
       ▼             ▼              ▼
     Models        Skills         Memory
       │             │
       │      定义任务执行过程
       │             │
       │       ┌─────┼──────┐
       │       ▼     ▼      ▼
       │     MCP   Scripts  Knowledge
       │       │     │
       │       ▼     ▼
       │      API / CLI
       │
       ▼
    模型推理
```

这里有两个重要的判断。

**第一，Skill 与 MCP 不应该相互替代。**

MCP 偏向工具接口标准化，Skill 偏向任务执行方法标准化。

例如，查询云服务器状态是 MCP 工具能力；根据实例指标完成故障诊断，则更适合通过 Skill 来封装。

**第二，Skill 不应该直接等同于 Agent。**

Agent 具有任务理解、决策、工具调用和执行控制等能力。

Skill 则是一种被 Agent 使用的能力资源。

一个 Agent 可以同时使用多个 Skills，一个 Skill 也可以被多个 Agent 复用。

---

## 八、对华为云 AI 资产平台的建设建议

如果要把 Skills 正式作为 AI 资产平台的一等资产，我建议构建一条完整的生命周期管理链路：

**生产 → 导入 → 检测 → 托管 → 分发 → 安装 → 使用 → 反馈**

可以分成以下五个能力模块。

| 能力模块 | 需要构建的能力 | 建设优先级 |
|---|---|---|
| Skill 资产接入 | GitHub 导入、ZIP 上传、Skill 规范校验 | P0 |
| Skill 资产管理 | 元数据、版本、文件预览、依赖声明、许可证、安全扫描 | P0 |
| Skill 资产分发 | 下载、CLI 安装、安装指引、仓库地址 | P0 |
| Skill 资产生产 | AI Skill Creator、从 MCP/API/文档生成 Skill | P1 |
| Skill 资产运行 | 在线调试、Agent 集成、运行环境管理、评测 | P1 |

优先级是针对资产平台建设的建议，不代表所有企业的实施顺序都必须如此。

### 8.1 建议优先打通三个核心链路

**链路一：Skill 资产托管与分发**

```text
GitHub / ZIP / Skill Creator
             │
             ▼
        AI 资产平台
             │
      校验、审核、托管
             │
             ▼
       Skill 资产详情页
             │
       ┌─────┼──────┐
       ▼     ▼      ▼
      下载  CLI安装  Git地址
             │
             ▼
       Codex / Claude Code
```

这是最容易形成初步闭环的能力。

**链路二：Skill 生产与发布**

```text
用户自然语言描述
         │
         ▼
    AI Skill Creator
         │
         ▼
    生成 Skill 目录
         │
         ▼
      测试与评测
         │
         ▼
    发布到资产平台
```

这里可以与已有的 AgentArts、OpenJiuwen 等平台协同，避免重复建设底层执行工具。

**链路三：Skill + MCP 组合资产**

```text
        已有 MCP Server
               │
               ▼
       AI 辅助生成 Skill
               │
               ▼
       Skill + MCP 依赖描述
               │
               ▼
         组合资产包
               │
               ▼
           安装使用
```

这一链路尤其有价值，因为它可以把已有的工具资产进一步封装成面向业务任务的能力资产。

不过组合资产需要额外管理 MCP 端点、鉴权、网络访问和权限。不能简单地认为打包一个 Skill 就可以自动部署 MCP Server。

### 8.2 资产管理需要补充的重要元数据

Agent Skills 开放标准解决了基本文件格式和加载问题，但它并没有完整定义企业资产平台所需的治理元数据。

因此建议平台在不修改原始 Skill 标准的前提下，增加独立的资产元数据层。

| 元数据 | 作用 |
|---|---|
| Skill ID | 平台资产唯一标识 |
| Version | 版本管理 |
| Provider | 发布者 |
| Source | Git 仓库或上传来源 |
| License | 使用和分发许可证 |
| Runtime | 依赖 Python、Node.js、Shell 等环境 |
| Tool Dependencies | 依赖 MCP、CLI、API 等 |
| Compatible Agents | 已验证的兼容 Agent |
| Security Status | 安全检测结果 |
| Evaluation Result | 技能质量与效果评测结果 |

其中 `Runtime`、`Tool Dependencies`、`Compatible Agents` 尤其重要。

因为 Skill 虽然具备跨 Agent 的开放文件格式，但实际能否运行，仍然取决于宿主 Agent 的执行能力和环境。

---

## 九、最终总结：Skills 的生产、安装、使用

可以用下面这张表直接作为调研报告的总结。

| 维度 | 总结 |
|---|---|
| **资产定义** | 面向 Agent 的可复用任务能力包 |
| **资产格式** | 以 SKILL.md 为核心的目录结构，可包含 Scripts、References、Assets |
| **核心标准** | Agent Skills 开放规范 |
| **资产类型** | Prompt 型、Knowledge 型、Script 型、Tool/MCP 型、Composite 型（建议分类） |
| **生产方式** | 人工编写、AI 生成、现有工具封装、公共 Skill 二次开发 |
| **生产工具** | Skill Creator、IDE、AI 编码工具 |
| **分发形态** | Git 目录、ZIP、Skill Marketplace、Plugin、平台托管资产 |
| **分发平台** | GitHub、Skills.sh、OpenAI Plugin Directory 等 |
| **安装方式** | 本地复制、CLI 安装、Agent 内安装、插件市场安装、API 上传 |
| **调用方式** | Agent 自动匹配、用户显式调用 |
| **执行机制** | 宿主 Agent 加载 Skill 指令，按需使用知识、脚本和外部工具 |
| **执行环境** | 通常依赖宿主 Agent 的工具执行或沙箱环境 |
| **与 MCP 的关系** | Skill 定义流程，MCP 提供工具能力，二者可以组合 |
| **与 Agent 的关系** | Skill 是 Agent 可复用的能力资源，通常不是独立 Agent |
| **资产平台价值** | 标准化沉淀专业能力，并支持跨 Agent 发现、安装、复用和治理 |

### 对 AI 资产平台最重要的三个结论

**1. Skill 已经具备相对成熟的开放资产格式。**

可以优先兼容 Agent Skills 标准，避免重新定义一套独立的 Skill 文件协议。

**2. Skill 的资产交付与执行应该解耦。**

资产平台主要承担 Skill 的生产、管理、托管、检索和分发；Codex、Claude Code、AgentArts 或其他兼容的 Agent 运行环境负责实际执行。

如果资产平台希望提供在线试用，再建设配套的沙箱和 Agent 执行能力。

**3. Skill 是连接 MCP 工具资产与 Agent 应用资产的重要中间层。**

它将底层工具和知识组织成面向任务的能力，能够提高已有 AI 资产的复用价值。

从资产体系上，我建议华为云 AI 资产平台形成：

**Model → Tool/MCP → Skill → Agent → Application**

这是一条表达能力封装层次的逻辑链路，并不意味着所有 Agent 都必须依次依赖这些资产。

其中，**Skill 值得成为与 Model、MCP、Agent 并列管理的一等资产类型，同时支持作为 Plugin 或 Agent Package 的组成部分交付。**