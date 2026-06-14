# Baku Design System

Baku/Basic-XYZ 的个人品牌设计系统 skill，用于生成可直接打开的 HTML 页面、图文卡片和个人虚拟形象。

它复用 `esther-design-system` 的工作方式：先读取品牌 DNA，再按场景选择教程页、landing、App 工具页、图文卡片或个人头像相关参考，最后用 checklist 自检。但它不是简单换名，颜色、字体、页面气质、头像使用规则和默认模板都已经收束到 Baku 自己的个人品牌方向。

## 适合做什么

- 生成 Baku 风格的个人网站、作品集、landing page 和教程页。
- 把文章、方法论或产品说明转成图文卡片。
- 生成 App 型工具界面、看板页和工作台页面。
- 维护 `brand-dna.md`，集中调整颜色、字体、气质关键词和头像规则。
- 设计或迭代 Baku 的个人虚拟形象。

## 安装

```bash
npx skills add https://github.com/Basic-XYZ/baku-skills --skill baku-design-system
```

## 想做你自己的版本

不要只改仓库名。至少需要替换：

- `brand-dna.md`：你的品牌名、颜色、字体、气质关键词和禁忌。
- `assets/avatar.jpg`：你的个人 IP 形象或头像。
- `references/virtual-avatar.md`：你的人物设定、穿着、发型、表情和负面约束。
- `SKILL.md`：触发描述、品牌语境和工作流里的名字。

基础的场景参考、布局规则、组件规则和 checklist 可以继续复用，再按你的页面类型扩展。
