# 生图提示词模板

每张图单独生成。根据正文内容替换变量，不要把多张图拼在一起。

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Warm paper background close to #F7F4EA, clean and spacious. Hand-drawn ink line art using #161A22, slightly imperfect pencil/marker lines, restrained paper-note texture, lots of blank space. Calm engineering workbench mood, not a marketing illustration. Use sparse handwritten Chinese annotations in short phrases. Add limited accents from Baku Yellow #F6D21F, Signal Green #18A058, Work Blue #2563EB, Amber #D97706, and Vermilion #D64B3A. No blue-purple gradients, no glassmorphism, no stock-photo background, no dense UI, no commercial SaaS vector style, no PPT infographic look, no cute mascot poster, no children's illustration.

Recurring IP character required:
Baku, an East Asian male-presenting adult programmer character with short-to-medium fluffy layered black hair, natural messy fringe or subtle side-swept fringe, no center part, round thin-frame glasses, plain black T-shirt, slim natural oval face, adult neck and shoulder proportions, calm focused expression, sitting or standing at a practical desk with a laptop/notebook/sticky notes nearby. Prefer 2D crayon, pencil, sticker-like hand-drawn, or warm watercolor character rendering. Baku must perform the core conceptual action, not decorate the scene. Make him reliable, restrained, thoughtful, and work-focused, not chibi, not toy-like, not influencer-like, not round-faced, not chubby-cheeked, not a default 3D mascot.

Theme:
{正文配图主题}

Structure type:
{结构类型：Workflow / 证据链 / 系统局部 / 前后对比 / 角色状态 / 工作台隐喻 / 方法分层 / 地图路线}

Core idea:
{这张图要表达的核心意思}

Composition:
{具体画面：Baku 在哪里、正在做什么、主要物件是什么、信息如何流动}

Suggested elements:
{元素1} / {元素2} / {元素3} / {元素4}

Chinese handwritten labels:
{标注词1} / {标注词2} / {标注词3} / {标注词4} / {可选标注词5}

Color use:
Ink for line art and text. Paper for background. Baku Yellow only for the main memory accent such as a sticky note or lamp glow. Work Blue for tool/system/AI state. Signal Green for pass/ready/result. Amber for main path/time/risk. Vermilion only for warnings or hard problems.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 30% blank space. Use at most 5-8 short handwritten Chinese labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, dashboard, UI mockup, or dense explainer. Do not use center-parted hair, round chubby face, balloon cheeks, toy-like 3D head, oversized doll eyes, or soft 3D mascot style unless explicitly requested. Do not copy Xiaohei or Buer illustration compositions; invent a fresh workbench metaphor for this specific article. It should be clear, useful, calm, and personal, with just enough visual wit to be memorable.
```

## 图像编辑提示

去掉左上角标题：

```text
Edit the provided image. Remove only the handwritten title "{要删除的文字}" and its underline from the top-left corner. Fill that area with the same warm clean paper background, matching the surrounding blank area. Preserve everything else exactly: Baku character, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

让 Baku 更像动作主体：

```text
Regenerate this illustration with the same core meaning and simple layout, but make Baku more central to the conceptual action. He should be doing the work that explains the idea: checking evidence, connecting notes, repairing a chain, sorting inputs, or handing off the result. Keep the warm paper background, restrained hand-drawn style, sparse Chinese annotations, and engineering workbench mood.
```

修正人物过圆或中分：

```text
Edit or regenerate the illustration while preserving the same concept and composition. Make Baku closer to the preferred 2D hand-drawn character direction: short-to-medium fluffy layered black hair with messy fringe or subtle side-swept fringe, no center part, round thin-frame glasses, slim natural oval face, adult proportions, plain black T-shirt, calm focused expression. Avoid round chubby face, balloon cheeks, oversized doll eyes, toy-like 3D head, and soft 3D mascot rendering. Keep the warm paper / crayon / pencil hand-drawn style and all conceptual labels.
```

降低 PPT 感：

```text
Regenerate this illustration with fewer boxes, fewer arrows, and no formal diagram title. Turn the structure into a small hand-drawn workbench scene with Baku actively manipulating physical notes, wires, folders, or tools. Keep only 3-5 short Chinese labels and leave more empty space.
```
