# Style: Retro Future Mainframe

第三套可选风格。它来自 Baku 个人网站的复古未来感，适合个人网站、暗色技术作品集、AI workbench、项目 case study 和高冲击 landing page。它不是替代 Baku Workbench 或 Notion Warm Doc，也不要无意混合三套风格。

## 气质

- 像一张复古电脑主题的个人作品集海报：灰米色纸面、CRT 主视觉、黑白胶囊导航、首屏安静，下一屏进入深色系统面板。
- 关键词：retro computer、CRT、mainframe、editorial portfolio、scanline、case archive、AI delivery cockpit。
- 画面重点不是霓虹黑底，而是老式电脑图像、微弱扫描线、CRT 绿、琥珀色信号和黑白高对比控件。
- 不是泛 cyberpunk；不要把页面做成深蓝霓虹 dashboard。

## 配色

- 首屏纸面：`#D0CBC0`，配合灰米色复古照片或视频 poster。
- 下半深色：`#11110F`、`#090908`，用于 case、lab、系统面板区。
- 首屏文字：`#050505`。
- 深色区文字：`#F3EAD6`。
- 次级文字：`#A8A08F` 或 `rgba(243, 234, 214, 0.7)`。
- CRT 绿：`#B8FF6A`，用于信号、边框、状态、hover。
- 琥珀色：`#FFB45E`，用于主高亮、节点、局部 glow。
- 警示红：`#D66F52`，只用于风险或异常。

## 字体

- 技术 UI：`"Fira Code", "SFMono-Regular", Consolas, monospace`。
- 英文 display：`Fraunces`，必要时用 `Inter` 补足 UI 文字。
- 中文正文：`"Noto Sans SC", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif`。
- Hero 标题克制：`clamp(34px, 4.5vw, 68px)`，400-700，line-height 约 `1.08`。
- Kicker、badge、metric label 使用 mono、小字号、大写英文或短中文，字距只用于英文；中文保持 `letter-spacing: 0`。

## 背景

- 首屏优先使用用户确认过的复古电脑/CRT 视觉资产；没有确认素材时，用 CSS 构造 CRT 机器轮廓和信号背景，不要引入未确认图片。
- 不要引用 `assets/retro-future-hero.webp`；这张图已被淘汰，不应再放回项目。
- 背景叠加轻扫描线、纸面灰、暗角和 very subtle CRT 网格，不要做大面积蓝紫渐变。
- 首屏之后切到深色系统区：`#11110F` 背景、绿色/琥珀弱光、细线和 dashed border。
- 如果没有用户确认过的图像，先用纯 CSS CRT 视觉占位，再等待用户确认新资产；不要只用纯 CSS 终端卡替代。

## 组件

- 顶部导航：居中黑白胶囊，active 为黑底白字，其余为白底黑字，边框清晰。
- Hero：full-bleed 图像背景，左侧短介绍、主标题和白色 action pills；不要右侧再塞终端卡。
- Action pill：白底黑字，圆角 999px，轻边框；hover 可变黑底白字。
- Case card：深色面板、CRT 绿/琥珀细边、dashed inner border、项目编号和 proof chips。
- Lab/terminal panel：黑色或近黑底，扫描线、细绿边和 mono 日志，但只在下半内容区使用。
- Timeline：深色区左侧线条，琥珀节点，内容块用 `#F3EAD6` 文字。

## 布局

- 首屏必须 full viewport，主视觉覆盖全屏，文字和 action 位于左侧偏下。
- 首屏之后进入深色内容区，case grid、lab panel、timeline 才使用 CRT 面板语言。
- 内容最大宽度约 `min(1560px, calc(100% - 72px))`。
- 卡片圆角控制在 8px 到 12px；导航和 action pills 可以 999px。
- 移动端优先把 hero、指标、case grid 单列堆叠，保持无横向滚动。

## 适合

- 个人网站和工程作品集。
- AI workbench / Agent workflow 展示页。
- 技术项目 case study。
- 高冲击 landing page。
- 控制台、运行状态、交付链路、系统架构可视化页面。

## 禁忌

- 不要做成通用 SaaS hero、普通深色 dashboard 或赛博朋克霓虹页。
- 不要把首屏做成黑底终端面板；Baku 个人站的复古未来感首先来自复古电脑主视觉和灰米色影像。
- 不要使用大面积蓝紫渐变、玻璃拟态、光球和纯装饰发光元素。
- 不要过度霓虹，正文区域必须高对比、可读。
- 不要强制出现 `assets/avatar.jpg`；只有个人介绍、作者页或用户明确要求时再用。
- 不要引入 React/WebGL/动画库作为静态 HTML 模板的硬依赖；复杂动效只能作为增强。
