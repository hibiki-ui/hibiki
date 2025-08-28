# Hibiki UI Monorepo

一个基于 Python 和 PyObjC 的原生 macOS UI 框架项目集合

## 项目结构

这是一个 Python monorepo，使用 uv workspace 管理多个相关包：

```
hibiki-ui/
├── ui/                     # Hibiki UI 框架
│   ├── src/hibiki/ui/      # hibiki.ui 包
│   ├── examples/           # 使用示例
│   └── showcase.py         # 完整功能演示
├── music/                  # Hibiki Music 播放器
│   └── src/hibiki/music/   # hibiki.music 包  
└── docs/                   # 项目文档
```

## 包说明

### 🎨 Hibiki UI (`hibiki.ui`)
现代响应式 macOS UI 框架，基于信号系统的细粒度更新机制

**核心特性：**
- Signal 响应式系统 (Signal, Computed, Effect)
- Stretchable 专业布局引擎
- 统一组件 API (Label, Button, Container 等)
- Pure Core Animation 动画系统
- 原生 NSView 直接操作，无虚拟 DOM

### 🎵 Hibiki Music (`hibiki.music`)
智能音乐播放器，专注于本地音乐管理和智能标签系统

**核心特性：**
- 智能标签和分类系统
- 多语言歌曲版本关联
- 语义歌词分析 (NLP/AI)
- 灵活的筛选和发现功能
- 本地优先 + 用户数据主权

## 快速开始

### 环境要求
- Python 3.11+
- macOS 10.15+
- uv (推荐包管理器)

### 安装开发环境

```bash
# 克隆项目
git clone https://github.com/your-repo/hibiki-ui.git
cd hibiki-ui

# 安装依赖
uv sync --all-extras

# 运行 UI 框架示例
uv run python ui/examples/basic/01_hello_world.py

# 运行完整功能演示
uv run python ui/showcase.py
```

### 使用框架

```python
# 使用 Hibiki UI
from hibiki.ui import Signal, Label, Button, ManagerFactory

count = Signal(0)
label = Label(lambda: f"Count: {count.value}")
button = Button("Click me", on_click=lambda: setattr(count, 'value', count.value + 1))

app_manager = ManagerFactory.get_app_manager()
window = app_manager.create_window("Hello World", width=400, height=200)
window.set_content(Container(children=[label, button]))
app_manager.run()
```

## 开发指令

```bash
# 安装依赖
uv sync --all-extras

# 代码质量检查
uv run ruff check .
uv run black .
uv run mypy hibiki

# 运行测试
uv run pytest

# 构建包
uv build
```

## 项目愿景

基于多年音乐管理经验，创建一个真正理解用户需求的智能音乐播放器。结合现代化的 UI 框架，为 macOS 用户提供专业级的本地音乐管理体验。

**设计理念：**
- **本地优先**: 用户数据完全掌控，无需依赖云服务
- **智能标签**: AI 辅助的语言识别和情感分析  
- **Power User 工具**: 强大的批量编辑和管理功能
- **透明算法**: 推荐参数用户可见可调整

## 文档

- **UI 框架文档**: `ui/README.md`
- **音乐播放器文档**: `music/README.md` 
- **架构设计**: `docs/HIBIKI_MUSIC_MVP_ARCHITECTURE.md`
- **开发指南**: `CLAUDE.md`

## 许可证

MIT License - 详见 `LICENSE` 文件

---

*Built with ❤️ for music lovers and macOS developers*