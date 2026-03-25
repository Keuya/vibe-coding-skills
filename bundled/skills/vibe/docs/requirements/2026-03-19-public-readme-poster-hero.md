# 2026-03-19 Public README Poster Hero

## Goal

将仓库首页升级为横版海报式 README 首屏，在保留现有叙事力度与能力事实面的前提下，引入更强的品牌识别、版式美感与信息层次。

## Deliverables

- 在 `README.md` 首屏加入横版海报式 hero
- 在 `README.en.md` 首屏加入对应英文 hero
- 新增一枚可复用的小章鱼 SVG logo
- 新增中英双语 poster hero SVG 主视觉
- 新增本轮 requirement、design、plan 文档
- 更新 `docs/requirements/README.md` 与 `docs/plans/README.md` 当前入口

## Constraints

- 必须兼容 GitHub README 原生渲染，不依赖自定义 CSS 或 JavaScript
- 允许使用 `inline HTML + SVG + Markdown`，但不能引入需要额外部署的前端运行时
- 章鱼形象必须“简约可爱”，但整体气质仍需高级、理性、专业
- 首屏依然要服务于“宣传优先、安装后置”的公开入口主轴
- 能力展示必须建立在仓库内可验证事实上，不能为了视觉而引入不可证指标
- 中英文首页需要保持同等级别的设计完成度，而不是只优化中文

## Acceptance Criteria

- 用户打开 README 首屏时，第一视觉层就是一张横版海报式主视觉
- 小章鱼 logo 既形成品牌记忆点，也不破坏系统感和治理感
- 首页同时具备品牌层、能力层、叙事层和快速导航层，不再只是纯段落说明
- 首屏信息密度高但不拥挤，能明显看出“前端化设计处理”的痕迹
- 中英文两个版本都完成 poster hero、logo、能力卡片和导航区的统一设计

## Non-Goals

- 不修改 manifesto、quick-start、install 正文内容
- 不修改 runtime、router、setup、check 等运行逻辑
- 不将 README 变成依赖截图或单张大图的不可维护页面
- 不将品牌气质做成幼态卡通风

## Frozen User Intent

用户明确要求：

- 做一个“横版的海报式”仓库展示首页
- 里面要有 logo，logo 是“一只简约可爱的小章鱼”
- README 要“非常美观”，展示界面要“非常好看，有设计感”
- 气质选定为 `Hybrid`：主视觉可爱，版式和信息密度保持高级、理性、专业
- 希望善用 HTML 与前端设计方式来实现 GitHub README 的视觉升级

## Evidence Strategy

- 通过 `git diff --stat` 验证改动范围集中在 README、SVG 资产与治理索引
- 通过首屏片段检查验证 hero / logo / capability cards / quick paths 的顺序
- 通过工作树状态与阶段 cleanup receipt 保留本轮 governed traceability
