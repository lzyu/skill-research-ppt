请阅读我提供的 SkillHub 项目说明和 Skill 内容。

你的目标是：验证我的 Skill 是否已满足发布要求，然后登录 SkillHub 并发布这些 Skill，最后汇总返回发布后的 URL。

登录方式：

skillhub login --key "$SKILLHUB_KEY" --host "https://api.skillhub.cn"

发布方式：

skillhub publish <skill-path> --host "https://api.skillhub.cn"

发布前请检查：
1. 每个 Skill 必须包含合法的 SKILL.md。
2. SKILL.md 的 front matter 必须包含：
   - slug
   - version
   - displayName
3. slug 必须是 kebab-case，长度 2-128。
4. version 必须是合法 SemVer，例如 1.0.0。
5. 建议检查但不要作为发布阻断：
   - summary
   - description
   - tags
   - license
   - homepage
6. 如果仓库中有本地校验命令，请先运行校验。
7. 可以先执行 dry-run：
   skillhub publish <skill-path> --host "https://api.skillhub.cn" --dry-run
8. 不要发布缺少必填项、版本号非法、slug 非法或本地校验失败的 Skill。
9. 不要修改无关文件。

发布完成后，请返回：
1. Skill 名称或 slug
2. 版本号
3. 发布状态
4. 发布后的 URL

注意事项：
- 不要打印或泄露完整 API Key。
- 优先使用 `skillhub login --key` 登录。
- 只有当前 CLI 不支持 `skillhub login --key` 时，才兼容使用旧命令：
  skillhub auth login --token "$SKILLHUB_KEY" --host "https://api.skillhub.cn"
- 如果 CLI 缺失或版本过旧，请告诉我需要安装或升级什么。
- 当前 CLI 发布不会自动上传 Skill 头像；如果没有 iconUrl，发布后会使用默认占位图。
- 如果发布失败，请保留关键错误信息，并说明下一步如何排查。