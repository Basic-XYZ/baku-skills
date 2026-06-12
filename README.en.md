<div align="center">

[中文](./README.md) · **English**

# Baku Skills

#### Personal Agent Skills extracted from real workflows

[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-3-10B981?style=for-the-badge)](#skills)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)

</div>

This repository follows a flat skill layout similar to `khazix-skills`: each skill lives in a top-level directory and owns its `SKILL.md`, `references/`, `scripts/`, or `examples/`.

## Skills

| Name | Summary |
|---|---|
| [**coding-discipline**](./coding-discipline/SKILL.md) | Engineering discipline for coding, debugging, refactoring, review, and AI-generated code |
| [**boss-job-hunter**](./boss-job-hunter/SKILL.md) | Find, screen, rank, and prepare for BOSS Zhipin jobs from a resume and job preferences |
| [**codex-history-recovery**](./codex-history-recovery/SKILL.md) | Recover Codex Desktop local history visibility after account, API, provider, or model switches |

## Install

Use the [skills.sh](https://www.skills.sh/) command shape:

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline
```

Ask an agent that supports `SKILL.md` to install a skill directory:

```text
Install this skill: https://github.com/Basic-XYZ/baku-skills/tree/main/coding-discipline
```

Options:

- default: install globally to `~/.agents/skills`
- `--project`: install to `./.agents/skills` from the current working directory
- `--copy`: copy the skill directory
- `--symlink`: symlink a local skill directory
- `--agent claude-code`: use Claude Code's skill directory shape
- `--dest <path>`: override the install root
- `--force`: replace an existing install

Examples:

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill boss-job-hunter
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline --project --copy
npx skills add /path/to/baku-skills --skill boss-job-hunter --project --symlink
npx skills add https://github.com/Basic-XYZ/baku-skills --skill coding-discipline --agent claude-code --global --copy
```

## Layout

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
