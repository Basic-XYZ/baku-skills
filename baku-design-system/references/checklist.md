# Checklist

交付前逐条检查。P0 不通过就继续修改。

## P0 必须通过

- 已读取并遵守 `brand-dna.md`。
- 已选择一套视觉风格：`style-baku-workbench.md`、`style-notion.md` 或 `style-retro-future-mainframe.md`。不要无意混用。
- 输出不是通用 AI landing page：没有蓝紫渐变、玻璃拟态、光球和泛滥卡片。
- 如果使用 Retro Future Mainframe，复古未来感来自深色网格、主机面板、指标和黄绿信号，不来自过度霓虹或低可读对比。
- 第一屏能明确看出 Baku/Basic-XYZ 的主体或作品，不只在导航小字出现。
- 文本不溢出、不重叠，移动端和桌面端都能阅读。
- 所有按钮、卡片、表格、引用块、列表都有明确样式，不使用浏览器默认观感。
- 图像路径有效；只有需要头像时才引用 `assets/avatar.jpg`、`assets/avatars/` 中的头像或用户提供的新头像。
- 使用头像前已按 `references/virtual-avatar.md` 选择适合页面底色、场景和风格的版本。
- HTML 可直接在浏览器打开，不依赖未说明的构建步骤。

## P1 应该满足

- 每个主要 section 使用不同布局节奏。
- 信息密度适合工作流页面，不把工具页做成营销海报。
- CTA 和关键动作有图标或明确视觉状态。
- 颜色比例符合 Ink/Paper 为主、强调色少量使用。
- 有 hover/focus 状态，且不造成布局跳动。

## P2 加分

- 有可截图传播的卡片或首屏。
- 虚拟形象和页面气质一致。
- 动效细微且尊重 `prefers-reduced-motion`。
- 组件可以复制到下一次页面继续用。
