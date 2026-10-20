# SkillHub：聚焦 Skill 的供给、分发与安装

日期：2026-10-19。只读调研腾讯官方材料；未运行安装器、CLI 或任何 Skill，未登录、发布或创建线上会话。CLI 结论来自官网安装器直接引用的分发包源码，包内版本为 **2026.8.5**；结论不能自动推广到未来版本。

## 单页可直接使用的句子

- **供给：全球开源同步补规模，个人/团队上传与 GitHub 导入补本土供给，企业认证发布补垂直专业能力。** “来源”说明资产从哪里来，不等于由谁原创，也不代表安装落点。[官方 README](https://github.com/Tencent/skillhub/blob/main/README.md)、[官网发布教程](https://skillhub.cn/tutorials#publish-via-cli)
- **发布：网页上传文件夹/ZIP，或 CLI/Agent 提交本地包；发布成功先进入待审，上架后才可公开消费。** 作者在 SkillHub 主动发布后，官网提示该 Skill 不再继续从其他平台同步。[官方发布指引](https://skillhub.cn/ai/release.md)、[官网教程](https://skillhub.cn/tutorials#publish-via-cli)
- **分发：SkillHub 提供版本化文件与托管 ZIP，供网页、CLI、Open API 和宿主插件取用；同步来源与下载来源是两件事。** 下载 API 可指定 version/tag，并重定向至对象存储；无需把每次安装理解为直接访问上游 ClawHub。[下载接口](https://github.com/Tencent/skillhub/blob/main/docs/api/skills.md#下载-skill)
- **安装：把 Skill 文件落到宿主可发现的目录。** CLI 默认 `./skills`，DSH 插件默认 `~/.dsh/skills`；安装落盘不代表依赖、凭据和宿主调用条件已准备好。[官方 CLI 分发包](https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/latest.tar.gz)、[DSH 配置源码](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/src/config-store.ts)
- **消费：安装后由 Agent 按触发条件加载指令，再执行其中定义的任务。** DSH 的 Skill 安装器只解包写文件，不执行 Skill 脚本、不自动安装 Python/Node 依赖；DSH 插件市场另走可构建的程序安装流程，需分开说明。[Skill 安装源码](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/src/install.ts)、[插件说明](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/README.md)

建议示例（**仅展示，本次未执行**）：

```bash
skillhub install find-skill-skillhub --dir ./skills
```

该命令的 `install`、slug 及 `--dir` 均可在当前官方 CLI 的 `build_parser` / `cmd_install` 中核实。最终会进入当前工作目录的 `skills/find-skill-skillhub`；仍需确保对应 Agent 会发现此目录。不要在此例添加 `install --version`。[官网 CLI 分发入口](https://skillhub.cn/install/install.sh)、[源码快照](sources/v1/cli-skills_store_cli.py)

## 1. 把四类动作分开

| 动作 | 核心问题 | 平台可核实行为 |
|---|---|---|
| 来源/供给 | 包来自哪里、作者是谁 | 全球 Skills 同步；本土创作者上传；企业发布；GitHub 导入与原作者认领 |
| 发布 | 如何成为可被消费的版本 | 本地包经网页/CLI/Agent 提交，元信息与文件校验，进入审核，审核通过上架 |
| 分发 | 消费者从哪里获取内容 | 列表/搜索/详情/版本/文件 API，下载 ZIP，经平台对象存储交付；宿主插件可内嵌 |
| 安装 | 获取后写到哪里、如何可发现 | CLI 指定根目录及锁文件；DSH 插件写宿主 skills 目录；可见目录决定宿主是否发现 |

官方 README 明确“全球同步与本土共建”，包括 ClawHub 等来源；API 明确存在文件、版本、下载与质量接口。这支持“平台供给与分发枢纽”的定位，但不支持声称每个同步 Skill 均由腾讯原创、每个企业标签均是原创，或每次下载均从上游实时拉取。[README](https://github.com/Tencent/skillhub/blob/main/README.md)、[API 总览](https://github.com/Tencent/skillhub/blob/main/docs/api/README.md)

### 上游同步、GitHub 导入与主动发布

- **同步资产**：官网详情为 ClawHub 来源显示来源链接；公开详情还可能包含 `sourceUrl` 等来源元数据。它与下载时的 SkillHub 平台 URL 不同。[官网详情入口](https://skillhub.cn/skills)、[前端来源与发布摘录](sources/v1/website-distribution-excerpts.txt)
- **GitHub 导入**：当前官网发布前端提供本地上传/从 GitHub 导入两种入口；GitHub 导入要求绑定 GitHub 账号，再扫描公开仓库内的 `SKILL.md`，预备导入包后继续填写发布。这是创作者把内容纳入发布管理的路径，不等于平台对全网仓库的自动同步。[官网](https://skillhub.cn)、[生产前端](https://cloudcache.tencent-cloud.com/qcloud/tea/app/skillhub/assets/skill-hub.cpdwg332.js?max_age=31536000)
- **主动发布后维护权变化**：官网 Slug 可用提示明确作者发布后不再从其他平台继续同步此 Skill。不能把“已认领/主动发布”仍当成永久跟随上游更新的镜像。该行为来自前端提示，未发起真实发布验证。[摘录](sources/v1/website-distribution-excerpts.txt)
- **发布与消费状态**：官方教程示例成功返回 `status=pending_review`；因此“发布请求成功”与“公开上架可发现”不是同一时刻。CLI 可先 `--dry-run` 做本地元数据和打包预检；正式发布还需要登录和审核。[发布教程](https://skillhub.cn/tutorials#publish-via-cli)、[官方 Agent 发布指引](https://skillhub.cn/ai/release.md)

## 2. SkillHub 托管 ZIP 与分发渠道

官方下载契约为 `GET /api/v1/download?slug=...`，支持 `version`、`tag`；都不传则最新，二者都传以 version 为准。返回 302 跳到对象存储，临时地址不应作为永久地址转发。文件接口提供版本文件及 SHA-256，可另行校验。[下载与版本规则](https://github.com/Tencent/skillhub/blob/main/docs/api/skills.md#下载-skill)

这说明 SkillHub 提供了可交付的版本文件包与分发地址；上游仓库/ClawHub 是内容来源和可追溯入口。公开材料没有给出所有同步资源从上游到对象存储的服务端管线，因此不进一步断言后台缓存周期、同步实时性或与上游字节永久一致。

| 渠道 | 消费动作 | 安装是否同义 |
|---|---|---|
| 网页 | 发现、看描述/代码/版本/安全报告、复制安装方式、下载 | 浏览/下载本身不等于宿主已加载 |
| CLI | 搜索、下载解包、记录本地安装、发布、验签、更新 | 安装路径由 `--dir` 决定 |
| Open API | 在 Agent、IDE、企业门户或自有技能广场内嵌检索与下载 | API 返回文件，接入方完成落盘与宿主适配 |
| DSH 插件 | 对话搜索、卡片查看、安装/列出/卸载 Skill | 使用插件配置中的 skillsDir |

来源：[官方 Open API 定位](https://github.com/Tencent/skillhub/blob/main/docs/README.md)、[DSH 插件文档](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/README.md)。

## 3. CLI：精确行为与版本边界

取证路径为官网 `install/install.sh` → 腾讯对象存储 `install/latest.tar.gz` → 内含 `cli/skills_store_cli.py`、`skills_upgrade.py`、`version.json`。只在内存中读取归档并保存文本，未执行。`version.json` 为 2026.8.5；存档及获取方式见 [provenance.json](sources/v1/provenance.json)。滚动 latest URL 将来可能变化。

### 命令、落点与记录

| 项目 | 当前源码结论 |
|---|---|
| 基础安装 | `skillhub install <slug> --dir ./skills`；默认根目录是当前目录下 `./skills` |
| 已有目录 | 通常拒绝覆盖，提示 `--force`；同名来源冲突存在特殊自动覆盖分支，不宜概括为永不覆盖 |
| 本地记录 | 根目录下 `.skills_store_lock.json`；常规项含 name、zip_url、source、version、installedAt；命名空间项还含 installDir / namespace / internalSlug 等 |
| 本地枚举 | `skillhub list --dir ...` 读锁文件；与 DSH 读目录的行为不同 |
| 更新 | 命令名为 `upgrade`，可指定单个 slug 或全部锁定项；可 `--check-only` |
| 更新来源 | 从已装 Skill 的 `config.json` 读取 update/manifest URL，取新版本 ZIP；缺配置或更新 URL 会跳过，并非每次自动拿平台 latest |
| 卸载 | 当前命令解析器没有 `uninstall` 或 `remove` 子命令，不能在单页写“CLI 支持一键卸载” |
| 脚本/依赖 | 安装函数只下载、解压、搬移文件、写锁；未调用包内 setup/install 脚本，未遍历 requirements/package.json 自动装依赖 |

来源：[CLI 源码快照](sources/v1/cli-skills_store_cli.py)、[更新源码快照](sources/v1/cli-skills_upgrade.py)、[官方可获取分发包](https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/latest.tar.gz)。源码中的启动自更新机制针对 CLI 自身，不等于 Skill 包的依赖安装。

### `--version` 与指定 Skill 版本

**install 子命令没有 `--version`。** 顶层 `skillhub --version` 只显示 CLI 版本；`verify --version` 和 `publish --version` 各有自己的含义，不能移用到 install。

`parse_skill_ref` 接受 `@namespace/slug@version`。社区命名空间安装分支会向下载 API 传 version；企业分支也把 version 传入组织下载。**裸 `slug@version` 虽能被解析，但本版本普通安装分支未把解析出的 version 注入下载 URL，因此不建议在单页用它展示固定版本。** 此项是阅读调用链的结论，未实际安装验证。[CLI 快照，`parse_skill_ref`、`cmd_install`、`_install_community_resolved_skill`、`_install_enterprise_skill`](sources/v1/cli-skills_store_cli.py)

单页需要表达版本能力时，采用确定的公共契约：“**下载 API 支持按版本获取，DSH 安装工具支持传 version**”。[下载 API](https://github.com/Tencent/skillhub/blob/main/docs/api/skills.md#下载-skill)、[DSH README](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/README.md)

### 默认是否先查 registry，再回退 ClawHub？

**本次读取的当前 CLI 不存在“SkillHub 下载失败自动回退 ClawHub 原站”的普通安装链。**

普通 slug：先读取 SkillHub 索引 `skills.json`；找不到时调用 SkillHub search 做精确 slug 匹配；仍没有元数据也尝试直接用 slug 下载。最终 `install_zip_to_target_with_fallback` 虽然函数名含 fallback，但 `cmd_install` 只传一个候选 URL：默认 `https://api.skillhub.cn/api/v1/download?slug={slug}`。CLI metadata 中也保留对象存储模板，但普通安装调用并未据此增加第二个下载候选。不能根据函数名或旧配置字段推断 ClawHub 回退。[CLI 快照](sources/v1/cli-skills_store_cli.py)、[官方 metadata 快照](sources/v1/cli-metadata.json)

命名空间坐标：先尝试 SkillHub resolve；社区解析失败后可能进入企业源分支，走组织凭据及组织 registry 下载。这里的“fallback 企业源”仍不等于“回退 ClawHub”。

## 4. DSH 插件：只说明它实际实现的 Skill 安装

| 环节 | 可核实行为 |
|---|---|
| 默认目录 | `$DSH_HOME/skills`；DSH_HOME 未设置时 `~/.dsh/skills`；可配置 skillsDir |
| 版本 | `skillhub_install` 可传 version；安装器把它加入 `/download?...&version=...&source=dsh` |
| 包格式 | 检查 ZIP/octet-stream 类型或 PK 头；支持中央目录/本地文件头；拒绝截断、损坏、不支持压缩格式 |
| 路径 | 拒绝绝对路径、`..`、空段、`.` 等；去掉共同顶层包装目录 |
| 必需文件 | 归一化后必须有根级 `SKILL.md` |
| 落盘 | 写临时 staging 目录，然后删除已有目标并 rename；同 slug 安装会替换已有目录 |
| 记录 | 未写 CLI 锁文件；列出时枚举 skillsDir，读取 SKILL.md frontmatter，统计文件数/体积/mtime；版本显示来自 frontmatter/请求 |
| 脚本/依赖 | 无包内脚本执行、无 pip/npm 自动依赖安装；README 明确插件不执行 Skill 代码 |
| 完整性 | 安装器内未见 SHA-256 或数字签名校验调用；签名在详情卡片另行获取/展示。不能把“显示签名”写成“安装必经验签” |
| 卸载 | 确认目标目录有 `SKILL.md` 后删除该目录；可列出/卸载的是已落盘 Skill |
| 宿主发现 | 文档建议正确安装到 DSH skills 目录并新开对话；文件监视通常无需重启，不能把任意目录都当成可自动发现 |

来源：[install.ts](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/src/install.ts)、[unzip.ts](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/src/unzip.ts)、[config-store.ts](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/src/config-store.ts)、[api.ts](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/src/api.ts)、[DSH README](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/README.md)。

### Skill 安装与 DSH 插件安装不是同一过程

- **Skill**：下载 ZIP → 检查结构/路径 → 写 skills 目录 → 宿主发现指令文件。安装器不执行包内代码。
- **DSH 插件**：读取安装计划、校验仓库和 pinned commit，在宿主执行 `dsh plugin ... add`，可能触发 git prepare 构建和重启。README 的自动允许构建重试属于这一流程，不能泛化成“Skill 会自动运行安装脚本”。[官方插件文档](https://github.com/Tencent/skillhub/blob/main/dsh-plugin/README.md)

## 5. 单页建议关系图

```text
全球同步 ─┐
个人上传 ─┼→ 平台版本文件与审核 → 网页/CLI/API/宿主插件分发 → 解包到可发现目录 → Agent 调用
企业发布 ─┤                         （可指定下载版本）          （依赖/凭据另准备）
GitHub导入┘
```

该图是对公开产品与代码的归纳；它比把 Skill 与 SOUL/MCP 画成层级，更直接解释本页关心的 Skill 供给、交付和使用条件。
