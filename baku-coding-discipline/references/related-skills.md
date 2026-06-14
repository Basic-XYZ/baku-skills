# 相关 Skill 安装参考

这个文件只在需要安装、核对或解释相关 skill 时读取。只读 / 方案模式下不要执行安装命令，只能把命令作为建议列出。

## 相关 Skill

- `karpathy-guidelines`：编码底线纪律，覆盖先思考、简单优先、外科手术式修改和目标驱动验证。
- `tdd` 或 `mattpocock-skills:tdd`：功能和行为变更的测试驱动循环。
- `diagnose` 或 `mattpocock-skills:diagnose`：故障和性能回归的诊断循环。
- `request-refactor-plan` 或 `mattpocock-skills:request-refactor-plan`：大范围重构的计划拆分。
- `review` 或 `mattpocock-skills:review`：分支、PR、diff 和 AI 生成代码审查。

## 安装来源

- Matt Pocock skills: `https://github.com/mattpocock/skills`
- Karpathy guidelines: `https://github.com/multica-ai/andrej-karpathy-skills`

## skills.sh 风格命令

```bash
npx skills add https://github.com/mattpocock/skills --skill tdd --global --copy
npx skills add https://github.com/mattpocock/skills --skill diagnose --global --copy
npx skills add https://github.com/mattpocock/skills --skill request-refactor-plan --global --copy
npx skills add https://github.com/multica-ai/andrej-karpathy-skills --skill karpathy-guidelines --global --copy
```

## 本仓库本地安装器命令

在 `baku-skills` 仓库根目录可使用：

```bash
node ./bin/skills.js add https://github.com/mattpocock/skills --skill tdd --scope global --method copy
node ./bin/skills.js add https://github.com/mattpocock/skills --skill diagnose --scope global --method copy
node ./bin/skills.js add https://github.com/mattpocock/skills --skill request-refactor-plan --scope global --method copy
node ./bin/skills.js add https://github.com/multica-ai/andrej-karpathy-skills --skill karpathy-guidelines --scope global --method copy
```

如果所在 Agent 有原生 skill 或 plugin 安装器，优先使用原生安装器。
