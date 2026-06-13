# Baku Skills 推广素材

这个文件用于真实推广，不用于刷安装量或伪造使用数据。`skills.sh` 的安装量应来自真实用户执行官方安装命令。

## 已发布

| 时间 | 渠道 | 链接 | 说明 |
|---|---|---|---|
| 2026-06-13 | GitHub Release | https://github.com/Basic-XYZ/baku-skills/releases/tag/v0.1.0 | 首个公开版本发布帖 |
| 2026-06-13 | GitHub Discussions | https://github.com/Basic-XYZ/baku-skills/discussions/1 | Show and tell 反馈征集帖 |

## 推荐入口

优先级按“最可能带来真实 Agent Skill 用户”排序：

| 渠道 | 链接 | 建议动作 |
|---|---|---|
| skills.sh | https://skills.sh/Basic-XYZ/baku-skills | README 放 badge，持续让真实用户用 `npx skills add` 安装 |
| VoltAgent awesome-agent-skills | https://github.com/VoltAgent/awesome-agent-skills | 等仓库有基础 star / 使用反馈后提交 PR |
| awesome-claude-skills | https://github.com/travisvn/awesome-claude-skills | 面向 Claude Code 用户投稿，注意它通常更看重 social proof |
| Awesome Claude | https://awesomeclaude.ai/ | 适合做 Claude 生态曝光，先准备英文一句话介绍 |
| OpenAI Community | https://community.openai.com/ | 发 Codex Skills 使用经验帖 |
| Reddit r/ClaudeAI | https://www.reddit.com/r/ClaudeAI/ | 发 Claude Code / skills 经验帖 |
| Reddit r/OpenAI | https://www.reddit.com/r/OpenAI/ | 发 Codex / Agent Skills 经验帖 |
| Reddit r/SideProject | https://www.reddit.com/r/SideProject/ | 用开源小工具角度发布 |
| DEV Community | https://dev.to/ | 写一篇短文，讲为什么需要 coding-discipline |
| Hacker News Show HN | https://news.ycombinator.com/show | 等 README / 英文介绍更完整后发布 |

## 一句话介绍

中文：

> Baku Skills 是我在真实工作流里沉淀的中文 Agent Skills 仓库，目前包含编码纪律、BOSS 求职筛选、Codex 历史恢复，支持通过 `npx skills add` 安装到 Codex、Claude Code、Cursor 等 Agent。

English:

> Baku Skills is a Chinese-first Agent Skills repository for real workflows, currently covering coding discipline, BOSS job hunting, and Codex history recovery, installable through `npx skills add`.

## 推荐安装命令

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline
npx skills add https://github.com/Basic-XYZ/baku-skills --skill boss-job-hunter
npx skills add https://github.com/Basic-XYZ/baku-skills --skill codex-history-recovery
```

## GitHub Awesome List PR 文案

标题：

```text
Add Basic-XYZ/baku-skills
```

正文：

````markdown
This PR adds Basic-XYZ/baku-skills, a Chinese-first Agent Skills repository for practical coding and workflow automation.

Included skills:

- `coding-discipline`: keeps coding agents scoped, evidence-driven, and verification-oriented.
- `boss-job-hunter`: helps evaluate BOSS Zhipin job postings against a candidate profile and resume.
- `codex-history-recovery`: helps inspect and recover local Codex Desktop history metadata.

Install example:

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline
```
````

## 社区帖中文文案

标题：

```text
我整理了一个中文 Agent Skills 仓库，支持 Codex / Claude Code / Cursor
```

正文：

````markdown
我最近把自己真实工作流里反复用到的几个 Agent Skills 整理成了一个仓库：

https://github.com/Basic-XYZ/baku-skills

目前包含：

- `coding-discipline`：约束 AI 写代码时先明确目标、假设和验证标准，减少乱猜、过度设计和无关改动。
- `boss-job-hunter`：按简历和偏好筛选 BOSS 直聘岗位，强调 JD 证据和现实匹配。
- `codex-history-recovery`：排查和恢复 Codex Desktop 本地历史可见性。

安装示例：

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline
```

这个仓库偏中文工作流，不追求数量，只放我自己真的用过、觉得能减少返工的 skill。欢迎试用，也欢迎给 issue 反馈哪些场景触发不自然。
````

## 外部社区定制文案

### Reddit / r/claudeskills

Title:

```text
I built a Chinese-first Agent Skills repo for Codex / Claude Code workflows
```

Body:

````markdown
I published Baku Skills, a Chinese-first Agent Skills repo built from workflows I actually use with Codex and Claude Code.

Repo:
https://github.com/Basic-XYZ/baku-skills

skills.sh:
https://skills.sh/Basic-XYZ/baku-skills

Current skills:

- `coding-discipline`: keeps coding agents scoped, evidence-driven, and verification-oriented. This is the one I recommend installing first.
- `boss-job-hunter`: evaluates BOSS Zhipin job postings against a resume and preferences, using JD-first evidence instead of keyword-only matching.
- `codex-history-recovery`: helps inspect and recover local Codex Desktop history metadata after provider, model, or account changes.

Install example:

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline
```

