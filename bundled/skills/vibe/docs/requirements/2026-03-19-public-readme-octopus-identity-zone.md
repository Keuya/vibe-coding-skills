# 2026-03-19 Public README Octopus Identity Zone

## Goal

在 README 中英双语首屏加入一个不依赖图片素材的“可爱章鱼中枢”品牌识别区，让首页在保持能力展示与传播性的同时，获得更强的记忆点与品牌母体。

## Deliverables

- 在 `README.md` 首屏加入 Markdown 章鱼识别区
- 在 `README.en.md` 首屏加入对应英文识别区
- 新增本轮 requirement 与 plan 文档
- 更新 `docs/requirements/README.md` 与 `docs/plans/README.md` 当前入口

## Constraints

- 不引入图片、SVG、徽标文件或额外素材依赖
- 识别区必须保持简单、易传播、易记忆
- 识别区必须服务于品牌识别，不得破坏当前首页“宣传优先、安装后置”的主轴
- 章鱼形象必须偏可爱、亲和、可传播，但不能削弱系统感与控制力
- 中英文版本需要保持同等识别强度，而不是英文弱化成说明文本

## Acceptance Criteria

- 用户在进入 README 首屏时能立刻看到一个独特、可记忆的章鱼识别区
- 识别区与现有 capability snapshot 能共存，不互相抢话
- 识别区既有品牌记忆点，也能自然承接“多能力统一中枢”的系统语义
- 不依赖图片素材仍能形成清晰首屏辨识度

## Non-Goals

- 不在本轮设计正式 logo 文件或品牌视觉系统
- 不修改 manifesto、quick-start 或安装页正文
- 不修改运行时、路由器、安装与检查逻辑

## Frozen User Intent

- 希望首页出现一个不依赖图片素材的“徽标感 / 品牌识别区”
- 偏好生物形象，最终选择“可爱的章鱼”
- 采用“小章鱼中枢”方向
- 采用 `草案 A`：可爱、易记、系统感平衡最好

## Evidence Strategy

- 通过 README 首屏结构验证识别区与能力快照共存顺序
- 通过 `git diff --stat` 验证本轮只改动 README 与治理索引
- 通过 Node audit / cleanup receipts 保留阶段卫生证据
