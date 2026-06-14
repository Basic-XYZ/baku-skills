# Style: Notion Warm Doc

第二套可选风格。它不是替代 Baku Workbench，也不要和 Baku Workbench 强行混合。用户提到 Notion、暖白、文档型官网、极简产品页、知识库、内容型页面时使用。

## 气质

- 像一张安静的暖白纸面，内容自己站出来。
- 克制、轻、干净、阅读友好，不炫技。
- 主要依靠排版、间距、whisper border 和轻阴影建立层级。
- 不强制出现 Baku 头像；Notion 风格页面通常可以只用文字、图标、截图或文档块作为视觉锚点。

## 配色

- 页面背景：`#ffffff` 或暖白 `#f6f5f4`。
- 主文字：`rgba(0,0,0,0.95)`，不要纯黑硬压。
- 深色面：`#31302e`，比冷灰更暖。
- 次级文字：`#615d59`。
- 占位/说明：`#a39e98`。
- 主动作：`#0075de`。
- Hover/Active：`#005bab`。
- Badge 背景：`#f2f9ff`，文字 `#097fe8`。

## 字体

- 使用 `Inter, -apple-system, system-ui, "PingFang SC", "Noto Sans SC", sans-serif`。
- 标题可以略紧，但不要按 viewport 缩放字体。
- 英文大标题可轻微负字距；中文标题保持 `letter-spacing: 0`。
- 推荐层级：
  - Hero：`clamp(2.5rem, 6vw, 4rem)`，700，line-height 1.05。
  - Section：`clamp(2rem, 4vw, 3rem)`，700。
  - Card title：`1.25rem` 到 `1.4rem`，700。
  - Body：`16px`，line-height 1.5。
  - Caption/Badge：`12px` 到 `14px`。

## 组件

- 卡片：白底，`1px solid rgba(0,0,0,0.1)`，12px 半径，极轻多层阴影。
- 按钮：蓝色主按钮，4px 半径；次按钮用浅灰或透明。
- Badge：9999px 胶囊，蓝色浅底。
- 表格/列表：轻边框、暖白表头、充足 padding。
- 分隔：用 1px whisper border，不用重边框。

## 布局

- 内容最大宽度约 1120-1200px。
- 首屏可以单列居中，也可以文档 split，但不要过度装饰。
- 大 section 之间留 64-120px。
- 白底和 `#f6f5f4` 暖白 section 交替，制造轻节奏。
- 卡片网格最多 2-3 列；移动端自然堆叠。

## 适合

- 产品说明页。
- 知识库首页。
- 轻量 landing page。
- 文档型功能说明。
- 团队流程或方法论页面。

## 禁忌

- 不要让 Notion 风格吞掉 Baku 品牌库；它只是第二套可选页面风格。
- 不要强制放头像。
- 不要用重阴影、厚边框、大面积黄色、玻璃拟态或霓虹渐变。
- 不要把所有 section 做成一样的三卡片。
