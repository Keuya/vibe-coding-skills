# Public README Poster Hero Design

## Intent

把当前 README 从“有判断力的长文案首页”升级成“有品牌主视觉的公开入口页”。

这次设计不是把内容图像化，而是把首屏改造成接近前端 landing page 的阅读体验：第一眼有记忆点，第二眼有能力密度，第三眼能快速进入文档路径。

## Chosen Direction

采用 `Hybrid` 方向：

- 品牌识别由简约可爱的小章鱼承担
- 高级感由栅格、留白、信息卡片和色彩控制承担
- 专业感由指标、术语、治理叙事和可验证事实承担

不走纯卡通，也不走冷冰冰的纯技术海报。

## Visual System

### Color

- `Sea Salt`：温和的浅底，避免 README 首屏显脏或压抑
- `Deep Teal`：主要系统色，承接 runtime / governance / control 的语义
- `Slate Ink`：正文与结构信息色
- `Coral`：少量强调色，用在章鱼表情与关键点缀上

### Shape Language

- 大块圆角面板
- 细线网格与柔和发光
- 几何化小章鱼，触手节奏整齐，不做复杂插画
- 视觉上更像“产品发布页海报”，不是动漫吉祥物海报

### Typography

- Hero 内部使用 SVG 文本形成更强的字重与层次
- README 正文仍保持 GitHub 原生文本可读性
- 标题、解释、数据、路径分成四种视觉节奏，避免整页只是一种密度

## README Structure

首屏顺序调整为：

1. 语言切换
2. 横版 poster hero SVG
3. 小章鱼 logo 与标题区
4. capability cards
5. 价值叙事
6. 系统骨架说明
7. 快速路径入口

这样用户的浏览路径会从“被吸引”变成“被说服”，再进入“下一步行动”。

## Why SVG + HTML

GitHub README 无法依赖自定义 CSS/JS，因此最强可维护方案不是伪前端，而是：

- 用 SVG 承担海报级主视觉
- 用 HTML 表格承担信息卡片和横向布局
- 用 Markdown 承担正文、链接和长期维护

这让首页既有设计感，也不牺牲可维护性和版本管理体验。

## Asset Plan

- `docs/assets/vibeskills-octopus-mark.svg`
  - 单独可复用的小章鱼 logo
- `docs/assets/readme-poster-hero-cn.svg`
  - 中文 poster hero
- `docs/assets/readme-poster-hero-en.svg`
  - 英文 poster hero

## Content Strategy

文案上不推翻现有 README 的叙事优势，而是重新组织节奏：

- 保留“不是另一个 skills 仓库”这类判断句
- 保留时代焦虑与系统回应的叙事
- 把 capability snapshot 从普通表格升级成更像产品信息卡
- 把 quick-start / manifesto / install 路径做成更像落地页 CTA 区

## Success Condition

最终的 README 应该满足三个同时成立的目标：

1. 首屏有品牌记忆点
2. 首屏有系统级可信度
3. 首屏能引导用户继续阅读或安装，而不是只停留在“看起来好看”
