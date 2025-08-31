# Hibiki UI 项目文档

这里包含了 Hibiki UI 框架和相关项目的技术文档、设计指南和开发资源。

## 📚 文档索引

### 🎨 Hibiki UI 框架核心

- **[增强提案和路线图](hibiki_ui_enhancement_proposals.md)** ⭐️ *NEW*
  - 基于实际开发经验整理的框架改进想法
  - 包含调试工具、组件库扩展、可视化调试器等提案
  - 详细的实施优先级和技术考虑

- **[开发技巧总结](development_tips.md)**
  - 框架使用的最佳实践
  - 常见问题解决方案
  - 调试和性能优化建议

- **[动画设计原则](ANIMATION_DESIGN_PRINCIPLES.md)**
  - Core Animation 集成指南
  - 动画性能优化策略
  - 用户体验设计考虑

### 🔧 技术架构文档

- **[布局系统架构问题分析](layout_system_architecture_issues.md)**
  - 布局引擎的核心问题分析
  - 技术债务和改进建议

- **[布局系统修复方案](layout_system_fix_proposal.md)**
  - 具体的技术修复方案
  - 实施步骤和验证方法

- **[截图工具开发历程](screenshot_tool_development_journey.md)**
  - 截图功能的技术实现
  - CoreGraphics 和 AppKit 集成经验

### 🎵 Hibiki Music 相关

- **[智能音乐播放器项目](INTELLIGENT_MUSIC_PLAYER_PROJECT.md)**
  - 项目愿景和功能规划
  - AI 集成和用户体验设计

- **[Hibiki Music MVP 架构](HIBIKI_MUSIC_MVP_ARCHITECTURE.md)**
  - 最小可行产品的技术架构
  - 模块化设计和实施计划

### 🛠️ 开发工具和集成

- **[PyObjC 开发笔记](pyobjc-notes.md)**
  - Python 与 macOS 原生 API 集成
  - 常见问题和解决方案
  - 性能优化技巧

## 🚀 快速导航

### 对于新开发者
1. 从 [开发技巧总结](development_tips.md) 开始了解框架使用
2. 查看 [增强提案](hibiki_ui_enhancement_proposals.md) 了解项目方向
3. 参考 [PyObjC 笔记](pyobjc-notes.md) 掌握底层集成

### 对于贡献者  
1. 阅读 [布局系统架构分析](layout_system_architecture_issues.md) 理解技术背景
2. 查看 [增强提案](hibiki_ui_enhancement_proposals.md) 选择感兴趣的项目
3. 参考已有的修复方案了解代码标准

### 对于架构师
1. 重点关注 [布局系统修复方案](layout_system_fix_proposal.md) 的设计思路
2. 研究 [增强提案](hibiki_ui_enhancement_proposals.md) 中的长期愿景
3. 评估 [动画设计原则](ANIMATION_DESIGN_PRINCIPLES.md) 的性能影响

## 📝 文档维护

- **更新频率**: 随项目开发进展持续更新
- **贡献指南**: 新增重要技术决策或经验总结时请更新相关文档
- **版本管理**: 所有文档变更都通过 Git 版本控制

## 🔗 相关资源

- [Hibiki UI 示例程序](../ui/examples/) - 实际代码示例
- [测试用例](../ui/tests/) - 单元测试和集成测试
- [项目 CLAUDE.md](../CLAUDE.md) - AI 助手开发指南

---

*最后更新: 2025-08-31*  
*维护者: 项目开发团队*