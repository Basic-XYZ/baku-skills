# Style: Retro Future Mainframe

第三套可选风格。它来自 Baku 个人网站的复古未来感，适合个人网站、暗色技术作品集、AI workbench、项目 case study 和高冲击 landing page。它不是替代 Baku Workbench 或 Notion Warm Doc，也不要无意混合三套风格。

## 气质

- 像一台正在运行的个人 AI 主机：深色、密集、技术感强，但信息仍然清楚。
- 关键词：retro future、mainframe、terminal、signal、case archive、AI delivery cockpit。
- 画面有电影感和控制台感，重点靠网格、扫描线、指标、终端面板和黄绿高亮建立记忆。
- 不是泛 cyberpunk；不要把页面做成霓虹招牌或蓝紫渐变海报。

## 配色

- 深色底：`#050816`、`#071025`、`#0B1226`，不要用纯黑。
- 主文字：`#F7FBFF`。
- 次级文字：`#94A3BA`。
- 细线：`rgba(148, 163, 184, 0.18)`。
- 主高亮：`#D7FF24`，用于 active pill、主 CTA、关键数字和光标。
- 信号绿：`#7CFFD5`，用于网格、状态、section kicker、边框微光。
- 辅助蓝：`#6EA8FF`，只做少量链接或状态。
- 警示红：`#FF6B4F`，只用于风险或异常。

## 字体

- 技术 UI：`"IBM Plex Mono", "SFMono-Regular", Consolas, monospace`。
- 英文 display：`Aldrich`、`Michroma` 或 `Poppins`；没有外部字体时用系统 sans fallback。
- 中文正文：`"PingFang SC", "Noto Sans SC", "Microsoft YaHei", system-ui, sans-serif`。
- Hero 标题可大：`clamp(48px, 7vw, 112px)`，900，line-height 约 `1.02`。
- Kicker、badge、metric label 使用 mono、小字号、大写英文或短中文，字距只用于英文；中文保持 `letter-spacing: 0`。

## 背景

- 用深色线性渐变打底：上深、中段略亮、底部回深。
- 叠加固定细网格：56px 到 72px 间距，黄绿低透明度，不能抢正文。
- 可叠加径向微光：黄绿从底部或角落轻轻透出，不使用独立光球、bokeh 或大面积蓝紫渐变。
- 可加暗角或中心聚焦，让首屏像主机屏幕而不是普通黑页。

## 组件

- 顶部导航：固定或 sticky，半透明深色，细边框；active 状态用黄色 pill。
- Hero：左侧大标题和短 lead，右侧 terminal/mainframe panel、指标面板或项目信号卡；头像不是必选。
- Terminal panel：深色面板、细绿边、mono 行、状态点、命令提示符、输出块。
- Metric strip：3-4 个指标块，数字用黄色或白色，label 用 muted。
- Case card：深色半透明面板、细边框、顶部 label、项目编号、证明点、tag row。
- Timeline：左侧绿线，黄色节点，右侧深色内容块。
- CTA：主按钮黄色底深色字；次按钮透明深色底和绿边。

## 布局

- 页面最大宽度可更宽，约 `min(1680px, calc(100% - 72px))`，让个人网站有沉浸感。
- 首屏接近满屏，但必须露出下一段内容的线索。
- 主体 section 交替使用 hero split、metric strip、case grid、terminal split、timeline，不要整页都是卡片网格。
- 卡片圆角控制在 14px 到 18px；按钮可用 pill，但内容卡不要过圆。
- 移动端优先把 hero、指标、case grid 单列堆叠，保持无横向滚动。

## 适合

- 个人网站和工程作品集。
- AI workbench / Agent workflow 展示页。
- 技术项目 case study。
- 高冲击 landing page。
- 控制台、运行状态、交付链路、系统架构可视化页面。

## 禁忌

- 不要做成通用 SaaS hero 或普通深色 dashboard。
- 不要使用大面积蓝紫渐变、玻璃拟态、光球和纯装饰发光元素。
- 不要过度霓虹，正文区域必须高对比、可读。
- 不要强制出现 `assets/avatar.jpg`；只有个人介绍、作者页或用户明确要求时再用。
- 不要引入 React/WebGL/动画库作为静态 HTML 模板的硬依赖；复杂动效只能作为增强。
