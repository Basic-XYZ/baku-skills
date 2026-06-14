<div align="center">

[中文](./README.md) · **English**

# Baku Skills

#### Personal Agent Skills extracted from real workflows

[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-4-10B981?style=for-the-badge)](#skills)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)

</div>

This repository follows a flat skill layout similar to `khazix-skills`: each skill lives in a top-level directory and owns its `SKILL.md`, `references/`, `scripts/`, or `examples/`.

## Skills

| Name | Summary |
|---|---|
| [**baku-coding-discipline**](./baku-coding-discipline/SKILL.md) | Engineering discipline for coding, debugging, refactoring, review, and AI-generated code |
| [**baku-design-system**](./baku-design-system/SKILL.md) | Build Baku-branded HTML pages, social cards, and a personal virtual avatar |
| [**baku-illustrations**](./baku-illustrations/SKILL.md) | Generate Baku-style Chinese article illustrations and shot lists |
| [**codex-history-recovery**](./codex-history-recovery/SKILL.md) | Recover Codex Desktop local history visibility after account, API, provider, or model switches |

## Install

Use the [skills.sh](https://www.skills.sh/) command shape:

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-coding-discipline
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-design-system
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-illustrations
```

Ask an agent that supports `SKILL.md` to install a skill directory:

```text
Install this skill: https://github.com/Basic-XYZ/baku-skills/tree/main/baku-coding-discipline
```

## Layout

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

For new skills, keep one top-level directory per skill and use the `baku-` prefix for both the directory and frontmatter `name`. `codex-history-recovery` is an early exception and keeps its existing name.
