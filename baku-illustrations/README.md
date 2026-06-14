# Baku Illustrations

Baku/Basic-XYZ 的个人风格正文配图 skill。这个 skill 的结构和迁移方法借鉴自 Ian 的开源项目 [ian-xiaohei-illustrations](https://github.com/helloianneo/ian-xiaohei-illustrations)。

它借鉴了原小黑仓库的组织方式：`SKILL.md` 控制工作流，`references/` 拆出风格、角色、构图、prompt 和 QA，`assets/` 放校准素材。但它不是小黑换皮，也不是 Esther/不二换皮；核心已经换成 Baku 自己的程序员个人 IP、暖纸工作台、克制手绘线条和工程证据链气质。

## 适合做什么

- 为中文文章、博客、知识库、教程、复盘生成 16:9 正文配图。
- 先给 shot list，判断哪些段落值得配图。
- 把流程、证据链、系统局部、前后对比、角色状态和方法分层变成可读插图。
- 在图里使用 Baku 程序员 IP 承担核心动作，而不是只做装饰头像。

## 和参考仓库的差异

[ian-xiaohei-illustrations](https://github.com/helloianneo/ian-xiaohei-illustrations) 的核心是“纯白、极简、黑色怪诞小角色、少量红橙蓝批注”。

Baku 版本继续沿用这种迁移思路，但把风格换成：

- Baku 程序员个人 IP：圆框眼镜、中长黑发、黑 T、电脑和笔记工作台。
- 暖纸背景、Ink 黑线条、Baku Yellow 记忆点。
- Signal Green / Work Blue / Amber / Vermilion 只做少量状态和风险批注。
- 更强调工程判断、证据链、最小可行动作和真实工作台气质。
- 彩色蜡笔/马克笔纹理。

## 安装

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-illustrations
```

## 想做你自己的版本

看 [personal-style-skill-guide.md](./references/personal-style-skill-guide.md)。关键不是改名，而是一起替换角色 IP、风格 DNA、构图语法、prompt 模板、QA 标准和 README 说明。
