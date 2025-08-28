# Hibiki Music MVP 架构设计

## 项目概述

基于 Hibiki UI 框架的原生 macOS 音乐播放器 MVP，专注于智能标签和本地音乐管理。

## 技术架构

### 1. 核心模块架构

```
hibiki_music/
├── core/                          # 核心功能模块
│   ├── __init__.py
│   ├── player/                    # 播放器引擎
│   │   ├── __init__.py
│   │   ├── audio_player.py        # 音频播放核心
│   │   ├── playlist_manager.py    # 播放列表管理
│   │   └── playback_state.py      # 播放状态管理
│   ├── library/                   # 音乐库管理
│   │   ├── __init__.py
│   │   ├── scanner.py             # 文件扫描器
│   │   ├── importer.py            # 音乐导入器
│   │   └── organizer.py           # 文件整理器
│   ├── metadata/                  # 元数据系统
│   │   ├── __init__.py
│   │   ├── extractor.py           # 元数据提取
│   │   ├── manager.py             # 元数据管理
│   │   └── normalizer.py          # 数据规范化
│   └── tagging/                   # 智能标签系统 ⭐ 核心创新
│       ├── __init__.py
│       ├── tag_engine.py          # 标签引擎
│       ├── smart_classifier.py    # 智能分类器
│       └── manual_editor.py       # 手动编辑器
├── ai/                            # AI 分析模块
│   ├── __init__.py
│   ├── lyrics_analyzer.py         # 歌词语义分析
│   ├── metadata_enhancer.py      # 元数据增强
│   ├── similarity_engine.py       # 相似度计算
│   └── language_detector.py      # 语言检测
├── ui/                           # Hibiki UI 界面层
│   ├── __init__.py
│   ├── main_window.py            # 主窗口
│   ├── components/               # 自定义组件
│   │   ├── __init__.py
│   │   ├── player_controls.py    # 播放控制组件
│   │   ├── tag_editor.py         # 标签编辑组件
│   │   ├── music_library.py      # 音乐库组件
│   │   └── filter_panel.py       # 筛选面板组件
│   ├── views/                    # 主要视图
│   │   ├── __init__.py
│   │   ├── library_view.py       # 音乐库视图
│   │   ├── now_playing_view.py   # 当前播放视图
│   │   └── tag_management_view.py # 标签管理视图
│   └── dialogs/                  # 对话框
│       ├── __init__.py
│       ├── import_dialog.py      # 导入对话框
│       └── tag_editor_dialog.py  # 标签编辑对话框
├── data/                         # 数据层
│   ├── __init__.py
│   ├── models.py                 # 数据模型
│   ├── database.py               # SQLite 数据库管理
│   └── schema.sql                # 数据库架构
├── utils/                        # 工具模块
│   ├── __init__.py
│   ├── audio_utils.py            # 音频处理工具
│   ├── file_utils.py             # 文件管理工具
│   └── config.py                 # 配置管理
├── main.py                       # 应用入口
├── requirements.txt              # Python 依赖
└── README.md                     # 项目说明
```

### 2. 核心数据模型

```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from datetime import datetime
from hibiki import Signal, Computed

@dataclass
class Song:
    """歌曲核心数据模型"""
    # 基础信息
    id: str
    file_path: str
    title: str
    artist: str
    album: Optional[str] = None
    duration: float = 0.0
    file_size: int = 0
    format: str = "unknown"
    
    # 元数据
    genre: List[str] = None
    year: Optional[int] = None
    track_number: Optional[int] = None
    
    # 智能标签 ⭐ 核心功能
    language: Optional[str] = None          # 语言 (zh-HK, zh-CN, ja, en)
    emotions: Dict[str, float] = None       # 情感标签 {"nostalgic": 0.8, "romantic": 0.6}
    themes: List[str] = None                # 主题标签 ["love", "farewell", "memory"]
    era_tags: List[str] = None              # 年代标签 ["80s", "90s", "classic"]
    style_tags: List[str] = None            # 风格标签 ["ballad", "rock", "electronic"]
    custom_tags: List[str] = None           # 用户自定义标签
    
    # 关联信息
    language_versions: Dict[str, str] = None  # 多语言版本关联
    related_songs: List[str] = None          # 相关歌曲ID列表
    
    # 用户数据
    play_count: int = 0
    last_played: Optional[datetime] = None
    user_rating: Optional[int] = None        # 1-10 评分
    skip_count: int = 0
    favorite: bool = False
    
    # 技术信息
    bitrate: Optional[int] = None
    sample_rate: Optional[int] = None
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class SmartPlaylist:
    """智能播放列表"""
    id: str
    name: str
    query_conditions: Dict[str, Union[str, List[str], Dict]]
    # 示例: {"language": "zh-HK", "era_tags": ["80s"], "emotions": {"nostalgic": ">0.7"}}
    auto_update: bool = True
    created_at: datetime = None

@dataclass 
class TagFilter:
    """标签筛选器"""
    languages: List[str] = None       # ["zh-HK", "zh-CN"]
    eras: List[str] = None           # ["80s", "90s"]
    emotions: Dict[str, float] = None # {"nostalgic": ">0.5", "happy": "<0.3"}
    themes: List[str] = None         # ["love", "farewell"]
    custom_tags: List[str] = None    # 用户标签
    
    # 组合逻辑
    logic_operator: str = "AND"      # "AND" | "OR"
```

### 3. 响应式状态管理

