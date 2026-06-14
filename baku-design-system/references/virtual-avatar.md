# Virtual Avatar

用于生成、替换或选择 Baku 的个人 IP 头像。旧模板兼容 `assets/avatar.jpg`；新页面优先从 `assets/avatars/` 的多头像库中选择。

## 默认形象设定

Baku 是一个程序员型个人 IP：安静、可靠、能把复杂问题拆成可验证步骤。头像应传达“程序员、工作台、判断、执行”，而不是可爱吉祥物或未来感机器人。

当前兼容默认头像是 `assets/avatar.jpg`：黄色背景、手绘铅笔质感、中长黑发、圆框眼镜、黑色 T 恤、电脑、植物、咖啡杯、笔记本和代码符号。新页面、图文卡片和作者介绍优先从 `assets/avatars/` 选择更适合页面气质的版本；只有旧模板或未指定场景时才回退到 `assets/avatar.jpg`。

## 多头像库

所有头像都放在 `assets/avatars/`，命名规则为 `baku-avatar-风格-场景.png`。

| 文件 | 适合场景 |
|---|---|
| `assets/avatars/baku-avatar-crayon-light-desk.png` | 暖白页面、作者介绍、个人品牌首屏，需要桌面和工作感时使用。 |
| `assets/avatars/baku-avatar-crayon-light-portrait.png` | 暖白页面、小尺寸头像、个人简介 badge，需要干净头像时使用。 |
| `assets/avatars/baku-avatar-crayon-dark-desk.png` | 暗色页面、复古未来页面、工程工作台，需要桌面和电脑元素时使用。 |
| `assets/avatars/baku-avatar-crayon-dark-portrait.png` | 暗色页面、小尺寸头像、导航/侧栏/作者卡片。 |
| `assets/avatars/baku-avatar-anime-warm-desk.png` | 日系暖感、故事型页面、轻松但仍然有工作台的内容页。 |
| `assets/avatars/baku-avatar-soft-3d-desk.png` | 更现代、更产品化的 landing 或 App 展示页；谨慎使用，避免页面过圆润。 |
| `assets/avatars/baku-avatar-soft-3d-portrait.png` | 现代产品页的小头像或社交卡片；不作为默认主视觉。 |
| `assets/avatars/baku-avatar-marker-desk.png` | 美式/marker 插画感、案例页、复盘页、需要更强手绘冲击力时使用。 |
| `assets/avatars/baku-avatar-marker-portrait.png` | 卡片封面、作者头像、需要强识别但不占大画面时使用。 |
| `assets/avatars/baku-avatar-line-art-portrait.png` | 极简页、Notion Warm Doc、低干扰署名或页脚。 |
| `assets/avatars/baku-avatar-yellow-sticker.png` | 传播卡片、社交头像、轻量封面贴纸；不要在严肃报告中过度使用。 |
| `assets/avatars/baku-avatar-cat-line-art-sitting.png` | 黑白线稿、人物坐姿与猫同框；适合低干扰微信头像、个人页签名和极简作者介绍。 |
| `assets/avatars/baku-avatar-cat-crayon-sitting.png` | 彩色蜡笔质感、人物坐姿与猫同框；适合微信头像、社交名片、亲和型个人 IP 页面。 |
| `assets/avatars/baku-avatar-cat-crayon-close.png` | 彩色蜡笔近景、人物抱猫；适合强亲和头像、社交封面和需要生活气的作者卡片。 |

选择规则：

- Baku Workbench：优先 `crayon-light-desk`、`marker-desk`、`yellow-sticker`。
- Notion Warm Doc：优先 `line-art-portrait`、`crayon-light-portrait`，通常不强制出现头像。
- Retro Future Mainframe：优先 `crayon-dark-desk`、`crayon-dark-portrait`、`marker-portrait`。
- 作者页/个人主页：需要强主视觉时用 `*-desk`；需要头像 badge 时用 `*-portrait`。
- 图文卡片：封面可用 `yellow-sticker`、`marker-portrait`；正文解释型卡片可用 `crayon-light-desk`。
- 微信/社交头像：优先 `cat-crayon-sitting`、`cat-crayon-close`、`yellow-sticker`；需要更克制时用 `cat-line-art-sitting`。
- 不确定时，先选择和页面底色匹配的头像：浅底用 light/line-art/yellow，深底用 dark/marker。

## 生成提示词

中文：

```text
一张方形个人 IP 头像，程序员型个人品牌，东亚男性，中长蓬松黑发，圆框眼镜，黑色 T 恤，坐在电脑前，黄色背景，蓝色电脑，旁边有小植物、咖啡杯、笔记本和代码符号，手绘铅笔质感，温暖但克制，平静专注的表情，可以轻轻挥手，像真实个人品牌头像，不幼稚，不赛博朋克，不要重度二次元风格，不使用霓虹光效，不使用蓝紫渐变。
```

English:

```text
Square personal IP avatar for a programmer personal brand, East Asian male, medium-length fluffy black hair, round glasses, black T-shirt, sitting at a laptop, bright warm yellow background, blue laptop, small plant, coffee mug, notebook, and subtle code symbols, hand-drawn pencil texture, warm but restrained, calm focused expression, gentle waving gesture, credible personal brand portrait, not childish, not cyberpunk, not anime-heavy, no neon glow, no blue-purple gradient.
```

## 替换规则

- 兼容默认头像固定为 `assets/avatar.jpg`。
- 多头像库固定放在 `assets/avatars/`。
- 保持方形，建议至少 816x816。
- 标准图使用全图构图，保留头部、眼镜、黑 T、电脑和桌面道具。
- 小尺寸头像使用中心偏上裁切，至少保留头发、眼镜、脸、黑 T 和电脑上沿。
- 不要把 Baku 裁成只有脸的大头，也不要把黄色背景完全裁掉。
- 如果使用真人照片重新生成，避免过度滤镜和暗糊背景。
