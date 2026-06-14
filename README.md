<div align="center">

**中文** · [English](./README.en.md)

# Baku Skills

#### 我自己在真实工作流里跑过、觉得值得留下的 Agent Skills

[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-4-10B981?style=for-the-badge)](#skills)
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
| [**baku-coding-discipline（编码纪律）**](#baku-coding-discipline编码纪律) | 写代码、修 bug、重构、审查时先收束目标和验证标准，避免 AI 乱猜和过度设计 | [SKILL.md](./baku-coding-discipline/SKILL.md) |
| [**baku-design-system（Baku 设计系统）**](#baku-design-systembaku-设计系统) | 用 Baku 的品牌 DNA 构建 HTML 页面、图文卡片和个人虚拟形象 | [SKILL.md](./baku-design-system/SKILL.md) |
| [**baku-illustrations（Baku 正文配图）**](#baku-illustrationsbaku-正文配图) | 为中文文章生成 Baku 个人风格的正文配图和 shot list | [SKILL.md](./baku-illustrations/SKILL.md) |
| [**codex-history-recovery（Codex 历史恢复）**](#codex-history-recoverycodex-历史恢复) | 切换账号、API 或 provider 后，检查和恢复 Codex Desktop 本地历史可见性 | [SKILL.md](./codex-history-recovery/SKILL.md) |

---

## 安装方式

对外安装方式使用 [skills.sh](https://www.skills.sh/) 的命令形态：

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-coding-discipline
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-design-system
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-illustrations
npx skills add https://github.com/Basic-XYZ/baku-skills --skill codex-history-recovery
```

把 `--skill` 换成要装的目录名，比如 `baku-design-system` 或 `baku-coding-discipline`。安装器应该只安装包含 `SKILL.md` 的那个 skill 目录，不要把整个仓库当成一个 skill。

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
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-design-system
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-illustrations
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-coding-discipline --project --copy
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-coding-discipline --agent claude-code --global --copy
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-coding-discipline --dest /path/to/skills --copy
```

---

## Skills

<a id="skills"></a>

<table>
<tr><td>

### baku-coding-discipline（编码纪律）

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

→ [SKILL.md](./baku-coding-discipline/SKILL.md) · [模式路由](./baku-coding-discipline/references/mode-routing.md) · [成熟度清单](./baku-coding-discipline/references/maturity-checklist.md)

</td></tr>
</table>

<table>
<tr><td>

### baku-design-system（Baku 设计系统）

> *"把颜色、字体、页面模板和虚拟形象收束成同一个人的视觉语言。"*

这个 skill 是 Baku/Basic-XYZ 的个人品牌设计系统。它复刻了 `esther-design-system` 的工作方式：先读品牌 DNA，再按场景选择教程页、landing、App 工具或图文卡片模板，最后用 checklist 验收；但默认颜色、字体、气质关键词和头像都换成 Baku 自己的方向。

**它会做什么**

- 用 `brand-dna.md` 统一颜色、字体、气质关键词、禁忌和头像规则
- 从 HTML 模板开始生成教程页、landing page、App 型工具界面和图文卡片
- 通过场景参考文件约束布局、组件和自检标准
- 使用 `assets/avatar.jpg` 作为兼容默认头像，并从 `assets/avatars/` 多头像库里按场景选择合适的个人 IP 形象

**如果你要 fork 成自己的设计系统**

这个 skill 可以作为个人品牌设计系统的骨架复用，但不要只改仓库名。真正需要替换的是“这个人是谁”和“他的页面长什么样”。

必须调整：

- `baku-design-system/brand-dna.md`：改成你的品牌名、颜色、字体、气质关键词、页面禁忌和头像使用规则。
- `baku-design-system/assets/avatar.jpg`：换成你的兼容默认头像，文件名保持不变，避免旧模板引用失效。
- `baku-design-system/assets/avatars/`：放入你的多张个人 IP 头像，用统一命名规则区分风格和场景。
- `baku-design-system/references/virtual-avatar.md`：把人物设定、穿着、发型、表情、插画风格和负面约束改成你自己的版本。
- `baku-design-system/SKILL.md`：把 `Baku`、`Basic-XYZ`、触发描述和风格速查里的个人品牌语境换成你的名字。

建议调整：

- `baku-design-system/references/style-*.md`：保留你真正喜欢的风格，删掉或改掉不属于你的风格。
- `baku-design-system/assets/template-*.html`：替换模板里的品牌名、示例文案、默认 CTA、页脚和头像出现位置。
- `baku-design-system/agents/openai.yaml`：改 `display_name`、`short_description` 和 `default_prompt`，让 Agent 面板里显示你的 skill 名字。
- 仓库级 `README.md` / `README.en.md` / `skills.sh.json`：如果你要公开发布，把安装命令、skill 名、简介和 GitHub 地址换成你自己的。

可以不改：

- `references/scene-*.md`、`references/layouts.md`、`references/components.md`、`references/checklist.md` 的基础结构。它们是页面生成流程，不是 Baku 专属资产；只有当你的页面类型不同，才需要再扩展。

**怎么触发**

```text
用 Baku 的视觉风格做一个 landing page
把这篇文章转成图文卡片
设计一下我的个人虚拟形象
调整 baku-design-system 的 brand-dna.md
```

→ [SKILL.md](./baku-design-system/SKILL.md) · [Brand DNA](./baku-design-system/brand-dna.md) · [头像库](./baku-design-system/assets/avatars)

</td></tr>
</table>

<table>
<tr><td>

### baku-illustrations（Baku 正文配图）

> *"把文章里的判断、流程和证据链，画成像 Baku 工作台上长出来的正文配图。"*

这个 skill 面向中文文章、博客、知识库、教程和复盘的正文配图。它借鉴 `ian-xiaohei-illustrations` 的结构，但 Baku 版本把角色、颜色、线条质感、prompt 模板和 QA 标准全部换成了自己的个人风格。

**它会做什么**

- 先读文章，找出真正值得配图的认知锚点，而不是平均配图
- 输出 1-9 张 shot list，说明放置位置、核心意思、构图类型和中文标注
- 生成 16:9 横版暖纸手绘正文配图
- 使用 Baku 个人 IP 参与核心动作，表达证据链、流程、系统局部、前后对比和方法分层
- 用 `personal-style-skill-guide.md` 说明别人如何把它复刻成自己的个人风格插图 skill

**怎么触发**

```text
用 Baku 风格给这篇文章出一组配图建议
帮我生成 3 张正文配图
把这段工程复盘画成 Baku 工作台风格插图
我也想做自己的插图 skill，参考 baku-illustrations 怎么改
```

→ [SKILL.md](./baku-illustrations/SKILL.md) · [风格 DNA](./baku-illustrations/references/style-dna.md) · [复刻指南](./baku-illustrations/references/personal-style-skill-guide.md)

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
├── baku-coding-discipline/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── baku-design-system/
│   ├── SKILL.md
│   ├── brand-dna.md
│   ├── agents/
│   ├── assets/
│   └── references/
├── baku-illustrations/
│   ├── SKILL.md
│   ├── README.md
│   ├── agents/
│   ├── assets/
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

新增 skill 时，优先保持这个结构。新增目录和 frontmatter `name` 默认使用 `baku-` 前缀；`codex-history-recovery` 是早期例外，保持原名不改。不要把多个 skill 混在一个目录里，也不要把整个仓库包装成一个 skill。

---

## 关于

这个仓库是我的个人 skill 仓库。标准很简单：本地真实用过，能节省重复劳动，或者能明显减少 Agent 做错事的概率，才放进来。

如果要发布到 GitHub，建议保持每个 skill 的 `SKILL.md` 可独立阅读，根 README 只负责索引、安装和说明边界。

---

<div align="center">

[MIT License](./LICENSE) · 自由使用 / 修改 / 再分发

</div>
