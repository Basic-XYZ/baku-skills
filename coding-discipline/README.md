# 编码纪律

`coding-discipline` 是一个面向 Codex 风格 Agent 的工程纪律 skill，用来让软件改动保持小、可验证、可审查。它会在实现前把编码任务路由到最轻合适流程：微小修改、行为变更、故障诊断、重构或审查。

这个 skill 有意保持流程化。它不会往你的代码库里引入框架；它约束 Agent 如何思考、编辑、验证和汇报。

当 Matt Pocock skills 或 Karpathy 风格编码准则已经安装时，它可以叠加使用这些相关 skill。如果缺失，Agent 应该在运行时允许的情况下尝试安装准确缺失的 skill；如果无法安装，本包也已经内置核心工作流规则，可以继续执行。

它还轻量吸收了 Loom 这类 workflow harness 的 delivery guard 思想：Agent 必须跟踪当前权威来源、证据和停止条件。这个 skill 不创建状态目录，也不引入独立协议运行时；这些护栏保留在 Agent 的执行纪律和最终汇报里。

## 适用场景

当 Agent 被要求做这些事时使用：

- 实现功能或行为变更
- 修 bug、回归、失败测试或性能问题
- 审查分支、PR、diff 或 AI 生成补丁
- 规划或执行重构
- 先研究、只排查、先方案、不要执行的只读任务
- 降低复杂度，避免推测性过度设计

对于错别字或一行配置这类小改，skill 允许压缩流程：做最小改动，并运行最便宜的相关检查。

## 强制约束

- 编辑前明确目标、非目标、假设和成功标准。
- 用户要求只读或先方案时，禁止改代码、跑有副作用命令或顺手修复。
- 猜测前先读相关代码、测试和项目规范。
- 为任务选择一个主模式。
- 先解析相关 skill：已安装就使用，安全且支持安装时就安装，否则回退到内置规则。
- 优先用满足可观察行为的最小实现。
- 每一行改动都能追溯到用户请求或验证需要。
- 用最快的相关测试、类型检查、lint、fixture 或手动检查验证。
- 当当前模式已经有明确可运行的下一步时，不停在进度总结。
- 清楚汇报改动、涉及文件和验证结果。

## 安装

推荐的 Codex 全局安装方式：

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline --global --copy
```

上面的命令使用 [skills.sh](https://www.skills.sh/) 的安装方式，会把 skill 安装到 `~/.agents/skills/coding-discipline`。

### 全局 Skill 还是项目 Skill

如果你希望所有仓库都使用同一套工程纪律，使用全局 skill。这是个人编码工作流的推荐默认值。

如果某个仓库或团队希望固定准确版本，并让规则和代码一起 review，就使用项目 skill。此时按你的 Agent 运行时规则，把 skill 安装或复制到项目内的 skill 目录。

项目内 Codex 安装：

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline --project --copy
```

这会安装到当前工作目录的 `./.agents/skills/coding-discipline`。

如果要按 Claude Code 的目录组织安装：

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline --agent claude-code --global --copy
```

### 安装位置

如果运行时允许选择目标目录，安装到下面其中一个位置：

- `~/.agents/skills/coding-discipline`：供读取 `.agents/skills` 的 Agent 使用。
- `~/.codex/skills/coding-discipline`：供读取 `.codex/skills` 的 Codex 配置使用。
- 项目内 skill 目录：当规则需要跟随某个仓库一起维护时使用。

如果你的 Claude Code 环境不支持 installer 命令或这个 skill 格式，可以手动复制：

```bash
mkdir -p ~/.agents/skills
cp -R /path/to/coding-discipline ~/.agents/skills/coding-discipline
```

也可以保留一个源码 checkout，然后软链过去：

```bash
mkdir -p ~/.agents/skills
ln -s /path/to/coding-discipline ~/.agents/skills/coding-discipline
```

安装新 skill 后，重启 Codex，让下一次会话能发现它。

## 仓库结构

```text
.
├── SKILL.md
├── references/
│   ├── maturity-checklist.md
│   ├── related-skills.md
│   └── mode-routing.md
└── scripts/
    └── validate.py
```

`SKILL.md` 是入口。`references/` 放更长的路由规则和成熟度门禁，Agent 只有在任务需要时再加载。

## 校验

运行轻量仓库检查：

```bash
python3 scripts/validate.py
```

脚本会检查必需文件、skill frontmatter、本地 Markdown 链接、关键协议段落和明显的疑似密钥。

## 设计说明

这个 skill 刻意保守：

- 偏向小 diff，而不是大范围改写。
- 把测试和反馈循环当成实现的一部分，而不是收尾清理。
- 只有当前代码库真的能受益时才添加抽象。
- 成功标准薄弱或含糊时，先澄清。

## 许可证

MIT
