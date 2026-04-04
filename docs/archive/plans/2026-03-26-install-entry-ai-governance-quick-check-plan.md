# 安装入口补充 AI 治理快速检查执行计划

**日期**: 2026-03-26  
**需求文档**: [2026-03-26-install-entry-ai-governance-quick-check.md](../requirements/2026-03-26-install-entry-ai-governance-quick-check.md)

## 设计

只改三类公开面：

1. `docs/install/one-click-install-release-copy*.md`
2. `docs/install/prompts/full-version-install*.md`
3. `docs/install/prompts/framework-only-install*.md`

## 口径

1. 入口页只给一个简短检查说明 + 默认宿主根目录示例
2. 安装提示词要求安装助手在完成安装后主动输出：
   - 快速检查命令
   - 检查结果怎么看
3. 不把 probe 扩展成“平台总健康检查”

## 验证

1. 中文/英文口径一致
2. 不引入新的公开入口
3. 文档修改后仍保持单入口结构
