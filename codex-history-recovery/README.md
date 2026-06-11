# Codex History Recovery

用于恢复 Codex Desktop 本地历史记录可见性问题。典型场景是切换 ChatGPT 账号、API Key、自定义 provider、model provider 或 model 后，旧对话在本地仍然存在，但侧边栏不显示。

## 范围

- 主入口：`SKILL.md`
- 修复脚本：`scripts/codex_history_repair.py`
- OpenAI skill 元信息：`agents/openai.yaml`

## 能做什么

- 检查 `~/.codex/state_5.sqlite` 和 rollout JSONL 的 provider / model 元数据是否不一致。
- dry-run 同步 SQLite 和 JSONL 元数据。
- apply 前自动创建备份。
- 修复 provider / model 同步后旧线程时间显示异常的问题。
- 预览和删除归档历史记录，只处理 archived 记录和归档文件。
- 从自动备份中 dry-run / apply 恢复。

## 边界

- 不打印密钥、token、`.env` 或对话正文。
- 不默认修改历史记录的 `cwd`。
- 不手工编辑 SQLite 或删除 rollout 文件，优先使用脚本。
- 删除归档历史前必须先 dry-run。
- 写入前优先让用户完全退出 Codex Desktop；无法退出时必须说明 `--allow-running` 风险。

## 快速检查

把 `<skill-dir>` 替换成实际安装目录：

```bash
python3 <skill-dir>/scripts/codex_history_repair.py --json status
```

常见安装目录：

- `~/.agents/skills/codex-history-recovery`
- `~/.codex/skills/codex-history-recovery`
- 项目内 `.agents/skills/codex-history-recovery`
