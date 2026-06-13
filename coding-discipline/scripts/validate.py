#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "references/code-style.md",
    "references/frontend-ui-work.md",
    "references/mode-routing.md",
    "references/maturity-checklist.md",
    "references/related-skills.md",
]
SECRET_PATTERNS = [
    re.compile(r"gh[oprsu]_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
]
LOCAL_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED_TEXT = {
    "SKILL.md": [
        "## 相关 Skill 与安装",
        "## 内置纪律",
        "## 交付护栏",
        "## 完成标准",
        "code-style.md",
        "只读 / 方案",
        "frontend-ui-work.md",
        "不能结束的情况",
    ],
    "references/code-style.md": [
        "## 优先级",
        "## 局部风格",
        "## 命名与接口",
        "## 数据模型与实体对象",
        "字段必须能追溯到数据库列",
        "实体对象字段应逐字段注释",
        "## 注释",
        "需求代码、业务规则",
        "需求代码缺少必要注释",
        "## 自动化检查",
        "## 审查口径",
    ],
    "references/frontend-ui-work.md": [
        "## Brief Gate",
        "## Visual Target Gate",
        "## Existing Context First",
        "## Source vs Implementation QA",
        "## Handoff Evidence",
    ],
    "references/mode-routing.md": [
        "## 只读 / 方案",
        "code-style.md",
        "frontend-ui-work.md",
        "只读 / 方案模式优先于所有实现、修复、测试、安装和继续义务",
        "完成条件",
        "不能停的位置",
        "功能 / 行为变更",
        "故障 / 性能回归",
        "审查的两个轴",
    ],
    "references/related-skills.md": [
        "Matt Pocock skills",
        "Karpathy guidelines",
        "skills.sh 风格命令",
    ],
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_files() -> None:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    if missing:
        fail(f"缺少必需文件: {', '.join(missing)}")


def check_skill_frontmatter() -> None:
    text = read(ROOT / "SKILL.md")
    if not text.startswith("---\n"):
        fail("SKILL.md 必须以 YAML frontmatter 开头")

    end = text.find("\n---\n", 4)
    if end == -1:
        fail("SKILL.md frontmatter 没有闭合")

    frontmatter = text[4:end]
    for field in ("name:", "description:"):
        if field not in frontmatter:
            fail(f"SKILL.md frontmatter 缺少 {field}")


def check_markdown_links() -> None:
    for path in ROOT.rglob("*.md"):
        text = read(path)
        for match in LOCAL_LINK.finditer(text):
            target = match.group(1).strip()
            if should_skip_link(target):
                continue
            local_path = (path.parent / target.split("#", 1)[0]).resolve()
            try:
                local_path.relative_to(ROOT)
            except ValueError:
                fail(f"{path.relative_to(ROOT)} 链接到仓库外部: {target}")
            if not local_path.exists():
                fail(f"{path.relative_to(ROOT)} 存在失效链接: {target}")


def should_skip_link(target: str) -> bool:
    return (
        target.startswith("http://")
        or target.startswith("https://")
        or target.startswith("mailto:")
        or target.startswith("#")
    )


def check_for_obvious_secrets() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.name == ".DS_Store":
            continue
        try:
            text = read(path)
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"{path.relative_to(ROOT)} 可能包含密钥")


def check_required_text() -> None:
    for relative_path, snippets in REQUIRED_TEXT.items():
        text = read(ROOT / relative_path)
        missing = [snippet for snippet in snippets if snippet not in text]
        if missing:
            fail(f"{relative_path} 缺少必需文本: {', '.join(missing)}")


def main() -> None:
    check_required_files()
    check_skill_frontmatter()
    check_required_text()
    check_markdown_links()
    check_for_obvious_secrets()
    print("OK: coding-discipline skill 包校验通过")


if __name__ == "__main__":
    main()
