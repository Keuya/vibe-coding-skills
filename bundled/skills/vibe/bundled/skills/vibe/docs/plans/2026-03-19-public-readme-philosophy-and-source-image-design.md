# Public README Philosophy And Source Image Design

## Intent

这次改动不再追求“做出一张更强的海报”，而是回到更直接、更诚实的 README 表达方式：把作者自己的图直接放上去，把项目到底相信什么、整合了什么、要解决什么，说得更清楚。

## Chosen Direction

采用 `Direct Source Image + Strong Philosophy Framing`：

- 顶部先讲哲学，而不是先讲功能
- 直接展示作者原图，不再做 panel / mark / poster 二次包装
- 能力说明用更白话的表格表达，而不是只堆 runtime 术语
- 在正文中明确点名上游来源与整合价值

## Why This Direction Fits Better

用户这次不是要更强的视觉包装，而是要更直接地表达项目的精神内核。

所以开头要回答三个问题：

1. 这个项目最核心相信什么
2. 它整合了哪些能力和上游来源
3. 它最终想替用户完成什么

## Layout Decision

README 首屏采用以下顺序：

1. 语言切换
2. 项目标题
3. 核心哲学 blockquote
4. 哲学解释段落
5. 原始 Gemini SVG
6. 更易懂的 capability snapshot
7. 对上游整合和工作流价值的正文说明

## Content Strategy

能力表格不再强调“术语正确但理解成本高”，而是改成：

- 多少个可直接调用的 skills / 能力模块
- 多少个吸收和借鉴的上游优秀项目
- 多少条治理策略与契约
- 这些能力如何共同服务于需求澄清、计划设计、自动化编写、验证与维护

## Success Condition

如果改动成立，README 一开头就能让人理解：

- 这不是一个随意堆能力的仓库
- 这是一套以规范化为核心的 AI 工作系统
- 作者原图作为首屏视觉存在，但不会压过项目哲学本身
