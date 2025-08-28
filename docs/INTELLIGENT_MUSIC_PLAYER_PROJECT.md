# 智能音乐播放器项目设计文档

## 项目概述

基于 Hibiki UI 框架开发的现代化原生 macOS 音乐播放器，以本地文件为主，融合 AI 技术提供智能化音乐管理和个性化推荐体验。

### 核心理念

- **本地优先**: 以用户自有音乐库为核心，避免流媒体版权变化问题
- **用户主权**: 透明可控的算法，用户完全掌控自己的音乐数据和偏好
- **Power User 导向**: 提供强大的编辑、定制和分析功能
- **个人化驱动**: 首先满足开发者个人需求，确保实用性

## 技术架构

### 前端层：Hibiki UI
- 原生 macOS 界面，低资源消耗
- 流畅动效和复杂布局支持
- 响应式数据绑定
- 长期运行稳定性

### AI 核心层：Python NLP 技术栈
- 歌词语义分析引擎
- 情感和主题识别
- 智能推荐算法
- 自然语言查询支持

### 数据层
- 本地音乐库管理
- 全面的用户行为数据收集
- 元数据和标签系统
- 语义关系图构建

## 核心创新功能

### 1. 多语言版本关联系统
**问题**: 同一旋律的不同语言版本（粤语/国语/日语/英语）缺乏智能关联
**解决方案**: 
- 音频特征匹配算法识别同曲异词版本
- 用户手动关联和系统智能建议结合
- 基于关联关系的跨语言推荐

### 2. 歌词语义分析引擎
**能力**:
- 情感主题提取（失恋、暧昧、治愈、励志等）
- 意象元素识别（海、旅行、寂寞、城市等）
- 文学典故和文化引用分析
- 情感强度量化评估

**技术实现**:
```python
class LyricsAnalyzer:
    def analyze_emotion(self, lyrics: str) -> Dict[str, float]
    def extract_themes(self, lyrics: str) -> List[str]
    def identify_imagery(self, lyrics: str) -> List[str]
    def cultural_references(self, lyrics: str) -> List[str]
```

### 3. 智能推荐系统
**特点**:
- 完全透明的算法参数
- 用户可调整的权重系统
- 基于语义网络的关联推荐
- 上下文感知的情境推荐

**参数化控制**:
```python
class RecommendationParams:
    genre_weight: float = 0.3          # 流派相似度
    emotion_weight: float = 0.4        # 情感相似度  
    tempo_weight: float = 0.2          # 节奏相似度
    lyrics_similarity: float = 0.3     # 歌词语义相似度
    diversity_factor: float = 0.3      # 多样性 vs 相似性
    discovery_rate: float = 0.1        # 探索新音乐的比例
```

### 4. 自然语言音乐搜索
**支持查询类型**:
- 情感化搜索："找出和失恋有关的歌"
- 场景化搜索："适合跑步的歌"
- 意象搜索："有关大海的歌曲"
- 情绪转换："从悲伤到治愈的歌曲"

## Power User 功能设计

### 全面可编辑的元数据系统
```python
class EditableMetadata:
    # 基础信息
    title: str
    artist: str  
    album: str
    genre: List[str]
    
    # 语义标签
    emotions: Dict[str, float]         # 情感权重映射
    themes: List[str]                  # 主题标签
    instruments: List[str]             # 乐器识别
    tempo_feel: str                    # 节奏感觉
    
    # 个人化标签  
    personal_rating: int               # 个人评分 1-10
    mood_association: List[str]        # 心情关联
    listening_context: List[str]       # 听歌场景
    
    # 版本关联
    language_versions: Dict[str, str]  # 多语言版本关联
    cover_versions: List[str]          # 翻唱版本
```

### 插件架构系统
```python
class PluginAPI:
    def get_music_library(self) -> MusicLibrary
    def register_analyzer(self, analyzer: AudioAnalyzer)  
    def register_recommender(self, recommender: RecommendationEngine)
    def add_ui_component(self, component: UIComponent)
    def on_song_play(self, callback: Callable)
```

### 批量编辑工具
- 基于文件夹结构的批量标记
- 智能重复检测和合并
- 元数据补全向导
- 批量歌词分析处理

## 用户行为数据收集

### 详细播放记录
```python
@dataclass
class PlaybackRecord:
    timestamp: datetime
    song_id: str
    play_duration: int               # 实际播放时长
    completion_rate: float           # 播放完成度
    play_source: str                 # 播放来源
    repeat_mode: str                 # 播放模式
    user_action: str                 # 用户行为
    skip_position: Optional[int]     # 跳过位置
    volume_level: float              # 播放音量
    time_of_day: str                 # 时段信息
```

### 播放列表操作历史
```python
@dataclass 
class PlaylistOperation:
    timestamp: datetime
    operation_type: str              # create/modify/delete/rename
    playlist_id: str
    songs_added: List[str]           # 添加的歌曲
    creation_reason: Optional[str]   # 创建动机
    mood_tag: Optional[str]          # 心情标签
```

### 个人音乐分析
- 听歌模式识别（时间偏好、情绪周期）
- 音乐品味演化跟踪  
- 跳过行为模式分析
- 个性化洞察生成

## 音乐来源策略

### 本地文件为主
- 支持多种音频格式（FLAC, MP3, AAC, OGG）
- 自动元数据提取和管理
- 文件系统监控和同步
- 智能重复检测

### 流媒体为辅
- 预览试听功能
- 新音乐发现
- 临时播放支持
- 歌词同步获取

### 合法下载渠道
- Bandcamp 独立音乐
- Creative Commons 授权音乐
- 免费音乐网站集成
- 购买链接引导

## 开发策略

### 阶段 1：核心 MVP
- 本地音乐库管理
- 基础播放功能  
- 简单标签系统
- 播放历史记录
- 基础搜索功能

### 阶段 2：智能化增强
- 歌词语义分析
- 多语言版本关联
- 智能推荐算法
- 个性化播放列表
- 行为分析面板

### 阶段 3：Power User 工具
- 高级编辑功能
- 插件系统
- 可视化分析
- 导入导出工具
- 算法调优面板

## 技术实现要点

### Hibiki UI 框架挑战
- 复杂音乐播放器界面布局
- 实时播放进度和频谱显示
- 大量音乐数据的列表渲染
- 多面板和标签页管理
- 动画和视觉反馈效果

### Python AI 集成
- 中文 NLP 模型选择和优化
- 歌词数据预处理管道
- 语义相似度计算算法
- 推荐算法性能优化
- 本地模型部署和更新

### 数据管理
- SQLite 本地数据库设计
- 音频文件元数据提取（mutagen）
- 用户行为数据实时收集
- 数据备份和恢复机制
- 隐私保护和安全存储

## 项目价值

### 对 Hibiki UI 框架
- 复杂应用场景的全面测试
- 长期运行稳定性验证
- 性能优化需求驱动
- 社区展示和推广

### 对音乐播放器生态
- 本地优先的隐私保护方案
- 透明算法对抗黑箱推荐
- Power User 需求的深度满足
- 开源替代方案提供

### 个人价值
- 真实需求驱动的产品开发
- AI 技术在个人应用中的实践
- 长期使用的个人工具
- 技术能力的综合展示

## 后续规划

1. **个人使用阶段**: 优先满足开发者个人需求，持续迭代完善
2. **开源发布**: 功能稳定后作为开源项目发布
3. **社区建设**: 吸引志同道合的音乐和技术爱好者
4. **功能扩展**: 基于社区反馈继续演进功能

---

*文档创建时间: 2025-08-28*
*最后更新: 2025-08-28*