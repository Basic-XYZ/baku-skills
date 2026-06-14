<div align="center">

[中文](./README.md) · **English**

# Baku Skills

#### Personal Agent Skills extracted from real workflows

[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-5-10B981?style=for-the-badge)](#skills)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)

</div>

This repository follows a flat skill layout similar to `khazix-skills`: each skill lives in a top-level directory and owns its `SKILL.md`, `references/`, `scripts/`, or `examples/`.

## Skills

| Name | Summary |
|---|---|
| [**baku-coding-discipline**](./baku-coding-discipline/SKILL.md) | Engineering discipline for coding, debugging, refactoring, review, and AI-generated code |
| [**baku-design-system**](./baku-design-system/SKILL.md) | Build Baku-branded HTML pages, social cards, and a personal virtual avatar |
| [**baku-illustrations**](./baku-illustrations/SKILL.md) | Generate Baku-style Chinese article illustrations and shot lists |
| [**boss-job-hunter**](./boss-job-hunter/SKILL.md) | Find, screen, rank, and prepare for BOSS Zhipin jobs from a resume and job preferences |
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
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-design-system
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-illustrations
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-coding-discipline --project --copy
npx skills add /path/to/baku-skills --skill boss-job-hunter --project --symlink
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-coding-discipline --agent claude-code --global --copy
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

For new skills, keep one top-level directory per skill and use the `baku-` prefix for both the directory and frontmatter `name`. `boss-job-hunter` and `codex-history-recovery` are early exceptions and keep their existing names.

## Forking the Baku design system

`baku-design-system` can be reused as a personal brand design-system skeleton, but do not only rename the repository. Replace the identity layer first:

- `baku-design-system/brand-dna.md`: your name, colors, typography, tone keywords, visual rules, and avatar usage rules.
- `baku-design-system/assets/avatar.jpg`: your compatibility default avatar. Keep the filename to avoid breaking older template references.
- `baku-design-system/assets/avatars/`: your multi-avatar personal IP library, named by style and usage scenario.
- `baku-design-system/references/virtual-avatar.md`: your character setup, clothing, hair, expression, illustration style, and negative prompts.
- `baku-design-system/SKILL.md`: replace `Baku`, `Basic-XYZ`, trigger wording, and style-routing language with your own brand context.

Recommended follow-up changes:

- `baku-design-system/references/style-*.md`: keep only the visual styles you actually want.
- `baku-design-system/assets/template-*.html`: replace brand names, sample copy, CTA text, footer text, and avatar placement.
- `baku-design-system/agents/openai.yaml`: update `display_name`, `short_description`, and `default_prompt`.
- Repository-level `README.md`, `README.en.md`, and `skills.sh.json`: update install commands, skill names, summaries, and GitHub URLs before publishing.
