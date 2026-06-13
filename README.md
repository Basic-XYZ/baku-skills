<div align="center">

**中文** · [English](./README.en.md)

# Baku Skills

#### 我自己在真实工作流里跑过、觉得值得留下的 Agent Skills

[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-3-10B981?style=for-the-badge)](#skills)
[![skills.sh](https://skills.sh/b/Basic-XYZ/baku-skills)](https://skills.sh/Basic-XYZ/baku-skills)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)

![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square&logo=openai&logoColor=white)
![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97706?style=flat-square&logo=anthropic&logoColor=white)
![OpenCode](https://img.shields.io/badge/OpenCode-Skill-3B82F6?style=flat-square)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-8B5CF6?style=flat-square)

</div>

都是我自己做事时真的需要，整理成 `SKILL.md` 之后能反复用上的东西。这个仓库不追求数量，主要放两类 skill：一种是能直接帮我完成具体任务的，一种是能约束 Agent 工作方式、减少返工的。

这里的每个 Skill 都是 Agent 可以直接加载的结构化指令集，按 [Agent Skills](https://agentskills.io) 的目录习惯组织。Claude Code、Codex、OpenCode、OpenClaw 这类支持 `SKILL.md` 的工具都可以按目录安装。

关键词：`agent-skills`、`codex-skills`、`claude-code-skills`、`coding-agent`、`ai-agents`、`skills.sh`。

---

## 目录

| 名字 | 一句话 | 入口 |
|---|---|---|
| [**coding-discipline（编码纪律）**](#coding-discipline编码纪律) | 写代码、修 bug、重构、审查时先收束目标和验证标准，避免 AI 乱猜和过度设计 | [SKILL.md](./coding-discipline/SKILL.md) |
| [**boss-job-hunter（BOSS 求职猎手）**](#boss-job-hunterboss-求职猎手) | 从简历和偏好出发，搜索、筛选、评分 BOSS 直聘岗位，并给出简历和面试建议 | [SKILL.md](./boss-job-hunter/SKILL.md) |
| [**codex-history-recovery（Codex 历史恢复）**](#codex-history-recoverycodex-历史恢复) | 切换账号、API 或 provider 后，检查和恢复 Codex Desktop 本地历史可见性 | [SKILL.md](./codex-history-recovery/SKILL.md) |

---

## 安装方式

对外安装方式使用 [skills.sh](https://www.skills.sh/) 的命令形态：

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline
npx skills add https://github.com/Basic-XYZ/baku-skills --skill boss-job-hunter
npx skills add https://github.com/Basic-XYZ/baku-skills --skill codex-history-recovery
```

把 `--skill` 换成要装的目录名，比如 `boss-job-hunter` 或 `coding-discipline`。安装器应该只安装包含 `SKILL.md` 的那个 skill 目录，不要把整个仓库当成一个 skill。

在 Claude Code、Codex、OpenCode、OpenClaw 等支持 Skill 的 Agent 里，也可以直接说：

```text
帮我安装这个 skill：https://github.com/Basic-XYZ/baku-skills/tree/main/<skill-name>
```

**全局 skill 还是项目 skill**

- 默认安装到全局 `~/.agents/skills`，适合自己长期使用的通用 skill。
- 加 `--project` 安装到当前项目的 `.agents/skills`，适合某个仓库固定一套规则，和代码一起 review。

**复制还是软链**

- 默认复制目录，兼容性最好。
- 加 `--symlink` 软链到本地源码，适合正在开发 skill，希望改完立刻在本机验证。
- 如果 Claude Code 或其他 Agent 对软链支持不稳定，使用 `--copy`。

**兼容不同 Agent**

- 默认目标是 `.agents/skills`。
- 如果要按 Claude Code 的目录组织安装，使用 `--agent claude-code`。
- 如果你的运行时使用其他目录，使用 `--dest <path>` 精确指定。

更多例子：

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill boss-job-hunter
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline --project --copy
npx skills add /path/to/baku-skills --skill boss-job-hunter --project --symlink
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline --agent claude-code --global --copy
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline --dest /path/to/skills --copy
```

---

## Skills

<a id="skills"></a>

<table>
<tr><td>

### coding-discipline（编码纪律）

> *"先把目标、假设和验证标准讲清楚，再写最少的代码。"*

这个 skill 是写代码、修 bug、重构和 review 时的工程纪律入口。它不替项目做架构决策，也不引入框架；它约束 Agent 在动手前先理解上下文、选择最轻的执行模式，并在结束前交代验证结果。

它会优先解析相关 skill：已安装的 Matt Pocock / Karpathy 系列能力可以叠加使用；未安装但运行时支持安装时，应主动安装缺失 skill；不能安装时，则使用本 skill 内置的 TDD、诊断、重构和 review 流程继续执行。

**为什么需要它**

AI 写代码最常见的问题不是不会写，而是太容易默默假设、顺手重构、加过度抽象、改到无关文件，最后还没有一个明确的验收标准。这个 skill 把这些风险前置到流程里，让每一行改动都能追溯到用户请求或验证需要。

**它会把任务分到几类**

- Tiny Edit：错别字、明显一行配置、小文案，直接最小改动
- Feature / Behavior Change：新增行为，先定义可观察结果和验证路径
- Bug / Performance Regression：先复现和定位，再修复和补回归检查
- Refactor / Architecture Change：先确认收益、范围和回滚边界
- Review：先列风险和问题，再给摘要

**怎么触发**

```text
修这个 bug，但别越改越复杂
帮我 review 这次改动
按 TDD 加这个行为
先做一个小范围重构方案
```

**适合放在哪里**

它适合做全局 skill，因为几乎每个代码仓库都能用；也适合复制进项目 `.agents/skills`，让团队把这套工作纪律和项目代码一起维护。

→ [SKILL.md](./coding-discipline/SKILL.md) · [模式路由](./coding-discipline/references/mode-routing.md) · [成熟度清单](./coding-discipline/references/maturity-checklist.md)

</td></tr>
</table>

<table>
<tr><td>

### boss-job-hunter（BOSS 求职猎手）

> *"不是泛泛地说你适合什么岗位，而是把简历、偏好、岗位证据放到一起，排出最值得冲的目标。"*

这个 skill 面向 BOSS 直聘求职场景。用户主动触发搜索后，Agent 基于简历、求职要求和用户同意持久化的候选人画像，把信息拆成候选人画像、搜索关键词、硬性筛选条件和软性排序标准，然后基于可见岗位页面做证据化判断。

**它会做什么**

- 从简历里提取年限、技术栈、项目领域、成果证据、短板和面试卖点
- 根据城市、薪资、方向、公司规模、行业、加班和外包容忍度生成搜索策略
- 阅读可见 BOSS 岗位信息，记录 title、公司、城市、薪资、规模、行业、JD 摘要和风险点
- 按固定会话协议执行搜索，先做 JD 与候选人画像匹配，再用现实匹配、风险分类和评分样例校准每轮推荐
- 用评分规则筛掉硬伤岗位，排序真正“值得投、可能拿面试”的目标
- 给 top 岗位输出简历优化方向、面试准备重点和可沉淀的成长记忆
- 在用户同意时记录已过滤公司、偏好变化、能力短板和长期提升点

**边界很重要**

它不定期搜索、不后台监控、不自动投递、不自动和 HR 沟通、不绕过登录、验证码或访问限制。BOSS 页面拿不到证据时，它应该停下来，让用户登录、打开页面、提供截图或粘贴 JD，而不是继续编结果。

**怎么触发**

```text
帮我根据简历找 BOSS 岗位
筛一下杭州 Java 后端岗位
哪些岗位更容易拿面试
帮我针对这个 JD 优化简历表达
```

→ [SKILL.md](./boss-job-hunter/SKILL.md) · [输出模板](./boss-job-hunter/references/output-format.md) · [评分规则](./boss-job-hunter/references/scoring-rubric.md)

</td></tr>
</table>

<table>
<tr><td>

### codex-history-recovery（Codex 历史恢复）

> *"历史不是没了，很多时候只是 provider / model 元数据不一致，侧边栏把它过滤掉了。"*

这个 skill 用来处理 Codex Desktop 本地历史记录的恢复和归档清理。它的核心判断是：`state_5.sqlite` 只是索引 / 缓存，很多线程元数据还会从 `rollout-*.jsonl` 重建，所以修复不能只改 SQLite。

**它会做什么**

- 只读检查 `~/.codex/state_5.sqlite`、active / archived rollout 文件和 provider / model 元数据
- dry-run 预览 provider / model 同步，不直接写入
- 同步 SQLite `threads` 表和 rollout JSONL 里的 `session_meta` / `turn_context`
- 修复恢复后旧线程显示成“刚刚”的时间问题
- 预览和删除 archived 历史记录，并自动创建回滚备份
- 从脚本生成的 SQLite / JSONL 备份中恢复

**边界很重要**

它不打印密钥、token、`.env` 或对话正文；不默认修改历史记录的 `cwd`；不删除 active history。涉及写入或归档删除时，必须先 dry-run，并优先让用户关闭 Codex Desktop 后再 apply。

**怎么触发**

```text
切换 API 后 Codex 历史没了
帮我看看 Codex Desktop 旧聊天还在不在
恢复一下 Codex 历史的 provider
删除归档里的 Codex 历史记录，先 dry-run
```

→ [SKILL.md](./codex-history-recovery/SKILL.md) · [README](./codex-history-recovery/README.md)

</td></tr>
</table>

---

## 仓库结构

这个仓库参考 `khazix-skills` 的 flat layout：一个 skill 一个顶层目录，根目录只放说明、许可证和安装器。

```text
baku-skills/
├── coding-discipline/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── boss-job-hunter/
│   ├── SKILL.md
│   ├── agents/
│   ├── examples/
│   └── references/
├── codex-history-recovery/
│   ├── SKILL.md
│   ├── README.md
│   ├── agents/
│   └── scripts/
├── bin/
│   └── skills.js
├── README.md
├── README.en.md
├── LICENSE
└── package.json
```

新增 skill 时，优先保持这个结构。不要把多个 skill 混在一个目录里，也不要把整个仓库包装成一个 skill。

---

## 关于

这个仓库是我的个人 skill 仓库。标准很简单：本地真实用过，能节省重复劳动，或者能明显减少 Agent 做错事的概率，才放进来。

如果要发布到 GitHub，建议保持每个 skill 的 `SKILL.md` 可独立阅读，根 README 只负责索引、安装和说明边界。

---

<div align="center">

[MIT License](./LICENSE) · 自由使用 / 修改 / 再分发

</div>
