# Brand DNA - Baku

所有 Baku 页面、图文卡片和虚拟形象共享这份底层规范。用户要求调整品牌时，优先改这里，再让模板读取这些变量。

## 固定配色

| Token | 色值 | 用途 |
|---|---|---|
| Ink | `#161A22` | 主文字、强标题、深色界面底；黑色是稳定偏好 |
| Paper | `#F7F4EA` | 主背景，带一点纸张温度；暖白是稳定偏好 |
| Warm White | `#FFFDF6` | 高亮表面、文档页底色、Notion 风格页面主背景 |
| Baku Yellow | `#F6D21F` | IP 头像背景、活力强调、封面点亮 |
| Field | `#E9E2D0` | 分隔、面板底、低对比区域 |
| Signal Green | `#18A058` | 成功、通过、可执行状态 |
| Work Blue | `#2563EB` | 链接、焦点、关键动作 |
| Amber | `#D97706` | 重点提示、时间线、风险提醒 |
| Vermilion | `#D64B3A` | 少量强调、告警、头像点缀 |

比例：Ink/Paper/Warm White/Field 70%，Baku Yellow 15%，Signal Green/Work Blue 10%，Amber/Vermilion 5%。红色只能点到为止。不是所有页面都必须出现黄色，Notion 风格页面可以主要使用黑、暖白和 whisper border。

## 字体基因

- 中文正文：`Noto Sans SC`, `PingFang SC`, system-ui。
- 中文标题：优先 `Noto Serif SC` 或本地宋/明朝风格字体，用来制造“笔记、文档、判断”的气质。
- 英文标签：`IBM Plex Sans`, `Inter`, system-ui。不要整页都用过度科技感等宽字体。
- 代码/终端：`JetBrains Mono`, `SFMono-Regular`, `Menlo`, monospace，只用于代码、命令和数据。

字号建议：

- Hero 标题：`clamp(2.6rem, 6vw, 5rem)`
- Section 标题：`clamp(1.6rem, 3vw, 2.4rem)`
- 正文：`16px`
- 辅助文字：`0.82rem`
- 数据数字：`clamp(2.2rem, 5vw, 4.4rem)`

## 气质关键词

- 实用、克制、可信
- 有工程判断，不炫技
- 像真实工作台，不像营销模板
- 中文优先，证据链清楚
- 有个人识别度，但不幼稚
- 安静、有质感、可长期复用

## 虚拟形象

Baku 的默认虚拟形象是一个“程序员型个人 IP”：

- 中长深黑色头发，略蓬松，有手绘铅笔质感。
- 圆框眼镜、黑色 T 恤、坐在电脑前，表达程序员 / builder 身份。
- 黄色背景是主要记忆点，配合蓝色电脑、代码符号、植物、咖啡杯和笔记本。
- 表情平静、略认真，可以挥手或做轻量解释姿势；不要夸张卖萌。
- 头像构图保留上半身、电脑和桌面道具，不要裁成只有大头。

素材文件：

- 默认兼容头像：`assets/avatar.jpg`
- 多头像库：`assets/avatars/`
- 当前多头像库来自 Baku 程序员桌面系列，统一为 816x816 PNG。
- 旧模板仍可引用 `assets/avatar.jpg`；新页面优先从 `assets/avatars/` 按场景挑选更合适的头像。
- 头像是可选视觉锚点，不是强制元素。个人介绍、作者页、品牌页、图文卡片封面优先使用；普通文档页、工具页、报告页可以不使用。

## 通用禁忌

| 类型 | 禁止 |
|---|---|
| 配色 | 蓝紫渐变、霓虹青、纯黑纯白、单一深蓝/灰蓝整页 |
| 布局 | 千篇一律三卡片、卡片套卡片、所有 section 居中 |
| 装饰 | 玻璃拟态、光球、bokeh、无意义 SVG 背景 |
| 字体 | 整页等宽体、过度负字距、viewport 宽度驱动字号 |
| 文案 | 空泛口号、AI 味说明、过度解释功能 |
| 图片 | stock photo 感、暗糊背景、和主题无关的气氛图 |

## 响应式原则

- 断点：`920px` 两栏变单栏，`640px` 收紧字号和间距。
- 移动端重新排列内容，不隐藏关键字段。
- 固定格式组件使用 `aspect-ratio`、`minmax()` 和明确尺寸，避免 hover 或动态文本撑乱布局。
- 尊重 `prefers-reduced-motion`。
