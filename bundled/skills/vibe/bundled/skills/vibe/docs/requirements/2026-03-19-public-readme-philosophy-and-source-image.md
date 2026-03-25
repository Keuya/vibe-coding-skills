# 2026-03-19 Public README Philosophy And Source Image

## Goal

重写 README 首页开场，直接使用作者提供的 `Gemini_Generated_Image_75f8n575f8n575f8.svg` 作为首屏图片，不再做海报式二次设计，同时强化项目的核心哲学：规范化。

## Deliverables

- 将作者提供的原始 Gemini SVG 入库并直接用于 README 首屏展示
- 重写 `README.md` 开头哲学段落，强调规范化是项目核心
- 重写 `README.en.md` 对应开场与能力说明
- 将原先偏技术缩写的 capability table 改写为更白话、更容易理解的说明
- 在正文中明确说明项目吸收和借鉴的上游优秀项目与其整合价值
- 更新 requirement / plan 索引

## Constraints

- 不再做海报式 hero、mark、panel 等再设计
- 原图直接展示，不裁切、不改造其主视觉结构
- README 仍需保持 GitHub 原生渲染兼容性
- 能力说明必须更易懂，但不能脱离真实能力边界
- 需要明确说明项目的规范化哲学、工作流治理价值和维护价值

## Acceptance Criteria

- README 开头直接强调“规范化”是项目核心哲学
- 原始 Gemini SVG 在首屏展示，位置位于哲学开场后、能力说明前
- 能力表格不再只是术语堆叠，而是更容易被普通用户理解
- README 明确说明整合了 skills、MCP、插件、工作流和上游优秀项目经验
- README 明确表达“用户主要与 AI 交流需求，后续任务在规范化工作流中自动落地和维护”的目标
- 中英文版本保持语义一致

## Frozen User Intent

用户明确要求：

- 直接把 `Gemini_Generated_Image_75f8n575f8n575f8` 这个图片放上去
- 能力说明要从“规模 / 运行时 / 治理”的技术说法改成更简单易懂的表达
- 要明确说明整合了多少 skills、多少上游优秀项目，并点名说明代表性来源
- 要在正文中提到 `superpower`、`claude-scientific-skills`、`get-shit-done`、`aios-core`、`OpenSpec`、`ralph-claude-code`、`SuperClaude_Framework`
- 开头必须强调项目哲学：核心要义就是规范化；规范化能让人类描述更清晰、AI 工作更稳定、后续技术债更低

## Evidence Strategy

- 检查 README 首屏顺序：哲学段落 -> 原始 SVG -> 白话能力表格
- 检查图片路径已入库并被 README 正确引用
- 检查 README 正文包含指定上游项目名称和规范化工作流表述