This is not a huge skills collection. I am intentionally keeping it small and based on real usage. Feedback welcome, especially around whether the skill triggers feel natural and whether the coding workflow is too strict or useful.
````

### OpenAI Developer Community / Codex

Title:

```text
Sharing Baku Skills: Chinese-first Agent Skills for Codex workflows
```

Body:

````markdown
I published a small Chinese-first Agent Skills repository for Codex / coding-agent workflows:

https://github.com/Basic-XYZ/baku-skills

skills.sh page:

https://skills.sh/Basic-XYZ/baku-skills

The main skill is `coding-discipline`. It is meant to reduce common coding-agent failure modes: unclear scope, hidden assumptions, over-engineering, unrelated edits, and missing verification.

Install:

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline
```

The repo also includes:

- `boss-job-hunter`: BOSS Zhipin job matching from resume, preferences, and JD evidence.
- `codex-history-recovery`: local Codex Desktop history inspection and recovery after provider/model/account changes.

I am keeping the repository intentionally small and based on real workflows. Feedback is welcome, especially from Codex users who maintain project-level or global skills.
````

### V2EX / AI 或 分享创造

标题：

```text
分享一个中文 Agent Skills 仓库：约束 Codex / Claude Code 写代码别乱改
```

正文：

````markdown
最近把自己真实工作流里反复用到的几个 Agent Skills 整理成了一个公开仓库：

https://github.com/Basic-XYZ/baku-skills

skills.sh 页面：

https://skills.sh/Basic-XYZ/baku-skills

目前主要有 3 个：

- `coding-discipline`：写代码、修 bug、重构、review 时，让 Agent 先明确目标、假设、范围和验证标准，减少乱猜、过度设计、顺手乱改。
- `boss-job-hunter`：基于简历、偏好和 JD 证据筛选 BOSS 直聘岗位，不做关键词式泛泛推荐。
- `codex-history-recovery`：排查和恢复 Codex Desktop 本地历史可见性，适合切换账号、provider 或 model 后使用。

推荐先试这个：

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline
```

这个仓库不是大而全的收集站，只放我自己真实用过、觉得能减少返工的 skill。欢迎拍砖，尤其想听听大家对 `coding-discipline` 这种“先收束再编码”的流程是否觉得太重，还是确实能减少 AI 乱改。
````

### 掘金 / DEV.to

标题：

```text
我如何用 Agent Skill 约束 AI 写代码，减少乱猜和过度设计
```

正文开头：

````markdown
这段时间我在 Codex / Claude Code 里反复遇到一个问题：AI 不是不会写代码，而是太容易在目标不清楚时直接动手。

常见结果是：

- 用户只想修一个 bug，它顺手重构了一片；
- 没有验证标准，最后只能靠感觉说“应该好了”；
- 发现不确定点时不问，默默替用户做假设；
- 代码能跑，但改动范围和真实需求对不上。

所以我把自己常用的一套编码纪律整理成了一个 Agent Skill：

https://github.com/Basic-XYZ/baku-skills

安装：

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline
```

它做的事情很简单：让 Agent 在写代码前先判断任务类型、明确假设、收束范围、定义验证方式；实现时只做必要改动；结束时交代验证结果和剩余风险。
````

## X / LinkedIn 短帖

```text
I published Baku Skills, a Chinese-first Agent Skills repo for real Codex / Claude Code workflows.

Current skills:
- coding-discipline: scoped, evidence-driven coding agent workflow
- boss-job-hunter: BOSS Zhipin job matching from resume + JD evidence
- codex-history-recovery: local Codex Desktop history recovery

npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline

https://github.com/Basic-XYZ/baku-skills
https://skills.sh/Basic-XYZ/baku-skills
```

## 发布前检查

- README 第一屏能看到 `skills.sh` badge 和安装命令。
- GitHub repo topics 包含：`agent-skills`、`codex-skills`、`claude-code-skills`、`claude-code`、`cursor`、`ai-agents`、`coding-agent`、`skills-sh`。
- 每个 skill 的 `SKILL.md` 都有清晰的 `name` 和 `description`。
- 至少用官方命令验证一个远程安装路径。
- 社区投稿时说明边界，不承诺自动投递、自动登录、绕过验证码或后台监控。