```python
# 全局应用状态 - 基于 Hibiki UI Signal 系统
class MusicAppState:
    def __init__(self):
        # 播放状态
        self.current_song = Signal(None)  # Song | None
        self.is_playing = Signal(False)
        self.position = Signal(0.0)       # 播放位置 (秒)
        self.volume = Signal(0.8)         # 音量 0.0-1.0
        
        # 音乐库状态
        self.all_songs = Signal([])       # List[Song]
        self.filtered_songs = Computed(lambda: self._apply_filters())
        self.current_filter = Signal(TagFilter())
        
        # UI 状态
        self.selected_view = Signal("library")  # "library" | "now_playing" | "tags"
        self.search_query = Signal("")
        self.loading = Signal(False)
        
        # 标签系统状态
        self.available_tags = Computed(lambda: self._compute_available_tags())
        self.tag_suggestions = Signal([])
```

### 4. 智能标签系统设计 ⭐

```python
class SmartTagEngine:
    """智能标签引擎 - MVP 核心功能"""
    
    def __init__(self):
        self.language_detector = LanguageDetector()
        self.emotion_analyzer = EmotionAnalyzer()
        self.theme_extractor = ThemeExtractor()
        
    def analyze_song(self, song: Song) -> Dict[str, Any]:
        """智能分析歌曲并生成标签"""
        tags = {}
        
        # 1. 语言检测 (基于文件名/元数据)
        tags['language'] = self._detect_language(song)
        
        # 2. 年代分析 (基于发布年份/风格特征)
        tags['era_tags'] = self._analyze_era(song)
        
        # 3. 风格分析 (基于流派信息)
        tags['style_tags'] = self._analyze_style(song)
        
        # 4. 情感主题分析 (如果有歌词)
        if song.lyrics:
            tags['emotions'] = self._analyze_emotions(song.lyrics)
            tags['themes'] = self._extract_themes(song.lyrics)
            
        return tags
        
    def suggest_language_versions(self, song: Song) -> List[Song]:
        """建议可能的多语言版本"""
        # 基于相似标题、艺术家、时长等特征
        candidates = []
        # 实现逻辑...
        return candidates
```

### 5. 筛选和发现系统

```python
class MusicDiscoveryEngine:
    """音乐发现引擎"""
    
    def filter_songs(self, songs: List[Song], filter_obj: TagFilter) -> List[Song]:
        """根据标签筛选歌曲"""
        results = songs
        
        # 语言筛选
        if filter_obj.languages:
            results = [s for s in results if s.language in filter_obj.languages]
            
        # 年代筛选
        if filter_obj.eras:
            results = [s for s in results 
                      if any(era in s.era_tags for era in filter_obj.eras)]
                      
        # 情感筛选
        if filter_obj.emotions:
            results = self._filter_by_emotions(results, filter_obj.emotions)
            
        return results
        
    def smart_search(self, query: str, songs: List[Song]) -> List[Song]:
        """智能搜索 - 支持自然语言查询"""
        # "粤语 + 80年代" -> 转换为 TagFilter 对象
        # "怀旧的歌" -> 情感标签筛选
        # "邓丽君的慢歌" -> 艺术家 + 风格组合筛选
        pass
```

### 6. UI 组件设计

基于 Hibiki UI 的响应式组件：

```python
class TagFilterPanel(Container):
    """标签筛选面板组件"""
    
    def __init__(self, app_state: MusicAppState):
        super().__init__()
        self.app_state = app_state
        self.filter = app_state.current_filter
        
    def create_filter_section(self, title: str, options: List[str], 
                            selected: Signal[List[str]]) -> Container:
        """创建筛选区域"""
        checkboxes = []
        for option in options:
            checkbox = Checkbox(
                Signal(option in selected.value),
                label=option,
                on_change=lambda checked, opt=option: self._toggle_option(selected, opt, checked)
            )
            checkboxes.append(checkbox)
            
        return Container(
            children=[
                Label(title, font_weight="bold"),
                *checkboxes
            ],
            style=ComponentStyle(
                padding=px(10),
                margin_bottom=px(15),
                border="1px solid #ddd",
                border_radius=px(6)
            )
        )
```

## MVP 开发优先级

### 第一阶段：基础播放器 (2-3周)
1. ✅ 项目架构搭建
2. ✅ 基础音频播放功能 (AVPlayer)
3. ✅ 简单的音乐库扫描
4. ✅ 基础 UI (播放控制 + 歌曲列表)

### 第二阶段：智能标签系统 (3-4周) ⭐ 核心价值
1. ✅ 数据模型实现
2. ✅ 智能标签引擎
3. ✅ 标签编辑 UI
4. ✅ 基础筛选功能

### 第三阶段：高级筛选和发现 (2-3周)
1. ✅ 多条件组合筛选
2. ✅ 智能播放列表
3. ✅ 搜索系统优化
4. ✅ 用户体验优化

## 技术选择

- **UI 框架**: Hibiki UI (Signal, Computed, Effect)
- **音频播放**: macOS AVPlayer
- **数据库**: SQLite + Python ORM
- **AI/NLP**: 
  - 语言检测: langdetect
  - 情感分析: 轻量级中文NLP模型
  - 相似度计算: scikit-learn
- **音频元数据**: mutagen
- **包管理**: uv

## 关键创新点

1. **智能标签系统**: 自动语言识别、情感分析、主题提取
2. **多语言版本关联**: 相同旋律不同语言版本的智能识别
3. **灵活筛选组合**: "粤语 + 80年代 + 怀旧" 等复合条件
4. **透明推荐算法**: 用户可见、可调整的推荐参数
5. **Power User 工具**: 批量编辑、导入导出、插件系统

这个 MVP 设计专注于你最关心的核心功能 - 智能标签和灵活筛选，同时保持架构的可扩展性。