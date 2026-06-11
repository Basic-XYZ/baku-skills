# boss-job-hunter

一个面向 BOSS 求职的 Codex skill 方案：用户主动触发搜索后，agent 基于简历、求职要求和用户同意持久化的候选人画像，搜索 BOSS 职位、筛选、排序，并给出简历优化建议、面试准备和后续成长记忆。

## 范围

- 主入口：`SKILL.md`
- 产品说明：`references/product-brief.md`
- 终极目标和路线图：`references/north-star-and-roadmap.md`
- 搜索会话协议：`references/search-session-protocol.md`
- JD 匹配门槛：`references/jd-match-gate.md`
- 推荐前确认检查：`references/pre-recommendation-check.md`
- 浏览器和 BOSS 边界：`references/search-and-browser-boundaries.md`
- 评分规则：`references/scoring-rubric.md`
- 现实匹配策略：`references/realistic-fit-policy.md`
- 评分样例：`references/scoring-examples.md`
- 公司和岗位风险分类：`references/company-and-role-risk-taxonomy.md`
- 状态和记忆模型：`references/state-and-memory-model.md`
- 简历定制策略：`references/resume-tailoring-policy.md`
- 输出模板：`references/output-format.md`
- 示例：`examples/`

## 边界

第一版只做用户主动触发的阅读、筛选、分析、建议和记忆更新提议；不定期搜索、不后台监控、不自动投递、不自动沟通 HR、不绕过登录或验证码。
