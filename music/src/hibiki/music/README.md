# 🎵 Hibiki Music

智能原生 macOS 音乐播放器 - 基于 Hibiki UI 框架开发

## 项目概述

Hibiki Music 是一款专注于**智能标签系统**和**本地音乐管理**的现代化音乐播放器。以用户自有音乐库为核心，避免流媒体版权变化问题，提供透明可控的音乐发现和推荐体验。

### 🎯 核心特色

- **🏠 本地优先**: 以用户自有音乐库为核心
- **🤖 智能标签**: 自动语言识别、情感分析、主题提取
- **🔍 灵活筛选**: "粤语 + 80年代 + 怀旧" 等多维度组合查询
- **🔗 版本关联**: 同一旋律不同语言版本的智能识别
- **⚡ 响应式**: 基于 Hibiki UI Signal 系统的现代化界面
- **🛠️ Power User**: 为高级用户提供强大的编辑和定制功能

## 🚀 快速开始

### 环境要求

- macOS 11.0+
- Python 3.10+
- uv 包管理器

### 安装依赖

```bash
cd hibiki_music
uv sync
```

### 运行应用

```bash
# MVP v0.1 基础演示
uv run python main.py
```

## 🏗️ 项目架构

```
hibiki_music/
├── core/              # 核心功能模块
│   ├── player/        # 播放器引擎
│   ├── library/       # 音乐库管理
│   ├── metadata/      # 元数据系统
│   └── tagging/       # 智能标签系统 ⭐ 核心创新
├── ai/                # AI 分析模块
├── ui/                # Hibiki UI 界面层
├── data/              # 数据层 (SQLite)
└── utils/             # 工具模块
```

## 📋 开发路线图

### ✅ MVP v0.1 (当前版本)
- [x] 项目框架搭建
- [x] 响应式状态管理 (Hibiki UI Signal)
- [x] 基础播放器界面
- [x] 示例音乐数据展示
- [x] 播放控制 UI 组件

### 🚧 MVP v0.2 (计划中) - 智能标签系统
- [ ] 音频播放引擎 (AVFoundation)
- [ ] 音乐库文件扫描
- [ ] 元数据提取 (mutagen)
- [ ] 智能标签引擎
  - [ ] 语言检测
  - [ ] 年代风格分析
  - [ ] 情感主题提取
- [ ] 标签编辑界面

### 🔮 MVP v0.3 (未来) - 筛选发现系统
- [ ] 多维度标签筛选
- [ ] 智能播放列表
- [ ] 自然语言查询
- [ ] 多语言版本关联

## 🛠️ 技术栈

- **UI 框架**: [Hibiki UI](https://github.com/your-repo/hibiki-ui) - Signal-based 响应式 macOS 原生框架
- **音频播放**: macOS AVFoundation
- **数据库**: SQLite + SQLAlchemy
- **AI/NLP**: 
  - langdetect (语言检测)
  - jieba (中文分词)
  - scikit-learn (相似度计算)
- **音频元数据**: mutagen
- **包管理**: uv

## 🎨 界面预览

MVP v0.1 主要展示 Hibiki UI 的响应式特性：

- 🎮 播放器控制区域 (播放/暂停/上下首/音量)
- 🎵 当前播放信息显示
- 📚 音乐库列表 (带搜索功能)
- 📊 统计面板 (歌曲数量/总时长/播放状态)
- ⚡ 所有 UI 基于 Signal 响应式更新

## 🧪 开发调试

```bash
# 测试运行 (8秒超时，适合 GUI 应用)
timeout 8 uv run python main.py

# 代码格式化
uv run black .
uv run isort .

# 类型检查
uv run mypy hibiki_music
```

## 📖 设计文档

详细的设计文档和架构说明：

- [项目设计文档](../docs/INTELLIGENT_MUSIC_PLAYER_PROJECT.md)
- [MVP 架构设计](../docs/HIBIKI_MUSIC_MVP_ARCHITECTURE.md)

## 🤝 贡献指南

这个项目目前处于早期 MVP 开发阶段，主要为开发者个人需求服务。

## 📄 许可证

TBD - 计划在功能稳定后开源发布

---

*Hibiki Music v0.1.0 - 让音乐发现变得智能而透明* 🎵